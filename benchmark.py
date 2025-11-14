"""
Detailed performance comparison and profiling.
"""

import numpy as np
import time
from tanh_sinh_integration import tanh_sinh_int_original, tanh_sinh_int


def benchmark_detailed():
    """Detailed benchmark showing optimization impact."""
    
    print("\n" + "=" * 70)
    print("DETAILED PERFORMANCE BENCHMARK")
    print("=" * 70)
    
    test_cases = [
        {
            'name': 'Polynomial (x³)',
            'func': lambda x: x**3,
            'a': 0, 'b': 2,
            'expected': 4.0
        },
        {
            'name': 'Trigonometric (sin(x))',
            'func': lambda x: np.sin(x),
            'a': 0, 'b': np.pi,
            'expected': 2.0
        },
        {
            'name': 'Exponential (e^(-x))',
            'func': lambda x: np.exp(-x),
            'a': 0, 'b': 5,
            'expected': 1 - np.exp(-5)
        },
        {
            'name': 'Rational (1/(1+x²))',
            'func': lambda x: 1.0 / (1 + x**2),
            'a': -5, 'b': 5,
            'expected': 2 * np.arctan(5)
        },
        {
            'name': 'Gaussian (e^(-x²))',
            'func': lambda x: np.exp(-x**2),
            'a': -3, 'b': 3,
            'expected': 1.772414696519  # erf(3) * sqrt(pi)
        },
        {
            'name': 'Oscillatory (sin(20x))',
            'func': lambda x: np.sin(20 * x),
            'a': 0, 'b': np.pi,
            'expected': 0.1  # (1 - cos(20π)) / 20
        },
        {
            'name': 'Mixed (x²·sin(x))',
            'func': lambda x: x**2 * np.sin(x),
            'a': 0, 'b': np.pi,
            'expected': np.pi**2 - 4  # Analytical result
        },
        {
            'name': 'Logarithmic (ln(1+x))',
            'func': lambda x: np.log(1 + x),
            'a': 0, 'b': 1,
            'expected': 2 * np.log(2) - 1
        },
    ]
    
    num_runs = 50
    tol = 1e-10
    
    total_speedup = 0
    count = 0
    
    for test in test_cases:
        print(f"\n{test['name']}")
        print(f"  Integral from {test['a']} to {test['b']}")
        print(f"  Expected: {test['expected']:.12f}")
        
        # Benchmark original
        times_orig = []
        for _ in range(num_runs):
            start = time.perf_counter()
            result_orig = tanh_sinh_int_original(test['func'], test['a'], test['b'], tol=tol)
            times_orig.append(time.perf_counter() - start)
        time_orig = np.mean(times_orig)
        
        # Benchmark optimized
        times_opt = []
        for _ in range(num_runs):
            start = time.perf_counter()
            result_opt = tanh_sinh_int(test['func'], test['a'], test['b'], tol=tol)
            times_opt.append(time.perf_counter() - start)
        time_opt = np.mean(times_opt)
        
        # Calculate speedup
        speedup = time_orig / time_opt
        total_speedup += speedup
        count += 1
        
        # Check accuracy
        error_orig = abs(result_orig - test['expected'])
        error_opt = abs(result_opt - test['expected'])
        
        print(f"  Original: {result_orig:.12f} (error: {error_orig:.2e}, time: {time_orig*1000:.3f} ms)")
        print(f"  Optimized: {result_opt:.12f} (error: {error_opt:.2e}, time: {time_opt*1000:.3f} ms)")
        print(f"  Speedup: {speedup:.2f}x")
    
    print("\n" + "=" * 70)
    print(f"Average speedup: {total_speedup/count:.2f}x")
    print("=" * 70 + "\n")


def profile_operations():
    """Profile specific operations to show where time is spent."""
    
    print("\n" + "=" * 70)
    print("PROFILING: TIME SPENT IN KEY OPERATIONS")
    print("=" * 70)
    
    # Simple test function
    f = lambda x: np.sin(x)
    
    # Manually time key operations in original implementation
    print("\nOriginal implementation breakdown:")
    
    h = 0.5
    n = 10
    level = 0
    a, b = 0, np.pi
    center = 0.5 * (a + b)
    spread = 0.5 * (b - a)
    
    iterations = 1000
    
    # Time array generation
    start = time.perf_counter()
    for _ in range(iterations):
        t_pos = np.arange(h, n+h, h+(level > 0)*h)
    time_array_gen = (time.perf_counter() - start) / iterations * 1000
    print(f"  Array generation: {time_array_gen:.4f} ms")
    
    t_pos = np.arange(h, n+h, h+(level > 0)*h)
    
    # Time sinh/cosh calculation
    start = time.perf_counter()
    for _ in range(iterations):
        phi_pos = 0.5 * np.pi * np.sinh(t_pos)
        _ = np.cosh(phi_pos)
        _ = np.tanh(phi_pos)
        _ = np.cosh(t_pos)
    time_hyp = (time.perf_counter() - start) / iterations * 1000
    print(f"  Hyperbolic functions: {time_hyp:.4f} ms")
    
    phi_pos = 0.5 * np.pi * np.sinh(t_pos)
    cosh_phi = np.cosh(phi_pos)
    tanh_phi = np.tanh(phi_pos)
    cosh_t = np.cosh(t_pos)
    
    # Time x position calculation
    start = time.perf_counter()
    for _ in range(iterations):
        x_pos = center + spread * tanh_phi
        x_neg = center * 2 - x_pos
    time_xpos = (time.perf_counter() - start) / iterations * 1000
    print(f"  Position calculation: {time_xpos:.4f} ms")
    
    x_pos = center + spread * tanh_phi
    x_neg = center * 2 - x_pos
    
    # Time weight calculation (original method)
    start = time.perf_counter()
    for _ in range(iterations):
        dxdt = (cosh_phi > 1.e-50) * spread * (0.5 * np.pi * cosh_t) / (cosh_phi ** 2)
    time_weight_orig = (time.perf_counter() - start) / iterations * 1000
    print(f"  Weight calculation (original): {time_weight_orig:.4f} ms")
    
    # Time function evaluation
    start = time.perf_counter()
    for _ in range(iterations):
        f_pos = f(x_pos)
        f_neg = f(x_neg)
    time_func = (time.perf_counter() - start) / iterations * 1000
    print(f"  Function evaluation: {time_func:.4f} ms")
    
    print("\nOptimized implementation breakdown:")
    
    half_pi = 0.5 * np.pi
    pi_spread = spread * half_pi
    
    # Time optimized weight calculation
    start = time.perf_counter()
    for _ in range(iterations):
        sech_phi_sq = 1.0 - tanh_phi * tanh_phi
        mask = sech_phi_sq > 1e-50
        dxdt = np.zeros_like(t_pos)
        dxdt[mask] = pi_spread * cosh_t[mask] * sech_phi_sq[mask]
    time_weight_opt = (time.perf_counter() - start) / iterations * 1000
    print(f"  Weight calculation (optimized): {time_weight_opt:.4f} ms")
    
    print(f"\n  Weight calculation speedup: {time_weight_orig/time_weight_opt:.2f}x")
    
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    benchmark_detailed()
    profile_operations()
