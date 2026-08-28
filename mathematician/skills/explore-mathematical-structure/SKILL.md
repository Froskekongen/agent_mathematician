---
name: explore-mathematical-structure
description: Explore a vague mathematical idea, question, or provisional formalism through rapid contrastive tests so the user can choose promising next directions.
disable-model-invocation: true
---

# Explore Mathematical Structure

Run a **contrastive laboratory**: formalize only enough to make candidate
structures disagree, execute the cheapest useful discriminator, and turn the
result into a research choice.

The exploration brief is the authoritative result. In an authorized
file-backed round, maintain three information layers:

1. a self-contained canonical Markdown document;
2. its `<stem>.research.sqlite` companion, optional for understanding and
   containing curated noncanonical research memory; and
3. one skill-created directory under the operating system's temporary
   directory for raw round state.

Read and follow the shared
[research-memory protocol](../research-mathematics/references/research-memory.md)
before creating, reading, or updating a companion database. Use the shared
[research-memory CLI](../research-mathematics/scripts/research_memory.py) for
database access.
Chat-only and read-only runs create no files and never initialize a database.

When the primary task is to combine multiple canonical documents or theory
companions, recommend `$consolidate-math-documents` instead of treating their
contents as candidates in one exploration round.

## Run one tracer round

Unless the user requests a one-shot artifact or gives a larger autonomous
budget, stop after the first decision-relevant round.

### 1. Establish the round

Read the canonical document before its companion. In a file-backed round,
run the protocol's `ensure` preflight for the writable home pair before
creating a workpad. With no locator, let `ensure` create or validate the
default companion and add the schema-2 locator only after success. With a
locator, resolve it relative to the canonical document and require the exact
database with `--require-existing`. Stop and report a located-but-missing
companion; do not replace it or begin the round.

After successful preflight, create one temporary workpad directory and record
its exact path. Keep working contracts, candidate versions, comparisons,
predictions, raw probes, source search notes, scout reports, and superseded
drafts there—not beside the canonical document and not in SQLite.

Frame a working contract containing the mathematical job, typed objects and
maps, one observable or question, one anchor example or family, fixed choices,
reversible assumptions, and live semantic forks.

Keep two to four active candidates. They may have different roles—such as an
objective, representation, algebraic theory, mechanism, regime, construction,
or typed bundle—so compare them by what they contribute to the user's goal,
not through a false common ontology. Candidate notes own their mathematics;
keep selection criteria separate, and aggregate measurements only with
user-approved weights.

Resolve a semantic fork locally when one shared example exposes its
consequences. If intended meaning still blocks comparison, ask one **wedge
question** whose alternatives lead to different structures, examples, or
maps. Framing is complete when the candidates make distinct, checkable
predictions or the unresolved semantic choice is explicit.

### 2. Predict and probe

Before inspecting a decisive result when practical, state each affected
candidate's prediction, nearest competing explanation, and cheap break-test.
Prefer the smallest example, counterexample, deformation, boundary case, or
exact finite family that separates candidates. Execute the
highest-information probe first and record its exact mathematical scope and
artifact risks in the workpad.

Use computation, formal checking, search, or scouts only when they address the
current uncertainty. For material computation, solver work, formal checking,
or parallel scouts, read and follow the
[advanced probe protocol](references/probes-and-evidence.md).

### 3. Update and allocate

Update the affected candidate notes while retaining the original prediction
beside a repair for the duration of the round. Distinguish independently:

- a claim's quantified scope and mathematical status;
- the evidence's actual coverage, method, and semantic fidelity; and
- the direction's workflow disposition.

Reserve `refuted` for a checked counterexample to the literal claim.
`rejected` means that a research route is no longer worth current investment;
it does not assert mathematical falsity. A finite or numerical check covers
only the recorded family, and a formal checker certifies only its encoded
statement and checked correspondence.

A non-discriminating probe still affects the conclusion by documenting
non-separation, but it becomes durable only when it changes the canonical
mathematics or passes the card-retention threshold below.

