---
name: explain-mathematics
description: Explain advanced mathematics to a mature nonspecialist without changing its meaning or status.
disable-model-invocation: true
---

# Explain Mathematics

Help the reader see why the mathematics works, not merely what its formal
statements say. Follow the
[shared mathematical integrity](../research-mathematics/references/mathematical-integrity.md).
Preserve the exact mathematics and its current status, but optimize for
motivation, mental models, examples, and mechanism. A complete proof is optional
unless the request is genuinely proof-bearing.

## File handling (internal)

Default to chat. Supplying or naming a file is not authorization to change it;
files and companions remain read-only unless the user explicitly asks to update
or rewrite a named canonical target. For research history, read the
[research-memory rules](../research-mathematics/references/research-memory.md),
query the companion read-only, and describe the result as history.

An in-place request authorizes only that target's Markdown/SQLite pair. A
separate explanation has its own companion and leaves the source pair read-only;
no two Markdown documents share one database. For writable work, read the
rules completely and act as sole writer.

## 1. Know the reader

Infer the reader's relevant background from the request. Unless told otherwise,
write for a mathematically mature reader who is new to this specialty. Decide
what can be assumed, what needs a short reminder, and what must be developed
here.

## 2. Start with the point and a picture

Begin with the problem, obstruction, or phenomenon that makes the mathematics
worth studying. Give a mental picture in language or mathematics the reader
already knows. Then say which exact objects and relations the picture represents.
For an analogy, explain what carries over and where it breaks.

Move from motivation to mechanism before giving the most abstract formulation.
A useful order is: the problem, the new structure, how it resolves the problem,
an informal result, and then the exact statement.

## 3. Connect the picture to the exact mathematics

Introduce definitions, conventions, constructions, and imported results before
they are used. Explain why each important definition has the form it does.
State the main object or theorem with every qualifier that changes its meaning.
Keep proved, conjectural, incomplete, and merely suggested material distinct,
using natural prose rather than repeated status labels.

## 4. Make the mechanism visible in examples

Choose the shortest examples that make the central mechanism work and reveal a
useful boundary. Usually one small example and one boundary case or nonexample
are enough; one example may do both jobs. Add more only when they teach
something genuinely different.

For each example, make the objects, assumptions, and calculation clear, then
say what the example teaches and what it does not prove.

## 5. Add proof only where it helps

If the proof explains the mechanism, give its main idea and show what each major
step accomplishes. Spend detail on the crux and compress routine work that this
reader can reconstruct. If a complete cross-specialty proof is needed,
recommend `$write-proof-exposition`.

## 6. Check the mathematics and write naturally

Check every important example, analogy boundary, citation, theorem qualifier,
and move from the mental picture to the exact mathematics. Compare a substantial
rewrite with the source theorem and proof when available.

For a machine-checked result, explain the human mathematical idea and state
what the formal encoding actually says, what the checker verified, and what it
assumes. If an important step or source does not check out, say so plainly and
keep the issue unresolved. Recommend `$destroy-theory` for a possible defect,
`$audit-assumptions` for a question about necessity, or `$research-mathematics`
for repair or certification.

For an authorized rewrite, draft separately and compare the final account with
the source before replacing it. Preserve meaning, status, and provenance. If a
faithful explanation would require new mathematics, leave the source unchanged
and hand that work to the appropriate research skill.

## Completion

Write a natural mathematical explanation, not a visible audit trail. Do not
force fixed headings. Lead with motivation and the governing idea; place
definitions, examples, exact statements, proof ideas, and boundaries where they
best support understanding. Keep file rules, database terms, internal checks,
and routing notes out of the explanation.

Complete when the reader can say what the main objects are, why the definitions
are natural, how the mechanism works in a checked example, where the picture
breaks, and which parts are intuition versus proof. Give proof detail only to
the depth promised by the request.
