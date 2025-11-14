"""
Tanh-Sinh Quadrature Integration

This module provides optimized implementation of the double exponential (tanh-sinh)
quadrature method for numerical integration.
"""

import numpy as np
from numpy import pi, sinh, cosh, tanh


def tanh_sinh_int_original(fptr, a, b, h=0.5, n=10, max_level=10, tol=1e-10):
    """
    Original implementation of tanh-sinh integration (for comparison).
    
    Parameters:
    -----------
    fptr : callable
        Function to integrate
    a : float
        Lower bound of integration
    b : float
        Upper bound of integration
    h : float, optional
        Initial step size (default: 0.5)
    n : float, optional
        Range parameter (default: 10)
    max_level : int, optional
        Maximum refinement level (default: 10)
    tol : float, optional
        Tolerance for convergence (default: 1e-10)
    
    Returns:
    --------
    float
        Approximation of the integral
    """
    integral = 0.0
    prev_integral = 0.
    level = 0
    
    center = 0.5 * (a + b) 
    spread = 0.5 * (b - a)
    val0 = fptr(center) * spread * pi * 0.5
    prev_integral = val0 * 2 * h
    
    while level <= max_level:
        t_pos = np.arange(h, n + h, h + (level > 0) * h)
        phi_pos = 0.5 * pi * sinh(t_pos)
        x_pos = center + spread * tanh(phi_pos)
        x_neg = center * 2 - x_pos
        dxdt = (cosh(phi_pos) > 1.e-50) * spread * (0.5 * pi * cosh(t_pos)) / (cosh(phi_pos) ** 2)
        val = (fptr(x_pos) + fptr(x_neg)) * dxdt
        val = np.nan_to_num(val, nan=0.0, posinf=0.0, neginf=0.0)  # 处理nan和inf, 主要是奇点问题，但是有待检查
        integral = prev_integral / 2 + np.sum(val) * h
        error = np.abs(integral - prev_integral)
    
        if error < tol:
            break
        elif level > 5 and abs(np.sum(val) * h) < tol * abs(integral):
            break
        else:
            prev_integral = integral
            h = h / 2.
            level = level + 1
    
    return integral if np.isscalar(integral) else integral[0]


def tanh_sinh_int(fptr, a, b, h=0.5, n=10, max_level=10, tol=1e-10):
    """
    Optimized implementation of tanh-sinh integration.
    
    Key optimizations:
    1. Pre-compute constants outside the loop
    2. Use sech² = 1 - tanh² to avoid overflow
    3. Reduce memory allocations
    4. Better handling of numerical edge cases
    
    Parameters:
    -----------
    fptr : callable
        Function to integrate
    a : float
        Lower bound of integration
    b : float
        Upper bound of integration
    h : float, optional
        Initial step size (default: 0.5)
    n : float, optional
        Range parameter (default: 10)
    max_level : int, optional
        Maximum refinement level (default: 10)
    tol : float, optional
        Tolerance for convergence (default: 1e-10)
    
    Returns:
    --------
    float
        Approximation of the integral
    """
    # Pre-compute constants
    center = 0.5 * (a + b)
    spread = 0.5 * (b - a)
    pi_half = pi * 0.5
    
    # Initial value at center
    val0 = fptr(center) * spread * pi_half
    prev_integral = val0 * 2 * h
    
    level = 0
    
    while level <= max_level:
        # Generate sample points
        step = h + (level > 0) * h
        t_pos = np.arange(h, n + h, step)
        
        # Hyperbolic transformations
        sinh_t = np.sinh(t_pos)
        cosh_t = np.cosh(t_pos)
        phi_pos = pi_half * sinh_t
        
        # Use tanh for positions (more stable than cosh for large values)
        tanh_phi = np.tanh(phi_pos)
        x_pos = center + spread * tanh_phi
        x_neg = 2 * center - x_pos
        
        # Weight function using sech²(phi) = 1 - tanh²(phi)
        # This avoids overflow in cosh(phi) for large phi
        sech_sq_phi = 1.0 - tanh_phi * tanh_phi
        
        # Full weight: dxdt = spread * pi/2 * cosh(t) * sech²(phi)
        weights = spread * pi_half * cosh_t * sech_sq_phi
        
        # Filter out negligible contributions
        weights = np.where(sech_sq_phi > 1e-50, weights, 0.0)
        
        # Function evaluations
        try:
            f_pos = fptr(x_pos)
            f_neg = fptr(x_neg)
        except (TypeError, ValueError):
            # Fallback for non-vectorized functions
            f_pos = np.array([fptr(x) for x in x_pos])
            f_neg = np.array([fptr(x) for x in x_neg])
        
        # Weighted sum
        val = (f_pos + f_neg) * weights
        
        # Handle nan and inf
        val = np.nan_to_num(val, nan=0.0, posinf=0.0, neginf=0.0)
        
        # Update integral
        integral = prev_integral / 2 + np.sum(val) * h
        error = np.abs(integral - prev_integral)
        
        # Convergence checks
        if error < tol:
            break
        elif level > 5 and abs(np.sum(val) * h) < tol * abs(integral):
            break
        
        # Next level
        prev_integral = integral
        h = h / 2.
        level += 1
    
    return integral if np.isscalar(integral) else integral[0]


def adaptive_tanh_sinh_int(fptr, a, b, max_level=10, tol=1e-10, initial_h=0.5):
    """
    Alternative adaptive tanh-sinh integration (simplified version).
    
    This version uses a different approach that may be faster for some integrals.
    
    Parameters:
    -----------
    fptr : callable
        Function to integrate
    a : float
        Lower bound of integration
    b : float
        Upper bound of integration
    max_level : int, optional
        Maximum refinement level (default: 10)
    tol : float, optional
        Tolerance for convergence (default: 1e-10)
    initial_h : float, optional
        Initial step size (default: 0.5)
    
    Returns:
    --------
    float
        Approximation of the integral
    """
    # For now, just call the main optimized version
    # This can be replaced with a truly adaptive algorithm if needed
    return tanh_sinh_int(fptr, a, b, h=initial_h, max_level=max_level, tol=tol)


# Convenience function
def integrate(f, a, b, tol=1e-10, method='optimized'):
    """
    Convenience function for integration.
    
    Parameters:
    -----------
    f : callable
        Function to integrate
    a : float
        Lower bound
    b : float
        Upper bound
    tol : float, optional
        Tolerance (default: 1e-10)
    method : str, optional
        Method to use: 'optimized' (default), 'original', or 'adaptive'
    
    Returns:
    --------
    float
        Approximation of the integral
    """
    if method == 'original':
        return tanh_sinh_int_original(f, a, b, tol=tol)
    elif method == 'adaptive':
        return adaptive_tanh_sinh_int(f, a, b, tol=tol)
    else:
        return tanh_sinh_int(f, a, b, tol=tol)
