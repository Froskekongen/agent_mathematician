---
name: research-mathematics
description: Research, formulate, prove, verify, or repair a substantial mathematical theorem, conjecture, derivation, or theory. Use for open-ended mathematical research, rigorous proof construction, independent verification, or improving a theorem. Reserve this full workflow for nontrivial claims rather than routine calculations or exposition-only requests.
---

# Research Mathematics

Optimize for mathematical truth. Produce claims that can survive expert review, and expose an exact gap, counterexample, or unresolved obligation whenever proof is unavailable.

Read [rigor-standards.md](references/rigor-standards.md) completely before working. Read [evidence-based-methods.md](references/evidence-based-methods.md) when formal verification, computation, literature retrieval, candidate search, or example-driven discovery could materially help.

## 1. Formalize

Rewrite the problem as a precise claim.

- Type every object and map with domains and codomains.
- State quantifiers, dimensions, regularity, ambient structures, boundary or initial conditions, and deterministic or stochastic qualifiers.
- Specify topology, norm, measure, filtration, and the mode of equality or convergence when relevant.
- Surface requirements needed merely for expressions to exist.
- State the chosen interpretation of any ambiguity and note material alternatives.
- Create an atomic assumption ledger with stable identifiers such as `A1`, `A2`, and `A3`.
- Freeze a versioned target contract before substantial search: the literal claim, intended interpretation, definitions, fixed versus search variables, permitted assumptions or axioms, and representative non-vacuous instances. Record every later reformulation as a diff and re-audit it rather than silently changing the problem.

Complete this phase only when the claim is well-posed and every symbol and qualifier has a declared meaning.

## 2. Expose the mechanism

Identify the structure that could make the result true: invariance, conservation, monotonicity, convexity, compactness, coercivity, orthogonality, analyticity, algebraic closure, a universal property, or another concrete mechanism.

Build an example laboratory containing the smallest nontrivial case, representative cases, relevant boundary or degenerate cases, and at least one plausible near-miss. Compute explicit examples where possible. Record observed patterns as evidence rather than theorems.

Before committing substantial effort to a proof, run a bounded truth triage on the frozen target: try the cheapest substitutions, small cases, dimensional or scaling checks, and exact counterexample searches from the `destroy-theory` funnel. Retain every certified counterexample and failed boundary case in the example laboratory. Failure to refute within a stated scope is not evidence of truth.

Complete this phase with either a candidate mechanism tied to the examples or an explicit account of what remains unexplained.

## 3. Build a strategy portfolio

For a nontrivial claim, develop at least two materially different routes. Consider direct, contradiction, induction, approximation, compactness, duality, algebraic, probabilistic, variational, spectral, transform, geometric, combinatorial, representation-theoretic, or reduction approaches as the problem warrants.

For each route, record:

- the proposed mechanism;
- the assumptions it appears to need;
- the hardest subgoal;
- its likely failure mode;
- why it is selected, deferred, or rejected.

Include a clearly labelled speculative route when a nonstandard idea could reveal new structure. Complete this phase only after selecting a route for mathematical reasons rather than because it appeared first.

## 4. Construct a checkable proof

Separate creative proposal from verification.

1. Draft the strategic argument.
2. Convert it into a dependency-ordered graph from definitions through lemmas to the main claim.
3. Attach assumptions and imported results to the exact nodes that use them.
4. Prove each open subgoal and record its status.
5. Check the proof one inference at a time without silently adding a new idea during the checking pass.

For every lemma, verify well-definedness, available hypotheses, sufficient conclusion strength, absence of circularity, justified limit or operator interchanges, the correct topology, exceptional sets, parameter-independent constants, and finite- versus infinite-dimensional distinctions.

Use the smallest viable generate--verify--revise loop first. For a long search, maintain durable state: the frozen target, proof DAG, verified nodes, current best proof, failed-route ledger, source and assumption ledgers, counterexamples, checker errors, and reusable lessons. Set attempt, tool-call, compute, time, or cost budgets and explicit stopping or human-escalation conditions. Escalate to parallel or evolutionary search only after a simpler loop shows a concrete bottleneck, and report the attempt denominator rather than only selected successes.

Use exact source statements for external theorems and verify every hypothesis. Prefer a proof assistant, symbolic checker, exact arithmetic, or executable invariant for load-bearing steps when a faithful formalization is practical. Before the main target, test new definitions with sanity lemmas, positive and boundary examples, and expected laws. Lock the encoded statement, scan the complete dependency closure for `sorry`, `admit`, unsafe axioms, or equivalent escape hatches, and pin tool and library versions. Reject obligation laundering: renaming the central difficulty as a helper lemma does not close it. A checker certifies the encoding, not its fidelity to the intended theorem.

