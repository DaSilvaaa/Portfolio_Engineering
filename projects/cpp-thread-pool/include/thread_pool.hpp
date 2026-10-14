#pragma once
#include <condition_variable>
#include <functional>
#include <future>
#include <memory>
#include <mutex>
#include <queue>
#include <stdexcept>
#include <thread>
#include <type_traits>
#include <vector>

class ThreadPool {
public:
    explicit ThreadPool(size_t n = std::thread::hardware_concurrency()) {
        if (n == 0) n = 1;
        for (size_t i = 0; i < n; ++i)
            workers_.emplace_back([this] {
                for (;;) {
                    std::function<void()> task;
                    {
                        std::unique_lock<std::mutex> lk(m_);
                        cv_.wait(lk, [this] { return stop_ || !q_.empty(); });
                        if (stop_ && q_.empty()) return;
                        task = std::move(q_.front());
                        q_.pop();
                    }
                    task();
                }
            });
    }

    ThreadPool(const ThreadPool&) = delete;
    ThreadPool& operator=(const ThreadPool&) = delete;

    ~ThreadPool() {
        {
            std::lock_guard<std::mutex> lk(m_);
            stop_ = true;
        }
        cv_.notify_all();
        for (auto& w : workers_) w.join();
    }

    template <class F, class... A>
    auto submit(F&& f, A&&... a) -> std::future<std::invoke_result_t<std::decay_t<F>, std::decay_t<A>...>> {
        using R = std::invoke_result_t<std::decay_t<F>, std::decay_t<A>...>;
        auto task = std::make_shared<std::packaged_task<R()>>(
            std::bind(std::forward<F>(f), std::forward<A>(a)...));
        auto fut = task->get_future();
        {
            std::lock_guard<std::mutex> lk(m_);
            if (stop_) throw std::runtime_error("thread pool parado");
            q_.emplace([task] { (*task)(); });
        }
        cv_.notify_one();
        return fut;
    }

private:
    std::vector<std::thread> workers_;
    std::queue<std::function<void()>> q_;
    std::mutex m_;
    std::condition_variable cv_;
    bool stop_ = false;
};