"""Coupling layer (spec section 3/7): reports association between independently measured series. It never asserts causality
and returns None, not 0, when a correlation is undefined."""
import math
from .common import UdfeError, finite

OUTCOMES = ("correlated_dissolution_and_dissipation", "dissolution_without_measurable_dissipation",
            "dissipation_without_measurable_dissolution", "weak_or_absent_coupling")

def _check(name, xs):
    if len(xs) < 3: raise UdfeError(f"{name}: need at least 3 observations")
    return [finite(name, x) for x in xs]

def pearson(x, y):
    n = len(x); mx, my = sum(x) / n, sum(y) / n
    sx, sy = sum((a - mx) ** 2 for a in x), sum((b - my) ** 2 for b in y)
    if sx == 0 or sy == 0: return None
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / math.sqrt(sx * sy)

def _ranks(v):
    order = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[order[j + 1]] == v[order[i]]: j += 1
        for k in range(i, j + 1): r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r

def spearman(x, y): return pearson(_ranks(x), _ranks(y))

def analyze(series, corr_threshold=0.7, change_threshold=0.05):
    """series: dict with equal-length lists for any of D_C, D_org, P_diss. Missing keys are reported as unavailable, not zero."""
    names = [k for k in ("D_C", "D_org", "P_diss") if k in series]
    if len(names) < 2: raise UdfeError("coupling needs at least two independently measured series")
    data = {k: _check(k, series[k]) for k in names}
    if len({len(v) for v in data.values()}) != 1: raise UdfeError("series must have equal length")
    pairs = {}
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            pairs[f"{a}~{b}"] = {"pearson": pearson(data[a], data[b]), "spearman": spearman(data[a], data[b])}
    rng = {k: max(v) - min(v) for k, v in data.items()}
    result = {"pairs": pairs, "ranges": rng, "unavailable": [k for k in ("D_C", "D_org", "P_diss") if k not in data],
              "causal_claim": False, "note": "association only; causal claims need controlled interventions and a specified model"}
    if "D_org" in data and "P_diss" in data:
        d_meas, p_meas = rng["D_org"] >= change_threshold, rng["P_diss"] >= change_threshold
        r = pairs["D_org~P_diss"]["pearson"]
        if d_meas and p_meas and r is not None and abs(r) >= corr_threshold: out = OUTCOMES[0]
        elif d_meas and not p_meas: out = OUTCOMES[1]
        elif p_meas and not d_meas: out = OUTCOMES[2]
        else: out = OUTCOMES[3]
        result["outcome"] = out
    return result
