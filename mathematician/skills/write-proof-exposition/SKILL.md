---
name: write-proof-exposition
description: Turn an established proof into a self-contained account that a mathematician outside the specialty can follow, without changing the result.
disable-model-invocation: true
---

# Write Proof Exposition

Turn an established proof into an account that a mathematically mature reader
outside the specialty can follow and reconstruct. Follow the
[shared mathematical integrity](../research-mathematics/references/mathematical-integrity.md).
The exposition keeps the source result's mathematical status; it does not prove,
repair, or strengthen the result.

Use `$explain-mathematics` when intuitive understanding is primary and a
complete proof is unnecessary. Use `$research-mathematics` when an essential
argument must be invented, repaired, challenged, or certified.

## File handling (internal)

Default to chat; source files and companions remain read-only unless the user
explicitly asks to update or rewrite a named canonical target. Merely supplying
or naming one is not authorization. For research history, read the
[research-memory rules](../research-mathematics/references/research-memory.md),
query the companion read-only, and label the result as history.

An in-place request authorizes only that target's Markdown/SQLite pair. An
explicitly requested separate proof exposition gets its own companion and
leaves the source pair read-only; no two Markdown documents share one database.
For writable work, read the rules completely and act as sole writer.

## 1. Fix the source and the reader

Identify the exact theorem, definitions, assumptions, conventions, current
status, proof or certificate, imported results, known limits, and provenance.
Distinguish a complete proof from a proof sketch, an incomplete argument, or a
citation that has not been checked here.

Infer the reader's relevant background. Decide which prerequisites can be
assumed, briefly recalled, developed here, or cited. “Self-contained” means
complete relative to that stated background, not free of every dependency.

If an essential argument is missing, preserve the source's lower status and
recommend `$research-mathematics` rather than silently adding new research.

## 2. Explain the idea before the details

Begin with the problem, the governing mental picture, the main mechanism, and
the proof's hardest idea. Then divide the argument into a small number of
mathematical stages and say what each stage accomplishes. Connect this overview
to the exact theorem so the picture remains useful once the proof becomes
formal.

Use examples, diagrams, or analogies when they reveal the mechanism. Identify
the exact objects they describe, what structure they preserve, and where the
comparison breaks. Compress routine details only when the intended reader can
reconstruct them and they do not hide the central idea.

## 3. Write a proof the reader can reconstruct

Present definitions and imported results before use. For each nonroutine step,
explain what it accomplishes and where the idea comes from. Show every essential
inference, or cite an exact theorem after checking its assumptions and
conventions. Expand specialist shorthand around the crux; compress only work
the target reader can reliably recover.

Keep the mathematical statement, its proof, and any formal or executable
encoding distinct. For a machine-checked source, explain what the checker
verified and what it assumes, while reconstructing the human mathematical idea.
The readable reconstruction supplements the certificate; it does not replace it.

## 4. Compare the exposition with the source

Compare the source and exposition: theorem statement, definitions, assumptions,
quantifiers, conventions, imported results, validity limits, provenance, and
status must agree. Check examples, diagrams, formulas, citations, and any
details expanded during the rewrite. Read the proof once locally, step by step,
and once globally, for the main idea and flow.

If the rewrite reveals a missing bridge, stronger conclusion, added assumption,
or unverified repair, do not present the draft as a complete proof. State the
problem plainly and return it to `$research-mathematics`; use `$destroy-theory`
or `$audit-assumptions` when the issue specifically calls for those reviews.

## 5. Publish a readable account when authorized

Draft separately from the target and publish only after the comparison with the
source succeeds. For authorized file-backed work, keep the mathematics and
provenance in canonical Markdown, retain only reusable background in memory,
and finish under the shared research-memory rules.

## Completion

Write mathematics, not an audit report. Let the argument determine the order,
but normally move from motivation and mental picture to the exact statement,
needed prerequisites, proof idea, complete proof, and meaningful boundaries.
Put status and provenance in a compact note when they matter. Keep file rules,
review checklists, and internal routing out of the exposition.

Complete only when the theorem and status match the source, the proof closes
relative to the stated prerequisites, every essential step or imported result
is recoverable by the target reader, the central idea is more visible than the
routine detail, and the exposition introduces no unverified mathematical change.
