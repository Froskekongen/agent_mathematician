---
name: audit-assumptions
description: Audit mathematical assumptions for well-posedness, proof use, necessity, or weakening, including a fresh review requested by another skill.
---

# Audit Assumptions

Determine what each hypothesis contributes. Follow the
[shared mathematical integrity](../research-mathematics/references/mathematical-integrity.md).
Keep three questions separate: does the assumption make the statement
meaningful, does the present proof use it, and is it necessary for the theorem
to be true? These questions need different evidence.

Default to chat. Nested work is read-only and tied to the supplied digest. For
authorized writable work, read the
[research-memory rules](../research-mathematics/references/research-memory.md)
and act as sole writer.

## 1. Fix the theorem and its dependencies

State the theorem precisely and split compound hypotheses into their
mathematical parts. Include ambient conventions, conditions required by the
definitions, assumptions imported through other results, hidden proof
premises, and boundary or convergence conditions. Record implications,
incompatibilities, and hypotheses that matter only in combination.

Trace each assumption through the argument. Identify the objects it makes
well-defined and the lemmas, interchanges, existence or uniqueness statements,
constants, or imported results that use it. Mark a hypothesis unused when no
such dependence exists; that is a statement about this proof, not yet about the
theorem.

The dependency map is complete when every explicit and hidden assumption
appears once and every proof use points back to it.

## 2. Remove and weaken carefully

For each assumption, remove it while holding the others fixed and state the
resulting theorem exactly. Check first whether the remaining hypotheses already
imply it. Then identify the weakest local property needed at each proof use and
ask whether that property follows under a natural weakening or through a
different argument. Test interacting hypotheses together when removing them
separately misses the real dependence.

Every variant must say what changed in the objects, definitions, domain,
quantifiers, hypotheses, conclusion, convergence, or interpretation. Move
through understandable intermediate weakenings rather than jumping to a final
statement with no supporting argument.

When a material finite, randomized, symbolic, numerical, or certificate-backed
search bears on the question, read
[computational-checking.md](../research-mathematics/references/computational-checking.md)
and use `falsify`. An unsuccessful counterexample search establishes only its
reported scope.

## 3. Match each conclusion to its evidence

An assumption is needed for well-posedness when removing it leaves a named
object, expression, or interpretation undefined. It is used by the proof when
an exact inference or imported result depends on it. Neither conclusion shows
that the theorem itself needs the assumption.

Necessity for the theorem requires a checked example satisfying the other
hypotheses and violating the conclusion. Redundancy requires a derivation from
the remaining assumptions or a checked proof of the unchanged conclusion that
does not use it. A successful weakening requires the revised theorem and a
proof that closes under its weaker hypotheses. State any remaining proof step
instead of presenting the weakening as established.

Call an assumption merely technical only after a checked argument removes it.
When the relevant evidence is absent, leave that question unresolved even if
the other two questions have answers.

Report each hypothesis according to what is established: part of the
well-posed setting, used by the present proof, necessary for the theorem,
stronger than needed, redundant, or unresolved. Several descriptions may apply
to the same hypothesis.

## Write the result

Lead with the mathematical lesson: which hypotheses define the setting, which
drive the proof, which are known to be necessary, and where a cleaner theorem
may lie. A compact table may compare an assumption, its origin and proof uses,
what is known about necessity, the evidence, and a possible weakening. Explain
important interactions and counterexamples in prose.

For nested work, append the internal fields `candidate_digest` and
`requested_attacks`, even when empty, without weaving them into the
mathematical discussion. A standalone audit may recommend `$destroy-theory`
for broader counterexample search or `$research-mathematics` to prove a
proposed weakening.

For writable work, place accepted assumptions and proved weakenings beside the
theorem or proof they clarify. The canonical document presents the mathematical
conclusions and their arguments; keep reusable unresolved directions and review
bookkeeping in memory.

Finish when every assumption and proof use is traced, every assumption has been
tested by removal or weakening, every conclusion about necessity or redundancy
has the evidence it requires, and every proposed weakening has an exact
statement and explicit remaining proof work. Give the scope and next test for
any unfinished search.
