# Quick paired test: `formalize-concepts` refactor vs v3

Date: 2026-08-29

## Result

The refactor is substantially smaller and produced shorter answers, but it did
not clearly preserve quality in this one-repeat smoke test. It won the fairness
case, while v3 won the resilience and diversity cases. The practical verdict is
therefore **keep the refactor direction, but harden its checking instructions
before treating it as a clean replacement for v3**.

This is a diagnostic sample, not a benchmark. It uses one run per arm and prompt,
one model, no blind grading, and no repeats.

## Frozen arms

- Refactor: Git commit `f44538374a02fc5dd11d8af9e58a1055119719af`;
  skill SHA-256 `83df93d152471d6f24b79f1026709fb85ed0c382994e327a83a493590c93ebc0`.
- v3: Git commit `38740199ec1d0266cd9c1425d0d81f8bcffd2595`;
  skill SHA-256 `c096320560bc2eb4d6278b4b5263a5cfd93a37f3409db4483f0e88955dfcd5d0`.

Static instruction size:

| Arm | Lines | Words | Bytes |
|---|---:|---:|---:|
| Refactor | 67 | 387 | 2,891 |
| v3 | 111 | 967 | 6,635 |

The refactor removes 60.0% of the skill words and 56.4% of its bytes.

## Protocol

- Each scored run was a fresh Codex CLI session using `gpt-5.6-luna` at medium
  reasoning effort, read-only sandboxing, and no web access.
- The prompt and model settings were identical across arms.
- Each run was explicitly told to locate and read its repo-local `SKILL.md`.
  The execution log confirmed the exact arm file was read before answering.
- An earlier parallel smoke run was excluded after one session failed to find
  the skill. Sequential runs removed that harness artifact.
- Evaluation was manual and focused on semantic fidelity, mathematical
  correctness and well-posedness, candidate discrimination, wedge-question
  quality, requested checks, and status calibration.

The examples were adapted from published concepts rather than copied solutions:

