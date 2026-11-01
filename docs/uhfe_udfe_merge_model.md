# Proposed UHFE–UDFE Merge Model

**Status:** Draft numerical contract; not established physical law.

## State
\[
V_8=(h,R,u,d,\tau,\chi,s,f)
\]
with \(h,R,u,d,s,f\in[0,1]\), \(\chi\in[-1,1]\), and \(\tau\) normalized against an explicit reference interval. Let \(\chi_{01}=(\chi+1)/2\) and \(\tau_{01}\) be the explicitly normalized temporal coordinate.

## Paired heads

UHFE:
\[
H=\left(
\frac{h+R+u}{3},
\frac{\tau_{01}+s}{2},
\frac{f+h+R}{3},
\frac{\chi_{01}+\tau_{01}+R}{3},
\frac{s+h+d}{3}
\right).
\]

UDFE:
\[
D=\left(
\frac{d+(1-u)+(1-h)}{3},
\frac{(1-\tau_{01})+(1-s)}{2},
\frac{(1-f)+(1-h)+(1-R)}{3},
\frac{(1-\chi_{01})+(1-\tau_{01})+(1-R)}{3},
\frac{(1-s)+(1-h)+d}{3}
\right).
\]

Pair order: Bubble/AntiBubble, Honeycomb/InverseHoneycomb, SpiderWeb/Inverse radial lines, ChiralDNA/ChiralVoid, CompoundEye/Discrete singular dots. These UDFE equations are current proposed mappings and must be versioned if changed.

For each pair:
\[
J_i=H_i+D_i\in[0,2],\qquad
\Delta_i=H_i-D_i\in[-1,1].
\]
Do not normalize the raw sum silently. If a bounded joint score is wanted, use \(J_i/2\) and label it.

## Fermi-inspired complement

\[
\Delta E_i=D_i-H_i=-\Delta_i,\quad
n_i=\frac{1}{1+\exp((\Delta E_i-\mu)/T_F)},\quad
\bar n_i=1-n_i.
\]
Require \(T_F>0\), compatible units for \(\Delta E_i,\mu,T_F\), and overflow-safe logistic evaluation. The occupancy pair is complementary by construction; raw \(H_i,D_i\) need not sum to one. With \(\mu=0\):
\[
n_i=\frac{1}{1+\exp(-\Delta_i/T_F)}.
\]
This is a Fermi-inspired diagnostic mapping, not a claim that head scores are quantum energies or that the model realizes a physical Fermi sea.

## Shared geometry and phase scaffold

Both channels use the same state/domain. The 8D cross-polytope is
\[
\mathcal H_8=\{q\in\mathbb R^8:\sum_i|q_i|\le1\},
\]
not the \(E_8\) lattice. For a pulse:
\[
\epsilon_i=\operatorname{wrap}(\theta_i-\theta_{\mathrm{ref}}-\delta_i),\quad
P_i=\sigma_iA_i\cos(\epsilon_i),
\]
where UHFE has \(\sigma_i=+1\), UDFE has \(\sigma_i=-1\), and \(A_i\ge0\). Timestamp monotonicity, reference phase, wrap interval, and offsets are explicit input contracts.

Golden ratio constants:
\[
\phi=(1+\sqrt5)/2,\quad -1/\phi=1-\phi,
\quad \alpha=360^\circ/\phi^2\approx137.507764^\circ.
\]
The golden angle is a declared geometric convention, not proof of a physical mechanism.

## Required validation
- Enforce domains and require temporal normalization.
- Verify every head range and paired-head order.
- Verify sum/difference ranges and occupancy complementarity.
- Exercise extreme logistic inputs and reject invalid temperature.
- Test pulse alternation and monotonic timestamps.
- Preserve raw, transformed, and derived values for audit.
- Keep numerical conformance separate from empirical physical validation.
