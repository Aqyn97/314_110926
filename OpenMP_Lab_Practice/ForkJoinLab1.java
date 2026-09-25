import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.concurrent.CountDownLatch;
public class ForkJoinLab1 {

    static final int[] SWEEP_SIZES = {1, 2, 4, 8, 16, 32, 64};
    static final int TRIALS_PER_SIZE = 5;
    static final long WORKLOAD_SQRT_OPS = 10_000_000L;

    public static void main(String[] args) throws Exception {
        String mode = args.length > 0 ? args[0] : "identify";

        switch (mode) {
            case "identify" -> {
                int n = args.length > 1 ? Integer.parseInt(args[1]) : 4;
                runTeamIdentify(n);
            }
            case "sweep" -> runOversubscriptionSweep();
            case "workload" -> {
                int n = args.length > 1 ? Integer.parseInt(args[1]) : 4;
                runWorkload(n);
            }
            default -> System.out.println("Unknown mode. Use: identify | sweep | workload");
        }
    }

    // ---- Task 1.1
    static void runTeamIdentify(int numThreads) throws InterruptedException {
        System.out.println("--- Forking a team of " + numThreads + " threads ---");
        Thread[] team = new Thread[numThreads];
        CountDownLatch barrier = new CountDownLatch(numThreads);

        for (int tid = 0; tid < numThreads; tid++) {
            final int rank = tid;
            team[tid] = new Thread(() -> {
            long nativeTid = Thread.currentThread().getId();
            String role = (rank == 0) ? "Master" : "Worker";
            double busy = 0;
            for (long k = 0; k < 3_000_000L; k++) {
                busy += Math.sqrt(k + rank);
            }
            if (busy < 0) System.out.println("unreachable " + busy);
            System.out.printf("[%s] Logical Rank: %d of %d | Native OS TID: %d%n",
                    role, rank, numThreads, nativeTid);
            barrier.countDown();
        });
            team[tid].start();
        }
        for (Thread t : team) t.join(); 
        System.out.println("--- Joined thread team. Execution returned to serial master ---\n");
    }

    // Task 1.2
    static void runOversubscriptionSweep() throws Exception {
        System.out.println("Running oversubscription sweep across P = {1,2,4,8,16,32,64}...");
        try (PrintWriter csv = new PrintWriter(new FileWriter("data/lab1_oversubscription.csv"))) {
            csv.println("threads,trial,time_ms");
            for (int p : SWEEP_SIZES) {
                double total = 0;
                for (int trial = 1; trial <= TRIALS_PER_SIZE; trial++) {
                    long t0 = System.nanoTime();
                    Thread[] team = new Thread[p];
                    for (int tid = 0; tid < p; tid++) {
                        team[tid] = new Thread(() -> {
                        });
                        team[tid].start();
                    }
                    for (Thread t : team) t.join();
                    long t1 = System.nanoTime();
                    double ms = (t1 - t0) / 1_000_000.0;
                    total += ms;
                    csv.printf("%d,%d,%.4f%n", p, trial, ms);
                }
                System.out.printf("P=%3d | Avg fork-join time: %.4f ms%n", p, total / TRIALS_PER_SIZE);
            }
        }
        System.out.println("Wrote data/lab1_oversubscription.csv");
    }

    //  Task 1.3
    static void runWorkload(int numThreads) throws InterruptedException {
        System.out.println("Running CPU saturation workload with " + numThreads
                + " threads (" + WORKLOAD_SQRT_OPS + " sqrt ops each).");
        System.out.println("Switch to htop / Task Manager / Activity Monitor now.");
        Thread[] team = new Thread[numThreads];
        long t0 = System.nanoTime();
        for (int tid = 0; tid < numThreads; tid++) {
            team[tid] = new Thread(() -> {
                double acc = 0;
                for (long i = 0; i < WORKLOAD_SQRT_OPS; i++) {
                    acc += Math.sqrt(i);
                }
                if (acc < 0) System.out.println("unreachable " + acc);
            });
            team[tid].start();
        }
        for (Thread t : team) t.join();
        long t1 = System.nanoTime();
        System.out.printf("Completed in %.4f seconds.%n", (t1 - t0) / 1e9);
    }
}
