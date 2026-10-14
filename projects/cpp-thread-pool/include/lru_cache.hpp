#pragma once
#include <cstddef>
#include <list>
#include <mutex>
#include <optional>
#include <stdexcept>
#include <unordered_map>
#include <utility>

template <class K, class V>
class LruCache {
public:
    explicit LruCache(size_t capacity) : cap_(capacity) {
        if (capacity == 0) throw std::invalid_argument("capacidade deve ser > 0");
    }

    std::optional<V> get(const K& k) {
        std::lock_guard<std::mutex> lk(m_);
        auto it = map_.find(k);
        if (it == map_.end()) return std::nullopt;
        items_.splice(items_.begin(), items_, it->second);
        return it->second->second;
    }

    void put(const K& k, V v) {
        std::lock_guard<std::mutex> lk(m_);
        auto it = map_.find(k);
        if (it != map_.end()) {
            it->second->second = std::move(v);
            items_.splice(items_.begin(), items_, it->second);
            return;
        }
        items_.emplace_front(k, std::move(v));
        map_[k] = items_.begin();
        if (map_.size() > cap_) {
            map_.erase(items_.back().first);
            items_.pop_back();
        }
    }

    size_t size() const {
        std::lock_guard<std::mutex> lk(m_);
        return map_.size();
    }

private:
    using Item = std::pair<K, V>;
    size_t cap_;
    mutable std::mutex m_;
    std::list<Item> items_;
    std::unordered_map<K, typename std::list<Item>::iterator> map_;
};