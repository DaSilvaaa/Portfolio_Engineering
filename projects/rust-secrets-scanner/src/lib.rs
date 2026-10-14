use regex::Regex;
use std::sync::OnceLock;

#[derive(Debug, Clone, PartialEq)]
pub struct Finding {
    pub rule: &'static str,
    pub line: usize,
    pub snippet: String,
}

struct Rule {
    name: &'static str,
    re: Regex,
}

fn rules() -> &'static Vec<Rule> {
    static R: OnceLock<Vec<Rule>> = OnceLock::new();
    R.get_or_init(|| {
        vec![
            Rule { name: "aws-access-key", re: Regex::new(r"\bAKIA[0-9A-Z]{16}\b").unwrap() },
            Rule { name: "github-token", re: Regex::new(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b").unwrap() },
            Rule { name: "slack-token", re: Regex::new(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b").unwrap() },
            Rule {
                name: "private-key",
                re: Regex::new(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----").unwrap(),
            },
        ]
    })
}

fn generic() -> &'static Regex {
    static G: OnceLock<Regex> = OnceLock::new();
    G.get_or_init(|| {
        Regex::new(r#"(?i)(?:secret|token|passw(?:or)?d|api[_-]?key)\s*[:=]\s*["']([A-Za-z0-9/+=_\-]{20,})["']"#)
            .unwrap()
    })
}

pub fn shannon_entropy(s: &str) -> f64 {
    if s.is_empty() {
        return 0.0;
    }
    let mut counts = [0usize; 256];
    for b in s.bytes() {
        counts[b as usize] += 1;
    }
    let n = s.len() as f64;
    counts
        .iter()
        .filter(|&&c| c > 0)
        .map(|&c| {
            let p = c as f64 / n;
            -p * p.log2()
        })
        .sum()
}

fn redact(s: &str) -> String {
    if s.len() <= 8 {
        "****".into()
    } else {
        format!("{}…{}", &s[..4], &s[s.len() - 2..])
    }
}

pub fn scan_text(text: &str) -> Vec<Finding> {
    let mut out = Vec::new();
    for (i, line) in text.lines().enumerate() {
        if line.contains("scanner:ignore") {
            continue;
        }
        for r in rules() {
            if let Some(m) = r.re.find(line) {
                out.push(Finding { rule: r.name, line: i + 1, snippet: redact(m.as_str()) });
            }
        }
        if let Some(c) = generic().captures(line) {
            let v = &c[1];
            if shannon_entropy(v) >= 3.5 {
                out.push(Finding { rule: "generic-high-entropy", line: i + 1, snippet: redact(v) });
            }
        }
    }
    out
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn entropy_values() {
        assert_eq!(shannon_entropy("aaaa"), 0.0);
        assert!((shannon_entropy("abcd") - 2.0).abs() < 1e-9);
    }

    #[test]
    fn detects_aws_key_and_redacts() {
        let key = format!("AKIA{}", "IOSFODNN7EXAMPLE");
        let f = scan_text(&format!("aws = {key}"));
        assert_eq!(f.len(), 1);
        assert_eq!(f[0].rule, "aws-access-key");
        assert_eq!(f[0].line, 1);
        assert!(!f[0].snippet.contains(&key));
    }

    #[test]
    fn detects_github_token() {
        let t = format!("ghp_{}", "a".repeat(36));
        let f = scan_text(&format!("x\nT={t}"));
        assert_eq!(f.len(), 1);
        assert_eq!(f[0].rule, "github-token");
        assert_eq!(f[0].line, 2);
    }

    #[test]
    fn detects_private_key_header() {
        let h = format!("-----BEGIN {} PRIVATE KEY-----", "RSA");
        assert_eq!(scan_text(&h)[0].rule, "private-key");
    }

    #[test]
    fn generic_requires_high_entropy() {
        let hi = format!("api_key = \"{}\"", "Zx9fQ2LmP8vTa7BnKc4R");
        let lo = format!("token = \"{}\"", "a".repeat(24));
        assert_eq!(scan_text(&hi)[0].rule, "generic-high-entropy");
        assert!(scan_text(&lo).is_empty());
    }

    #[test]
    fn ignore_marker_skips_line() {
        let key = format!("AKIA{}", "IOSFODNN7EXAMPLE");
        assert!(scan_text(&format!("{key} # scanner:ignore")).is_empty());
    }
}