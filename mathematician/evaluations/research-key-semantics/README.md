# Research-key semantics evaluation

This corpus checks whether every mathematical skill applies the shared
research-key contract by subject identity rather than by report shape. It is a
behavioral evaluation: lowercase-kebab syntax alone does not pass.

## Protocol

For each scenario in `prompts.md`, use a fresh workspace and the named skill.
Run the base request, archive read-only copies of its response, canonical pair,
and `check` result, then run the metamorphic follow-up in the same workspace.
Give a fresh grader both persisted states and `answer-key.md`, but do not expose
the answer key to the solver. Run each S7 branch check from an independent copy
of its stated fixture.

File-backed skills must finish with a current Markdown/SQLite pair. A chat-only
run must create neither file. `formalize-concepts` must perform no database
work: its handoff may contain a proposed key, but the receiving writer owns the
authoritative allocation decision.

## Pass condition

A scenario passes only when all applicable checks pass:

- keys identify durable mathematical subjects and remain stable when only
  order, heading, recommendation, or claim status changes;
- summaries, navigation, report roles, and aggregate decisions remain
  unindexed unless they independently name a durable subject;
- one key identifies one subject, with no aliases after a correction, split,
  or merge;
- every writable result is self-contained and its companion reports `current`;
- S7 respects explicit write authorization, pair ownership, and the
  no-publication fidelity gate;
- every retained card or artifact link resolves to the intended subject;
- `formalize-concepts` proposes rather than allocates a document key and does
  not touch SQLite.

Record the keys before and after, database revisions, `check` output, and any
card/artifact link changes. A single semantic-identity or ownership failure
fails the scenario.