Complete this phase only when every dependency node is proved or explicitly open.

## 5. Attack and repair

Apply the installed `destroy-theory` skill to the theorem, its critical lemmas, and the proof. If skill-to-skill invocation is unavailable, read and execute [the sibling skill](../destroy-theory/SKILL.md).

Repair each verified defect, weaken the conclusion, strengthen the assumptions, or downgrade the epistemic status. When the original claim is false, search for the nearest natural true statement and explain why the counterexample no longer applies.

Complete this phase only when each fatal finding has been repaired or remains visible in the result status.

## 6. Audit hypotheses

Apply the installed `audit-assumptions` skill. If skill-to-skill invocation is unavailable, read and execute [the sibling skill](../audit-assumptions/SKILL.md).

Revise the theorem and proof for missing, redundant, implied, proof-specific, or weakenable assumptions. Preserve the distinction between an assumption needed by this proof and one necessary for the theorem itself.

Complete this phase when every explicit and discovered hidden assumption has an exact use or is marked unused, and every claimed relaxation has explicit proof obligations.

## 7. Verify independently

Discard the proof path as a verification aid and perform a genuinely fresh check. Give the verifier the frozen target and necessary sources, not the proposer's persuasive narrative. Use at least one of:

- a second proof;
- a fresh derivation of the crucial lemma;
- an alternative characterization;
- a trusted checker, different model, or human specialist given only the claim and source material;
- a complete dependency trace reconstructed from scratch.

Compare the results and resolve discrepancies. Separate proof-correctness review from statement-fidelity review. A fresh-context same-model subagent is a useful correlated check but not independent evidence; after major revisions, reset the critic and, for an independence claim, also require a different proof, trusted checker, different model, or human specialist. Rereading the original derivation alone does not satisfy this phase.

Complete this phase when the central argument has an independent check or the absence of one is reported as a limitation.

## 8. Improve and contextualize

Investigate stronger conclusions, weaker hypotheses, converses, quantitative or stability results, uniqueness, characterizations, larger spaces, finite-dimensional approximations, computational consequences, and connections to other theories.

Search primary literature when priority, attribution, or novelty matters. Search the exact claim, equivalent formulations, key constructions, and proof motifs; inspect proof context rather than matching only theorem titles. Verify exact sources and state what the search covered. Treat failure to find a reference as an unresolved novelty question rather than evidence of novelty, and preserve enough provenance to distinguish a new result from rediscovery, prompted reconstruction, or human strengthening.

## 9. Present the result

Use the smallest structure that preserves checkability. For substantial work, report:

1. **Problem and interpretation**
2. **Assumption ledger**
3. **Main result and status**
4. **Mechanism and example laboratory**
5. **Strategy comparison**
6. **Proof and dependency structure**
7. **Adversarial findings and repairs**
8. **Independent verification**
9. **Assumption analysis**
10. **Extensions, sources, and novelty status**
11. **Verification and provenance card**, for research-level or AI-assisted results
12. **Exact unresolved point**, when applicable

Use one terminal status:

- `PROVED`: every material step is justified and the final audit, adversarial attack, assumption audit, and independent check pass;
- `INCOMPLETE`: a promising argument has a precisely located proof obligation;
- `CONJECTURAL`: evidence exists without a proof architecture that closes;
- `FALSE`: a certified counterexample or contradiction defeats the claim;
- `UNRESOLVED`: the available work does not determine the truth value.

Keep five evidence axes separate: logical correctness, statement fidelity, novelty or significance, provenance or autonomy, and human-readable reconstruction. Add precise tags where useful, such as `kernel-checked`, `expert-refereed`, `statement-faithful`, `novelty-audited`, `computationally tested`, or `literature-supported`. These tags describe support and do not replace the terminal status.

For the provenance card, report material model and tool versions, prompts or human hints, edits or strengthened claims, retries and selection, attempt denominator, budget, checker versions, expert review, and literature-search coverage. Include failures and abstentions when they affect the evidential weight. Do not collapse a kernel-checked proof, faithful formalization, independent mathematical review, and novelty review into one claim of “verification.”

When the user requests an accessible treatment, apply `explain-mathematics` after the mathematics is settled. If direct invocation is unavailable, read [the sibling skill](../explain-mathematics/SKILL.md).
