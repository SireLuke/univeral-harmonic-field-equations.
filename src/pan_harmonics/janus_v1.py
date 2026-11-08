"""JANUS-HYDRA-DYNAMIC-INVERSE-v1 / v1.1, evaluated straight from the spec JSON (single source of truth).
Expressions are parsed with ast and only + - * / numbers and the 8 coordinate names (plus lambda_*) are allowed."""
import ast, json, operator, pathlib, re
from fractions import Fraction
SPEC=json.load(open(pathlib.Path(__file__).with_name("janus_hydra_dynamic_inverse_v1.json")))
NAMES=tuple(SPEC["coordinate_order"]); PAIRS=tuple(SPEC["pairs"])
_OPS={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.USub:operator.neg}
def _ev(node,env):
    if isinstance(node,ast.Expression): return _ev(node.body,env)
    if isinstance(node,ast.Constant) and isinstance(node.value,(int,float)): return node.value
    if isinstance(node,ast.Name): return env[node.id]
    if isinstance(node,ast.BinOp) and type(node.op) in _OPS: return _OPS[type(node.op)](_ev(node.left,env),_ev(node.right,env))
    if isinstance(node,ast.UnaryOp) and type(node.op) in _OPS: return _OPS[type(node.op)](_ev(node.operand,env))
    raise ValueError("disallowed expression element: "+ast.dump(node))
_cache={}
def ev(expr,env):
    if expr not in _cache: _cache[expr]=ast.parse(expr,mode="eval")
    return _ev(_cache[expr],env)
LAM={"bubble":"lambda_B","compoundEye":"lambda_E","honeycomb":"lambda_H","spiderweb":"lambda_W","chiralDNA":"lambda_C"}
def _dexpr(pair):                                   # v1.1 inverse head: scale only the density term d -> lambda*d
    D=SPEC["pairs"][pair]["D"]
    return re.sub(r"(?<![A-Za-z_])d(?![A-Za-z_])", f"({LAM[pair]}*d)", D)
def heads(state,lam=None):
    """state: dict name->value (float or Fraction). Returns {pair:{H,D,delta,delta_norm}}; lam: dict pair->lambda in (0,1] (default all 1)."""
    if set(state)!=set(NAMES): raise ValueError("state must have exactly the 8 V8 coordinates")
    lam=lam or {}; out={}
    for p in PAIRS:
        l=lam.get(p,1)
        if not 0<l<=1: raise ValueError(f"lambda for {p} must be in (0,1]")
        env=dict(state); env[LAM[p]]=l
        H=ev(SPEC["pairs"][p]["H"],env); D=ev(_dexpr(p),env); dl=H+D-1
        out[p]=dict(H=H,D=D,delta=dl,delta_norm=dl*(4 if p in("spiderweb","chiralDNA") else 3))
    return out
def spec_delta(p,state,lam=1):
    env=dict(state); env[LAM[p]]=lam
    return ev(SPEC["v1_1_proposal"]["defects"][p],env)   # v1.1 closed form; equals the v1 defect at lam=1
