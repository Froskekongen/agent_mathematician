Let \(x(t)\) describe lake state, with a clear-water attractor \(C\), a turbid attractor \(T\), and dynamics

\[
\dot x=f(x,u),
\]

where \(u\) is nutrient loading or another disturbance.

### 1. Engineering resilience: local recovery rate

For a small perturbation \(x(0)=C+\delta\), define the return time

\[
\tau_\varepsilon(\delta)
=\inf\{t\ge 0:\|x(t)-C\|\le \varepsilon\}.
\]

Resilience could be measured by the local recovery rate

\[
R_{\mathrm{local}}
=\liminf_{\delta\to 0}\frac{1}{\tau_\varepsilon(\delta)},
\]

or, locally, by the dominant negative eigenvalue of \(Df(C)\).

- Captures: how quickly the lake returns after a small nutrient shock.
- Consequence: a strongly attracting clear state has high \(R_{\mathrm{local}}\).
- Limitation: it says little about large shocks that cross into the turbid basin.

### 2. Ecological resilience: basin stability

Let \(B_C\) be the basin of attraction of the clear regime. For a disturbance set \(D_A\) of magnitude \(A\), define

\[
R_{\mathrm{basin}}(A)
=\frac{\mu(B_C\cap D_A)}{\mu(D_A)},
\]

where \(\mu\) measures the possible post-shock states.

- Captures: the fraction of large shocks from which the lake ultimately avoids a permanent turbid shift.
- Consequence: a lake can have high basin resilience even if its return is slow.
- Limitation: it does not directly reward rapid recovery within the clear basin.

### 3. Composite resilience: recovery plus persistence

Represent resilience as a pair

\[
\mathcal R
=
\bigl(R_{\mathrm{local}},\,R_{\mathrm{basin}}(A)\bigr),
\]

possibly with a scalarization such as

\[
R_{\mathrm{comp}}
=
\alpha R_{\mathrm{local}}
+
(1-\alpha)R_{\mathrm{basin}}(A),
\qquad 0\le \alpha\le 1.
\]

Alternatively, use a thresholded feasibility definition:

\[
R_{\mathrm{comp}}\ge (r_0,b_0)
\]

when recovery is sufficiently fast, \(R_{\mathrm{local}}\ge r_0\), and large-shock persistence is sufficiently high, \(R_{\mathrm{basin}}(A)\ge b_0\).

- Captures: both rapid small-shock recovery and avoidance of regime shift.
- Consequence: makes explicit whether the two properties are jointly required or traded off.
- Limitation: a weighted scalar requires a substantive choice of \(\alpha\); the pair preserves the distinction but does not produce one ranking.

### Question

Should resilience remain a two-dimensional profile that keeps rapid recovery and regime-shift avoidance distinct, or should it produce a single ranking that trades them off?