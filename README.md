# Universal Harmonic Field Equations (UHFE/UDFE)

This repository defines the proposed mathematical/software contract for the PAN V8 Universal Harmonic Field Equations (UHFE), Universal Dissolution Field Equations (UDFE), and their coupled formation–dissolution model.

## Start here

- **[Canonical V8 / UHFE / UDFE specification](docs/unified_harmonic_formula.md)** — canonical coordinate meanings, proposed five-head mappings, paired merge equations, Fermi occupancy/hole diagnostics, alternating phase-pulse scaffold, legacy operators, and conformance tests.
- **[Proposed UHFE–UDFE merge model](docs/uhfe_udfe_merge_model.md)** — concise reference for the paired fields and aggregation rules.
- **[V8 contract](docs/v8_contract.md)** — machine-facing domain and validation contract.
- **[Cross-Polytope ↔ E₈ Lattice Mapping Contract](docs/cross_polytope_e8_mapping.md)** — explicit definitions, lattice membership, root system, normalization, quantization, residuals, and mapping tests.

## Core model

\[
V_8=(h,R,u,d,\tau,\chi,s,f)
\]

UHFE represents the constructive/formation channel; UDFE represents the dissolution/inverse channel. They are evaluated on the same eight-dimensional state/domain and remain separately observable. The proposed merge preserves both values and derives:

\[
J_i=H_i+D_i,\qquad \Delta_i=H_i-D_i.
\]

A Fermi-inspired diagnostic maps \(\Delta E_i=D_i-H_i\) to occupancy \(n_i\) and complementary hole \(1-n_i\). This is a computational analogy, not a claim of validated quantum or cosmological physics.

## Status and scope

The formulas are a versioned mathematical proposal. Software conformance tests can establish that an implementation follows this specification; they do not establish empirical physical validity. Legacy integral and boundary operators are retained but clearly marked pending dimensional analysis and validation.

The canonical repo name currently includes a trailing period: `univeral-harmonic-field-equations.`.
