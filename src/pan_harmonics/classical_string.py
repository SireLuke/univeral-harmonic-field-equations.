"""Classical fixed-end string reference model (Branch A).

This module is deliberately independent of PAN V8 and speculative field mappings.
All inputs use SI units: length [m], tension [N], linear density [kg/m].
"""
from __future__ import annotations

import math
from numbers import Integral, Real


def _positive_finite(name: str, value: Real) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number")
    result = float(value)
    if not math.isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be finite and > 0")
    return result


def _mode_index(n: int) -> int:
    if isinstance(n, bool) or not isinstance(n, Integral) or n < 1:
        raise ValueError("mode index n must be a positive integer")
    return int(n)


def wave_speed(tension: Real, linear_density: Real) -> float:
    """Return c = sqrt(tension / linear_density), in m/s."""
    tension = _positive_finite("tension", tension)
    linear_density = _positive_finite("linear_density", linear_density)
    return math.sqrt(tension / linear_density)


def frequency(mode: int, length: Real, tension: Real, linear_density: Real) -> float:
    """Return the nth fixed-end ideal-string frequency, in Hz."""
    n = _mode_index(mode)
    length = _positive_finite("length", length)
    c = wave_speed(tension, linear_density)
    return n * c / (2.0 * length)


def angular_frequency(mode: int, length: Real, tension: Real, linear_density: Real) -> float:
    """Return omega_n = 2*pi*f_n, in rad/s."""
    return 2.0 * math.pi * frequency(mode, length, tension, linear_density)


def eigenfunction(mode: int, x: Real, length: Real) -> float:
    """Return the unnormalized fixed-end spatial mode sin(n*pi*x/L)."""
    n = _mode_index(mode)
    length = _positive_finite("length", length)
    if isinstance(x, bool) or not isinstance(x, Real):
        raise TypeError("x must be a real number")
    x = float(x)
    if not math.isfinite(x) or not 0.0 <= x <= length:
        raise ValueError("x must be finite and lie in [0, length]")
    return math.sin(n * math.pi * x / length)


def normalized_eigenfunction(mode: int, x: Real, length: Real) -> float:
    """Return sqrt(2/L)*sin(n*pi*x/L), L2-normalized on [0,L]."""
    length = _positive_finite("length", length)
    return math.sqrt(2.0 / length) * eigenfunction(mode, x, length)


def barbershop_scale(mode: int, x: Real) -> float:
    """Return dimensionless b_n(x)=n*2**(-x), independent of string physics."""
    n = _mode_index(mode)
    if isinstance(x, bool) or not isinstance(x, Real):
        raise TypeError("x must be a real number")
    x = float(x)
    if not math.isfinite(x):
        raise ValueError("x must be finite")
    try:
        result = n * math.exp2(-x)
    except OverflowError as exc:
        raise ValueError("barbershop scale is outside floating-point range") from exc
    if not math.isfinite(result) or result == 0.0:
        raise ValueError("barbershop scale is outside representable floating-point range")
    return result


def modal_displacement(
    x: Real,
    t: Real,
    length: Real,
    tension: Real,
    linear_density: Real,
    cosine_coefficients: tuple[Real, ...],
    sine_coefficients: tuple[Real, ...] | None = None,
) -> float:
    """Evaluate a finite real modal expansion.

    Coefficients are displacement amplitudes in metres. Tuple position i
    corresponds to mode n=i+1. This is a finite-mode solution of the ideal
    linear string equation.
    """
    length = _positive_finite("length", length)
    c = wave_speed(tension, linear_density)
    if isinstance(x, bool) or not isinstance(x, Real) or not math.isfinite(float(x)) or not 0 <= x <= length:
        raise ValueError("x must be finite and lie in [0, length]")
    if isinstance(t, bool) or not isinstance(t, Real) or not math.isfinite(float(t)):
        raise ValueError("t must be finite")
    if sine_coefficients is None:
        sine_coefficients = (0.0,) * len(cosine_coefficients)
    if len(cosine_coefficients) != len(sine_coefficients):
        raise ValueError("cosine and sine coefficient arrays must have equal length")
    total = 0.0
    for n, (a, b) in enumerate(zip(cosine_coefficients, sine_coefficients), start=1):
        if any(isinstance(v, bool) or not isinstance(v, Real) or not math.isfinite(float(v)) for v in (a, b)):
            raise ValueError("modal coefficients must be finite real numbers")
        omega = n * math.pi * c / length
        total += (float(a) * math.cos(omega * float(t)) + float(b) * math.sin(omega * float(t))) * math.sin(n * math.pi * float(x) / length)
    return total
