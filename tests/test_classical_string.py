"""Standard-library conformance tests for Branch A."""
import math
import unittest

from pan_harmonics.classical_string import (
    angular_frequency,
    barbershop_scale,
    eigenfunction,
    frequency,
    modal_displacement,
    normalized_eigenfunction,
    wave_speed,
)


def simpson(function, a, b, intervals=2000):
    if intervals % 2:
        raise ValueError("intervals must be even")
    h = (b - a) / intervals
    total = function(a) + function(b)
    total += 4.0 * sum(function(a + i * h) for i in range(1, intervals, 2))
    total += 2.0 * sum(function(a + i * h) for i in range(2, intervals, 2))
    return total * h / 3.0


class ClassicalStringTests(unittest.TestCase):
    def setUp(self):
        self.length = 0.65
        self.tension = 72.0
        self.density = 0.006

    def test_wave_speed_and_fundamental(self):
        c = wave_speed(self.tension, self.density)
        self.assertAlmostEqual(c, math.sqrt(12000.0), places=12)
        self.assertAlmostEqual(frequency(1, self.length, self.tension, self.density), c / (2 * self.length))

    def test_integer_harmonic_ratios(self):
        f1 = frequency(1, self.length, self.tension, self.density)
        for n in range(1, 13):
            self.assertAlmostEqual(frequency(n, self.length, self.tension, self.density) / f1, float(n), places=12)

    def test_angular_frequency_consistency(self):
        for n in range(1, 8):
            self.assertAlmostEqual(angular_frequency(n, self.length, self.tension, self.density),
                                   2 * math.pi * frequency(n, self.length, self.tension, self.density))

    def test_fixed_endpoints(self):
        for n in range(1, 10):
            self.assertAlmostEqual(eigenfunction(n, 0.0, self.length), 0.0, places=14)
            self.assertAlmostEqual(eigenfunction(n, self.length, self.length), 0.0, places=13)

    def test_analytic_orthogonality(self):
        # Integral sin(m*pi*x/L) sin(n*pi*x/L) dx = L/2 * delta_mn.
        for m in range(1, 6):
            for n in range(1, 6):
                expected = self.length / 2 if m == n else 0.0
                value = simpson(lambda x: eigenfunction(m, x, self.length) *
                                eigenfunction(n, x, self.length), 0.0, self.length)
                self.assertAlmostEqual(value, expected, delta=2e-10)

    def test_normalized_modes(self):
        for n in range(1, 6):
            norm = simpson(lambda x: normalized_eigenfunction(n, x, self.length) ** 2,
                           0.0, self.length)
            self.assertAlmostEqual(norm, 1.0, delta=2e-10)

    def test_barbershop_halving_is_independent(self):
        for n in range(1, 8):
            for k in (-3, 0, 1, 5):
                self.assertAlmostEqual(barbershop_scale(n, k + 1) / barbershop_scale(n, k), 0.5)

    def test_modal_solution_respects_fixed_ends(self):
        args = (0.17, 0.23, self.length, self.tension, self.density, (0.2, -0.1), (0.03, 0.07))
        self.assertAlmostEqual(modal_displacement(0.0, *args[1:]), 0.0, places=14)
        self.assertAlmostEqual(modal_displacement(self.length, *args[1:]), 0.0, places=13)
        self.assertTrue(math.isfinite(modal_displacement(*args)))

    def test_invalid_physical_inputs_rejected(self):
        for bad in (0, -1, float("nan"), float("inf")):
            with self.assertRaises((TypeError, ValueError)):
                wave_speed(bad, self.density)
            with self.assertRaises((TypeError, ValueError)):
                frequency(1, bad, self.tension, self.density)

    def test_invalid_modes_and_coordinates_rejected(self):
        for bad in (0, -1, 1.5, True):
            with self.assertRaises(ValueError):
                frequency(bad, self.length, self.tension, self.density)
        with self.assertRaises(ValueError):
            eigenfunction(1, self.length + 0.01, self.length)
        with self.assertRaises(ValueError):
            barbershop_scale(1, float("nan"))

    def test_modal_coefficients_must_match(self):
        with self.assertRaises(ValueError):
            modal_displacement(0.2, 0.1, self.length, self.tension, self.density, (1.0,), (1.0, 2.0))


if __name__ == "__main__":
    unittest.main()
