"""Dissipation parameters engine (spec 2.3). Independent of graph structure; no claim that it follows from decoherence.
Energies in J, times in s, rates in 1/s. System boundary and sign convention must be declared."""
from .common import UdfeError, finite, positive, nonneg, quantity, require_keys, provenance

CONVENTIONS = ("positive_into_system", "positive_out_of_system")

def energy_balance(energy_in, energy_out, delta_system, boundary):
    """Residual = E_in - E_out - dE_system for the declared boundary. Zero means the accounting closes; it is not a law claim."""
    require_keys("energy balance", {"boundary": boundary}, ["boundary"])
    ei, eo, ds = quantity("energy_in", energy_in, "J"), quantity("energy_out", energy_out, "J"), quantity("delta_system", delta_system, "J")
    return {"boundary": boundary, "energy_balance": ei - eo - ds}

def heat_flow(delta_energy_system, convention, work_j=None):
    """Heat from the first law dE = Q + W (Q into system). work_j must be declared (0 allowed), never assumed."""
    if convention not in CONVENTIONS: raise UdfeError(f"sign convention must be one of {CONVENTIONS}")
    if work_j is None: raise UdfeError("work must be declared explicitly (use 0 J if none)")
    q_in = quantity("delta_energy_system", delta_energy_system, "J") - quantity("work", work_j, "J")
    return q_in if convention == "positive_into_system" else -q_in

def rates_consistency(gamma_1, gamma_phi, gamma_2, model, tol=1e-9):
    """Check G2 = G1/2 + Gphi. Valid ONLY for the declared Markovian qubit model; anything else is rejected, not assumed."""
    if model != "markovian_qubit": raise UdfeError("the relation G2 = G1/2 + Gphi is only asserted for model 'markovian_qubit'")
    g1, gp, g2 = nonneg("gamma_1", gamma_1), nonneg("gamma_phi", gamma_phi), nonneg("gamma_2", gamma_2)
    r = g2 - (g1 / 2 + gp)
    return {"model": model, "residual": r, "consistent": abs(r) <= tol}

def evaluate(e_in, e_out, e_sys_start, e_sys_end, dt, boundary, convention, work_j, rates=None, entropy_production=None, environment_coupling=None, measurement_confidence=None):
    dt = positive("dt", quantity("dt", dt, "s")) if isinstance(dt, dict) else positive("dt", dt)
    d_sys = quantity("e_sys_end", e_sys_end, "J") - quantity("e_sys_start", e_sys_start, "J")
    bal = energy_balance(e_in, e_out, {"value": d_sys, "unit": "J"}, boundary)
    out = {"energy_balance": bal["energy_balance"], "boundary": boundary, "power_transfer_w": d_sys / dt,
           "heat_flow": heat_flow({"value": d_sys, "unit": "J"}, convention, work_j), "sign_convention": convention,
           "entropy_production": entropy_production,      # None unless a declared model supplies it; never inferred from system entropy
           "environment_exchange": environment_coupling, "measurement_confidence": measurement_confidence}
    if rates:
        out.update({"energy_relaxation_rate": rates["gamma_1"], "pure_dephasing_rate": rates["gamma_phi"], "total_coherence_decay_rate": rates["gamma_2"],
                    "rates_check": rates_consistency(rates["gamma_1"], rates["gamma_phi"], rates["gamma_2"], rates.get("model", ""))})
    out["provenance"] = provenance({"boundary": boundary, "convention": convention, "dt": dt, "d_sys": d_sys}, "SIMULATED", ["first law dE=Q+W with declared work", "declared boundary and sign convention"])
    return out
