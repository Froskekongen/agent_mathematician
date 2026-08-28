---
name: destroy-theory
description: Falsify or stress-test a mathematical statement, proof, or theory. Use when asked to destroy, attack, red-team, referee, find counterexamples or gaps, test consistency or claimed generality, or locate the exact boundary where a claim fails.
disable-model-invocation: true
---

# Destroy Theory

Act as a hostile referee in service of truth. Read and apply the shared
[rigor chain](../research-mathematics/references/rigor.md). Survival is scoped
evidence, never proof.

Default to a conversation-only report. A nested run attacks the supplied
candidate digest read-only. For an authorized writable theory, first read the
[research-memory protocol](../research-mathematics/references/research-memory.md)
and remain the sole writer.

## 1. Freeze and negate

Separate definitions, assumptions, lemmas, principal claims, and consequences.
Type-check every object and write the exact logical negation of each principal
claim. Distinguish literal wording from intended meaning and flag any repaired
definition, added assumption, restricted domain, or changed quantifier as a
new target.

Complete this step when every attack target has a precise statement,
dependency position, and negation.

## 2. Run the cheap-refute funnel

Prioritize load-bearing universal, existence, uniqueness, boundary, closure,
inversion, interchange, uniformity, and finite-to-infinite claims. Adapt the
following families rather than applying them mechanically: zero and constant
objects; the smallest dimensions; finite, discrete, linear, or diagonal
models; degenerate and boundary cases; scaling and symmetry mutations;
minimally regular objects; loss of compactness; noncommutativity; and infinite
dimension.

When material computation is needed, read the shared
[computational-checking role](../research-mathematics/references/computational-checking.md)
and dispatch `falsify`. Report the candidate universe, denominator, budget,
stopping rule, and exact coverage. Promote only a checked witness.

Complete this step when every load-bearing claim has received at least one
adapted attack or the unsearched territory is explicit.

## 3. Attack the proof and encoding

Locate the earliest unsupported inference. Check quantifier or domain changes,
circularity, well-posedness, operation interchanges, topology, exceptional
sets, uniform constants, imported hypotheses, finite-dimensional leakage,
conclusion strength, hidden premises, and renamed central obligations. Check
an executable encoding separately from the intended theorem and its proof.

Classify every finding as target defeated, proof defeated, encoding defeated,
or not falsified within scope.

## 4. Certify, minimize, and repair

A reported counterexample must define the object, verify every hypothesis,
prove the exact conclusion failure, identify the first defeated claim, and
separate exact evidence from heuristic leads. Minimize it when that clarifies
the boundary. Propose the nearest natural correction and list the obligations
it creates; a repair is a new target rather than a victory over the original.

## Return and completion

Return the frozen target and negation, dependency and attack maps, certified
witnesses or proof defects, exact validity boundary, candidate repairs,
residual attack surface, search scope, and one shared truth status. Use finding
types such as inconsistent assumptions, proof invalid, overstated claim, or
survived within scope without inventing another status vocabulary. A certified
counterexample or contradiction gives `REFUTED`; a proof defect or survived
attack alone leaves the theorem `UNRESOLVED`.

For writable work, preserve certified failures and accepted boundaries in
canonical Markdown; retain only reusable obstructions, expensive negative
searches, and residual attacks in memory. Complete only when every witness is
certified and every unsearched or unresolved region is visible.
