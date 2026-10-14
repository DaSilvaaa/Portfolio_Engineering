package dev.portfolio.ratelimit;

import java.util.concurrent.ConcurrentHashMap;

/**
 * Gestão de token buckets isolados por chave (ex.: IP, utilizador, API key).
 */
public final class KeyedRateLimiter<K> {
    private final ConcurrentHashMap<K, TokenBucket> buckets = new ConcurrentHashMap<>();
    private final long capacity;
    private final double refillPerSecond;

    public KeyedRateLimiter(long capacity, double refillPerSecond) {
        this.capacity = capacity;
        this.refillPerSecond = refillPerSecond;
    }

    public boolean allow(K key) {
        return buckets.computeIfAbsent(key, k -> new TokenBucket(capacity, refillPerSecond)).tryAcquire();
    }

    public int trackedKeys() {
        return buckets.size();
    }
}