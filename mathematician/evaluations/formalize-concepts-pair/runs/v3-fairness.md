## Mathematical reading

Model two demographic groups \(A\in\{0,1\}\), repayment outcome \(Y\in\{0,1\}\), risk score \(S\in[0,1]\), and treatment decision \(T\) (approval, price, limit, etc.).

The goals are:

1. People with the same repayment outcome should receive the same treatment, in distribution.
2. A score \(s\) should mean the same repayment probability in either group.
3. Base repayment rates may differ: \(\Pr(Y=1\mid A=0)\ne\Pr(Y=1\mid A=1)\).

## Selected formalism

Use equalized odds for treatment and groupwise calibration for the score.

**Equal treatment conditional on outcome:**

\[
T\perp A\mid Y,
\]

equivalently, for every outcome \(y\) and treatment value \(t\),

\[
\Pr(T=t\mid Y=y,A=0)
=
\Pr(T=t\mid Y=y,A=1).
\]

For a binary approval decision \(T\in\{0,1\}\), this requires equal true-positive and false-positive rates:

\[
\Pr(T=1\mid Y=y,A=0)
=
\Pr(T=1\mid Y=y,A=1),
\qquad y\in\{0,1\}.
\]

**Common score meaning:**

\[
\Pr(Y=1\mid S=s,A=a)=s
\]

for every score \(s\) and group \(a\). Thus \(S=0.7\) means a 70% repayment rate within either group.

These conditions are jointly feasible in important special cases, especially with a perfect score \(S=Y\), but generally not when prediction is imperfect and base rates differ. Under the usual nondegeneracy assumptions—both outcomes occur, both groups occur, and the score has predictive error—simultaneous exact calibration and equalized odds forces equal base rates. Therefore, with genuinely different base rates, one generally must relax at least one requirement.

The formalism establishes statistical parity of treatment conditional on the observed outcome and statistical calibration of the score. It does not establish that any particular individuals are treated identically, that the decision is causally fair, that the outcome is measured without bias, or that the policy is substantively just.

## Sanity checks

- **Anchor example:** If \(S=Y\) and \(T=S\), then scores \(0\) and \(1\) are perfectly calibrated, and treatment is identical for everyone with the same repayment outcome. Groups may still have different base rates.

- **Boundary case:** Suppose group 0 has repayment rate \(0.8\), group 1 has rate \(0.5\), and the score is imperfect. A common score value \(0.7\) must represent 70% repayment in both groups. Equalized odds simultaneously requires the treatment error rates to be identical conditional on repayment status. These constraints are generally incompatible with the different prevalences; group-specific thresholds or randomized decisions can restore equalized odds only by sacrificing common calibration or score comparability.

## Alternatives set aside

- **Demographic parity:** \(\Pr(T=1\mid A=0)=\Pr(T=1\mid A=1)\). Captures equal overall treatment rates, but not equal treatment among people with the same outcome.

- **Group-specific calibration only:** Preserves the meaning of \(S=0.7\), but permits different treatment error rates across groups.

- **Equalized odds only:** Captures equal conditional treatment rates, but a score of \(0.7\) need not mean the same repayment probability across groups.

## Open questions and handoff

The central unresolved normative choice is which requirement to relax when base rates differ:

- preserve score meaning and accept unequal conditional treatment errors;
- preserve equalized odds and permit group-dependent score interpretation or randomized treatment;
- use a weaker compromise, such as bounded calibration error and bounded error-rate disparity.

A final policy specification should also define whether “treatment” means approval alone or the full loan package, and should audit whether \(Y\) is a valid, comparable repayment outcome across groups.