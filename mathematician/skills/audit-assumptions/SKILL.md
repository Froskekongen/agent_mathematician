---
name: audit-assumptions
description: Audit hypotheses in a mathematical theorem, proof, or theory. Use when identifying hidden, missing, implied, or redundant assumptions; locating their exact proof uses; testing necessity; or proposing and validating weaker assumptions and alternative hypothesis sets.
disable-model-invocation: true
---

# Audit Assumptions

Determine what each assumption actually buys. Keep four questions separate: well-posedness, use by the current proof, necessity for the theorem, and evidence for that necessity.

Read the shared [rigor standards](../research-mathematics/references/rigor-standards.md) before acting.

## Execution role and research state

Choose the role before auditing:

- **Nested research specialist:** audit the exact frozen candidate and digest supplied by the coordinator. Begin with a cold pass over that candidate alone. Afterwards, research-memory databases may be queried read-only for known relaxations or witnesses, and every imported finding must be marked. Perform cheap local removal tests, but do not invoke another `destroy-theory` worker. Return uncovered attacks as `requested_attacks` for the coordinator. Do not modify the candidate, canonical document, home database, foreign databases, or other theory artifacts.
- **Standalone report-only:** inspect the supplied theorem and answer in the conversation without changing the filesystem. A constrained `$destroy-theory` pass may be used for necessity witnesses, but both skills remain report-only.
- **Standalone writable theory round:** use this role only when the user has authorized changes to a file-backed theory workspace. Own one canonical document and one home research-memory database, open every foreign theory database read-only, and use one OS-temporary workpad. A constrained `destroy-theory` pass remains read-only and reports back to this coordinator.

Default to report-only when writable authority or a home theory is absent. Before any nested or standalone writable use of research memory, read the shared [research-memory protocol](../research-mathematics/references/research-memory.md) and use its [CLI](../research-mathematics/scripts/research_memory.py).

## 1. Normalize assumptions

Rewrite the theorem precisely and split compound hypotheses into atomic assumptions with stable identifiers. Include:

- ambient structures and conventions;
- definitional and well-posedness requirements;
- explicit theorem hypotheses;
- assumptions imported by external results;
- hidden assumptions introduced by the proof;
- boundary, dimensional, stochastic, and convergence qualifiers;
- interpretation and formalization choices, including fixed versus evolvable quantities;
- conventions and premises imported from cited sources.

Record implication, equivalence, incompatibility, and joint-sufficiency relationships in a transient assumption map. Complete this phase when every stated or discovered assumption appears exactly once in that map.

Freeze the original theorem in the returned report or temporary workpad before mutation. For every proposed relaxation, record a diff of hypotheses, conclusion, definitions, domains, quantifiers, convergence modes, and intended interpretation so that deleting one assumption cannot silently weaken or change something else.

## 2. Map exact uses

Link each assumption to the precise definitions, expressions, lemmas, proof steps, interchanges, existence or uniqueness results, constants, and external theorems that use it. Also inspect each proof step for assumptions absent from the statement.

For every assumption, answer independently:

1. Is it needed for the statement to be well-defined?
2. Is it used by the current proof?
3. Is it necessary for the theorem itself?
4. What evidence supports the answer?

Mark unused assumptions. Proof use establishes proof dependence, not theorem-level necessity.

## 3. Run removal and mutation tests

For each assumption `Ai`:

- delete it while retaining the others;
- check whether another assumption already implies it;
- weaken it to the local property the proof actually uses;
- replace it with a nearby or incomparable condition;
- test relevant reversals or strengthened conclusions;
- examine interacting groups and alternative sufficient sets, prioritizing assumptions that feed the same proof node;
- mutate interpretation or formalization choices and test whether the theorem becomes vacuous, trivial, or a different question.

In standalone mode, apply `$destroy-theory` in constrained mode to search for necessity witnesses. If skill-to-skill invocation is unavailable, read and execute [the sibling skill](../destroy-theory/SKILL.md) in constrained mode. In a full `research-mathematics` round, perform only cheap local removal tests and return uncovered searches to the coordinator as `requested_attacks`; the coordinator decides whether one targeted `destroy-theory` follow-up is needed. State the exact finite, symbolic, numerical, random, or literature search scope. A failed search leaves necessity unresolved.