- fairness: Hardt, Price, and Srebro, [Equality of Opportunity in Supervised
  Learning](https://proceedings.neurips.cc/paper_files/paper/2016/hash/6a9659feb1216f14f7384ba499518b38-Abstract.html),
  and Kleinberg, Mullainathan, and Raghavan, [Inherent Trade-Offs in the Fair
  Determination of Risk Scores](https://arxiv.org/abs/1609.05807);
- resilience: Holling, [Resilience and Stability of Ecological
  Systems](https://pure.iiasa.ac.at/id/eprint/26/);
- diversity: Hill, [Diversity and Evenness: A Unifying Notation and Its
  Consequences](https://doi.org/10.2307/1934352).

## Prompts

The common prefix was:

> `$formalize-concepts` is repo-local. Before answering, read its `SKILL.md` and
> follow it.

### Fairness: one-shot ambiguous objects

> Formalize fairness for a loan risk model. I want people in two demographic
> groups with the same repayment outcome to receive the same treatment, but I
> also want a score of 0.7 to mean a 70% repayment rate in either group. Base
> rates differ. Give me a one-shot proposal, not a dialogue. State what the
> formalism can and cannot establish.

### Resilience: live semantic fork

> I want a mathematical notion of resilience for a lake ecosystem. It should
> capture both returning quickly after a small nutrient perturbation and
> avoiding a permanent shift to a turbid regime after a large shock. Give me the
> candidate formalisms, then ask exactly one question that would choose between
> them. Do not finish the selection yet.

### Diversity: expert, fixed structure

> Let `p=(p_1,...,p_n)` be species proportions. I need diversity measured as an
> effective number of species: `D(uniform on n species)=n`, `D` is symmetric and
> continuous, independent communities multiply, and a parameter should tune
> sensitivity to rare species. Give a one-shot proposal with an anchor example
> and a boundary case. The structure is fixed; do not introduce unrelated model
> classes.

## Paired findings

| Case | Refactor | v3 | Verdict |
|---|---|---|---|
| Fairness | 329 words; distinguished score-level separation from the weaker decision-level reading and gave a Bayes argument on the exact score object | 520 words; used decision-level equalized odds, then incorrectly transferred the score-level calibration incompatibility to that downstream decision | **Refactor** |
| Resilience | 327 words; good local/basin split, but its displayed return-rate definition is ill-posed and its final question does not distinguish every candidate it introduced | 350 words; used a clean spectral recovery rate and a genuine three-way profile/tradeoff/bottleneck wedge | **v3** |
| Diversity | 147 words; chose the correct Hill family but calculated `D_2(1/2,1/4,1/4)=2` | 258 words; chose the same family and correctly obtained `D_2=8/3`, with a better boundary-continuity note | **v3** |

Across the three final answers, the refactor used 803 words versus v3's 1,128,
a 28.8% reduction.

### Fairness detail

The refactor formalized the strong reading as score-level separation

\[
S\perp A\mid Y
\]

together with within-group calibration. Its Bayes calculation correctly keeps
the impossibility claim on the score. It also preserved decision-level
equalized odds as a weaker alternative.

V3 instead imposed `T independent of A given Y` on the treatment while keeping
calibration on a separate score `S`, then claimed the two are generally
incompatible. That does not follow: post-processing a score into an
equalized-odds decision need not alter the calibration of the retained score,
and a constant randomized decision is an immediate boundary example. V3's
report structure was clearer, but its main incompatibility statement was on
the wrong object.

The refactor answer was not flawless: its weaker-alternative paragraph says
decision-level equalized odds does not make the score equally interpretable,
although groupwise calibration can still be retained. The win is relative.

### Resilience detail

The refactor defined

\[
\tau_\varepsilon(\delta)=\inf\{t\ge0:\lVert x(t)-C\rVert\le\varepsilon\},
\qquad
R_{\mathrm{local}}=\liminf_{\delta\to0}\frac1{\tau_\varepsilon(\delta)}.
\]

For fixed positive `epsilon`, sufficiently small `delta` already starts inside
the target ball, so the hitting time is zero and the reciprocal is undefined
or infinite. V3 avoided this by using the spectral recovery rate directly.
V3's final question also maps cleanly to all three candidates; the refactor's
question asks only profile versus scalar even though it also introduced a
thresholded feasibility interpretation.

### Diversity detail

Both arms correctly selected Hill numbers and avoided unrelated candidates.
The refactor was markedly more concise, but its anchor calculation is wrong:

\[
D_2(1/2,1/4,1/4)
=\frac{1}{1/4+1/16+1/16}
=\frac83,
\]

not `2`. V3 computed this correctly and more clearly explained why `q=0` is a
support limit rather than a continuous boundary value on the whole simplex.

## Recommendation

Do not revert the refactor wholesale. Its core loop survived, its fairness
response was the best of the pair, and the context/output reduction is real.
Before broader adoption, add compact instructions equivalent to:

1. Every displayed candidate must already be well-typed and well-defined on
   its stated domain, even before the selection step.
2. Recompute every displayed numerical sanity check, and keep each claimed
   consequence or impossibility theorem on the exact objects constrained by
   the formalism.
3. For one-shot answers, visibly separate the mathematical reading, selected
   or provisional formalism, checks, serious alternatives, and exact open
   fork; this was the most useful behavior lost with v3's report contract.

Then rerun at least three alternating repeats. The observed 2-1 v3 edge is too
small and too sample-sensitive to justify a version decision by itself.

## Raw final answers

- [Refactor fairness](runs/refactor-fairness.md)
- [v3 fairness](runs/v3-fairness.md)
- [Refactor resilience](runs/refactor-resilience.md)
- [v3 resilience](runs/v3-resilience.md)
- [Refactor diversity](runs/refactor-diversity.md)
- [v3 diversity](runs/v3-diversity.md)
