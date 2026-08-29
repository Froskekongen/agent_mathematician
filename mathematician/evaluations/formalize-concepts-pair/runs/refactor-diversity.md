## SELECTED — effective-number diversity

For a fixed sensitivity parameter \(q>0\), define

\[
D_q(p)=
\begin{cases}
\left(\displaystyle\sum_{i=1}^n p_i^q\right)^{1/(1-q)}, & q\neq 1,\\[1.2ex]
\exp\!\left(-\displaystyle\sum_{i=1}^n p_i\log p_i\right), & q=1.
\end{cases}
\]

This is the effective number of species associated with diversity order \(q\) (`effective-number-diversity`).

It is symmetric, continuous on the probability simplex, and satisfies

\[
D_q\!\left(p\otimes r\right)=D_q(p)D_q(r),
\]

so independent communities multiply. For the uniform distribution \(p_i=1/n\),

\[
D_q(p)=n.
\]

The parameter controls rarity sensitivity: smaller \(q\) gives more weight to rare species; \(q=1\) gives the exponential Shannon diversity; \(q=2\) gives inverse Simpson diversity.

Anchor example: for \(p=(1/2,1/4,1/4)\),

\[
D_1(p)=\exp\!\left(-\tfrac12\log\tfrac12
-2\cdot\tfrac14\log\tfrac14\right)=2\sqrt2\approx2.83,
\]

whereas \(D_2(p)=1/\sum_i p_i^2=2\). Thus larger \(q\) discounts the two rarer species more strongly.

Boundary case: if \(p=(1,0,\ldots,0)\), then

\[
D_q(p)=1
\]

for every \(q>0\). As \(q\downarrow0\), \(D_q(p)\) approaches the number of species with positive proportion, but \(q=0\) itself is excluded to retain continuity when species proportions can reach zero.