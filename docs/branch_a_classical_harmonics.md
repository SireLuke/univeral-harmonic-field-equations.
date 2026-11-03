# Branch A — Classical Harmonic Baseline

**Status:** Proposed computational baseline  
**Branch:** `feat/branch-a-classical-harmonics`  
**Scope:** Ideal one-dimensional string with fixed endpoints. This branch establishes classical reference behavior before any PAN V8, UHFE/UDFE, Fermi, E₈, or string-theory-inspired coupling.

## 1. Physical model

For a uniform string of length \(L>0\), tension \(T_s>0\), and linear mass density \(\mu>0\), the transverse displacement \(y(x,t)\) in the small-amplitude approximation satisfies

\[
\mu\,\frac{\partial^2 y}{\partial t^2}
= T_s\,\frac{\partial^2 y}{\partial x^2},
\qquad 0<x<L,
\]

with fixed-end boundary conditions \(y(0,t)=y(L,t)=0\). The wave speed is

\[
c=\sqrt{T_s/\mu}.
\]

The spatial eigenfunctions and angular frequencies are

\[
\psi_n(x)=\sin\!\left(\frac{n\pi x}{L}\right),\qquad
k_n=\frac{n\pi}{L},\qquad
\omega_n=c k_n,\qquad
f_n=\frac{\omega_n}{2\pi}=\frac{n c}{2L},
\]

for positive integer mode index \(n\). Thus \(f_n=n f_1\) for this ideal nondispersive string.

A real modal solution is

\[
y(x,t)=\sum_{n=1}^{N}
\left[A_n\cos(\omega_n t)+B_n\sin(\omega_n t)\right]\psi_n(x).
\]

The normalized eigenfunctions are \(\widehat\psi_n(x)=\sqrt{2/L}\,\psi_n(x)\), with

\[
\int_0^L\widehat\psi_m(x)\widehat\psi_n(x)\,dx=\delta_{mn}.
\]

## 2. Complex modal amplitudes

For analysis and later phase diagnostics, represent each mode by

\[
a_n(t)=A_n(t)e^{i\theta_n(t)}.
\]

The relative phase is \(\Delta\theta_{mn}=\theta_m-\theta_n\). Phase coherence metrics are deliberately **not** fixed in Branch A; they belong to the next integration stage and must declare their weighting, missing-mode behavior, and normalization.

## 3. Exponential barbershop correspondence

The existing geometric scaling can be evaluated as a separate dimensionless coordinate:

\[
b_n(x)=n\,2^{-x},\qquad n\in\mathbb N^+,\;x\in\mathbb R.
\]

At integer \(x=k\), adjacent scale levels obey \(b_n(k+1)/b_n(k)=1/2\). This is a mathematical scaling correspondence, not a consequence of the string wave equation and not evidence of a physical connection between the string and the barbershop construction.

## 4. Explicit non-claims

- This is a classical continuum string model, not superstring theory or M-theory.
- Integer harmonic ratios hold for the ideal uniform, fixed-end, nondispersive string; real strings can deviate due to stiffness, damping, inhomogeneity, and boundary compliance.
- No V8 coordinate is redefined or added. In particular, Branch A does not add a ninth coordinate.
- No Fermi sea, negative-frequency sector, E₈ lattice, cross-polytope, or UHFE/UDFE complement is inferred from these equations.
- Passing numerical tests validates this implementation against this model only; it does not validate a broader physical theory.

## 5. Acceptance tests

1. Reject non-finite or non-positive physical parameters.
2. Return \(c=\sqrt{T_s/\mu}\) and \(f_n=n c/(2L)\).
3. Verify integer frequency ratios for positive integer modes.
4. Verify fixed-end eigenfunctions vanish at both endpoints.
5. Verify analytical orthogonality and normalized inner products for distinct modes.
6. Verify barbershop half-scaling independently of the physical frequency calculation.
7. Verify outputs remain finite for supported inputs and invalid mode indices are rejected.

## 6. Promotion gate

Branch A is ready for review only when the reference implementation and tests pass, numerical quadrature agrees with the analytical orthogonality result within a declared tolerance, and the model's assumptions remain visible in the documentation. Branch A must not silently absorb V8 or speculative physical mappings.
