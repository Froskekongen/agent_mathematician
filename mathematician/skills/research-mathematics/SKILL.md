---
name: research-mathematics
description: Prove, verify, repair, or rigorously resolve a substantial mathematical claim.
disable-model-invocation: true
---

# Research Mathematics

Resolve a substantial claim rigorously or expose its exact failure or open
obligation. Read and apply the shared [rigor chain](references/rigor.md)
completely. If meanings or objects remain unsettled, stop this run and recommend
`$formalize-concepts`; if a provisional formalism still lacks an exact target,
stop and recommend `$explore-mathematical-structure`.

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
Identify the structure that could make the claim true. Compare credible routes
only far enough to select one; when route selection is itself substantial, stop
this run and recommend `$explore-proof-strategies`.

Use material computation only when it can decide truth, route allocation, or a
load-bearing step. Then read
[computational-checking.md](references/computational-checking.md) and dispatch
the appropriate internal mode. Decide materiality first; do not load that
reference merely to classify a hand-checkable calculation.

Complete this step with a selected route justified by the mathematics, or an
explicit proof-strategy handoff.

## 3. Construct the evidence

Turn the selected route into a dependency-ordered proof graph. Attach each
assumption and imported theorem to its exact uses, prove every node, and mark
the remainder explicitly open. Check one inference at a time after proposal;
the checking pass introduces no silent repairs.

Complete this step when every dependency node is proved or has one precise
open obligation.

## 4. Challenge the unchanged candidate

Freeze the target, proof graph, assumptions, sources, axioms, and artifacts
under one digest. Dispatch two fresh, mutually isolated, read-only contexts on
that candidate, digest, and no peer report: the first prompt invokes
`$destroy-theory`; the second invokes `$audit-assumptions`.

Reject a mismatched `candidate_digest`. Deduplicate `requested_attacks` and
`requested_assumption_audits`; route new items to `$destroy-theory` and
`$audit-assumptions`, respectively. After the initial pair, allow at most one
fresh call to each worker containing all unseen requests of its type; do not
recurse, and preserve later requests as open obligations. The coordinator
routes review work and integrates or repairs findings as sole writer;
specialists only review. A material repair redigests and repeats both reviews;
unavailable isolation leaves the gate open.

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
bounds, stability, uniqueness, or extensions. Recommend `$audit-assumptions`
when hypothesis minimization becomes substantial. Reopen affected gates for
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
