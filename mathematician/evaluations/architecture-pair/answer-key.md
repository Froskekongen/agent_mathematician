# Adjudicator answer key

Never expose this file or its links to a solver or cold verifier. The problem
statements in `prompts.md` are lightly rephrased; the mathematical content is
unchanged.

## P1 — Product of cosines

**Expected conclusion:** the least integer is `18`.

Near zero,

\[
\cos(kx)=1-\frac{k^2x^2}{2}+O(x^4),
\]

so the coefficient of \(x^2\) in the product is
\(-\tfrac12\sum_{k=1}^n k^2\). Hence

\[
f_n''(0)=-\sum_{k=1}^n k^2=-\frac{n(n+1)(2n+1)}6.
\]

The magnitude is increasing with \(n\), and its values at 17 and 18 are 1785
and 2109. Both the threshold calculation and minimality are required.

**Authoritative source:** Mathematical Association of America,
[2023 Putnam Session A problems and official solutions](https://maa.org/wp-content/uploads/2024/10/2023_Putnam_Solutions_A.pdf),
A1 on page 1. The [MAA Putnam archive](https://maa.org/maa-putnam-archive/)
identifies the PDF as the official 2023 problems-and-solutions document.

## P2 — Prime plus twice a square

**Expected conclusion:** `5777`.

For a complete exact certification, the program or argument must establish:

1. 5777 is odd and composite; for example, \(5777=53\cdot109\).
2. For every integer \(s\) from 1 through 53, the positive odd integer
   \(5777-2s^2\) is nonprime. The upper bound is exact because
   \(s\le\lfloor\sqrt{(5777-2)/2}\rfloor=53\).
3. Every smaller odd composite, starting at 9, has at least one representation
   with prime \(p\) and positive integer \(s\).

An acceptable standard-library checker can enumerate odd integers in order,
classify primality by deterministic trial division through the integer square
root, and test the complete finite range of \(s\). The cold verifier should
inspect the bounds and primality predicate, run positive and negative controls,
and replay it. Floating square-root or probable-prime tests need additional
justification here and are unnecessary.

Do not award an unbounded claim about all later integers: the requested theorem
is only the identity of the first failing odd composite.

**Primary problem source:** [Project Euler, Problem 46](https://projecteuler.net/problem=46).
The expected exceptional values are independently cross-indexed in the
[OEIS entry A046921](https://oeis.org/A046921), which cites L. Hodges,
“A lesser-known Goldbach conjecture,” *Mathematics Magazine* 66 (1993), 45–47.
The trial's own exhaustive checker, rather than the cross-index, must certify
minimality.

## P3 — Reciprocal interpolation

**Expected conclusion:** the other real numbers are
\(x=\pm 1/n!\).

Let \(g(t)=t^2p(t)-1\). It is monic of degree \(2n+2\), has constant term
\(-1\) and no linear term, and has the \(2n\) roots
\(t=\pm1/k\), \(1\le k\le n\). Therefore

\[
g(t)=\prod_{k=1}^{n}\left(t^2-\frac1{k^2}\right)(t^2+at+b).
\]

The coefficient of \(t\) forces \(a=0\). At \(t=0\), using that \(n\) is
even,

\[
-1=g(0)=\frac{b}{(n!)^2},
\]

so \(b=-(n!)^2\). The two remaining roots of \(g\) are \(t=\pm n!\).
Since the equation in the problem is \(g(1/x)=0\), the additional values are
\(x=\pm1/n!\). Degree/root counting proves completeness.

Common fidelity failures are confusing \(x\) with \(1/x\), losing the
evenness hypothesis in the constant-term sign, or presenting the extra roots
of \(g\) as the requested values.

**Authoritative source:** Mathematical Association of America,
[2023 Putnam Session A problems and official solutions](https://maa.org/wp-content/uploads/2024/10/2023_Putnam_Solutions_A.pdf),
A2 on pages 2–3. See also the [official archive](https://maa.org/maa-putnam-archive/).

## P4 — Sum-of-powers claim

**Expected conclusion:** the universal claim is false.

One exact witness is

\[
27^5+84^5+110^5+133^5=144^5=61{,}917{,}364{,}224.
\]

It uses four positive fifth powers on the left, so \(m=4<5=k\). Exact integer
evaluation plus the direct mapping \((k,m,a_1,\ldots,a_m,b)\) to the quantified
claim is a complete refutation. A large search or proof that the witness is
smallest is not required. If a run nevertheless claims minimality, that claim
must be scored against the scope actually searched and can trigger a status
failure without invalidating the certified refutation itself.

For retained search code, inspect pair-sum bounds and ordering assumptions as
well as the final integer identity. For a witness-only checker, mutation of one
base or exponent is a useful negative control.

**Primary source:** L. J. Lander and T. R. Parkin,
[“Counterexample to Euler's conjecture on sums of like powers”](https://doi.org/10.1090/S0002-9904-1966-11654-3),
*Bulletin of the American Mathematical Society* 72 (1966), 1079. The
[publisher-hosted PDF](https://www.ams.org/journals/bull/1966-72-06/S0002-9904-1966-11654-3/S0002-9904-1966-11654-3.pdf)
states the exact identity and what it refutes.

