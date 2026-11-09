"""SI constants and Planck units, for unit checks and non-dimensionalising only.

Sources: 2019 SI redefinition (c, h, k_B exact); G from CODATA 2018 (6.67430(15)e-11,
unchanged in CODATA 2022). Planck units are derived, not measured. Nothing here asserts
a minimum length/time or any discretisation (spec section 11)."""
import math
from .common import positive

C = 299_792_458.0            # m/s, exact
H = 6.626_070_15e-34         # J s, exact
K_B = 1.380_649e-23          # J/K, exact
G = 6.674_30e-11             # m^3 kg^-1 s^-2, rel. u = 2.2e-5
G_REL_UNCERTAINTY = 2.2e-5
HBAR = H / (2 * math.pi)

L_P = math.sqrt(HBAR * G / C**3)     # m
T_P = L_P / C                        # s
M_P = math.sqrt(HBAR * C / G)        # kg
E_P = M_P * C**2                     # J
TEMP_P = E_P / K_B                   # K

def to_planck_time(seconds):
    """Dimensionless t/t_P. Display/scaling aid only."""
    return positive("seconds", seconds) / T_P

def to_planck_length(metres):
    return positive("metres", metres) / L_P
