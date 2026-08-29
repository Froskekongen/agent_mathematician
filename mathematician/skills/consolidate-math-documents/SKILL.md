---
name: consolidate-math-documents
description: Combine mathematical documents into one coherent account and safely retire their source pairs.
disable-model-invocation: true
---

# Consolidate Mathematical Documents

Create one coherent mathematical account from several documents. Preserve
definitions, assumptions, validity limits, mathematical status, and provenance.
Follow the
[shared mathematical integrity](../research-mathematics/references/mathematical-integrity.md),
[research-memory rules](../research-mathematics/references/research-memory.md),
and, before retiring any source, the
[source-retirement rules](references/source-retirement.md). Consolidation may
reorganize and clarify existing mathematics, but it does not certify new
mathematics.

## 1. Fix the sources and target

Require an explicit deduplicated source list and at least two mathematical
documents in total. In preview mode, report without filesystem changes. In a
writable run, require an explicit absent Markdown target or explicit existing
canonical target; exactly that target pair is writable, while all sources and
their companions remain read-only until close.

Decide whether the documents describe one theory or connect several theories.
In a temporary work area, record immutable copies and digests of the sources,
their companions, the target baseline, native artifacts, and inbound links.
Create no repository manifest. Record which sources might later be retired, but
wait for a stable target draft before making the final retirement plan.

Complete this step when every input is immutable and the prospective retirement
set and source eligibility are explicit.

## 2. Reconcile the mathematics behind the scenes

Build an internal reconciliation map covering every definition, notation
choice, ambient structure, assumption, claim and status, dependency, boundary,
counterexample, open problem, citation, link, native artifact, research key,
memory card, origin, and relation. For each item, decide whether to integrate
it, merge an equivalent version, keep it as an alternative, preserve it only in
memory or as a native artifact, discard it with its source, or leave a visible
conflict. Record where each retained item will go or why it is excluded.

Equal names need not denote equal objects. Compare domains, quantifiers,
assumptions, and status before merging anything, and merge only when the sources
already establish equivalence. Otherwise keep the conflict visible. Recommend
`$audit-assumptions` for mismatched assumptions, `$destroy-theory` for
incompatible validity claims, or `$research-mathematics` when a new equivalence
proof is needed. When several theories are involved, keep their modules clear
and explain the translations between them. Recency alone does not resolve a
conflict.

Complete this step when every source item has one clear destination or one clear
reason for exclusion. The reconciliation map is an internal tool, not the
outline of the final document.

## 3. Write one coherent account

Organize the target for mathematical understanding rather than source order.
Introduce notation once, place definitions before use, connect motivation to
results, and keep proofs, examples, counterexamples, and boundaries near the
claims they explain. Preserve accepted assumptions, support, important negative
results, unresolved conflicts, citations, and deliberate native artifacts.
Resolve relative links and label collisions. Assign one research key per
durable mathematical subject under the memory rules.

Curate source memory rather than merging databases. Keep only reusable open
problems, directions worth reviving, demonstrated obstructions,
counterexamples, and important source-applicability findings. A target memory
card derived from a source must make sense on its own and retain its source
digest and local mapping.

Complete this step when the target is understandable without opening the source
documents and its stable draft is ready to bind the retirement plan. Do not copy
the reconciliation ledger, file mechanics, or database language into the
mathematical narrative.

## 4. Publish and retire safely

Construct and check the exact retirement plan under the source-retirement
rules. Revalidate source digests, database revisions, and the target baseline;
publish and close the target pair under the research-memory rules; then recheck
and apply the fixed retirement plan. Recheck the target after retirement.

## Completion

A writable run is complete only when the target pair validates, every source
item is accounted for, every authorized retired source pair is absent and
recoverable from Git, and the temporary work area is deleted. A preview returns
the reconciliation, conflicts, and proposed retirement plan without changing
files.
