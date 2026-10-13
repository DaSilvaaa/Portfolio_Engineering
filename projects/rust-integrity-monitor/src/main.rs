use sha2::{Digest, Sha256};
use std::collections::BTreeMap;
use std::{env, fs, io, path::Path, process::ExitCode};

type Snapshot = BTreeMap<String, String>;

#[derive(Debug, PartialEq, Default)]
struct Diff {
    modified: Vec<String>,
    added: Vec<String>,
    removed: Vec<String>,
}

fn walk(p: &Path, out: &mut Snapshot) -> io::Result<()> {
    if p.is_dir() {
        for e in fs::read_dir(p)? {
            walk(&e?.path(), out)?;
        }
    } else if p.is_file() {
        let data = fs::read(p)?;
        out.insert(p.display().to_string(), hex::encode(Sha256::digest(&data)));
    }
    Ok(())
}

fn save(s: &Snapshot, path: &str) -> io::Result<()> {
    let body: String = s.iter().map(|(p, h)| format!("{h}  {p}\n")).collect();
    fs::write(path, body)
}

fn load(path: &str) -> io::Result<Snapshot> {
    let mut s = Snapshot::new();
    for line in fs::read_to_string(path)?.lines() {
        if let Some((h, p)) = line.split_once("  ") {
            s.insert(p.to_string(), h.to_string());
        }
    }
    Ok(s)
}

fn diff(old: &Snapshot, new: &Snapshot) -> Diff {
    let mut d = Diff::default();
    for (p, h) in new {
        match old.get(p) {
            None => d.added.push(p.clone()),
            Some(o) if o != h => d.modified.push(p.clone()),
            _ => {}
        }
    }
    for p in old.keys() {
        if !new.contains_key(p) {
            d.removed.push(p.clone());
        }
    }
    d
}

fn main() -> ExitCode {
    let a: Vec<String> = env::args().collect();
    if a.len() != 4 {
        eprintln!("uso: {} <baseline|verify> <diretoria> <ficheiro_baseline>", a[0]);
        return ExitCode::from(2);
    }
    let mut cur = Snapshot::new();
    if let Err(e) = walk(Path::new(&a[2]), &mut cur) {
        eprintln!("erro: {e}");
        return ExitCode::from(2);
    }
    match a[1].as_str() {
        "baseline" => match save(&cur, &a[3]) {
            Ok(_) => {
                println!("{} ficheiros registados", cur.len());
                ExitCode::SUCCESS
            }
            Err(e) => {
                eprintln!("erro: {e}");
                ExitCode::from(2)
            }
        },
        "verify" => {
            let old = match load(&a[3]) {
                Ok(o) => o,
                Err(e) => {
                    eprintln!("erro: {e}");
                    return ExitCode::from(2);
                }
            };
            let d = diff(&old, &cur);
            for p in &d.modified {
                println!("MODIFICADO {p}");
            }
            for p in &d.added {
                println!("NOVO       {p}");
            }
            for p in &d.removed {
                println!("REMOVIDO   {p}");
            }
            if d == Diff::default() {
                println!("OK: integridade verificada");
                ExitCode::SUCCESS
            } else {
                ExitCode::from(1)
            }
        }
        _ => ExitCode::from(2),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn snap(items: &[(&str, &str)]) -> Snapshot {
        items.iter().map(|(p, h)| (p.to_string(), h.to_string())).collect()
    }

    #[test]
    fn detects_all_change_types() {
        let old = snap(&[("a", "1"), ("b", "2"), ("c", "3")]);
        let new = snap(&[("a", "1"), ("b", "X"), ("d", "4")]);
        let d = diff(&old, &new);
        assert_eq!(d.modified, vec!["b"]);
        assert_eq!(d.added, vec!["d"]);
        assert_eq!(d.removed, vec!["c"]);
    }

    #[test]
    fn identical_snapshots_have_no_diff() {
        let s = snap(&[("a", "1")]);
        assert_eq!(diff(&s, &s), Diff::default());
    }
}