package dev.portfolio.ratelimit;

import java.util.function.LongSupplier;

/**
 * Token bucket thread-safe com relógio injetável para testes determinísticos.
 */
public final class TokenBucket {
    private final long capacity;
    private final double refillPerSecond;
    private final LongSupplier nanoTime;
    private double tokens;
    private long last;

    public TokenBucket(long capacity, double refillPerSecond) {
        this(capacity, refillPerSecond, System::nanoTime);
    }

    public TokenBucket(long capacity, double refillPerSecond, LongSupplier nanoTime) {
        if (capacity <= 0 || refillPerSecond <= 0) {
            throw new IllegalArgumentException("capacity e refillPerSecond têm de ser > 0");
        }
        this.capacity = capacity;
        this.refillPerSecond = refillPerSecond;
        this.nanoTime = nanoTime;
        this.tokens = capacity;
        this.last = nanoTime.getAsLong();
    }

    public synchronized boolean tryAcquire(int permits) {
        if (permits <= 0 || permits > capacity) {
            throw new IllegalArgumentException("permits inválido: " + permits);
        }
        refill();
        if (tokens >= permits) {
            tokens -= permits;
            return true;
        }
        return false;
    }

    public boolean tryAcquire() {
        return tryAcquire(1);
    }

    private void refill() {
        long now = nanoTime.getAsLong();
        long delta = now - last;
        if (delta > 0) {
            tokens = Math.min(capacity, tokens + delta * refillPerSecond / 1e9);
            last = now;
        }
    }
}