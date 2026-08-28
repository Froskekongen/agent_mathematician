---
name: research-mathematics
description: Research, formulate, prove, verify, or repair a substantial mathematical theorem, conjecture, derivation, or theory. Use for open-ended mathematical research, rigorous proof construction, independent verification, or improving a theorem. Reserve this full workflow for nontrivial claims rather than routine calculations or exposition-only requests.
disable-model-invocation: true
---

# Research Mathematics

Optimize for mathematical truth. Produce claims that survive expert review, or expose the exact counterexample, gap, or unresolved obligation.

Read [rigor-standards.md](references/rigor-standards.md) completely. Read [evidence-based-methods.md](references/evidence-based-methods.md) when formal verification, computation, literature retrieval, candidate search, or example-driven discovery could materially help. If no research target is ready, recommend `$explore-mathematical-structure` rather than inventing one.

## Own one research round

For an authorized file-backed round, read and follow the writable-home coordinator path—including its `ensure` preflight—in the [research-memory protocol](references/research-memory.md) before retrieving memory or creating round state. This agent alone owns the canonical Markdown, its writable companion, and one OS-temporary workpad; other theory databases are read-only. Chat-only work and read-only review create no artifacts.

Address durable canonical subjects with human-semantic research keys. Use the
protocol's canonical-section tool to add or change their generated Markdown
markers; never edit those markers by hand. Retrieve memory by exact canonical
key or alias before broad summary search, and expand only selected sections or
cards. A card about exactly the same subject uses the canonical key as its
slug. At closure, explicitly refresh changed canonical items and review every
affected card link at the current snapshots. These operations record curation
state, not logical or mathematical freshness.

## 1. Formalize

Rewrite the problem as a precise claim.

- Type every object and map, including domains and codomains.
- State quantifiers, dimensions, regularity, ambient structures, boundary or initial conditions, and deterministic or stochastic qualifiers.
- Specify topology, norm, measure, filtration, and mode of equality or convergence when relevant.
- Surface conditions needed merely for expressions to exist.
- Choose an interpretation of ambiguity and record material alternatives.
- Create an atomic assumption map with human-semantic durable identifiers;
  use `A1` or `Ai` only as transient local notation.
- Freeze a content-bound target contract: literal claim, interpretation, definitions, fixed and search variables, permitted assumptions or axioms, and representative non-vacuous instances. Diff and re-audit later changes.

Complete this phase when every symbol and qualifier has a declared meaning and the claim is well-posed.

## 2. Expose the mechanism

Identify what could make the claim true: invariance, conservation, monotonicity, convexity, compactness, coercivity, orthogonality, analyticity, algebraic closure, a universal property, or another concrete structure.

Build an example laboratory with the smallest nontrivial case, representative and boundary cases, and a plausible near-miss. Before substantial proof effort, run bounded truth triage: cheap substitutions, small models, scaling or dimensional checks, and adapted counterexample searches from the `destroy-theory` funnel. Computation is scoped evidence, and failure to refute is not evidence of truth.

Complete this phase with a mechanism tied to examples or an exact account of what remains unexplained.

## 3. Compare strategies

Develop at least two materially different routes for a nontrivial claim. For each, record its mechanism, required assumptions, hardest subgoal, likely failure mode, and reason for selection, deferral, or rejection. Include a labelled speculative route when a nonstandard idea could reveal structure.

Complete this phase after choosing a route for mathematical reasons rather than arrival order.

## 4. Construct a checkable proof

Separate proposal from verification:

1. Draft the strategic argument.
2. Convert it into a dependency-ordered graph from definitions through lemmas to the claim.
3. Attach assumptions and imported results to their exact uses.
4. Prove each subgoal and record its status.
5. Check one inference at a time without adding new ideas during the checking pass.

For every lemma, check well-definedness, available hypotheses, conclusion strength, circularity, limit or operator interchanges, topology, exceptional sets, uniform constants, and finite- versus infinite-dimensional distinctions.

Start with the smallest viable generate--verify--revise loop. Set attempt, tool, compute, time, or cost budgets and escalation conditions; report the denominator, not only selected successes. Use exact source statements for imported theorems. When faithful formalization is practical, prefer trusted checking or executable certificates for load-bearing steps; test new definitions with sanity lemmas, lock the encoded statement, scan the full dependency closure for escape hatches, and pin tool and library versions. A checker certifies the encoding, not fidelity to the intended theorem. A helper lemma that merely renames the central difficulty remains open.

Complete this phase when every dependency node is proved or explicitly open.

## Specialist-review fork

Freeze a content-hashed candidate containing the target, theorem and proof, dependency graph and statuses, assumption map, permitted axioms, exact sources with hypothesis mappings, and formal environment. A material change creates a new digest.

