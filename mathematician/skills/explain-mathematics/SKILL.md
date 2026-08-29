---
name: explain-mathematics
description: Explain advanced mathematics to a mature nonspecialist without changing its meaning or status.
disable-model-invocation: true
---

# Explain Mathematics

Build a bridge from the reader's mathematical background to the focal theory
without changing the mathematics. When explaining a theorem or proof, use the
shared [rigor chain](../research-mathematics/references/rigor.md) to preserve its
exact target and status.

## File modes

With no explicit file-change request, answer in chat and keep every supplied
file and companion read-only. Merely supplying or naming a file does not
authorize a rewrite. When the user asks about research history, rejected
routes, or development process, read the
[research-memory protocol](../research-mathematics/references/research-memory.md),
query the companion read-only, and label the result as research history.

An explicit request that names an existing canonical target and asks to update
or rewrite it authorizes an in-place rewrite of exactly that Markdown/SQLite
pair. Read the research-memory protocol completely and act as its sole writer.
Create a separate explanatory target only when the user explicitly requests
one; it owns a new companion while the source pair remains read-only. Two
Markdown documents never share one SQLite database.

## 1. Set the audience contract

Infer the reader's relevant background from the request. Default to a
mathematically mature nonspecialist. Partition prerequisites into assumed,
bridged here, and optional.

Complete this step when the audience and prerequisite budget are explicit.

## 2. Build the bridge

Order field-specific definitions, conventions, constructions, and imported
theorems by dependency. Introduce each bridged prerequisite before use. For a
cross-field idea, give its purpose, exact statement, nearest familiar analogue,
and the point where the analogy fails.

Orient the reader before abstraction: motivation or obstruction, introduced
structure, resolving mechanism, informal result, then the exact qualified
theorem.

Complete this step when the exact theorem can be parsed without an undeclared
specialist dependency.

## 3. Expose the mechanism with examples

Use the shortest example ladder that makes the mechanism appear, operate, and
fail at a boundary. Include a smallest nontrivial example, a representative
example, and at least one checked boundary case or nonexample. Add trivial,
parameterized, or pathological rungs only when they teach a distinct feature.
For each rung state its objects, assumptions, calculation, lesson, and what it
does not establish.

## 4. Explain and check fidelity

Present a proof map, annotate assumptions at mechanism-bearing steps, preserve
unresolved obligations and source status, and emphasize fragile reductions,
cross-field transfers, and imported results.

For an executable or machine-checked result, reconstruct the human mechanism,
map the intended theorem to the encoded statement and dependencies, and state
the checker's trust boundary and semantic limitations. Check every example,
prerequisite order, analogy boundary, citation, and theorem qualifier; compare
a heavily rewritten exposition against the checked proof. On a load-bearing
defect, preserve the recorded source status only as provenance, label it not
revalidated, and report the defect as unresolved. Recommend `$destroy-theory`;
recommend `$audit-assumptions` for necessity or `$research-mathematics` for
repair or certification.

## 5. Rewrite a canonical pair when authorized

For an in-place rewrite, use one OS-temporary workpad to:

1. freeze the canonical bytes and digest, database revision, key outline,
   affected links, cards, artifacts, terminology, and claim statuses;
2. map every subject, definition, term, notation, and key, then draft the
   complete rewrite outside the target;
3. verify that every definition, hypothesis, conclusion, dependency, status,
   boundary, obligation, and provenance item survives unchanged in meaning;
4. preserve keys for unchanged subjects, rekey only misleading keys or genuine
   splits and merges, and plan the complete link migration;
5. update affected card titles, summaries, details, reuse conditions, and
   `term` and `symbol` facets to current terminology, retaining historical
   wording as provenance; and
6. refresh each card-key link whose section digest or card revision changed,
   even when its relation and note do not.

Keep accepted terminology and definitions in Markdown; do not create a term
registry or cards that merely duplicate exposition. After fidelity passes,
publish the Markdown, apply one optimistic memory transaction, run `check`,
and exactly reread every changed key, card, and artifact. If fidelity exposes
a load-bearing defect or requires mathematical repair, leave the original pair
unchanged and hand off to the appropriate research or review skill.

## Return and completion

Use the smallest useful ordering of audience contract, orientation,
definitions, exact theorem, mechanism, example ladder, proof, boundary cases,
and optional next prerequisites. Distinguish intuition from justification.

Complete only when the reader can identify the hypotheses, conclusion,
mechanism, proof dependencies, and limitations, and when both a
mechanism-bearing example and a boundary or nonexample have been checked. A
writable rewrite also requires a current pair and exact rereads of every
changed memory entity.