Recommend one next direction and at most two live alternatives. Give the
cheapest decisive next test and an outcome map: what each result would select,
reject, split, park, or revive. Run another round only within the agreed budget
and when its expected decision value is clear.

A tracer is complete when one consequential contrast is better determined—or
its non-separation is diagnosed—with scoped evidence, checked artifact risk,
updated dispositions, and a next allocation.

## Promote, curate, and discard

Before closing a file-backed round, classify the workpad's useful content:

- **Canonical Markdown:** the selected formalism, exact current definitions
  and hypotheses, decisive evidence, load-bearing boundary examples or
  counterexamples, current recommendation, unresolved obligations that affect
  interpretation, and the next discriminator.
- **Native artifacts:** formal proof sources, certificates, programs, or
  datasets that must remain independently inspectable; link them from the
  canonical document.
- **Research-memory cards:** reusable but noncanonical open, parked, or
  rejected directions; structural obstructions; expensive probe results;
  source-applicability findings; and revival conditions that would prevent
  repeated work.
- **Discard:** routine failed manipulations, cheap screens, superseded drafts,
  raw scout chatter, and mechanical round history.

Create a card only when it offers a concrete next test, a demonstrated reason
for rejection, a useful obstruction, a realistic revival condition, or enough
cost to justify preventing repetition. Make every card's summary mathematically
self-contained. The companion may support later research, but accepted
mathematics never depends on a card and canonical prose never requires an
opaque card identifier to be understood.

This skill is the sole writer for its standalone round. It may query other
theories read-only and never ensures or creates their companions. If a foreign
card materially affects the result, follow the shared protocol's local-snapshot
and `card_origin` rules rather than creating a live cross-database dependency.

Close in this order:

1. integrate and verify the canonical document;
2. apply one curated database batch;
3. run the shared database checks and inspect every materially changed card;
4. delete only the exact skill-created temporary directory.

Retain the workpad and report its path when canonical integration, database
application, or validation fails. If only cleanup fails, report the residual
path; the completed canonical and database updates remain valid. Never perform
Git operations without separate authorization.

## Return the brief first

Every response starts with a standalone **Exploration brief**, organized by
the user's decision. It contains:

1. the current conclusion or live uncertainty and why it matters;
2. the decisive mechanism and smallest useful witness, with exact scope;
3. the live options and recommended direction; and
4. the next discriminator, its outcome map, and a wedge question when human
   meaning is the blocker.

Use a small decision table only when it reduces reading effort. Preserve every
load-bearing hypothesis, quantifier, regime, and semantic distinction while
using plain language around the formalism. Keep an intermediate brief near 500
words and a concluding brief near 800–1,200 words unless the user requests
depth.

In chat-only mode, return the brief and create no persistent artifacts. In a
file-backed round, make the canonical document self-contained and mention the
companion only as optional research memory. Do not append database dumps,
workpad records, or persistent specialist reports.

## Literature, boundaries, and completion

When any source enters the round, terminology, prior art, or novelty affects
the decision, or before major investment in an apparently new direction, read
the [literature and privacy protocol](references/literature-and-privacy.md).

This skill may use local derivations and micro-lemmas to discriminate
structures, but it does not certify an end-to-end proof. Preserve an incidental
complete argument in the returned brief for chat-only work or in the canonical
document for a file-backed round, labelled `CANDIDATE FULL PROOF — NOT
CERTIFIED`. Database persistence never upgrades a mathematical status.

When comparison is no longer the primary task, hand off: meaning to
`$formalize-concepts`, proof routes to `$explore-proof-strategies`, rigorous
resolution to `$research-mathematics`, falsification to `$destroy-theory`, or
hypothesis necessity to `$audit-assumptions`.

Complete only when the brief supports a research decision, the canonical
document is mathematically self-contained, every durable noncanonical item
passes the card-retention threshold, validations succeed, and the temporary
workpad has either been deleted or reported for recovery.
