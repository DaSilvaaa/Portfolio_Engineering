# cpp-thread-pool

Thread pool genérico (`submit` devolve `std::future`) e cache LRU thread-safe, header-only, C++17.

## Funcionalidades
- **Concorrência Genérica:** Execução assíncrona de tarefas parametrizadas com retorno tipado via `std::future`.
- **Cache LRU Thread-Safe:** Evicção $O(1)$ com sincronização via *mutex* de granularidade fina.
- **Validação de Sanitizers:** Concebido para validação em CI sob ThreadSanitizer (TSan) e AddressSanitizer (ASan/UBSan).

## Compilação e Execução de Testes
```bash
# Compilação padrão e testes
cmake -S . -B build && cmake --build build && ctest --test-dir build --output-on-failure

# Com ThreadSanitizer (em sistemas Linux/macOS)
cmake -S . -B build-tsan -DSANITIZE=thread && cmake --build build-tsan && ctest --test-dir build-tsan