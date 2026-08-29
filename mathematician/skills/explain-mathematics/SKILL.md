---
name: explain-mathematics
description: Explain advanced mathematics to a mature nonspecialist without changing its meaning or status.
disable-model-invocation: true
---

# Explain Mathematics

Build a bridge from the reader's mathematical background to the focal theory
without changing the mathematics. Read and apply the shared
[mathematical-integrity contract](../research-mathematics/references/mathematical-integrity.md).
This skill's rigor is explanatory: preserve exact core mathematics and status
while optimizing mental models, motivation, examples, and mechanism. A complete
proof is optional unless the request is genuinely proof-bearing.

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

## 2. Orient with a recoverable mental model

Begin with the problem, obstruction, or phenomenon that makes the theory
useful. Give a mental model in language or mathematics already available to
the reader, then identify the exact objects and relations it represents. For a
cross-field analogy, say what structure transfers and where the comparison
breaks.

Orient the reader before abstraction: motivation or obstruction, introduced
structure, resolving mechanism, informal result, then the exact qualified
theorem.

Complete this step when the reader has a usable model whose exact referents and
limits are visible.

## 3. Install the exact backbone

Order field-specific definitions, conventions, constructions, and imported
results by dependency. Introduce each bridged prerequisite before use. State
the focal object or theorem with all qualifiers that affect meaning, and keep
source, conjectural, incomplete, and proved material visibly distinct.

Complete this step when the exact mathematics can be parsed without an
undeclared specialist dependency and can be related back to the mental model.

## 4. Make the mechanism operate

Use the shortest checked example set that makes the mechanism operate and
shows a relevant boundary. Usually one mechanism-bearing example and one
boundary case or nonexample suffice; one example may do both jobs. Add a
representative, parameterized, or pathological rung only when it teaches a
distinct feature. For each rung state its objects, assumptions, calculation,
lesson, and what it does not establish.

Give a proof map only when the proof is focal or it materially explains the
mechanism. Emphasize the crux and the purpose of its main components rather
than expanding routine detail by default. If the user needs a complete proof
that a nonspecialist mathematician can reconstruct, recommend
`$write-proof-exposition`.

## 5. Check explanatory and mathematical fidelity

Preserve unresolved obligations and source status. Check every load-bearing
example, analogy boundary, citation, theorem qualifier, and transition from the
mental model to the exact mathematics. A heavily rewritten account is compared
against its source claim and checked proof when one exists.

For an executable or machine-checked result, reconstruct the human mechanism,
map the intended theorem to the encoded statement and dependencies, and state
the checker's trust boundary and semantic limitations. On a load-bearing
defect, preserve the recorded source status only as provenance, label the local
account not revalidated, and report the defect as unresolved. Recommend
`$destroy-theory`; recommend `$audit-assumptions` for necessity or
`$research-mathematics` for repair or certification.

## 6. Rewrite faithfully when authorized

Draft outside the target from a workpad snapshot and audit the complete rewrite
against the integrity and canonical contracts. Preserve meaning, status, and
provenance. If fidelity would require mathematical repair, leave the pair
unchanged and hand off to the appropriate research or review skill. Otherwise
close through the protocol.

## Return and completion

Use the smallest useful ordering of audience contract, orientation,
mental model, definitions, exact theorem, mechanism, example ladder, optional
proof map, boundary cases, and next prerequisites. Distinguish intuition from
justification without interrupting every intuitive passage with proof
ceremony.

Complete only when the reader can identify the exact object or claim, explain
the mechanism in the mental model, distinguish that model from its
justification, and see both a checked mechanism-bearing example and a checked
boundary or nonexample. Proof dependencies are required only to the depth
promised by the request.
