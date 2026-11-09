"""Two-level open-system reference models (spec 2.1, Experiments A and B).

Basis (declared): energy eigenbasis, index 0 = excited |e>, index 1 = ground |g>.
H = (E_gap/2) sigma_z, sigma_z = diag(+1,-1). Energies in J, rates in 1/s, times in s.
Coherence: l1 norm of off-diagonals, C = 2|rho_01|, in this basis."""
import cmath, math
from .common import finite, nonneg, positive, quantity, require_keys, provenance, UdfeError

BASIS = "energy eigenbasis (index 0 = excited, 1 = ground)"

def _check_state(rho, tol=1e-9):
    for row in rho:
        for z in row: finite("rho entry (real)", z.real); finite("rho entry (imag)", z.imag)
    if abs(rho[0][1] - rho[1][0].conjugate()) > tol: raise UdfeError("rho is not Hermitian")
    if abs(rho[0][0] + rho[1][1] - 1) > tol: raise UdfeError("trace(rho) != 1")
    if rho[0][0].real < -tol or rho[1][1].real < -tol or abs(rho[0][1]) ** 2 > rho[0][0].real * rho[1][1].real + tol:
        raise UdfeError("rho is not positive semidefinite")

def state(p_excited, coherence_phase_amplitude):
    """rho = [[p, c],[c*, 1-p]] with complex c = rho_01."""
    p = finite("p_excited", p_excited)
    c = complex(coherence_phase_amplitude)
    rho = [[complex(p), c], [c.conjugate(), complex(1 - p)]]
    _check_state(rho); return rho

def coherence_l1(rho): return 2 * abs(rho[0][1])

def retention(rho_t, rho_0):
    """H_C(t) = C(t)/C(0); requires C(0) > 0 (spec 2.1)."""
    c0 = coherence_l1(rho_0)
    if not c0 > 0: raise UdfeError("C(0) must be > 0 for the normalized coherence measure")
    return coherence_l1(rho_t) / c0

def decoherence_signal(rho_t, rho_0): return 1.0 - retention(rho_t, rho_0)

def energy(rho, e_gap_j):
    e = quantity("e_gap", e_gap_j, "J")
    return 0.5 * e * (rho[0][0].real - rho[1][1].real)

def entropy_nats(rho):
    """Von Neumann entropy of the qubit (a SYSTEM property; not entropy production)."""
    d = rho[0][0].real - rho[1][1].real
    r = math.sqrt(d * d + 4 * abs(rho[0][1]) ** 2)
    s = 0.0
    for lam in ((1 + r) / 2, (1 - r) / 2):
        if lam > 1e-15: s -= lam * math.log(lam)
    return s

def analytic(rho0, t, gamma_1, gamma_phi, omega=0.0):
    """Exact solution of the Markovian qubit master equation with amplitude damping and pure dephasing."""
    g1, gp, t = nonneg("gamma_1", gamma_1), nonneg("gamma_phi", gamma_phi), nonneg("t", t)
    p = rho0[0][0].real * math.exp(-g1 * t)
    c = rho0[0][1] * cmath.exp(-(g1 / 2 + gp) * t - 1j * finite("omega", omega) * t)
    return state(p, c)

# ---- independent numerical check: Lindblad equation integrated with RK4 ------------------------------
def _mm(a, b): return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def _dag(a): return [[a[j][i].conjugate() for j in range(2)] for i in range(2)]
def _add(a, b): return [[a[i][j] + b[i][j] for j in range(2)] for i in range(2)]
def _sc(a, s): return [[a[i][j] * s for j in range(2)] for i in range(2)]

def _rhs(rho, h, ops):
    comm = _add(_mm(h, rho), _sc(_mm(rho, h), -1))
    out = _sc(comm, -1j)
    for l in ops:
        ld = _dag(l); ldl = _mm(ld, l)
        out = _add(out, _add(_mm(_mm(l, rho), ld), _sc(_add(_mm(ldl, rho), _mm(rho, ldl)), -0.5)))
    return out

def lindblad(rho0, t, gamma_1, gamma_phi, omega=0.0, steps=4000):
    g1, gp, t = nonneg("gamma_1", gamma_1), nonneg("gamma_phi", gamma_phi), nonneg("t", t)
    h = [[omega / 2, 0j], [0j, -omega / 2]]
    ops = [[[0j, 0j], [math.sqrt(g1) + 0j, 0j]],                      # sqrt(g1) |g><e|  (amplitude damping)
           [[math.sqrt(gp / 2) + 0j, 0j], [0j, -math.sqrt(gp / 2) + 0j]]]  # sqrt(gp/2) sigma_z (pure dephasing)
    rho, dt = [row[:] for row in rho0], t / steps
    for _ in range(steps):
        k1 = _rhs(rho, h, ops); k2 = _rhs(_add(rho, _sc(k1, dt / 2)), h, ops)
        k3 = _rhs(_add(rho, _sc(k2, dt / 2)), h, ops); k4 = _rhs(_add(rho, _sc(k3, dt)), h, ops)
        rho = _add(rho, _sc(_add(_add(k1, _sc(k2, 2)), _add(_sc(k3, 2), k4)), dt / 6))
    return rho

def run_experiment(config):
    """Experiment A/B driver. config: name, e_gap {'value','unit':'J'}, p_excited, c0 (complex), gamma_1, gamma_phi,
    times (list of s). Returns time series of populations, energy, coherence, D_C with provenance."""
    require_keys("experiment config", config, ["name", "e_gap", "p_excited", "gamma_1", "gamma_phi", "times"])
    rho0 = state(config["p_excited"], config.get("c0", 0.5))
    series = []
    for t in config["times"]:
        r = analytic(rho0, t, config["gamma_1"], config["gamma_phi"])
        series.append({"t": t, "p_excited": r[0][0].real, "energy_j": energy(r, config["e_gap"]), "coherence_l1": coherence_l1(r),
                       "H_C": retention(r, rho0), "D_C": decoherence_signal(r, rho0), "entropy_nats": entropy_nats(r)})
    cfg = {k: (str(v) if isinstance(v, complex) else v) for k, v in config.items()}
    return {"series": series, "basis": BASIS,
            "provenance": provenance(cfg, "ESTABLISHED", ["Markovian master equation", "declared basis: " + BASIS, "H_C = C(t)/C(0), l1 coherence"])}
