"""Dissolution metrics engine, structural branch (spec 2.2, Experiment C). Independent of any quantum model.

Declared conventions: undirected weighted graph on nodes 0..n-1, edge weight w > 0 means present (weakening = lower w).
G_L   fraction of nodes in the largest connected component.
Lambda  algebraic connectivity lambda_2 of the combinatorial Laplacian, normalized as lambda_2(G)/lambda_2(G0); G0 must be connected.
F     fragmentation = (components - 1)/(n - 1).
Q     functional retention = fraction of node pairs still mutually reachable (declared proxy; other definitions are possible).
D_org = w1(1-G_L) + w2(1-Lambda) + w3 F + w4(1-Q): a PAN-specific composite, evidence class HYPOTHESIS.
NOTE: these four components are strongly dependent (Lambda = 0 iff disconnected), so the composite double counts structure."""
import math, random
from .common import UdfeError, finite, require_keys, provenance

class Graph:
    def __init__(self, n, edges, name="custom"):
        if not isinstance(n, int) or n < 2: raise UdfeError("graph needs n >= 2 integer nodes")
        self.n, self.name, self.w = n, name, {}
        for e in edges:
            if len(e) == 2: (a, b), wt = e, 1.0
            else: a, b, wt = e
            if not (isinstance(a, int) and isinstance(b, int) and 0 <= a < n and 0 <= b < n and a != b):
                raise UdfeError(f"invalid edge {e!r}")
            wt = finite("edge weight", wt)
            if wt < 0: raise UdfeError("edge weight must be >= 0")
            if wt > 0: self.w[(min(a, b), max(a, b))] = wt
    def copy(self): g = Graph(self.n, [], self.name); g.w = dict(self.w); return g
    def edges(self): return sorted(self.w)
    def remove(self, edges):
        g = self.copy()
        for a, b in edges:
            k = (min(a, b), max(a, b))
            if k not in g.w: raise UdfeError(f"edge {k} is not in the graph")
            del g.w[k]
        return g
    def weaken(self, edge, factor):
        k = (min(edge), max(edge)); f = finite("factor", factor)
        if k not in self.w or not 0 <= f <= 1: raise UdfeError("bad weaken request")
        g = self.copy()
        if f == 0: del g.w[k]
        else: g.w[k] *= f
        return g

def ring(n): return Graph(n, [(i, (i + 1) % n) for i in range(n)], f"ring{n}")
def path(n): return Graph(n, [(i, i + 1) for i in range(n - 1)], f"path{n}")
def complete(n): return Graph(n, [(i, j) for i in range(n) for j in range(i + 1, n)], f"complete{n}")
def grid(r, c):
    idx = lambda i, j: i * c + j
    e = [(idx(i, j), idx(i, j + 1)) for i in range(r) for j in range(c - 1)] + [(idx(i, j), idx(i + 1, j)) for i in range(r - 1) for j in range(c)]
    return Graph(r * c, e, f"grid{r}x{c}")
def gnp(n, p, seed):
    rng = random.Random(seed)   # deterministic: seed recorded in provenance by callers
    return Graph(n, [(i, j) for i in range(n) for j in range(i + 1, n) if rng.random() < p], f"gnp{n}_{p}_seed{seed}")

def components(g):
    parent = list(range(g.n))
    def find(x):
        while parent[x] != x: parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for a, b in g.w: parent[find(a)] = find(b)
    sizes = {}
    for v in range(g.n): r = find(v); sizes[r] = sizes.get(r, 0) + 1
    return sorted(sizes.values(), reverse=True)

def laplacian(g):
    L = [[0.0] * g.n for _ in range(g.n)]
    for (a, b), w in g.w.items():
        L[a][a] += w; L[b][b] += w; L[a][b] -= w; L[b][a] -= w
    return L

def jacobi_eigenvalues(A, tol=1e-12, max_sweeps=100):
    """Cyclic Jacobi for a real symmetric matrix; returns sorted eigenvalues. Independent of any library."""
    n = len(A); a = [row[:] for row in A]
    for _ in range(max_sweeps):
        off = sum(a[i][j] ** 2 for i in range(n) for j in range(i + 1, n))
        if off < tol ** 2: break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-300: continue
                th = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = (1 if th >= 0 else -1) / (abs(th) + math.sqrt(th * th + 1))
                c = 1 / math.sqrt(t * t + 1); s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
    return sorted(a[i][i] for i in range(n))

def algebraic_connectivity(g):
    lam = jacobi_eigenvalues(laplacian(g))[1]
    return 0.0 if abs(lam) < 1e-9 else lam    # numerical zero of a PSD matrix, declared and documented

def metrics(g, g0):
    if g.n != g0.n: raise UdfeError("graph and baseline must have the same node set")
    l0 = algebraic_connectivity(g0)
    if not l0 > 0: raise UdfeError("baseline graph must be connected (lambda_2 > 0) to normalize Lambda")
    comp, n = components(g), g.n
    pairs = n * (n - 1) / 2
    return {"giant_component_ratio": comp[0] / n,
            "algebraic_connectivity": algebraic_connectivity(g) / l0,
            "fragmentation_measure": (len(comp) - 1) / (n - 1),
            "functional_retention": sum(s * (s - 1) / 2 for s in comp) / pairs}

def dissolution_index(m, weights=(0.25, 0.25, 0.25, 0.25)):
    if len(weights) != 4 or any(finite("weight", w) < 0 for w in weights) or abs(sum(weights) - 1) > 1e-12:
        raise UdfeError("weights must be 4 nonnegative numbers summing to 1")
    parts = {"w1*(1-G_L)": weights[0] * (1 - m["giant_component_ratio"]), "w2*(1-Lambda)": weights[1] * (1 - m["algebraic_connectivity"]),
             "w3*F": weights[2] * m["fragmentation_measure"], "w4*(1-Q)": weights[3] * (1 - m["functional_retention"])}
    return sum(parts.values()), parts

def recovery_threshold(g_damaged, g0, restore_order, tolerance, weights=(0.25,) * 4):
    """Smallest number k of edges restored (in the stated order) with D_org <= tolerance; None if never reached."""
    g = g_damaged
    for k, e in enumerate([None] + list(restore_order)):
        if e is not None: g = Graph(g.n, [(a, b, w) for (a, b), w in g.w.items()] + [(e[0], e[1], g0.w[(min(e), max(e))])], g.name)
        if dissolution_index(metrics(g, g0), weights)[0] <= tolerance: return k
    return None

def evaluate(g0, perturbed, weights=(0.25,) * 4, measurement_confidence=None, restore_order=(), tolerance=None):
    m = metrics(perturbed, g0); d, parts = dissolution_index(m, weights)
    out = {"dissolution_index": d, "components": parts, "weights": list(weights), **m,
           "recovery_threshold": (recovery_threshold(perturbed, g0, restore_order, tolerance, weights) if tolerance is not None else None),
           "measurement_confidence": measurement_confidence}   # None = not assessed; never silently 0
    cfg = {"baseline": g0.name, "n": g0.n, "baseline_edges": g0.edges(), "perturbed_edges": perturbed.edges(), "weights": list(weights)}
    out["provenance"] = provenance(cfg, "HYPOTHESIS", ["composite D_org is PAN-specific and unvalidated", "Q = reachable-pair fraction", "Lambda normalized to baseline"])
    return out
