---
name: write-proof-exposition
description: Write a self-contained, proof-bearing exposition of stabilized mathematics for a mathematician outside the source specialty, without repairing or upgrading the result.
disable-model-invocation: true
---

# Write Proof Exposition

Turn stabilized mathematics into a proof-bearing account that a mathematically
mature reader outside the source specialty can reconstruct. Read and apply the
shared
[mathematical-integrity contract](../research-mathematics/references/mathematical-integrity.md).
This skill's rigor is source fidelity plus audience-relative reconstructibility;
it inherits rather than establishes the result's truth status.

Use `$explain-mathematics` when intuitive understanding is primary and a
complete proof is unnecessary. Use `$research-mathematics` when a load-bearing
argument must be invented, repaired, challenged, or certified.

## File modes

Default to chat; source files and companions remain read-only unless the user
explicitly asks to update or rewrite a named canonical target. Merely supplying
or naming one is not authorization. For research history, read the
[research-memory protocol](../research-mathematics/references/research-memory.md),
query the companion read-only, and label the result as history.

An in-place request authorizes only that target's Markdown/SQLite pair. An
explicitly requested separate proof exposition gets its own companion and
leaves the source pair read-only; no two Markdown documents share one database.
For writable work, read the protocol completely and act as sole writer.

## 1. Bind the source and audience contracts

Record the exact theorem or result, definitions, assumptions, conventions,
truth status, proof or certificate, imported results, known boundaries, and
provenance that the exposition must preserve. Distinguish a proved source from
a proof sketch, incomplete argument, or trusted but unchecked citation.

Infer the reader's relevant background. Partition prerequisites into assumed,
briefly recalled, developed here, and cited. Self-contained means complete
relative to this declared prerequisite boundary, not free of all dependencies.

Complete this step when the source package and audience boundary are explicit.
If the source lacks a load-bearing argument, preserve its lower status and
recommend `$research-mathematics` rather than silently supplying new research.

## 2. Build the two-level proof map

First expose the problem, governing mental model, mechanism, and proof crux.
Then partition the proof into dependency-ordered modules and state what each
module accomplishes. Connect the high-level account to the exact theorem and
module interfaces so the intuition remains recoverable.

Use examples, diagrams, or analogies when they reveal the mechanism. Identify
their exact referents, preserved structure, and relevant breakpoint. Routine
details may remain compressed only when they are routine for the declared
audience and do not hide the crux.

Complete this step when the reader can see both why the route should work and
how its modules close the exact theorem.

## 3. Write the reconstructible proof

Present definitions and imported results before use. For each nonroutine step,
make visible both its mathematical task and where the idea could reasonably
come from. Show every load-bearing inference or cite an exact imported theorem
after mapping all hypotheses and conventions. Expand specialist shorthand at
the crux; compress only derivations the target reader can reliably recover.

Keep statement, proof, and any formal or executable encoding distinct. For a
machine-checked source, state the trust boundary and reconstruct the human
mechanism without claiming that the reconstruction replaces the certificate.

Complete this step when the proof is complete relative to the audience
contract and every imported interface matches exactly.

## 4. Audit the transformation

Compare source and exposition for the theorem statement, definitions,
assumptions, quantifiers, conventions, dependency interfaces, validity
boundaries, provenance, and status. Check the examples, diagrams, formulas,
citations, and newly expanded derivations. Verify both local justifications and
the global mechanism and modular structure.

A substantive missing bridge, stronger conclusion, added assumption, or
unverified repair blocks a complete proof exposition. Preserve the source
status as provenance, label the local draft appropriately, and return the exact
defect or open obligation to `$research-mathematics`; use `$destroy-theory` or
`$audit-assumptions` when the defect calls specifically for those reviews.

## 5. Write when authorized

Draft outside the target from a workpad snapshot. Publish only after the source
fidelity and reconstructibility audits pass. For an authorized file-backed
round, preserve decision-bearing mathematics and provenance in canonical
Markdown, retain only reusable noncanonical context in memory, and close under
the shared protocol.

## Return and completion

Use the smallest useful arrangement of audience contract, motivation and
mental model, exact statement, prerequisites, proof architecture, complete
proof, boundaries, status, and provenance. Let mathematical dependencies, not
a fixed template, determine the final order.

Complete only when the theorem and status match the source, the proof closes
relative to declared prerequisites, every load-bearing step or imported result
is recoverable by the target reader, the crux is more visible than routine
detail, and no mathematical repair has been smuggled into exposition.
