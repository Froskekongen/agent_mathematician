---
name: explain-mathematics
description: Explain advanced mathematics to a mathematically mature reader outside the specialty while preserving its meaning and status.
disable-model-invocation: true
---

# Explain Mathematics

Make the governing idea visible without changing the mathematics. Follow the
[shared mathematical integrity](../research-mathematics/references/mathematical-integrity.md).
Develop motivation, a mental model, its exact realization, and revealing
examples before adding technical detail. A complete proof is optional unless
the request is genuinely proof-bearing.

## File handling (internal)

Default to chat. Supplying or naming a file is not authorization to change it;
files and companions remain read-only unless the user explicitly asks to
update or rewrite a named canonical target. For research history, read the
[research-memory rules](../research-mathematics/references/research-memory.md)
and query the companion read-only, describing anything retrieved as history.

An in-place rewrite authorizes only that target's Markdown/SQLite pair. A
separate explanation has its own companion and leaves the source pair
read-only; no two Markdown documents share one database. For writable work,
read the rules completely and act as sole writer.

## 1. Find the point of the mathematics

Infer the reader's relevant background from the request. Unless told otherwise,
write for a mathematically mature reader who is new to this specialty. Decide
which ideas can be assumed, which need a reminder, and which must be developed
from the beginning.

Start from the problem, obstruction, or phenomenon that calls for the new
mathematics. Explain what the central definition or construction makes possible
that was difficult to see before.

## 2. Build a mental model and realize it exactly

Give the reader a way to think about the mechanism in familiar mathematical
language. Then identify the exact objects, maps, relations, or operations that
realize that model. Use a picture or diagram when the reasoning is genuinely
visual or geometric.

An analogy should preserve a stated system of relations, not merely a surface
resemblance. Say what corresponds to what, which consequences survive the
comparison, and where it ceases to be reliable.

## 3. Let examples do mathematical work

Choose the shortest example in which the mechanism can be seen operating, then
use a boundary case or nonexample to show its limit. One example may do both.
Make the objects, assumptions, and calculation explicit enough to check, and
say what the example explains without treating it as a proof of the general
claim.

## 4. Introduce the exact statement at the right moment

Bring in definitions, conventions, and imported results when the reader can see
why they are needed. Explain the form of each important definition, and state
the main object or theorem with every qualifier that changes its meaning. Keep
proved, conjectural, incomplete, and heuristic material distinct in ordinary
prose.

Proof is optional. When the argument illuminates the mechanism, give its main
idea and explain what the major steps accomplish. Expand the crux; compress
routine work the intended reader can reconstruct.

## 5. Check the explanation against the mathematics

Check every example, analogy boundary, theorem qualifier, citation, and passage
from the mental model to the exact statement. For a substantial rewrite,
compare the account with the source theorem and proof.

For a machine-checked result, explain both the human mathematical mechanism and
the proposition represented by the formal encoding, including what the checker
verified and assumed. If a source or important step fails to check, leave the
issue unresolved and say why.

For an authorized rewrite, draft separately and replace the target only after
meaning, status, and provenance agree with the source. 

## Write the result

Write a natural mathematical explanation. Let motivation, definitions,
examples, exact statements, proof ideas, and boundaries appear where they best
support understanding. Keep file rules, database terms, checks, and routing
outside the explanation.
