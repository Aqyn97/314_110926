import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.atomic.AtomicLong;

public class Part2_Synchronized {

    static final long TOTAL_TOSSES = 50_000_000L;
    static final int NUM_THREADS = 4;

    static class TossWorker extends Thread {
        final long tossesForThisThread;
        final AtomicLong sharedHits;

        TossWorker(long tosses, AtomicLong sharedHits) {
            this.tossesForThisThread = tosses;
            this.sharedHits = sharedHits;
        }

        @Override
        public void run() {
            ThreadLocalRandom rnd = ThreadLocalRandom.current();
            for (long i = 0; i < tossesForThisThread; i++) {
                double x = rnd.nextDouble();
                double y = rnd.nextDouble();
                if (x * x + y * y <= 1.0) {
                    sharedHits.incrementAndGet(); // atomic, correct, but contends
                }
            }
        }
    }

    static long countHitsSingleThreaded(long tosses) {
        ThreadLocalRandom rnd = ThreadLocalRandom.current();
        long hits = 0;
        for (long i = 0; i < tosses; i++) {
            double x = rnd.nextDouble();
            double y = rnd.nextDouble();
            if (x * x + y * y <= 1.0) hits++;
        }
        return hits;
    }

    public static void main(String[] args) throws InterruptedException {
        // --- multithreaded, atomic, correct ---
        AtomicLong hits = new AtomicLong(0);
        long perThread = TOTAL_TOSSES / NUM_THREADS;
        Thread[] threads = new Thread[NUM_THREADS];
        for (int i = 0; i < NUM_THREADS; i++) {
            threads[i] = new TossWorker(perThread, hits);
        }

        long start = System.nanoTime();
        for (Thread t : threads) t.start();
        for (Thread t : threads) t.join();
        long multiThreadedMs = (System.nanoTime() - start) / 1_000_000;

        double piMulti = 4.0 * hits.get() / TOTAL_TOSSES;
        System.out.printf("Multithreaded (AtomicLong): pi ~= %.6f  time=%d ms%n", piMulti, multiThreadedMs);

        // --- single-threaded baseline, same total work ---
        long start2 = System.nanoTime();
        long singleHits = countHitsSingleThreaded(TOTAL_TOSSES);
        long singleThreadedMs = (System.nanoTime() - start2) / 1_000_000;

        double piSingle = 4.0 * singleHits / TOTAL_TOSSES;
        System.out.printf("Single-threaded baseline:   pi ~= %.6f  time=%d ms%n", piSingle, singleThreadedMs);

        System.out.printf("%nSlowdown factor (multi/single): %.2fx%n",
                (double) multiThreadedMs / singleThreadedMs);
    }
}
