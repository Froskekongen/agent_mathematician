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

Default to chat; files and companions remain read-only unless the user
explicitly asks to update or rewrite a named canonical target. Merely supplying
or naming one is not authorization. For research history, read the
[research-memory protocol](../research-mathematics/references/research-memory.md),
query the companion read-only, and label the result as history.

An in-place request authorizes only that target's Markdown/SQLite pair. An
explicitly requested separate explanation gets its own companion and leaves
the source pair read-only; no two Markdown documents share one database.
For writable work, read the protocol completely and act as sole writer.

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

## 5. Rewrite faithfully when authorized

Draft outside the target from a workpad snapshot and audit the complete rewrite
against the shared rigor chain and the protocol's canonical contract. Preserve
meaning and provenance. If fidelity would require mathematical repair, leave
the pair unchanged and hand off to the appropriate research or review skill.
Otherwise close through the protocol.

## Return and completion

Use the smallest useful ordering of audience contract, orientation,
definitions, exact theorem, mechanism, example ladder, proof, boundary cases,
and optional next prerequisites. Distinguish intuition from justification.

Complete only when the reader can identify the hypotheses, conclusion,
mechanism, proof dependencies, and limitations, and when both a
mechanism-bearing example and a boundary or nonexample have been checked.
