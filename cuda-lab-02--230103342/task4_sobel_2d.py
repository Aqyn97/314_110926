"""Task 4: 2D Sobel-X convolution with boundary-safe indexing and dynamic 2D grid."""
import numpy as np
from numba import cuda

THREADS_2D = (16, 16)


@cuda.jit
def sobel_x_kernel(d_in, d_out, rows, cols):
    col, row = cuda.grid(2)
    if row < rows and col < cols:
        if row > 0 and row < rows - 1 and col > 0 and col < cols - 1:
            d_out[row, col] = (
                np.float32(-1.0) * d_in[row - 1, col - 1] + np.float32(1.0) * d_in[row - 1, col + 1]
                + np.float32(-2.0) * d_in[row, col - 1] + np.float32(2.0) * d_in[row, col + 1]
                + np.float32(-1.0) * d_in[row + 1, col - 1] + np.float32(1.0) * d_in[row + 1, col + 1]
            )
        else:
            d_out[row, col] = np.float32(0.0)


def run_sobel(h_img):
    h_img = np.ascontiguousarray(h_img, dtype=np.float32)
    rows, cols = h_img.shape
    d_in = cuda.to_device(h_img)
    d_out = cuda.device_array((rows, cols), dtype=np.float32)
    # x-dimension of the grid maps to columns, y-dimension to rows
    grid = ((cols + THREADS_2D[0] - 1) // THREADS_2D[0],
            (rows + THREADS_2D[1] - 1) // THREADS_2D[1])
    sobel_x_kernel[grid, THREADS_2D](d_in, d_out, rows, cols)
    cuda.synchronize()
    return d_out.copy_to_host()


def cpu_sobel_x(img):
    out = np.zeros_like(img)
    out[1:-1, 1:-1] = (
        -img[:-2, :-2] + img[:-2, 2:]
        - 2.0 * img[1:-1, :-2] + 2.0 * img[1:-1, 2:]
        - img[2:, :-2] + img[2:, 2:]
    )
    return out


def main():
    rows = cols = 2048
    rng = np.random.default_rng(0)
    h_img = rng.random((rows, cols)).astype(np.float32)

    gpu = run_sobel(h_img)
    ref = cpu_sobel_x(h_img)
    assert np.allclose(gpu, ref, atol=1e-4), "Task 4 mismatch against CPU"
    assert np.all(gpu[0, :] == 0) and np.all(gpu[-1, :] == 0)
    assert np.all(gpu[:, 0] == 0) and np.all(gpu[:, -1] == 0)

    flat = run_sobel(np.ones((rows, cols), dtype=np.float32))
    assert np.max(np.abs(flat[1:-1, 1:-1])) < 1e-5, "Flat field gradient != 0"

    print(f"TASK 4 PASSED: MAX DELTA = {float(np.max(np.abs(gpu - ref)))}")


if __name__ == "__main__":
    main()
