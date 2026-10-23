#!/usr/bin/env bash
set -uo pipefail
cd "$(dirname "$0")/.."
fail=0; ran=0

run() {
  local name=$1; shift
  local cmd=$1

  # No caso do .NET, valida se o SDK está mesmo instalado e não apenas o runtime
  if [ "$cmd" = "dotnet" ]; then
    if command -v dotnet >/dev/null 2>&1 && dotnet --list-sdks 2>/dev/null | grep -q '[0-9]'; then
      ran=$((ran+1)); echo "==> $name"
      "$@" || { echo "FALHOU: $name"; fail=1; }
    else
      echo "-- ignorado (.NET SDK não instalado localmente): $name"
    fi
    return
  fi

  if command -v "$cmd" >/dev/null 2>&1; then
    ran=$((ran+1)); echo "==> $name"
    "$@" || { echo "FALHOU: $name"; fail=1; }
  else
    echo "-- ignorado ($cmd não instalado localmente): $name"
  fi
}

export SECRET_KEY="${SECRET_KEY:-local-dev-secret-key-with-32-or-more-chars}"
run "python-security" python -m pytest projects/secure-web-api/tests projects/sast-mini/tests projects/password-auditor/tests projects/port-scanner/tests projects/log-analyzer-siem/tests -q
run "python-ml" python -m pytest projects/ml-intrusion-detection/tests projects/ml-from-scratch/tests projects/ml-tabular-pipeline/tests projects/ml-energy-forecasting/tests -q
run "rust-integrity" cargo test -q --manifest-path projects/rust-integrity-monitor/Cargo.toml
run "rust-secrets" cargo test -q --manifest-path projects/rust-secrets-scanner/Cargo.toml
run "java-vault" mvn -q -f projects/java-aes-vault/pom.xml test
run "java-rate-limiter" mvn -q -f projects/java-rate-limiter/pom.xml test
run "cpp-thread-pool" bash -c 'cd projects/cpp-thread-pool && cmake -B build >/dev/null && cmake --build build >/dev/null && ctest --test-dir build --output-on-failure'
run "cpp-packet-parser" bash -c 'cd projects/cpp-packet-parser && cmake -B build >/dev/null && cmake --build build >/dev/null'
run "csharp-auth" dotnet test projects/csharp-auth-log-analyzer/tests --nologo -v q
run "csharp-tls" dotnet test projects/csharp-tls-inspector/tests --nologo -v q

echo "======================================"
echo "Suites executadas: $ran | Falhas: $fail"
echo "======================================"
exit $fail