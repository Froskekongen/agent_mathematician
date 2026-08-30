---
name: consolidate-math-documents
description: Reconcile mathematical documents into one coherent account and safely retire the exact source pairs.
disable-model-invocation: true
---

# Consolidate Mathematical Documents

Create one mathematical account from several documents. Preserve definitions,
assumptions, validity limits, status, and provenance while organizing the result
by mathematical meaning. Follow the
[shared mathematical integrity](../research-mathematics/references/mathematical-integrity.md),
[research-memory rules](../research-mathematics/references/research-memory.md),
and, before retiring any source, the
[source-retirement rules](references/source-retirement.md). Consolidation may
clarify existing mathematics; it does not certify new mathematics.

## 1. Fix the sources, target, and authority

Start from an explicit deduplicated source list containing at least two
mathematical documents in total. A preview changes no files. A writable run
needs either an explicit absent Markdown target or an explicitly named existing
canonical target. Exactly that target pair is writable; every source and source
companion remains read-only until retirement.

Decide whether the documents develop one theory or connect several. In a
temporary work area, preserve immutable copies and digests of the sources,
companions, target baseline, native artifacts, and inbound links. Keep this
material out of the repository. Identify sources that may later be retired,
but bind no final retirement plan until the target draft is stable.

Proceed when every input is frozen and the possible retirement set and its
eligibility are explicit.

## 2. Reconcile the mathematics behind the scenes

Build an internal map of every mathematical item that may survive: objects,
definitions, notation, ambient structures, assumptions, claims and statuses,
proof dependencies, boundaries, counterexamples, open problems, citations,
links, artifacts, research keys, memory, and provenance. Give each source item
one destination in the target or memory, or one explicit reason for exclusion.

Equal names do not imply equal objects. Compare domains, quantifiers,
assumptions, conventions, and status before identifying two formulations, and
merge them only when the sources already establish the required equivalence.
Otherwise retain the alternatives or state the conflict. For several theories,
keep their modules visible and explain the maps or translations between them.
Recency alone resolves nothing.

Recommend `$audit-assumptions` for a substantive mismatch of hypotheses,
`$destroy-theory` for incompatible validity claims, or
`$research-mathematics` when consolidation would require a new equivalence
proof. The reconciliation map is complete when every source item is accounted
for; it remains an internal instrument rather than the outline of the document.

## 3. Write one mathematical account

Order the target by meaning and dependence, not by source. Introduce notation
once and definitions before use. Let motivation lead to results, and place
proofs, examples, counterexamples, and boundaries beside the claims they
explain. Preserve accepted assumptions, support, important negative results,
unresolved conflicts, citations, and deliberate native artifacts. Resolve
relative links and label collisions.

Assign one research key to each durable mathematical subject under the memory
rules. Curate source memory rather than merging databases: retain only reusable
open problems, directions worth reviving, demonstrated obstructions,
counterexamples, and important source-applicability findings. A retained card
must make sense on its own and preserve its source digest and local mapping.

The stable draft is ready when it can be understood without reopening the
sources and every retained item has found its mathematical place. Reconciliation
maps, file mechanics, digests, and database language stay outside the account.

## 4. Publish and retire safely

After the draft stabilizes, construct and check the exact retirement plan under
the source-retirement rules. Revalidate the frozen source digests, database
revisions, and target baseline. Publish and close the target pair under the
research-memory rules, recheck the fixed retirement plan, apply it, and check
the target once more after retirement.

A writable run finishes only when the target pair validates, every source item
is accounted for, every authorized retired source pair is absent and
recoverable from Git, and the temporary work area is gone. A preview returns
the mathematical reconciliation, unresolved conflicts, and proposed retirement
plan without changing files.
