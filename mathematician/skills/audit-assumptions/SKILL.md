---
name: audit-assumptions
description: Audit mathematical assumptions. Use for hidden premises, proof uses, necessity witnesses, weakenings, or another skill's assumption gate.
---

# Audit Assumptions

Determine what each assumption buys. Read and apply the shared
[mathematical-integrity contract](../research-mathematics/references/mathematical-integrity.md).
This skill's rigor is assumption-local: well-posedness, use by this proof,
theorem necessity, redundancy, and successful weakening require different
certificates and never collapse into one verdict.

Default to a conversation-only report. Nested work is read-only and bound to
the supplied digest. For writable work, read the
[research-memory protocol](../research-mathematics/references/research-memory.md).

## 1. Normalize and map

Rewrite the theorem precisely. Split compound hypotheses into atomic semantic
units and include ambient conventions, definition requirements, premises
imported by results, hidden proof assumptions, boundary or convergence
qualifiers, and interpretation choices. Record implication, equivalence,
incompatibility, and jointly sufficient sets.

Link every assumption to the exact expressions, definitions, lemmas,
interchanges, existence or uniqueness claims, constants, and imported results
that use it. For each answer independently:

1. Is it needed for well-posedness?
2. Is it used by this proof?
3. Is it necessary for the theorem?
4. What evidence supports each answer?

Complete this step when every explicit and discovered assumption occurs once
in the map and every proof use is linked or marked unused.

## 2. Remove, mutate, and mine

Delete each assumption while keeping the rest fixed; test whether another
implies it; weaken it to the local property actually used; try nearby or
incomparable replacements; and inspect interacting groups and alternative
sufficient sets. Diff the resulting statement's hypotheses, conclusion,
definitions, domains, quantifiers, convergence modes, and interpretation.

At each proof use, extract the weakest local sufficient property and ask
whether approximation, localization, truncation, density, compactness,
duality, or a different route can globalize it. Build a weakening ladder rather
than jumping to a speculative endpoint.

For a material finite, randomized, symbolic, numerical, or certificate-backed
necessity search, read the shared
[computational-checking role](../research-mathematics/references/computational-checking.md)
and dispatch `falsify`. Failure to find a witness leaves theorem necessity
unresolved.

Complete this step when each assumption has a tested removal or weakening and
every remaining search has exact scope and a proposed next test.

## 3. Classify and evaluate

Classify each assumption as necessary for well-posedness, demonstrably
theorem-necessary, needed by the current proof, sufficient but nonminimal,
redundant, or unresolved. Call it technical only after a verified route removes
it.

Match each conclusion to its local certificate:

- well-posedness records the expression, object, or interpretation that fails
  without the assumption;
- proof dependence identifies every exact proof node that uses it;
- theorem necessity gives a checked witness satisfying the remaining
  hypotheses and defeating the conclusion;
- redundancy derives it from the remaining assumptions or supplies a checked
  proof that avoids it; and
- weakening states the revised theorem, affected proof nodes, semantic-fidelity
  diff, and exact new obligations.

Anything short of the corresponding certificate remains unresolved at that
level, even when another level is settled.

## Return and completion

Return a table of semantic assumption, origin, exact uses, well-posedness role,
proof dependence, theorem necessity, evidence, and candidate weakening. Add
hidden assumptions, interactions, alternative sufficient sets, certified
witnesses, relaxation portfolio, prioritized obligations, and—for nested
work—`candidate_digest` plus `requested_attacks`, even when empty. A standalone
audit recommends `$destroy-theory` for broad falsification or
`$research-mathematics` to prove a proposed relaxation.

For writable work, keep accepted assumptions and proved relaxations in
canonical Markdown and only reusable unresolved or rejected alternatives in
memory. Do not assign one truth status to the audit as a whole. Complete only
when every assumption and proof use is mapped, every necessity or redundancy
claim has its matching certificate, and every proposed relaxation has an exact
statement, evidence level, and proof obligations.
