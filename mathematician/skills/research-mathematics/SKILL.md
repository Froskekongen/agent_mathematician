---
name: research-mathematics
description: Prove, verify, repair, or rigorously resolve a substantial mathematical claim.
disable-model-invocation: true
---

# Research Mathematics

Prove or refute a substantial claim, or identify exactly what remains open.
Follow the [shared mathematical integrity](references/mathematical-integrity.md)
and the complete research-only
[claim-resolution process](references/claim-resolution.md). These checks govern
the work; they need not become the voice or outline of the final mathematics.
If the objects are still unclear, recommend `$formalize-concepts`. If the
formalism is clear but the right claim is not, recommend
`$explore-mathematical-structure`.

For authorized file-backed work or explicit research-history retrieval, read
the [research-memory rules](references/research-memory.md). Chat-only work
creates no theory files. This skill is the sole writer in its round.

## 1. State the exact claim

State the claim, intended interpretation, typed objects, quantifiers,
definitions, individual assumptions, permitted axioms, and representative
non-vacuous cases. Before sending the claim to another reviewer, give this exact
version a content digest. If the statement changes, create a new digest and
repeat every check affected by the change.

Complete this step when every symbol and qualifier has a declared meaning and
the statement is well-posed.

## 2. Find the mechanism and choose a route

Test the smallest nontrivial, representative, boundary, and near-miss cases.
Identify the structure that could make the claim true. Compare credible routes
only far enough to select one; when route selection is itself substantial, stop
this run and recommend `$explore-proof-strategies`.

Use material computation only when it can decide the claim, the choice of
route, or an essential step. Then read
[computational-checking.md](references/computational-checking.md) and dispatch
the appropriate internal mode. Decide materiality first; do not load that
reference merely to classify a hand-checkable calculation.

Complete this step with a selected route justified by the mathematics, or an
explicit proof-strategy handoff.

## 3. Build the proof

Turn the selected route into a dependency-ordered map from definitions and
lemmas to the main claim. Show where each assumption and imported theorem is
used. Prove every step, and state any unfinished step plainly. Check proposed
inferences one at a time; if checking requires a repair, record the repair as a
change rather than silently folding it in.

Complete this step when every dependency node is proved or has one precise
open obligation.

## 4. Challenge the unchanged candidate

Bundle the exact claim, proof map, assumptions, sources, axioms, and artifacts
under one digest. Dispatch two fresh, mutually isolated, read-only contexts on
that candidate, digest, and no peer report: the first prompt invokes
`$destroy-theory`; the second invokes `$audit-assumptions`.

Reject a report with a mismatched `candidate_digest`. Combine duplicate
`requested_attacks` and `requested_assumption_audits`. After the initial pair,
allow at most one fresh call to each worker containing all unseen requests of
its type. Do not start a recursive review loop; preserve later requests as open
work. The coordinator routes review work and integrates or repairs findings as
sole writer; specialists only review. A material repair gets a new digest and
repeats both reviews. If fresh isolation is unavailable, this review remains
unfinished.

Complete this step when both reports cover the same unchanged version and every
important finding has been resolved, accepted as an open issue, or shown not to
apply.

## 5. Verify independently

Give the stabilized candidate to a fresh verifier. Use a second derivation,
independent reconstruction of the crux or dependency graph, an alternative
characterization, an audited checker, a different model, or a qualified human
as appropriate. Withhold the submitted proof when requesting an independent
derivation and withhold persuasive narrative during correctness review.

An essential executable artifact also receives a fresh `replay` under the
computational-checking rules. Resolve every discrepancy against the same
version; a material change restarts challenge and verification.

Complete this step when an independent check covers the central argument and
every success, failure, or inability to verify has been recorded.

## 6. Write the result

Only after the main claim is stable, consider useful strengthenings,
weakenings, converses, bounds, stability, uniqueness, or extensions. Recommend
`$audit-assumptions` when minimizing hypotheses becomes a substantial task.
Repeat the affected checks after any accepted mathematical change. When
attribution or novelty matters, search primary literature for the exact claim
and equivalent formulations, match assumptions, and report what was searched.

Assign the mathematical status under the claim-resolution process. Write the
main account as mathematics: motivation, exact statement, examples, mechanism,
proof or counterexample, assumptions, limitations, and remaining open questions.
Include review findings only when they clarify the mathematics. Put digests,
worker routing, check histories, and detailed provenance in a compact technical
note or research memory rather than the main exposition.

For file-backed work, keep accepted mathematics in canonical Markdown, retain
only reusable background in memory, and finish under the research-memory rules.

The run is complete only when the reported status is justified for one final
version of the claim; `PROVED` requires every part of the claim-resolution
process. When a stabilized proof needs a cross-specialty mathematical account,
recommend `$write-proof-exposition` rather than expanding this research round
into a separate writing task.
