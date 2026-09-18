import java.util.concurrent.ThreadLocalRandom;

public class Part3_Reduction {

    static final long TOTAL_TOSSES = 100_000_000L;
    static final int[] THREAD_COUNTS = {1, 2, 4, 8, 16, 32};

    // Each thread accumulates into its OWN local variable - no shared state
    // touched during the hot loop at all. Partial sums are combined once,
    // after every thread has finished (the "reduction" step).
    static class TossWorker extends Thread {
        final long tossesForThisThread;
        long localHits = 0; // private to this thread object

        TossWorker(long tosses) {
            this.tossesForThisThread = tosses;
        }

        @Override
        public void run() {
            ThreadLocalRandom rnd = ThreadLocalRandom.current();
            long hits = 0;
            for (long i = 0; i < tossesForThisThread; i++) {
                double x = rnd.nextDouble();
                double y = rnd.nextDouble();
                if (x * x + y * y <= 1.0) hits++;
            }
            localHits = hits; // single write at the very end
        }
    }

    static long runTrial(int numThreads) throws InterruptedException {
        long perThread = TOTAL_TOSSES / numThreads;
        TossWorker[] workers = new TossWorker[numThreads];
        for (int i = 0; i < numThreads; i++) {
            workers[i] = new TossWorker(perThread);
        }

        long start = System.nanoTime();
        for (TossWorker w : workers) w.start();
        for (TossWorker w : workers) w.join();
        long elapsedMs = (System.nanoTime() - start) / 1_000_000;

        long totalHits = 0;
        for (TossWorker w : workers) totalHits += w.localHits; // reduction

        double pi = 4.0 * totalHits / TOTAL_TOSSES;
        System.out.printf("  (sanity check pi ~= %.6f)%n", pi);
        return elapsedMs;
    }

    public static void main(String[] args) throws InterruptedException {
        System.out.println("Threads | Runtime(ms) | Speedup vs T1 | Efficiency");
        System.out.println("--------------------------------------------------");

        long baseline = -1;
        for (int t : THREAD_COUNTS) {
            long ms = runTrial(t);
            if (baseline == -1) baseline = ms;
            double speedup = (double) baseline / ms;
            double efficiency = speedup / t * 100.0;
            System.out.printf("%7d | %11d | %13.2fx | %8.1f%%%n", t, ms, speedup, efficiency);
        }
    }
}
