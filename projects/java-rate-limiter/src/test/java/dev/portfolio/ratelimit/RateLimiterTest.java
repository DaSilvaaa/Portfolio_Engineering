package dev.portfolio.ratelimit;

import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicLong;

import static org.junit.jupiter.api.Assertions.*;

class RateLimiterTest {
    @Test
    void burstThenBlocked() {
        TokenBucket b = new TokenBucket(5, 1.0, () -> 0L);
        for (int i = 0; i < 5; i++) {
            assertTrue(b.tryAcquire());
        }
        assertFalse(b.tryAcquire());
    }

    @Test
    void refillsOverTime() {
        AtomicLong clock = new AtomicLong();
        TokenBucket b = new TokenBucket(2, 1.0, clock::get);
        assertTrue(b.tryAcquire(2));
        assertFalse(b.tryAcquire());
        clock.set(1_000_000_000L); // Avança 1 segundo em nanos
        assertTrue(b.tryAcquire());
        assertFalse(b.tryAcquire());
    }

    @Test
    void neverExceedsCapacityAfterLongIdle() {
        AtomicLong clock = new AtomicLong();
        TokenBucket b = new TokenBucket(2, 1.0, clock::get);
        clock.set(3_600_000_000_000L); // Avança 1 hora em nanos
        assertTrue(b.tryAcquire(2));
        assertFalse(b.tryAcquire());
    }

    @Test
    void rejectsInvalidArguments() {
        assertThrows(IllegalArgumentException.class, () -> new TokenBucket(0, 1.0));
        TokenBucket b = new TokenBucket(2, 1.0, () -> 0L);
        assertThrows(IllegalArgumentException.class, () -> b.tryAcquire(3));
    }

    @Test
    void neverExceedsCapacityUnderContention() throws Exception {
        TokenBucket b = new TokenBucket(1000, 1.0, () -> 0L);
        ExecutorService ex = Executors.newFixedThreadPool(16);
        AtomicInteger ok = new AtomicInteger();
        List<Callable<Void>> jobs = new ArrayList<>();
        for (int t = 0; t < 16; t++) {
            jobs.add(() -> {
                for (int i = 0; i < 500; i++) {
                    if (b.tryAcquire()) ok.incrementAndGet();
                }
                return null;
            });
        }
        ex.invokeAll(jobs);
        ex.shutdown();
        assertEquals(1000, ok.get());
    }

    @Test
    void keysAreIndependent() {
        KeyedRateLimiter<String> l = new KeyedRateLimiter<>(1, 0.001);
        assertTrue(l.allow("a"));
        assertFalse(l.allow("a"));
        assertTrue(l.allow("b"));
        assertEquals(2, l.trackedKeys());
    }
}