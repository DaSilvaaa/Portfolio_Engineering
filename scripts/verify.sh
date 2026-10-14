#!/usr/bin/env bash
set -uo pipefail
cd "$(dirname "$0")/.."
fail=0; ran=0

run() {
  local name=$1; shift
  if command -v "$1" >/dev/null 2>&1; then
    ran=$((ran+1)); echo "==> $name"
    "$@" || { echo "FALHOU: $name"; fail=1; }
  else
    echo "-- ignorado ($1 não instalado localmente): $name"
  fi
}

run "python-security" python -m pytest projects/secure-web-api/tests projects/sast-mini/tests projects/password-auditor/tests -q
run "python-ml" python -m pytest projects/ml-intrusion-detection/tests projects/ml-from-scratch/tests projects/ml-tabular-pipeline/tests -q
run "rust-integrity" cargo test -q --manifest-path projects/rust-integrity-monitor/Cargo.toml
run "rust-secrets" cargo test -q --manifest-path projects/rust-secrets-scanner/Cargo.toml
run "java-vault" mvn -q -f projects/java-aes-vault/pom.xml test
run "java-rate-limiter" mvn -q -f projects/java-rate-limiter/pom.xml test
run "csharp-auth" dotnet test projects/csharp-auth-log-analyzer/tests --nologo -v q
run "csharp-tls" dotnet test projects/csharp-tls-inspector/tests --nologo -v q

echo "======================================"
echo "Suites executadas: $ran | Falhas: $fail"
echo "======================================"
exit $fail