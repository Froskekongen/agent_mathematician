## Mathematical reading

Model the lake by a state \(x(t)\) (nutrients, algae, oxygen, etc.) with dynamics

\[
\dot x=f(x,u),
\]

where the clear regime is an attractor \(x_C\), and the turbid regime is another attractor \(x_T\). Resilience should capture both:

1. recovery speed after a small perturbation near \(x_C\);
2. resistance to crossing into the basin of \(x_T\) after a large shock.

## Candidate formalisms

### 1. Two-component resilience profile

Define local recovery resilience by the dominant eigenvalue of the linearization:

\[
r_{\mathrm{local}}
=
-\max_i \operatorname{Re}\lambda_i\bigl(Df(x_C)\bigr).
\]

Larger \(r_{\mathrm{local}}\) means faster asymptotic recovery.

Define regime-persistence resilience as the size or probability of remaining in the clear basin:

\[
r_{\mathrm{basin}}
=
\frac{\mu\!\left(B_C\cap \mathcal S\right)}{\mu(\mathcal S)},
\]

where \(B_C\) is the basin of attraction of \(x_C\), and \(\mathcal S\) is the set of plausible post-shock states.

Resilience is then the pair

\[
\mathcal R=(r_{\mathrm{local}},r_{\mathrm{basin}}).
\]

This preserves the distinction between “returns quickly” and “does not switch regimes.” Its limitation is that it does not produce one scalar ranking.

### 2. Scalar weighted resilience

Combine the two dimensions:

\[
R_\alpha
=
\alpha\,\phi(r_{\mathrm{local}})
+
(1-\alpha)\,\psi(r_{\mathrm{basin}}),
\qquad 0\leq \alpha\leq 1,
\]

where \(\phi,\psi\) normalize the two terms.

This gives a single score suitable for comparing management strategies. Its limitation is that the ranking depends on the chosen weight \(\alpha\), and high recovery speed can compensate for poor regime persistence.

### 3. Bottleneck or lexicographic resilience

Treat permanent regime shifts as unacceptable, and optimize recovery only among systems that meet a persistence requirement:

\[
\max r_{\mathrm{local}}
\quad\text{subject to}\quad
r_{\mathrm{basin}}\geq \rho.
\]

Alternatively, define

\[
R_{\min}
=
\min\{\phi(r_{\mathrm{local}}),\psi(r_{\mathrm{basin}})\}.
\]

This makes the weaker dimension decisive and reflects precaution around irreversible turbidity shifts. Its limitation is that it may rank a slightly slower but much safer system above a fast-recovering system without expressing how much speed is worth sacrificing.

The unresolved fork is whether fast recovery and avoidance of regime shift should be treated as separate dimensions, traded off, or governed by a bottleneck constraint.

**When they disagree, should resilience be reported as a two-dimensional profile, collapsed using an explicit value-based tradeoff, or determined by the weaker/required dimension?**