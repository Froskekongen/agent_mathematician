---
name: audit-assumptions
description: Trace what mathematical assumptions do and whether they are needed for the statement, the proof, or the theorem, including when another skill needs a fresh assumption review.
---

# Audit Assumptions

Find out what each assumption is doing. Follow the
[shared mathematical integrity](../research-mathematics/references/mathematical-integrity.md).
Keep three questions separate: Is the assumption needed to make the statement
meaningful? Is it used by this proof? Is it genuinely needed for the theorem to
be true? These questions need different evidence.

Default to a conversation-only result. Nested work is read-only and tied to the
supplied digest. For writable work, read the
[research-memory rules](../research-mathematics/references/research-memory.md).

## 1. State the theorem and trace each assumption

Write the theorem precisely. Split compound hypotheses into individual
assumptions. Include ambient conventions, conditions needed by definitions,
assumptions imported through cited results, hidden proof premises, boundary or
convergence conditions, and choices of interpretation. Note when assumptions
imply, contradict, or work only in combination with one another.

Trace each assumption through the proof: identify the definitions, lemmas,
interchanges, existence or uniqueness claims, constants, and imported results
that use it. Ask separately:

1. Is it needed for well-posedness?
2. Is it used by this proof?
3. Is it necessary for the theorem?
4. What evidence supports each answer?

Complete this step when every explicit or hidden assumption appears once in the
map and every proof use is linked or marked unused.

## 2. Try removing or weakening assumptions

Remove each assumption while keeping the others fixed. Check whether another
assumption already implies it. Replace it with the weaker local property the
proof actually uses, and try natural alternatives. Also inspect groups of
assumptions that work together. For every changed theorem, state clearly how
its hypotheses, conclusion, definitions, domains, quantifiers, convergence, or
interpretation differ from the original.

At each proof use, identify the weakest local property that would suffice. Ask
whether approximation, localization, truncation, density, compactness, duality,
or a different proof can extend that local property to the full theorem. Weaken
assumptions in understandable steps rather than jumping to a speculative final
version.

For a material finite, randomized, symbolic, numerical, or certificate-backed
search, read
[computational-checking.md](../research-mathematics/references/computational-checking.md)
and use `falsify`. Failure to find a counterexample does not show that the
assumption is necessary.

Complete this step when each assumption has a tested removal or weakening and
every remaining search has exact scope and a proposed next test.

## 3. Say what each assumption contributes

For each assumption, say whether it is needed to state the problem, needed by
the current proof, known to be necessary for the theorem, stronger than needed,
redundant, or still unresolved. Call an assumption merely technical only after
a checked proof removes it.

Use the right evidence for each conclusion:

- To show that an assumption is needed for the statement to make sense, identify
  the expression, object, or interpretation that fails without it.
- To show that the present proof needs it, identify the exact steps that use it.
- To show that the theorem needs it, give a checked example satisfying the
  other assumptions but violating the conclusion.
- To show that it is redundant, derive it from the other assumptions or give a
  checked proof that avoids it.
- For a weakening, state the revised theorem, the proof steps it changes, and
  what remains to be proved.

If the required evidence is missing, leave that particular question unresolved
even if the other questions have answers.

## Write the result

Lead with the mathematical lesson: which assumptions express the setting,
which drive the proof, which appear genuinely necessary, and where a cleaner
theorem may be possible. Use a compact table when it makes the comparison easier
to see, with columns for the assumption, where it comes from, where it is used,
what is known about necessity, the supporting evidence, and a possible
weakening. Explain important interactions and counterexamples in prose.

For nested work, append the internal fields `candidate_digest` and
`requested_attacks`, even when empty; do not weave them into the mathematical
discussion. A standalone audit recommends `$destroy-theory` for broader
counterexample search or `$research-mathematics` to prove a proposed weakening.

For writable work, place accepted assumptions and proved weakenings near the
theorem or proof they clarify. Keep only reusable unresolved or rejected ideas
in memory. Do not turn the canonical document into an audit ledger. Complete
when every assumption and proof use is traced, every claim of necessity or
redundancy has the right evidence, and every proposed weakening has an exact
statement and clear remaining proof work.
