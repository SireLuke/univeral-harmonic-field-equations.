# UDFE Phase 1 reference models: implementation notes

Implements Phase 1 (reference models) and the minimum of Phase 2 needed by acceptance tests UDFE-001..010 of **PAN-UDFE-SPEC-001 v0.1** (research draft; the spec text itself is not included here). Code: `src/pan_harmonics/udfe/`; tests: `tests/test_udfe_phase1.py` (standard library only; run with `PYTHONPATH=src python -m unittest discover -s tests -v`).

## What is verified, and how
- Qubit with amplitude damping and pure dephasing: closed form vs an independent RK4 integration of the Lindblad equation (agree to ~1e-15 at the tested point). Coherence is the l1 norm in the **declared energy eigenbasis**; retention H_C = C(t)/C(0) requires C(0) > 0; D_C = 1 - H_C. G2 = G1/2 + Gphi is checked only for the model `markovian_qubit` and rejected otherwise.
- Graph metrics: algebraic connectivity from a hand-written Jacobi eigen-solver, checked against closed forms (ring 2-2cos(2pi/n), path 2-2cos(pi/n), complete n) and against monotonicity under edge removal.
- Determinism and provenance: each result carries its configuration, a SHA-256 of it, an evidence class and its assumptions.

## Choices the spec left open (all declared, all changeable)
- **Q (functional retention)** = fraction of node pairs still mutually reachable. **F** = (components - 1)/(n - 1). **Lambda** = lambda_2(G)/lambda_2(G0), which requires a connected baseline. Equal weights 0.25 by default.
- **recovery_threshold** = smallest number of restored edges, in a stated order, with D_org <= a stated tolerance (None if never).
- **measurement_confidence** is None ("not assessed") unless supplied; missing observations are never replaced by 0. A correlation that is undefined (constant series) is None, not 0.
- **entropy_production** is None unless a declared model supplies it; the qubit's von Neumann entropy is reported separately as a *system* property and is not production.
- The coupling layer classifies the four outcomes with declared thresholds (|r| >= 0.7, measurable range >= 0.05) and always returns `causal_claim: False`.

## Cautions raised by this implementation
1. **D_org double counts.** G_L, Lambda, F and Q are strongly dependent (Lambda = 0 exactly when disconnected), so equal weights overstate structural change; the composite is labelled HYPOTHESIS.
2. **Experiment A's energy claim holds only for dephasing in the energy eigenbasis.** The code fixes that basis and says so.
3. **V8 degeneracy risk (Phase 4):** the spec maps h to coherence retained (H_C) and d to the parent decoherence signal. If d := D_C then d = 1 - h exactly and two V8 coordinates collapse into one. Section 11 of the spec also says entropy and decoherence must not be interchangeable, yet d is described as "decoherence / entropy". Define d independently of h before the V8 mapping.
4. **Correlations between branches in a simulation reflect how the models are coupled**, not a discovered law; sweeps must be designed with that in mind.

Not included: the dissipation engine is a minimal accounting layer (energy balance with declared boundary, first-law heat with declared work and sign convention); there is no environment model and no thermodynamic entropy production, and no Planck-scale parameters (the spec defers them).
