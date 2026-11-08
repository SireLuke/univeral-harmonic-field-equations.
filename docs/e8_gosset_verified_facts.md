# E₈ / Gosset 4₂₁ — facts checked by computation, and what remains convention

**Status:** Evidence note. The reproduction scripts were run in an external working session and are **not yet in this repository**; treat each line as "computed once, reproducible on request", not as a CI-enforced test.

## Standard mathematics, checked numerically

- Gosset 4₂₁ f-vector: 240 vertices (E₈ roots, norm² = 2), 6,720 edges, 60,480 triangles, 241,920 tetrahedra; each vertex has 56 nearest neighbours.
- |W(E₈)| = 696,729,600.
- Even sign-flip changes of coordinates (the D₈ Weyl subgroup) preserve the E₈ lattice; arbitrary sign flips (B₈) do not.
- E₈/2E₈ has 256 classes = 1 (zero) + 120 (root pairs ±α) + 135 (norm-4 classes, 16 vectors each); 135 = index of W(D₈) in W(E₈).
- Projected to a Coxeter plane, 2,160 triangular faces remain equilateral, in 72 orbits of 30. Face stabiliser order 11,520; tetrahedral-cell stabiliser order 2,880 (S₄ × W(A₄)).
- Sub-structure ladder from face types: vertex → SU(2) with E₇ complement (126 roots); edge → SU(3) with E₆ (72); triangle → SU(4) with SO(10) (40); cell → SU(5) with SU(5) (20 + 20 + 200 decomposition). Layer counts 1+56+126+56+1 match the SU(2)×E₇ branching 2+126+112.

## Icosian construction and the golden-ratio automorphism

- E₈ is built from the icosians via q ↦ (q, σq) (σ the Galois conjugate φ → −1/φ) with weight μ = (6+8φ)/5 (found by search), giving an even unimodular lattice.
- M = diag(φ,φ,φ,φ,−1/φ,−1/φ,−1/φ,−1/φ) in that basis is an integer lattice automorphism: det 1, trace 4, characteristic polynomial (x²−x−1)⁴. It is **not** norm-preserving (it is not an isometry).
- Expressed in standard E₈ coordinates, M is symmetric with entries ±½ and 1.5; the explicit pattern depends on the chosen isometry between the two coordinate systems, i.e. on a convention.

## Not established here

Nothing in this note shows that E₈ or the golden-ratio automorphism has physical meaning for V8; those remain modelling choices, as `cross_polytope_e8_mapping.md` already states.
