"""
Test and benchmark suite for tanh-sinh integration.
"""

import numpy as np
import time
from tanh_sinh_integration import (
    tanh_sinh_int_original,
    tanh_sinh_int,
    adaptive_tanh_sinh_int,
    integrate
)


def test_basic_integrals():
    """Test basic integrals with known results."""
    print("Testing basic integrals...")
    
    # Test 1: ∫(x^2)dx from 0 to 1 = 1/3
    def f1(x):
        return x**2
    
    result = integrate(f1, 0, 1, tol=1e-10)
    expected = 1/3
    error = abs(result - expected)
    print(f"  ∫x²dx from 0 to 1: {result:.12f} (expected: {expected:.12f}, error: {error:.2e})")
    assert error < 1e-9, f"Error too large: {error}"
    
    # Test 2: ∫(sin(x))dx from 0 to π = 2
    def f2(x):
        return np.sin(x)
    
    result = integrate(f2, 0, np.pi, tol=1e-10)
    expected = 2.0
    error = abs(result - expected)
    print(f"  ∫sin(x)dx from 0 to π: {result:.12f} (expected: {expected:.12f}, error: {error:.2e})")
    assert error < 1e-9, f"Error too large: {error}"
    
    # Test 3: ∫(e^x)dx from 0 to 1 = e - 1
    def f3(x):
        return np.exp(x)
    
    result = integrate(f3, 0, 1, tol=1e-10)
    expected = np.e - 1
    error = abs(result - expected)
    print(f"  ∫e^x dx from 0 to 1: {result:.12f} (expected: {expected:.12f}, error: {error:.2e})")
    assert error < 1e-9, f"Error too large: {error}"
    
    # Test 4: ∫(1/x)dx from 1 to e = 1
    def f4(x):
        return 1/x
    
    result = integrate(f4, 1, np.e, tol=1e-10)
    expected = 1.0
    error = abs(result - expected)
    print(f"  ∫(1/x)dx from 1 to e: {result:.12f} (expected: {expected:.12f}, error: {error:.2e})")
    assert error < 1e-9, f"Error too large: {error}"
    
    print("✓ All basic tests passed!\n")


def test_oscillatory_integrals():
    """Test oscillatory integrals."""
    print("Testing oscillatory integrals...")
    
    # ∫(cos(10x))dx from 0 to 2π = 0
    def f_osc(x):
        return np.cos(10 * x)
    
    result = integrate(f_osc, 0, 2 * np.pi, tol=1e-9)
    expected = 0.0
    error = abs(result - expected)
    print(f"  ∫cos(10x)dx from 0 to 2π: {result:.12f} (expected: {expected:.12f}, error: {error:.2e})")
    assert error < 1e-7, f"Error too large: {error}"
    
    print("✓ Oscillatory test passed!\n")


def test_difficult_integrals():
    """Test integrals with challenging features."""
    print("Testing difficult integrals...")
    
    # Gaussian integral approximation: ∫(e^(-x²))dx from -3 to 3
    # The actual value is erf(3) * √π ≈ 1.772414
    def f_gauss(x):
        return np.exp(-x**2)
    
    result = integrate(f_gauss, -3, 3, tol=1e-9)
    # Use scipy.special.erf if available, otherwise use numerical approximation
    try:
        from scipy.special import erf
        expected = erf(3) * np.sqrt(np.pi)
    except ImportError:
        # Numerical reference value for this specific integral
        expected = 1.772414696519  # High-precision reference
    
    error = abs(result - expected)
    print(f"  ∫e^(-x²)dx from -3 to 3: {result:.12f} (expected: {expected:.12f}, error: {error:.2e})")
    # More relaxed tolerance for this one
    assert error < 1e-7, f"Error too large: {error}"
    
    print("✓ Difficult integral test passed!\n")


def test_vectorized_functions():
    """Test that vectorized functions work correctly."""
    print("Testing vectorized function support...")
    
    # Vectorized function
    def f_vec(x):
        return np.sin(x) * np.exp(-x)
    
    result = integrate(f_vec, 0, 2, tol=1e-10)
    # Expected: analytical result would be (1 - e^(-2)(cos(2) + sin(2)))/2
    expected = (1 - np.exp(-2) * (np.cos(2) + np.sin(2))) / 2
    error = abs(result - expected)
    print(f"  ∫sin(x)e^(-x)dx from 0 to 2: {result:.12f} (expected: {expected:.12f}, error: {error:.2e})")
    assert error < 1e-9, f"Error too large: {error}"
    
    print("✓ Vectorized function test passed!\n")


