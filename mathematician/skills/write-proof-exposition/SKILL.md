---
name: write-proof-exposition
description: Reconstruct an established proof as a self-contained mathematical account for readers outside the specialty, without changing the result.
disable-model-invocation: true
---

# Write Proof Exposition

Reconstruct an established proof for a mathematically mature reader outside the
specialty. The reader should be able to follow the argument and recover every
essential step. Follow the
[shared mathematical integrity](../research-mathematics/references/mathematical-integrity.md).
The exposition keeps the source result's mathematical status; it does not
prove, repair, or strengthen the result.

Use `$explain-mathematics` when intuitive understanding is primary and a
complete proof is unnecessary. Use `$research-mathematics` when an essential
argument must be invented, repaired, challenged, or certified.

## File handling (internal)

Default to chat. Merely supplying or naming a file is not authorization to
change it; source files and companions remain read-only unless the user asks to
update or rewrite a named canonical target. For research history, read the
[research-memory rules](../research-mathematics/references/research-memory.md)
and query the companion read-only, describing anything retrieved as history.

An in-place rewrite authorizes only that target's Markdown/SQLite pair. A
separate proof exposition has its own companion and leaves the source pair
read-only; no two Markdown documents share one database. For writable work,
read the rules completely and act as sole writer.

## 1. Fix the source and the intended reader

Identify the exact theorem, definitions, assumptions, conventions, current
status, proof or certificate, imported results, validity limits, and
provenance. A proof sketch, incomplete argument, or unchecked citation remains
such; exposition cannot promote it to a complete proof.

Infer the reader's relevant background. Decide which prerequisites may be
assumed, briefly recalled, developed, or cited. Self-contained means complete
relative to that stated background, not free of every dependency.

If an essential argument is absent, preserve the lower status and return the
mathematical problem to `$research-mathematics`.

## 2. Reveal the architecture of the proof

Begin with the problem, the mechanism that makes the theorem plausible, and
the hardest idea. Divide the proof into a few mathematical stages and explain
what each stage accomplishes: what obstacle it removes, what new object it
constructs, or what reduction it makes possible. Connect this architecture to
the exact theorem before entering technical detail.

Use an example, analogy, or diagram when it reveals the mechanism. Identify
the objects and relations involved, the structure preserved, and the point
where the model stops being reliable.

## 3. Reconstruct the argument locally

Introduce definitions and imported results before they do work. For each
nonroutine step, explain its mathematical task, why the move is natural at that
point, which hypotheses it uses, and how it advances the global argument.
Expand specialist shorthand around the crux.

Show every essential inference, or cite an exact theorem after matching its
assumptions and conventions to the present setting. Compress routine work only
when the intended reader can reliably recover it and the compression does not
hide the central idea.

Keep the theorem, its proof, and any formal or executable encoding distinct.
For a machine-checked source, state what the checker verified and assumed while
reconstructing the human mathematical argument. The exposition supplements the
certificate; it does not replace it.

## 4. Compare the reconstruction with the source

Read the draft once locally, checking each inference and imported result, and
once globally, checking the architecture and flow. Then compare it with the
source. The theorem statement, definitions, assumptions, quantifiers,
conventions, dependencies, validity limits, status, and provenance must agree;
check every example, formula, diagram, and citation added during the rewrite.

A missing bridge, stronger conclusion, added assumption, or unverified repair
means the draft is not a complete exposition of the source proof. State the
discrepancy and return it to `$research-mathematics`; use `$destroy-theory` or
`$audit-assumptions` when the issue specifically calls for those reviews.

## 5. Write and publish the account

Let the argument determine the order. A natural account usually moves from
motivation and proof architecture to the exact statement, prerequisites,
proof, and meaningful boundaries. Keep status and provenance compact, and keep
file rules, review mechanics, and internal routing outside the exposition.

For authorized file-backed work, draft separately and publish only after the
source comparison succeeds. Keep the mathematics and provenance in canonical
Markdown, retain only reusable background in memory, and finish under the
research-memory rules.

Finish only when the theorem and status match the source, the proof closes
relative to the stated prerequisites, every essential step or imported result
is recoverable by the target reader, the central idea remains visible through
the technical detail, and the exposition contains no unverified mathematical
change.
