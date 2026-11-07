# Explicit Cross-Polytope ↔ E₈ Lattice Mapping Contract

**Status:** Proposed geometric interface for PAN V8; definitions are standard mathematics, while the chosen mapping policy is a project convention.  
**Version:** 1.0-draft

## 1. The 8D cross-polytope

Let \(e_1,\ldots,e_8\) be the standard basis of \(\mathbb R^8\). The unit 8D cross-polytope (also called the 8-orthoplex or 8D hyperoctahedron) is

\[
C_8=\operatorname{conv}\{\pm e_i:i=1,\ldots,8\}
=\left\{q\in\mathbb R^8:\|q\|_1=\sum_{i=1}^8|q_i|\le1\right\}.
\]

Its defining features:
- Dimension: 8.
- Vertices: exactly 16, namely \(\pm e_i\).
- Boundary: \(\partial C_8=\{q:\|q\|_1=1\}\).
- Interior: \(\|q\|_1<1\).
- Origin: \(q=0\), the center.
- It is a continuous convex body, so it contains infinitely many points.
- Its polar dual under the standard Euclidean pairing is the 8D hypercube \([-1,1]^8\).

For a point \(q\in C_8\), the constraint is the L1 norm \(\|q\|_1\le1\), not the Euclidean constraint \(\|q\|_2\le1\). Every point satisfying the L1 constraint also satisfies the Euclidean unit-ball constraint, but the reverse is not generally true.

## 2. The E₈ lattice

Define the E₈ lattice in standard orthonormal coordinates by

\[
\Lambda_{E_8}=
\left\{x\in\mathbb Z^8:\sum_i x_i\in2\mathbb Z\right\}
\cup
\left\{x\in(\mathbb Z+\tfrac12)^8:\sum_i x_i\in2\mathbb Z\right\}.
\]

Thus an E₈ lattice point is either:
1. an integer-coordinate vector whose coordinate sum is even; or
2. a vector with all eight coordinates half-integers whose coordinate sum is even.

This is a discrete, infinite additive lattice in \(\mathbb R^8\), not a bounded polytope. In the conventional normalization, the shortest nonzero lattice vectors have squared Euclidean length 2. These 240 shortest vectors are the E₈ roots:

\[
\Phi_{E_8}=
\{\text{vectors with two entries }\pm1\text{ and six entries }0\}
\cup
\left\{\tfrac12(\pm1,\ldots,\pm1):\text{an even number of minus signs}\right\}.
\]

The first family has \(\binom82\,4=112\) roots; the second has 128; total \(112+128=240\). Every root has \(\|x\|_2=\sqrt2\). The lattice contains infinitely many points beyond these 240 roots.

## 3. Do not identify the two objects

\(C_8\) is a continuous, bounded polytope with 16 vertices. \(\Lambda_{E_8}\) is a discrete, unbounded lattice with 240 shortest vectors in its root shell. They are not the same geometry, have different defining norms/structures, and have no natural one-to-one correspondence between all their points.

The PAN architecture may use both:
- \(C_8\) as the continuous bounded state/domain for a normalized geometric coordinate \(q\).
- \(\Lambda_{E_8}\) as a discrete high-symmetry lattice used for reference points, candidate directions, or quantized embeddings.

Any use of E₈ symmetry must declare whether it means the lattice, its root system, its Weyl group, a projection, or a chosen subset. These are related but distinct mathematical objects.

## 4. Explicit map A — E₈ point to cross-polytope direction plus radius

For any nonzero lattice point \(x\in\Lambda_{E_8}\), define

\[
r_1=\|x\|_1=\sum_i|x_i|,\qquad q=\frac{x}{r_1}.
\]

Then \(q\in\partial C_8\), because \(\|q\|_1=1\), and \(x=r_1q\). The pair \((q,r_1)\) preserves the original point exactly. If only \(q\) is retained, radial/magnitude information is lost and multiple lattice points on the same ray map to the same direction. Define the zero point separately as \(x=0\mapsto(q=0,r_1=0)\).

For E₈ roots specifically:
- integer-type roots have \(\|x\|_1=2\);
- half-integer roots have \(\|x\|_1=4\).

