---
name: research-mathematics
description: Research, formulate, prove, verify, or repair a substantial mathematical theorem, conjecture, derivation, or theory. Use for open-ended mathematical research, rigorous proof construction, independent verification, or improving a theorem. Reserve this full workflow for nontrivial claims rather than routine calculations or exposition-only requests.
disable-model-invocation: true
---

# Research Mathematics

Resolve a substantial claim rigorously or expose its exact failure or open
obligation. Read and apply the shared [rigor chain](references/rigor.md)
completely. If the target is not yet precise enough to judge, hand it to
`$explore-mathematical-structure` rather than inventing a theorem.

For authorized file-backed work or explicit research-history retrieval, read
the [research-memory protocol](references/research-memory.md). Chat-only work
creates no theory files. This skill is the sole writer in its round.

## 1. Freeze the target

State the claim, intended interpretation, typed objects, quantifiers,
definitions, atomic assumptions, permitted axioms, and representative
non-vacuous cases. Give the target a content digest before delegation. A
material change produces a new digest and restarts every affected gate.

Complete this step when every symbol and qualifier has a declared meaning and
the statement is well-posed.

## 2. Expose the mechanism and compare routes

Test the smallest nontrivial, representative, boundary, and near-miss cases.
Identify the structure that could make the claim true. Compare at least two
materially different proof routes for a nontrivial claim; for each record its
mechanism, assumptions, hardest subgoal, likely failure, and disposition.

Use material computation only when it can decide truth, route allocation, or a
load-bearing step. Then read
[computational-checking.md](references/computational-checking.md) and dispatch
the appropriate internal mode. Decide materiality first; do not load that
reference merely to classify a hand-checkable calculation.

Complete this step with a selected route justified by the mathematics, or an
exact account of why no route is yet viable.

## 3. Construct the evidence

Turn the selected route into a dependency-ordered proof graph. Attach each
assumption and imported theorem to its exact uses, prove every node, and mark
the remainder explicitly open. Check one inference at a time after proposal;
the checking pass introduces no silent repairs.

Complete this step when every dependency node is proved or has one precise
open obligation.

## 4. Challenge the unchanged candidate

Freeze the target, proof graph, assumptions, sources, permitted axioms, and
artifacts under one candidate digest. Dispatch two cold specialist contexts
against exactly that candidate:

- a falsifier attacks the theorem, proof, specification, and critical lemmas;
- an assumption auditor separates well-posedness, proof use, and theorem
  necessity, and identifies uncovered witness searches.

After both return, run only uncovered attacks. Each finding is repaired,
closed by content-bound re-evaluation, or preserved as an open defect. A
material repair creates a new candidate and repeats both reviews.

Complete this step when both reports cover one unchanged digest and every
material finding has a disposition.

## 5. Verify freshly

Give the stabilized candidate to a fresh verifier. Use a second derivation,
independent reconstruction of the crux or dependency graph, an alternative
characterization, an audited checker, a different model, or a qualified human
as appropriate. Withhold the submitted proof when requesting an independent
derivation and withhold persuasive narrative during correctness review.

A load-bearing executable artifact also receives a fresh `replay` under the
computational-checking role. Reconcile every discrepancy against the same
digest; material change reopens challenge and verification.

Complete this step when a fresh content-bound report checks the central
argument and every verifier outcome, failure, or abstention is recorded.

## 6. Improve, contextualize, and close

Only after stabilization, test useful strengthenings, weakenings, converses,
bounds, stability, uniqueness, or extensions. Reopen the affected gates for
every accepted material change. When attribution or novelty matters, search
primary literature for the exact claim and equivalent formulations, map
hypotheses, and report coverage.

Assign the terminal status under the shared rigor chain. Present the target,
mechanism, proof dependencies, specialist findings and repairs, assumption
analysis, independent verification, provenance, and exact remaining
obligations. For file-backed work, keep accepted mathematics in canonical
Markdown, curate only reusable noncanonical memory, and complete the shared
memory close.

The run is complete only when the reported status is justified for one final
target digest; `PROVED` additionally requires the entire shared completion
gate.
