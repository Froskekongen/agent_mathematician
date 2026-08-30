---
name: destroy-theory
description: Attack mathematical claims, proofs, and encodings by finding checked counterexamples, invalid inferences, or validity boundaries, including a fresh review requested by another skill.
---

# Destroy Theory

Try to break the exact claim, proof, or encoding. Follow the
[shared mathematical integrity](../research-mathematics/references/mathematical-integrity.md).
A negative conclusion needs exact evidence: a checked counterexample,
contradiction, or invalid inference. An unsuccessful search reports where it
looked and nothing stronger.

Default to chat. A nested run examines the supplied candidate digest read-only.
For authorized writable work, read the
[research-memory rules](../research-mathematics/references/research-memory.md)
and act as sole writer.

## 1. Fix the target and its negation

Separate definitions, assumptions, lemmas, principal claims, and consequences.
Type-check the objects and write the exact logical negation of every principal
claim under attack. Keep literal wording distinct from intended meaning. A
repaired definition, added assumption, restricted domain, or changed quantifier
creates a new target.

Begin attacking only when the claim has a precise statement, a known place in
the argument, and an exact negation.

## 2. Let the logical form choose the attack

A universal assertion asks for one object satisfying the hypotheses and
violating the conclusion. Uniqueness asks for two admissible objects that the
claim identifies incorrectly. An implication asks for its hypotheses together
with the failure of its conclusion; an equivalence can fail in either
direction. An existence theorem instead calls for an obstruction or a proof
that no admissible object can exist.

Search first in the smallest setting that still carries the proposed
mechanism. Zero or constant objects, low dimensions, diagonal or finite models,
boundary regularity, a scaling limit, or loss of compactness are useful only
when they stress a specific inference. Let the mathematics of the claim choose
the family.

When material computation is needed, read
[computational-checking.md](../research-mathematics/references/computational-checking.md)
and use `falsify`. Record the encoded proposition, candidate family, budget,
and stopping point. A computational candidate becomes a counterexample only
after every hypothesis and the failed conclusion have been checked exactly.

Continue until every important claim has received an attack suited to its
logical and mathematical form, or the main unsearched territory is explicit.

## 3. Inspect the proof and the encoding separately

Locate the earliest unsupported inference. Check changes of domain or
quantifier, well-posedness, circularity, operation interchanges, exceptional
sets, topology, uniform constants, imported hypotheses, finite-dimensional
reasoning used in an infinite-dimensional setting, and conclusions stronger
than the lemmas support. A renamed or hidden central obligation remains an open
obligation. Opacity is a reason to inspect a step, not evidence that it is
false.

An executable encoding is a third object beside the theorem and its proof.
Check whether it represents the intended statement and whether its output
establishes the proposition claimed for it.

Keep four outcomes distinct: the theorem is false, this proof fails, the
encoding fails to represent or establish the theorem, or no defect was found in
the tested scope. Record systematic questions about weaker assumptions for
`$audit-assumptions`; a nested run does not launch it.

## 4. Check and simplify the finding

A counterexample must define the object, verify every hypothesis, and show
that the conclusion fails. Identify the first claim it defeats and separate
the checked argument from the heuristic that suggested it. Simplify the example
when a smaller one makes the true boundary easier to understand.

If a natural correction becomes visible, state it as a new claim and name what
would still need proof. A broken proof or encoding does not by itself repair or
settle the theorem.

## Write the result

Lead with the mathematical outcome. For a false claim, present the smallest
clear counterexample or contradiction and the boundary it reveals. For a proof
or encoding failure, identify the first bad step and explain why the theorem
remains unresolved. If no attack succeeds, summarize the strongest tests and
the important territory left open.

For nested work, append the internal fields `candidate_digest` and
`requested_assumption_audits`, even when empty, outside the mathematical
narrative. Standalone work may recommend `$audit-assumptions` for systematic
weakening or `$research-mathematics` for a corrected claim.

Only a checked counterexample or contradiction proves `REFUTED`. A broken
proof leaves the theorem unresolved unless other evidence settles it, and a
broken encoding settles only the implementation. Otherwise report
`NOT FALSIFIED IN SCOPE`, state what was tested, and name the main remaining
ways the claim could fail.

For writable work, place checked counterexamples and accepted boundaries where
they clarify the mathematics. Keep reusable obstructions, unfinished search
directions, and review bookkeeping in memory. Finish when every reported
counterexample and proof defect is checked and the limits of the search are
clear.
