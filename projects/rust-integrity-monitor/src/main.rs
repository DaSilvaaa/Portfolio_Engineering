use sha2::{Digest, Sha256};
use std::{env, fs, path::Path};

fn walk(p: &Path, out: &mut Vec<(String, String)>) -> std::io::Result<()> {
    if p.is_dir() {
        for e in fs::read_dir(p)? {
            walk(&e?.path(), out)?;
        }
    } else {
        let data = fs::read(p)?;
        out.push((p.display().to_string(), hex::encode(Sha256::digest(&data))));
    }
    Ok(())
}

fn main() {
    let root = env::args().nth(1).unwrap_or_else(|| ".".into());
    let mut files = Vec::new();
    walk(Path::new(&root), &mut files).expect("Erro ao ler diretoria");
    files.sort();
    for (path, hash) in files {
        println!("{hash}  {path}");
    }
}
