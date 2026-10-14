#include <atomic>
#include <cstdio>
#include <cstdlib>
#include <stdexcept>
#include <string>

#include "lru_cache.hpp"
#include "thread_pool.hpp"

#define CHECK(c)                                                              \
    do {                                                                      \
        if (!(c)) {                                                           \
            std::fprintf(stderr, "FALHOU %s:%d: %s\n", __FILE__, __LINE__, #c); \
            std::exit(1);                                                     \
        }                                                                     \
    } while (0)

int main() {
    // 1. Verificação de computação paralela com futures
    {
        ThreadPool p(4);
        std::vector<std::future<int>> fs;
        for (int i = 0; i < 100; ++i) fs.push_back(p.submit([](int x) { return x * x; }, i));
        long s = 0;
        for (auto& f : fs) s += f.get();
        CHECK(s == 328350);
    }

    // 2. Execução massiva de tarefas atómicas
    {
        std::atomic<int> n{0};
        {
            ThreadPool p(8);
            for (int i = 0; i < 10000; ++i) p.submit([&n] { ++n; });
        }
        CHECK(n == 10000);
    }

    // 3. Captura e propagação de exceções através do future
    {
        ThreadPool p(2);
        auto f = p.submit([]() -> int { throw std::runtime_error("x"); });
        bool caught = false;
        try {
            f.get();
        } catch (const std::runtime_error&) {
            caught = true;
        }
        CHECK(caught);
    }

    // 4. Teste de lógica da política LRU
    {
        LruCache<std::string, int> c(2);
        c.put("a", 1);
        c.put("b", 2);
        CHECK(c.get("a").value_or(-1) == 1);
        c.put("c", 3); // Deve despejar "b"
        CHECK(!c.get("b").has_value());
        CHECK(c.get("a").value_or(-1) == 1);
        CHECK(c.get("c").value_or(-1) == 3);
        c.put("a", 10);
        CHECK(c.get("a").value_or(-1) == 10);
        CHECK(c.size() == 2);
    }

    // 5. Concorrência sob elevada contenção na cache
    {
        LruCache<int, int> c(64);
        ThreadPool p(8);
        std::vector<std::future<void>> fs;
        for (int t = 0; t < 8; ++t)
            fs.push_back(p.submit([&c, t] {
                for (int i = 0; i < 5000; ++i) {
                    c.put((i * 7 + t) % 200, i);
                    c.get(i % 200);
                }
            }));
        for (auto& f : fs) f.get();
        CHECK(c.size() <= 64);
    }

    std::puts("OK");
    return 0;
}