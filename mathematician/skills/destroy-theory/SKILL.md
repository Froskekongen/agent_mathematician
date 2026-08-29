---
name: destroy-theory
description: Find counterexamples, proof gaps, failed encodings, or validity boundaries, including when another skill needs a fresh adversarial review.
---

# Destroy Theory

Try to break the claim, proof, or encoding. Follow the
[shared mathematical integrity](../research-mathematics/references/mathematical-integrity.md).
A negative conclusion needs exact evidence: a checked counterexample,
contradiction, or invalid inference. A search that finds nothing reports only
where it searched.

Default to a conversation-only result. A nested run examines the supplied
candidate digest read-only. For authorized writable work, first read the
[research-memory rules](../research-mathematics/references/research-memory.md)
and remain the sole writer.

## 1. State the claim and its negation

Separate definitions, assumptions, lemmas, principal claims, and consequences.
Type-check every object and write the exact logical negation of each principal
claim. Distinguish literal wording from intended meaning and flag any repaired
definition, added assumption, restricted domain, or changed quantifier as a
new target.

Complete this step when every claim being tested has a precise statement, a
clear place in the argument, and an exact negation.

## 2. Try the cheapest counterexamples first

Prioritize important universal, existence, uniqueness, boundary, closure,
inversion, interchange, uniformity, and finite-to-infinite claims. Adapt the
following families rather than applying them mechanically: zero and constant
objects; the smallest dimensions; finite, discrete, linear, or diagonal
models; degenerate and boundary cases; scaling and symmetry mutations;
minimally regular objects; loss of compactness; noncommutativity; and infinite
dimension.

When material computation is needed, read
[computational-checking.md](../research-mathematics/references/computational-checking.md)
and use `falsify`. Record what candidates were searched, how many, under what
budget, and where the search stopped. Treat a candidate as a counterexample only
after checking it exactly.

Complete this step when every important claim has received at least one attack
suited to its mathematics, or when the unsearched territory is clear.

## 3. Inspect the proof and encoding

Locate the earliest unsupported inference. Check quantifier or domain changes,
circularity, well-posedness, operation interchanges, topology, exceptional
sets, uniform constants, imported hypotheses, finite-dimensional leakage,
conclusion strength, hidden premises, and renamed central obligations. Check
an executable encoding separately from the intended theorem and its proof.

Keep four outcomes distinct: the claim is false, this proof fails, the encoding
fails to represent or establish the claim, or no defect was found in the tested
scope. Record systematic questions about weaker assumptions for
`$audit-assumptions`; a nested run does not launch it.

## 4. Check and simplify the finding

A counterexample must define the object, verify every assumption, and show that
the conclusion fails. Identify the first claim it defeats and distinguish the
checked argument from any heuristic lead. Simplify the example when that makes
the true boundary easier to see. Suggest the nearest natural correction and say
what would still need proof; the corrected statement is a new claim.

## Write the result

Lead with the mathematical outcome. If the claim fails, present the smallest
clear counterexample or contradiction and explain the boundary it reveals. If
only the proof or encoding fails, identify the first bad step and explain why it
does not settle the theorem. If nothing fails, summarize the strongest tests and
the important territory left unexplored.

For nested work, append the internal fields `candidate_digest` and
`requested_assumption_audits`, even when empty; keep them out of the mathematical
narrative. Standalone work recommends `$audit-assumptions` for systematic
weakenings or `$research-mathematics` to resolve a corrected claim.

Only a checked counterexample or contradiction proves `REFUTED`. A broken proof
leaves the theorem unresolved unless other evidence settles it; a broken
encoding says only that the implementation fails. Otherwise report
`NOT FALSIFIED IN SCOPE`, say what was tested, and name the main remaining ways
the claim could fail. Difficulty understanding a step is a reason to investigate
it, not evidence that the step is wrong.

For writable work, place checked counterexamples and accepted boundaries where
they clarify the mathematics. Keep reusable obstructions, expensive negative
searches, and untried attacks in memory. Do not turn the canonical document into
an attack log. Complete when every reported counterexample is checked, every
claimed proof defect identifies the invalid or unsupported inference, and the
limits of the search are clear.
