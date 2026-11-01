# PAN V8 State Contract

**Version:** 1.0-draft

Canonical coordinate order: \((h,R,u,d,\tau,\chi,s,f)\).

| Index | Symbol | Meaning | Validation |
|---:|---|---|---|
| 0 | h | Harmonic coherence | finite, [0,1] |
| 1 | R | Recursive depth | finite, [0,1] after documented normalization |
| 2 | u | Constructive polarity | finite, [0,1] |
| 3 | d | Decoherence / entropy indicator | finite, [0,1] |
| 4 | τ | Temporal offset | finite; requires declared reference window and normalization |
| 5 | χ | Chirality / orientation | finite, [-1,1] |
| 6 | s | Information density | finite, [0,1] after documented normalization |
| 7 | f | Fractal forcing index | finite, [0,1] after documented normalization |

## Required rules

- Exactly eight coordinates; do not add T as a ninth dimension.
- \(T\) is a provisional legacy alias for \(\tau\); \(P_{\mathrm{time}}\), if used, is separate temporal persistence.
- Canonical recursive-depth symbol is uppercase \(R\); lowercase \(r\) requires an explicit alias.
- Convert chirality to a [0,1] score with \((\chi+1)/2\) only when the consumer needs a [0,1] orientation-preserving mapping. Do not substitute \(|\chi|\).
- Reject NaN, infinity, missing values, and undeclared units/normalization.
- Do not silently clamp invalid inputs.
- Preserve raw values, normalized values, transform version, timestamp, and validation outcome.
- Passing this contract is software validation, not physical validation.
