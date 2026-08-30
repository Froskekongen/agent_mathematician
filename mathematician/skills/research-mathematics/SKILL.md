---
name: research-mathematics
description: Resolve a substantial mathematical claim by proving it, refuting it, repairing it, or identifying exactly what remains open.
disable-model-invocation: true
---

# Research Mathematics

Resolve one substantial claim: prove it, refute it, repair it, or locate the
exact point that remains open. Follow the
[shared mathematical integrity](references/mathematical-integrity.md) and the
complete research-only
[claim-resolution process](references/claim-resolution.md). That process
determines status, not the voice or order of the mathematics. If the objects are
unclear, recommend `$formalize-concepts`; if the right claim is not yet clear,
recommend `$explore-mathematical-structure`.

For authorized file-backed work or explicit research-history retrieval, read
the [research-memory rules](references/research-memory.md). Chat-only work
creates no theory files. This skill is the sole writer in its round.

## 1. Fix the exact claim

Write the claim in a form on which a proof can bear: give its interpretation,
typed objects, domains, quantifiers, definitions, assumptions, permitted
axioms, and representative non-vacuous cases. Separate the submitted claim from
any repaired or restricted version.

Give the exact candidate a content digest before review. A changed statement is
a new target: give it a new digest and repeat every affected check. Do not begin
proof work until every symbol and qualifier has a meaning and the claim is
well-posed.

## 2. Learn from examples and choose an idea

Work through the smallest nontrivial cases, a representative case, and a
boundary or near miss. Use them to test the statement and discover what might
make its conclusion follow from its hypotheses.

Compare proof ideas only far enough to choose one. A credible route explains
why the hypotheses matter, what intermediate statement would unlock the proof,
and where the difficulty lies. If route selection needs substantial
exploration, recommend `$explore-proof-strategies`.

Use material computation only when it can decide the claim, the choice of
route, or an essential step. Then read
[computational-checking.md](references/computational-checking.md) and dispatch
the appropriate internal mode. Decide materiality first; do not load that
reference merely to classify a hand-checkable calculation.

Choose a route only for a mathematical reason; otherwise make an explicit
proof-strategy handoff.

## 3. Construct the argument

Organize the argument by mathematical dependence. For each nonroutine step, say
what it accomplishes, which hypotheses it uses, and where the idea comes from.
Match imported theorems to the present notation, assumptions, and conventions.

Prove each load-bearing inference and state every unfinished one plainly. A
repair is a mathematical change, not a silent edit. Challenge the candidate
only when every dependency is proved or has one precise open obligation; any
such obligation rules out `PROVED`.

## 4. Challenge the unchanged candidate

Challenge one unchanged candidate. Bundle the exact claim, proof map,
assumptions, sources, axioms, and artifacts under one digest. Dispatch two
fresh, mutually isolated, read-only contexts on that candidate, digest, and no
peer report: the first prompt invokes `$destroy-theory`; the second invokes
`$audit-assumptions`.

Reject a report with a mismatched `candidate_digest`. Combine duplicate
`requested_attacks` and `requested_assumption_audits`. After the initial pair,
allow at most one fresh call to each worker containing all unseen requests of
its type. Do not start a recursive review loop; preserve later requests as open
work. The coordinator routes review work and integrates or repairs findings as
sole writer; specialists only review. A material repair gets a new digest and
repeats both reviews. If fresh isolation is unavailable, this review remains
unfinished.

Treat the challenge as complete only when both reports cover the same unchanged
version and every important finding has been resolved, accepted as an open
issue, or shown not to apply.

## 5. Verify the central argument independently

Give the stabilized candidate to a fresh verifier. Choose a check that bears on
the crux, such as a second derivation, an independent reconstruction, an
alternative characterization, or an audited checker. A different model or
qualified human may also provide the check. Withhold the submitted proof when
asking for an independent derivation and withhold persuasive narrative during
correctness review.

An essential executable artifact also receives a fresh `replay` under the
computational-checking rules. Resolve every discrepancy against the same
version; a material change restarts challenge and verification.

Do not report `PROVED` until an independent check covers the central argument
and every discrepancy has been resolved. Record any failure or inability to
verify; it leaves the claim at a lower status.

## 6. Set the status and write the mathematics

Assign status under the claim-resolution process. `PROVED` requires one final,
unchanged target to pass the complete chain. Otherwise use the strongest honest
lower status and name the exact obstruction or open step.

Write for a mathematician, not for the internal workflow. Explain why the
question matters, what the examples reveal, and why the proof or counterexample
works. Place the exact statement, assumptions, limitations, and open questions
where they clarify the argument. Put digests, routing, check histories, and
detailed provenance in a technical note or research memory.

Only after the status is stable, consider natural strengthenings, weakenings,
or extensions. Recommend `$audit-assumptions` when minimizing hypotheses
becomes substantial. Any accepted change creates a new target and repeats the
affected checks. When attribution or novelty matters, search primary literature
for the exact claim and equivalent formulations, match assumptions, and report
what was searched.

For file-backed work, keep accepted mathematics in canonical Markdown, retain
only reusable background in memory, and finish under the research-memory rules.

When a stabilized proof needs a cross-specialty mathematical account, recommend
`$write-proof-exposition` rather than expanding this research round into a
separate writing task.
