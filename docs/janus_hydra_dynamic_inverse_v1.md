# JANUS-HYDRA-DYNAMIC-INVERSE-v1 (UDFE inverse-head baseline)

**Status:** Versioned computational baseline. Not a validated physical theory.
**Machine-readable source of truth:** `src/pan_harmonics/janus_hydra_dynamic_inverse_v1.json`
**Reference implementation / tests:** `src/pan_harmonics/janus_v1.py`, `tests/test_janus_v1.py` (stdlib only)
**Relation to §4 of `unified_harmonic_formula.md`:** that section's UDFE heads remain as written (v1.1-draft of the formula document). This document adds a *separate, named* inverse rule, in line with the repo rule that mappings are versioned, never silently altered. Implementations must declare which UDFE rule they use.

## 1. What changes relative to the §4 proposal

In the §4 proposal, the decoherence density `d` enters only AntiBubble and the discrete-singular-dots head. Under v1 **all five inverse heads carry `d`**. Formation (UHFE) heads are unchanged.

| Pair (UHFE / UDFE) | UHFE head H | UDFE head D (v1) | Defect δ = H + D − 1 | Normalized δ̂ |
|---|---|---|---|---|
| Bubble / `antibubble_cavitation` | (h+R+u)/3 | (d+(1−u)+(1−h))/3 | (R+d−1)/3 | 3δ |
| CompoundEye / `discretesingulardots_inversecompoundeye` | (s+h+d)/3 | ((1−s)+(1−h)+d)/3 | (2d−1)/3 | 3δ |
| Honeycomb / `inversehoneycomb` | (τ+s)/2 | ((1−τ)+(1−s)+d)/3 | (τ+s+2d−2)/6 | 3δ |
| SpiderWeb / `inversespiderweb_radialvoid` | (f+h+R)/3 | ((1−f)+(1−h)+(1−R)+d)/4 | (f+h+R+3d−3)/12 | 4δ |
| ChiralDNA / `chiralvoid` | (χ+τ+R)/3 | ((1−χ)+(1−τ)+(1−R)+d)/4 | (χ+τ+R+3d−3)/12 | 4δ |

All coordinates are in [0,1]. Here χ is the **already-mapped** chirality score (χ+1)/2 required by `v8_contract.md`; the reference implementation does not map it for you and rejects nothing silently, so callers must supply the mapped value.

Raw defects lie in [−1/3, 1/3] (Bubble, CompoundEye, Honeycomb) or [−1/4, 1/4] (SpiderWeb, ChiralDNA), and the normalized defects attain exactly [−1, 1]. Store raw and normalized values separately.

## 2. Exact structural facts (all checked with exact rational arithmetic)

- Every defect is affine in the eight coordinates, so its extrema occur at the 256 corners; ranges above were checked over all corners.
- Bubble defect depends only on (R, d): `h` and `u` cancel between H and D.
- CompoundEye defect depends only on `d`: `s` and `h` cancel.
- Sensitivity to `d`: ∂δ/∂d = 1/3 (Bubble), 2/3 (CompoundEye), 1/3 (Honeycomb), 1/4 (SpiderWeb), 1/4 (ChiralDNA).
- The zero-defect set is a hyperplane in each pair (e.g. CompoundEye: d = 1/2), not a point.
- **Defect-gradient rank (5×8 Jacobian):** 5 under v1, **2** under the §4 proposal where `d` enters two heads only. Raw-defect singular values ≈ 0.915, 0.311, 0.210, 0.112, 0.094 (condition number ≈ 9.7, computed numerically at the centre point; exact because the maps are affine). For comparison the UHFE head matrix has rank 5 with condition number ≈ 2.91.
- Rank 5 means the five defects are linearly independent functions of the state. It does **not** mean they measure anything physical.

## 3. v1.1 proposal (separate, not canonical)

Pair-specific coupling λ_k ∈ (0,1] scaling only the density term in D (`d → λ_k·d`). All λ_k = 1 reproduces v1 exactly. Defects become: Bubble (R+λ_B d−1)/3; CompoundEye ((1+λ_E)d−1)/3; Honeycomb (τ+s+2λ_H d−2)/6; SpiderWeb (f+h+R+3λ_W d−3)/12; ChiralDNA (χ+τ+R+3λ_C d−3)/12. Inverse heads stay in [0,1] for all λ in (0,1]. Experimental calibration of λ must not overwrite canonical v1.

## 4. Verification evidence and its limits

`tests/test_janus_v1.py` (16 checks): exact equality of H+D−1 with the boxed defect on 500 random rational states for v1 and v1.1; v1.1 at λ=1 equals v1; range and corner checks over all 256 corners; sensitivities; support sets; deterministic replay; λ guard rails; the expression parser rejects code. An independent implementation in the `pan-fractal-kernel` repository agrees with these closed forms to ≈3×10⁻¹⁶ (floating point) on 2000 random states.

These establish **implementation conformance to the stated algebra**. They do not establish that the heads or defects correspond to any physical or empirical quantity.

## 5. Guardrails (from the spec)

1. Janus Hydra is distinct from UHFE and UDFE.
2. A nonzero defect is not automatically evidence of a physical phenomenon.
3. Store raw and normalized defects separately.
4. Calibration experiments must not overwrite canonical v1.

## 6. Open naming item (needs the owner's decision)

The name of UDFE is not consistent across the project's own documents. This repository expands it as "Universal **Dissolution** Field Equation". `FGHCL_foundation.md` says "Universal **Decoherence** Field Equation", while the FGHCL `README.md` calls UHFE/UDFE "paired formation and **dissolution** representations". The V8 coordinate `d` is described as a "decoherence / entropy indicator" throughout. No formula depends on the word. This document does not choose; it should be settled in one place, and if "Decoherence" is kept it should be stated that `d` is a model coordinate, not quantum decoherence.