So this map places normalized root directions on the boundary of \(C_8\), while the retained radius distinguishes the two root families.

## 5. Explicit map B — continuous cross-polytope point to nearest E₈ lattice point

For a continuous state \(q\in C_8\), choose a declared scale \(\rho>0\) and define the nearest-lattice quantizer

\[
Q_{E_8,\rho}(q)=
\underset{x\in\Lambda_{E_8}}{\operatorname{argmin}}
\;\|\rho q-x\|_2^2.
\]

Because the lattice is discrete, a nearest point exists. At Voronoi boundaries there may be ties; implementations must use a deterministic tie-break rule (for example, lexicographic order of the eight coordinates) or return all tied minimizers.

This map is many-to-one and discontinuous at Voronoi boundaries. It is a quantization, not a bijection and not a lossless embedding of the continuous polytope. Keep the residual

\[
\epsilon=\rho q-Q_{E_8,\rho}(q)
\]

alongside the lattice point if approximation error matters. Report \(\|\epsilon\|_2\) as the quantization error. The scale \(\rho\) is a configuration parameter, not a universal constant.

If a rotation/reflection is desired before quantization, specify an orthogonal matrix \(A\) and use \(Q_{E_8,\rho,A}(q)=\arg\min_{x\in\Lambda_{E_8}}\|\rho A q-x\|_2^2\). Record \(A\), \(\rho\), and the coordinate convention in provenance. A general rotation does not necessarily preserve the E₈ lattice; only transformations in its actual automorphism group do so.

## 6. Optional root-direction map for candidate generation

To select the closest E₈ root direction to a nonzero state, define the finite root set \(\Phi_{E_8}\) above and

\[
p(q)=\underset{\alpha\in\Phi_{E_8}}{\operatorname{argmax}}
\;\frac{q\cdot\alpha}{\|q\|_2\,\|\alpha\|_2},
\qquad q\ne0.
\]

This chooses a root direction with maximum cosine similarity. Specify a deterministic tie-break or retain all ties. It is a discrete direction-selection operation, not the same as nearest-lattice quantization. At \(q=0\), direction is undefined; return no selected root or use an explicitly configured fallback.

## 7. Suggested PAN interface record

Store at least:

\[
\{q,\rho,A,x_{E_8},\epsilon,\|\epsilon\|_2,\text{map-id},\text{tie-policy},\text{timestamp}\}.
\]

- \(q\): original continuous state, with \(\|q\|_1\le1\).
- \(\rho\), \(A\): scale and optional orthogonal transform.
- \(x_{E_8}\): chosen lattice point or root.
- \(\epsilon\): residual, when using quantization.
- map-id: versioned mapping definition.
- tie-policy: deterministic tie-breaking or all-ties behavior.
- timestamp: event timestamp for reproducibility.

Do not overwrite the original V8 vector with its E₈ quantization. Preserve raw V8, normalized geometric coordinates, E₈ result, and residual separately.

## 8. Minimum tests

1. \(q\in C_8\) iff \(\sum_i|q_i|\le1\), within a declared numeric tolerance.
2. All 16 vertices \(\pm e_i\) satisfy the boundary condition.
3. E₈ integer-family membership requires an even coordinate sum.
4. E₈ half-integer-family membership requires all coordinates to be half-integers and their sum to be even.
5. Enumerate exactly 240 shortest roots with squared norm 2.
6. For each nonzero E₈ point, map A gives \(\|q\|_1=1\) and reconstructs \(x=r_1q\).
7. Quantizer output belongs to \(\Lambda_{E_8}\), tie handling is deterministic, and residual matches \(\rho q-x_{E_8}\).
8. Quantization is explicitly documented as many-to-one; no test assumes a bijection.
9. Any claimed symmetry-preserving transform is checked against the actual E₈ lattice/root system.

## 9. Mathematical versus physical status

These definitions are standard mathematical structures. Choosing either mapping for PAN is a design decision. Neither a successful mapping nor the use of E₈ symmetry demonstrates that the physical universe is E₈-shaped or that the resulting PAN model is a validated physical theory.
