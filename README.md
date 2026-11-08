# Universal Harmonic Field Equations (UHFE/UDFE)

This repository defines the proposed mathematical/software contract for the PAN V8 Universal Harmonic Field Equations (UHFE), Universal Decoherence Field Equations (UDFE), and their coupled formation–decoherence model.

## Start here

- **[Canonical V8 / UHFE / UDFE specification](docs/unified_harmonic_formula.md)** — canonical coordinate meanings, proposed five-head mappings, paired merge equations, Fermi occupancy/hole diagnostics, alternating phase-pulse scaffold, legacy operators, and conformance tests.
- **[Proposed UHFE–UDFE merge model](docs/uhfe_udfe_merge_model.md)** — concise reference for the paired fields and aggregation rules.
- **[V8 contract](docs/v8_contract.md)** — machine-facing domain and validation contract.
- **[Cross-Polytope ↔ E₈ Lattice Mapping Contract](docs/cross_polytope_e8_mapping.md)** — explicit definitions, lattice membership, root system, normalization, quantization, residuals, and mapping tests.

- **[JANUS-HYDRA-DYNAMIC-INVERSE-v1](docs/janus_hydra_dynamic_inverse_v1.md)** — versioned UDFE inverse-head rule (all five heads carry `d`), exact defects, rank/sensitivity facts, with a stdlib-only reference implementation and tests.
- **[E₈ / Gosset verified facts](docs/e8_gosset_verified_facts.md)** — computed facts and conventions behind the geometry contract.

## Core model

\[
V_8=(h,R,u,d,\tau,\chi,s,f)
\]

UHFE represents the constructive/formation channel; UDFE represents the decoherence/inverse channel. They are evaluated on the same eight-dimensional state/domain and remain separately observable. The proposed merge preserves both values and derives:

\[
J_i=H_i+D_i,\qquad \Delta_i=H_i-D_i.
\]

A Fermi-inspired diagnostic maps \(\Delta E_i=D_i-H_i\) to occupancy \(n_i\) and complementary hole \(1-n_i\). This is a computational analogy, not a claim of validated quantum or cosmological physics.

## Status and scope

The formulas are a versioned mathematical proposal. Software conformance tests can establish that an implementation follows this specification; they do not establish empirical physical validity. Legacy integral and boundary operators are retained but clearly marked pending dimensional analysis and validation.

The canonical repo name currently includes a trailing period: `univeral-harmonic-field-equations.`.
