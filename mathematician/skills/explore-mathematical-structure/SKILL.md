---
name: explore-mathematical-structure
description: Explore a vague mathematical idea, question, or provisional formalism through rapid contrastive tests so the user can choose promising next directions.
disable-model-invocation: true
---

# Explore Mathematical Structure

Run a **contrastive laboratory**: formalize only enough to make candidate
structures disagree, execute the cheapest useful discriminator, and turn the
result into a research choice.

Maintain two distinct outputs:

- an **exploration brief** for the human decision; and
- an **exploration ledger** as exact, reconstructible mathematical state.

## Run one tracer round

Unless the user requests a one-shot artifact or gives a larger autonomous
budget, stop after the first decision-relevant round.

### 1. Frame and contrast

Start at the user's current precision. Record a working contract containing
the mathematical job, typed objects and maps, one observable or question, one
anchor example or family, fixed choices, reversible assumptions, and live
semantic forks.

Keep two to four active candidates. They may have different roles—such as an
objective, representation, algebraic theory, mechanism, regime, construction,
or typed bundle—so compare them by what they contribute to the user's goal,
not through a false common ontology. Record only relations that affect
interpretation, testing, or allocation. Candidate records, not comparison
tables, own the mathematics. Keep selection criteria separate; aggregate
measurements only with user-approved weights.

Resolve a semantic fork locally when one shared example exposes its
consequences. If intended meaning still blocks comparison, ask one **wedge
question** whose alternatives lead to different structures, examples, or
maps.

### 2. Predict and probe

Before inspecting a decisive result when practical, state each affected
candidate's prediction, nearest competing explanation, and cheap break-test.
Prefer the smallest example, counterexample, deformation, boundary case, or
exact finite family that separates candidates. Execute the highest-information
probe first and record its exact mathematical scope and artifact risks.

Use computation, formal checking, search, or scouts only when they address the
current uncertainty. For material computation, solver work, formal checking,
or parallel scouts, read and follow the
[advanced probe protocol](references/probes-and-evidence.md).

### 3. Update and allocate

Update only dependent ledger records. Preserve the original prediction beside
a repair, and preserve informative failures with their reason and revival
condition. A non-discriminating probe still becomes evidence; only the
candidate, claim, and direction dispositions may remain unchanged.

Recommend one next direction and at most two live alternatives. Give the
cheapest decisive next test and an outcome map: what each result would select,
reject, split, park, or revive. Run another round only within the agreed budget
and when its expected decision value is clear.

A tracer is complete when one consequential contrast is better determined—or
its non-separation is diagnosed—with scoped evidence, checked artifact risk,
updated dispositions, and a next allocation.

## Keep the ledger exact

Before completing the first tracer, a multi-round exploration, a consequential
definition or claim change, a one-shot result, or a handoff, read and follow the
[canonical ledger protocol](references/exploration-ledger.md). It is the single
source of truth for record fields, status vocabularies, versioning,
invalidation, and snapshot or delta delivery.

The brief may simplify notation; the ledger retains every qualifier that can
change truth, typing, equivalence, applicability, or the research decision.
Never collapse claim scope, evidence coverage, mathematical status, evidence
kind, semantic fidelity, and workflow disposition into one field.

When any source enters the round, terminology, prior art, or novelty affects
the decision, or before major investment in an apparently new direction, read the
[literature and privacy protocol](references/literature-and-privacy.md).

## Return the brief first

Every response starts with a standalone **Exploration brief**, organized by
the user's decision rather than ledger order. It contains:

1. the current conclusion or live uncertainty and why it matters;
2. the decisive mechanism and smallest useful witness, with exact scope;
3. the live options and recommended direction; and
4. the next discriminator, its outcome map, and a wedge question when human
   meaning is the blocker.

Use a small decision table only when it reduces reading effort. Preserve every
load-bearing hypothesis, quantifier, regime, and semantic distinction, while
using plain language around the formalism. Keep an intermediate brief near 500
words and a concluding brief near 800–1,200 words unless the user requests
depth. The ledger does not count toward these limits.

Then deliver the ledger exactly as its protocol specifies. In chat, append the
snapshot or delta after the brief. For files, write `<topic>.md` and
`<topic>.exploration-ledger.md` with reciprocal links; combine them only when
the user requests one artifact. A handoff includes both.

## Boundaries and completion

This skill may use local derivations and micro-lemmas to discriminate
structures, but it does not certify an end-to-end proof. Preserve an incidental
complete argument as `CANDIDATE FULL PROOF — NOT CERTIFIED`. When comparison is
no longer the primary task, hand off: meaning to `$formalize-concepts`, proof
routes to `$explore-proof-strategies`, rigorous resolution to
`$research-mathematics`, falsification to `$destroy-theory`, or hypothesis
necessity to `$audit-assumptions`.

Complete only when every applicable canonical ledger field is present, every
reference resolves in the reconstructible state, version changes have
propagated through dependencies, and the brief alone lets the user say what was
learned, what to do next, and what would reverse that choice.
