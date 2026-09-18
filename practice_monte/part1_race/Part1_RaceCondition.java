import java.util.concurrent.ThreadLocalRandom;

public class Part1_RaceCondition {

    static long totalHits = 0; // counter 
    static final long TOTAL_TOSSES = 50_000_000L;
    static final int NUM_THREADS = 4;

    static class TossWorker extends Thread {
        final long tossesForThisThread;

        TossWorker(long tosses) {
            this.tossesForThisThread = tosses;
        }

        @Override
        public void run() {
            ThreadLocalRandom rnd = ThreadLocalRandom.current();
            for (long i = 0; i < tossesForThisThread; i++) {
                double x = rnd.nextDouble();
                double y = rnd.nextDouble();
                if (x * x + y * y <= 1.0) {
                    totalHits++; //  the race
                }
            }
        }
    }

    static double runOneTrial() throws InterruptedException {
        totalHits = 0;
        long perThread = TOTAL_TOSSES / NUM_THREADS;

        Thread[] threads = new Thread[NUM_THREADS];
        for (int i = 0; i < NUM_THREADS; i++) {
            threads[i] = new TossWorker(perThread);
        }
        for (Thread t : threads) t.start();
        for (Thread t : threads) t.join();

        return 4.0 * totalHits / TOTAL_TOSSES;
    }

    public static void main(String[] args) throws InterruptedException {
        System.out.println("Part 1: unsynchronized totalHits++ across 4 threads");
        System.out.println("Expected pi ~= 3.14159\n");
        for (int trial = 1; trial <= 5; trial++) {
            double pi = runOneTrial();
            System.out.printf("Trial %d: totalHits=%d  pi ~= %.6f%n", trial, totalHits, pi);
        }
    }
}