Each `requested_attacks` item must identify the frozen candidate digest, removed or weakened assumptions, exact target and negation, proposed search scope, and why the general attack pass does not already cover it.

In nested mode, include the frozen `candidate_digest` and a `requested_attacks` list in the report even when the list is empty. This lets the coordinator distinguish a completed audit from an omitted handoff.

Minimize any counterexample and verify every remaining hypothesis before treating it as evidence of necessity. Put load-bearing certified witnesses in the canonical mathematics during consolidation; otherwise propose a reusable research-memory card. When a formal certificate is practical, prove that the witness satisfies every retained assumption and violates the exact conclusion.

## 4. Mine the proof for relaxations

At every use of `Ai`, extract the weakest local property that makes the step go through. Ask whether:

- the local property can replace `Ai` globally;
- the conclusion must weaken or change topology;
- constants or exceptional sets become parameter-dependent;
- an approximation, localization, truncation, density, compactness, or duality argument can bridge the gap;
- a different proof bypasses the use entirely.

Build a weakening ladder rather than jumping directly to the weakest imaginable statement.

Treat every load-bearing claim called “standard,” “classical,” “immediate,” or “well-known” as an imported premise. Prove it locally or link it to an exact source statement and verify applicability. Otherwise record it as an open dependency node rather than an implicit assumption.

## 5. Classify evidence

Use these classifications:

- **necessary for well-posedness**: removing it makes an object or expression undefined;
- **demonstrably theorem-necessary**: a certified counterexample or no-go theorem applies after removal;
- **needed by the current proof**: an exact dependency is located, with theorem necessity undecided;
- **sufficient but apparently nonminimal**: the proof uses a verified weaker property;
- **redundant**: it follows from other assumptions or is unused and removable with proof;
- **status unresolved**: available arguments decide neither necessity nor redundancy.

Reserve “technical assumption” for a condition replaced by a proved alternative route, not for an intuition that it should be removable.

## 6. Evaluate each relaxation

For every proposed weakening, state:

1. the replacement assumption;
2. the revised theorem and any changed conclusion;
3. affected proof nodes;
4. new lemmas or proof obligations;
5. likely obstructions and known counterexamples;
6. evidence and search scope;
7. status: `PROVED`, `PLAUSIBLE`, `CONJECTURAL`, or `FALSE`.

Distinguish an immediate relaxation already supported by the proof from a research program that still needs a new lemma.

Separately audit statement fidelity: confirm that the revised informal theorem, any formal encoding, and each claimed relaxation express the intended question rather than a conveniently easier one.

## 7. Consolidate a writable round

In a standalone writable theory round:

- Put the exact final assumption set, accepted theorem changes, proved relaxations, and load-bearing necessity witnesses in the canonical document.
- Retain research-memory cards for unresolved necessity questions with next tests, parked weakenings with revival conditions, rejected relaxations with certified witnesses or reasons, and alternative sufficient sets worth revisiting.
- Keep the exhaustive assumption map, removal-test details, mutation variants, tool logs, and superseded theorem versions in the temporary workpad.

Apply one curated card batch only after the canonical update is ready. Validate the home database, then delete the workpad. If canonical integration, database application, or validation fails, retain the workpad and report its exact path. In nested mode, recommend canonical changes and card candidates to the coordinator instead of applying them.

## Report

Start with the transient assumption map:

| ID | Assumption | Origin | Exact uses | Well-posedness? | Current proof? | Theorem necessary? | Evidence | Candidate weakening |
|---|---|---|---|---|---|---|---|---|

Then report:

1. **Hidden or missing assumptions**
2. **Redundancy and implication graph**
3. **Removal witnesses and searched scopes**
4. **Interacting or alternative assumption sets**
5. **Relaxation portfolio**
6. **Revised theorem statements**
7. **Statement-fidelity diffs**
8. **Open proof obligations, prioritized by leverage**
9. **Requested attacks not covered by the general pass**, in nested mode
10. **Canonical and research-memory recommendations**, when nested in or closing a writable theory round

The map is returned in the conversation or kept in the temporary workpad rather than persisted as a separate artifact. Complete the audit only when every explicit and hidden assumption appears in the map, every proof use is linked or marked unused, every theorem-necessity claim has a certificate, and every relaxation has exact proof obligations.
