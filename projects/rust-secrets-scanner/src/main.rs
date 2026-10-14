use rust_secrets_scanner::scan_text;
use std::{env, fs, io, path::Path, process::ExitCode};

const SKIP: [&str; 4] = [".git", "target", "node_modules", ".venv"];

fn walk(p: &Path, files: &mut usize, hits: &mut usize) -> io::Result<()> {
    if p.is_dir() {
        if p.file_name().and_then(|n| n.to_str()).map_or(false, |n| SKIP.contains(&n)) {
            return Ok(());
        }
        for e in fs::read_dir(p)? {
            walk(&e?.path(), files, hits)?;
        }
    } else if p.is_file() {
        if fs::metadata(p)?.len() > 1_000_000 {
            return Ok(());
        }
        if let Ok(text) = fs::read_to_string(p) {
            *files += 1;
            for f in scan_text(&text) {
                *hits += 1;
                println!("{}:{} [{}] {}", p.display(), f.line, f.rule, f.snippet);
            }
        }
    }
    Ok(())
}

fn main() -> ExitCode {
    let root = env::args().nth(1).unwrap_or_else(|| ".".into());
    let (mut files, mut hits) = (0usize, 0usize);
    if let Err(e) = walk(Path::new(&root), &mut files, &mut hits) {
        eprintln!("erro: {e}");
        return ExitCode::from(2);
    }
    eprintln!("{files} ficheiros analisados, {hits} possíveis segredos");
    if hits > 0 {
        ExitCode::from(1)
    } else {
        ExitCode::SUCCESS
    }
}