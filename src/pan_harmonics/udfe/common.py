"""Validation, units and provenance shared by the UDFE modules (spec section 8)."""
import hashlib, json, math

EVIDENCE = ("ESTABLISHED", "REPRODUCED", "SIMULATED", "EMPIRICAL", "HYPOTHESIS", "ANALOGY")
UNITS = {"J", "s", "1/s", "W", "1", "nats"}

class UdfeError(ValueError):
    """Invalid, non-finite, missing or unit-incompatible input."""

def finite(name, x):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
        raise UdfeError(f"{name}: must be a finite real number, got {x!r}")
    return float(x)

def positive(name, x):
    x = finite(name, x)
    if x <= 0: raise UdfeError(f"{name}: must be > 0, got {x}")
    return x

def nonneg(name, x):
    x = finite(name, x)
    if x < 0: raise UdfeError(f"{name}: must be >= 0, got {x}")
    return x

def quantity(name, q, unit):
    """q must be {'value': number, 'unit': unit}. Wrong or missing unit is rejected, never converted."""
    if not isinstance(q, dict) or set(q) != {"value", "unit"}:
        raise UdfeError(f"{name}: expected {{'value', 'unit'}}, got {q!r}")
    if q["unit"] not in UNITS: raise UdfeError(f"{name}: unknown unit {q['unit']!r}")
    if q["unit"] != unit: raise UdfeError(f"{name}: incompatible unit {q['unit']!r}, expected {unit!r}")
    return finite(name, q["value"])

def require_keys(name, d, keys):
    missing = [k for k in keys if k not in d or d[k] is None or d[k] == ""]
    if missing: raise UdfeError(f"{name}: missing required metadata {missing}")

def provenance(config, evidence, assumptions):
    if evidence not in EVIDENCE: raise UdfeError(f"unknown evidence class {evidence!r}")
    blob = json.dumps(config, sort_keys=True, separators=(",", ":"))
    return {"config": config, "config_sha256": hashlib.sha256(blob.encode()).hexdigest(),
            "evidence": evidence, "assumptions": list(assumptions)}
