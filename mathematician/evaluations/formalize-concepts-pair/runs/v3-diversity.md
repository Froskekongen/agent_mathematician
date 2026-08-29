## Mathematical reading

Model diversity as an effective species count \(D_q(p)\), where \(q>0\) controls sensitivity to relative rarity. Require symmetry, continuity, normalization on uniform communities, and multiplicativity for independent combinations.

## Selected formalism

Use the Hill-number family:

\[
D_q(p)=
\begin{cases}
\left(\displaystyle\sum_{i=1}^n p_i^q\right)^{1/(1-q)}, & q\neq 1,\\[1.2ex]
\exp\!\left(-\displaystyle\sum_{i=1}^n p_i\log p_i\right), & q=1.
\end{cases}
\]

Here \(p_i\ge 0\) and \(\sum_i p_i=1\).

- \(D_q\) is symmetric and continuous for every fixed \(q>0\).
- For the uniform distribution \(p_i=1/n\),

\[
D_q(p)=n.
\]

- \(q<1\) gives greater sensitivity to rare species; \(q>1\) emphasizes abundant species.
- At \(q=1\), \(D_1\) is the exponential Shannon entropy.
- If independent communities have proportions \(p_i=a_i b_j\), then

\[
D_q(p)
=\left(\sum_{i,j}(a_i b_j)^q\right)^{1/(1-q)}
=D_q(a)D_q(b).
\]

Thus independent communities multiply.

## Sanity checks

Anchor example: for \(p=(1/2,1/4,1/4)\),

\[
D_2(p)=\frac{1}{(1/2)^2+(1/4)^2+(1/4)^2}
=\frac{8}{3},
\]

while

\[
D_{1/2}(p)=\left(\sqrt{1/2}+2\sqrt{1/4}\right)^2
=\left(1+\frac{1}{\sqrt2}\right)^2,
\]

which is larger because \(q=1/2\) gives more weight to the two rarer species.

Boundary case: for a completely concentrated community \(p=(1,0,\ldots,0)\),

\[
D_q(p)=1\qquad(q>0),
\]

as expected for one effectively present species. The formal \(q\to0\) limit recovers species richness on a fixed positive support, but is not continuous at distributions where species probabilities reach zero.

## Alternatives set aside

- \(q=1\) alone: captures entropy-based effective diversity but lacks a tunable rarity-sensitivity parameter.
- \(q=2\) alone: gives inverse Simpson diversity but fixes sensitivity toward common species.
- \(q=0\) alone: gives richness but fails continuity at the boundary of the simplex.

## Open questions and handoff

No material choice remains for the requested proposal. The selected definition is the Hill effective-number family, with \(q>0\) as the rarity-sensitivity parameter.