## SELECTED: conditional-treatment-parity + within-group-calibration

Let:

- \(A\in\{0,1\}\): demographic group
- \(Y\in\{0,1\}\): repayment outcome
- \(S\in[0,1]\): predicted repayment score
- \(\pi_a=P(Y=1\mid A=a)\): group base rate

Formalize the requirements as:

1. **Same outcome, same treatment**  
   \[
   S\perp A\mid Y,
   \]
   equivalently,
   \[
   P(S\in B\mid Y=y,A=0)
   =
   P(S\in B\mid Y=y,A=1)
   \]
   for every score set \(B\) and outcome \(y\). This is score-level equalized odds.

2. **Score meaning is group-invariant**  
   \[
   P(Y=1\mid S=s,A=a)=s
   \]
   for every group \(a\) and score \(s\) that occurs. Thus \(S=0.7\) means a 70% repayment rate in either group.

### Impossibility with unequal base rates

If \(\pi_0\ne\pi_1\), these requirements cannot both hold for any nontrivial, imperfect score.

Writing \(f_y(s)=P(S=s\mid Y=y)\), equalized odds makes \(f_y\) common across groups. Bayes’ rule then gives

\[
P(Y=1\mid S=s,A=a)
=
\frac{\pi_a f_1(s)}
{\pi_a f_1(s)+(1-\pi_a)f_0(s)}.
\]

For an interior score \(0<s<1\), both \(f_1(s)\) and \(f_0(s)\) must be positive. The expression necessarily changes when \(\pi_a\) changes, so it cannot equal the same value \(s\) in both groups.

Therefore, with differing base rates, the joint formalism permits only degenerate cases such as:

- a perfect predictor, with \(S=Y\) and scores only \(0\) or \(1\); or
- other boundary-support constructions that contain no genuinely uncertain scores.

In particular, a meaningful shared score such as \(0.7\) is incompatible with both requirements when base rates differ.

### Weaker alternative

If “same treatment” means only the final binary loan decision \(D\), impose

\[
D\perp A\mid Y
\]

rather than \(S\perp A\mid Y\). This preserves equalized odds for the decision while allowing the score distributions to differ by group. It does not, however, make the score itself equally interpretable across groups.

### What this establishes

The formalism establishes a precise statistical incompatibility: unequal base rates obstruct simultaneous score-level equalized odds and groupwise calibration, except in degenerate or perfect-prediction cases.

It does not establish causal fairness, individual fairness, absence of discrimination in features or processes, legal compliance, or which requirement should take priority. Those require additional causal, normative, institutional, and empirical assumptions.