def benchmark_performance():
    """Benchmark the different implementations."""
    print("Benchmarking performance...")
    print("=" * 60)
    
    # Test function: integrate sin(x) from 0 to π multiple times
    def f_bench(x):
        return np.sin(x)
    
    num_runs = 20
    
    # Benchmark original
    start = time.time()
    for _ in range(num_runs):
        result_orig = integrate(f_bench, 0, np.pi, tol=1e-10, method='original')
    time_orig = (time.time() - start) / num_runs
    
    # Benchmark optimized
    start = time.time()
    for _ in range(num_runs):
        result_opt = integrate(f_bench, 0, np.pi, tol=1e-10, method='optimized')
    time_opt = (time.time() - start) / num_runs
    
    # Benchmark adaptive
    start = time.time()
    for _ in range(num_runs):
        result_adap = integrate(f_bench, 0, np.pi, tol=1e-10, method='adaptive')
    time_adap = (time.time() - start) / num_runs
    
    print(f"Function: ∫sin(x)dx from 0 to π")
    print(f"Expected result: 2.0")
    print()
    print(f"Original implementation:")
    print(f"  Result: {result_orig:.12f}")
    print(f"  Time:   {time_orig*1000:.3f} ms")
    print()
    print(f"Optimized implementation:")
    print(f"  Result: {result_opt:.12f}")
    print(f"  Time:   {time_opt*1000:.3f} ms")
    print(f"  Speedup: {time_orig/time_opt:.2f}x")
    print()
    print(f"Adaptive implementation:")
    print(f"  Result: {result_adap:.12f}")
    print(f"  Time:   {time_adap*1000:.3f} ms")
    print(f"  Speedup: {time_orig/time_adap:.2f}x")
    print()
    
    # More challenging integral
    def f_bench2(x):
        return x**3 * np.exp(-x**2)
    
    print("=" * 60)
    print("More challenging function: ∫x³e^(-x²)dx from 0 to 3")
    
    start = time.time()
    for _ in range(num_runs):
        result_orig = integrate(f_bench2, 0, 3, tol=1e-10, method='original')
    time_orig = (time.time() - start) / num_runs
    
    start = time.time()
    for _ in range(num_runs):
        result_opt = integrate(f_bench2, 0, 3, tol=1e-10, method='optimized')
    time_opt = (time.time() - start) / num_runs
    
    start = time.time()
    for _ in range(num_runs):
        result_adap = integrate(f_bench2, 0, 3, tol=1e-10, method='adaptive')
    time_adap = (time.time() - start) / num_runs
    
    print(f"Original implementation:")
    print(f"  Result: {result_orig:.12f}")
    print(f"  Time:   {time_orig*1000:.3f} ms")
    print()
    print(f"Optimized implementation:")
    print(f"  Result: {result_opt:.12f}")
    print(f"  Time:   {time_opt*1000:.3f} ms")
    print(f"  Speedup: {time_orig/time_opt:.2f}x")
    print()
    print(f"Adaptive implementation:")
    print(f"  Result: {result_adap:.12f}")
    print(f"  Time:   {time_adap*1000:.3f} ms")
    print(f"  Speedup: {time_orig/time_adap:.2f}x")
    print()
    print("=" * 60)


def test_edge_cases():
    """Test edge cases."""
    print("Testing edge cases...")
    
    # Constant function
    def f_const(x):
        return 5.0
    
    result = integrate(f_const, 0, 2, tol=1e-10)
    expected = 10.0
    error = abs(result - expected)
    print(f"  ∫5dx from 0 to 2: {result:.12f} (expected: {expected:.12f}, error: {error:.2e})")
    assert error < 1e-9, f"Error too large: {error}"
    
    # Zero function
    def f_zero(x):
        return 0.0
    
    result = integrate(f_zero, 0, 1, tol=1e-10)
    expected = 0.0
    error = abs(result - expected)
    print(f"  ∫0dx from 0 to 1: {result:.12f} (expected: {expected:.12f}, error: {error:.2e})")
    assert error < 1e-9, f"Error too large: {error}"
    
    # Negative interval (should handle b < a)
    def f_simple(x):
        return x
    
    result = integrate(f_simple, 1, 0, tol=1e-10)
    expected = -0.5  # ∫x dx from 1 to 0 = -(1/2)
    error = abs(result - expected)
    print(f"  ∫x dx from 1 to 0: {result:.12f} (expected: {expected:.12f}, error: {error:.2e})")
    assert error < 1e-9, f"Error too large: {error}"
    
    print("✓ All edge case tests passed!\n")


def main():
    """Run all tests and benchmarks."""
    print("\n" + "=" * 60)
    print("Tanh-Sinh Integration Test Suite")
    print("=" * 60 + "\n")
    
    try:
        test_basic_integrals()
        test_oscillatory_integrals()
        test_difficult_integrals()
        test_vectorized_functions()
        test_edge_cases()
        
        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("=" * 60 + "\n")
        
        benchmark_performance()
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}\n")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}\n")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