Launch phases 5 and 6 concurrently when possible. Give both specialists the identical candidate. Each begins with a cold pass, may later query memory read-only with imported findings marked, changes no theory artifact, and returns a content-bound report. The coordinator alone repairs the candidate and writes the home pair.

## 5. Attack the candidate

Apply `$destroy-theory` to the theorem, critical lemmas, and proof. If skill-to-skill invocation is unavailable, execute [the sibling skill](../destroy-theory/SKILL.md). Treat proposed repairs as findings for phase 7.

Complete this phase when its report meets the skill's completion criterion on the current candidate.

## 6. Audit hypotheses

Apply `$audit-assumptions` to the same candidate, or execute [the sibling skill](../audit-assumptions/SKILL.md). Keep proof dependence distinct from theorem necessity. The nested audit performs cheap removal tests and returns uncovered `requested_attacks`; it does not launch another destroyer. After both reports join, send only uncovered requests to one constrained `destroy-theory` follow-up.

Complete this phase when its report meets the skill's completion criterion on the current candidate.

## 7. Reconcile and stabilize

Begin only after both principal reports cover the same candidate. Give every finding a disposition: repair it; close it by content-bound specialist re-evaluation or exact independent adjudication; or preserve it in the result status. Any unresolved material finding blocks `PROVED`.

Integrate repairs centrally. A material repair returns to the earliest affected phase and produces a new candidate reviewed by both specialists. Once unchanged, freeze a stabilization manifest containing the candidate digest, report lineage, dispositions, repair diffs, and re-evaluations.

Complete this phase when both latest reviews cover one unchanged candidate, every finding is dispositioned, and the stabilization manifest is frozen.

## 8. Verify independently

Promote the stabilized candidate unchanged. Bind each verifier and its exact input projection to that candidate and record every terminal outcome, including failure or abstention.

Use at least one of: a second proof; fresh derivation of the crux; alternative characterization; trusted checker, different model, or human specialist; or dependency reconstruction from scratch. For independent derivation, give the target and necessary sources but withhold the submitted proof. For correctness review, give the proof and necessary artifacts but withhold persuasive narrative. Check proof correctness and statement fidelity separately.

A material candidate or stabilization change invalidates verification and reopens the affected phases. Withhold research memory unless a source is necessary. A fresh-context same-model critic is useful but correlated; an independence claim also needs a different proof, trusted checker, different model, or human specialist.

Complete this phase when all current verifier outcomes and discrepancies are dispositioned and at least one content-bound report independently checks the central argument; otherwise state that limitation.

## 9. Improve and contextualize

Test stronger conclusions, weaker hypotheses, converses, quantitative or stability results, uniqueness, characterizations, extensions, approximations, consequences, and connections. Any accepted material improvement reopens the affected review and verification phases.

When priority, attribution, or novelty matters, search primary literature for the exact claim, equivalent formulations, constructions, and proof motifs. Verify exact sources and report coverage. Failure to locate a reference leaves novelty unresolved.

## 10. Present and close

Use the smallest structure that preserves checkability. For substantial work, cover the problem and interpretation, assumptions, result and status, mechanism and examples, strategy comparison, proof dependencies, specialist findings and repairs, assumption analysis, independent verification, extensions and sources, provenance, and the exact unresolved point.

Use one terminal status:

- `PROVED`: every material step and finding closes, and attack, assumption audit, and independent check cover the same final version;
- `INCOMPLETE`: a promising argument has a precise open obligation;
- `CONJECTURAL`: evidence exists without a closing proof architecture;
- `FALSE`: a certified counterexample or contradiction defeats the claim;
- `UNRESOLVED`: the work does not determine truth.

Keep logical correctness, statement fidelity, novelty or significance, provenance or autonomy, and readable reconstruction separate. Tags such as `kernel-checked`, `expert-refereed`, `statement-faithful`, `novelty-audited`, `computationally tested`, or `literature-supported` describe support rather than replacing status.

Report material model and tool versions, prompts or human hints, edits, retries and selection, attempt denominator, budget, checker versions, expert review, and literature-search coverage. Include material failures and abstentions; do not expose round-local identifiers or collapse proof checking, faithful formalization, independent review, and novelty review into one “verification” claim.

For file-backed work, integrate the accepted theorem, assumptions, proof, load-bearing negative results, unresolved obligations, and concise review/provenance summary into the canonical document. Curate only reusable noncanonical obligations, demonstrated obstructions, parked improvements, reusable counterexamples, assumption relaxations, source-applicability snapshots, residual attacks, and verification lessons as cards. All candidate versions, reports, manifests, logs, routine failures, and superseded state remain in the workpad. Close once under the shared protocol; completion leaves only the self-contained canonical document, curated companion, and deliberate native mathematical artifacts.

When the user requests an accessible treatment after the mathematics is settled, apply `$explain-mathematics` or execute [the sibling skill](../explain-mathematics/SKILL.md).
