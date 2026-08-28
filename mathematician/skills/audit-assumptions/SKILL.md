---
name: audit-assumptions
description: Audit hypotheses in a mathematical theorem, proof, or theory. Use when identifying hidden, missing, implied, or redundant assumptions; locating their exact proof uses; testing necessity; or proposing and validating weaker assumptions and alternative hypothesis sets.
disable-model-invocation: true
---

# Audit Assumptions

Determine what each assumption buys. Keep well-posedness, use by this proof, theorem necessity, and evidence for necessity separate. Read the shared [rigor standards](../research-mathematics/references/rigor-standards.md) first.

## Execution role

- **Nested specialist:** audit the coordinator's exact frozen candidate and digest. Begin cold, then optionally resolve supplied canonical research keys or aliases with read-only `lookup`; use broader `search` only when needed and `show` only for selected cards. Mark imports, create or change no theory artifact, run cheap local removal tests, and return uncovered searches as `requested_attacks` rather than launching another destroyer.
- **Standalone report-only:** answer in conversation without filesystem changes. A constrained `$destroy-theory` pass may seek necessity witnesses; both skills remain report-only, and memory access is limited to exact `lookup`, summary `search`, and selective `show`.
- **Standalone writable round:** only with authority to change a file-backed home theory, read and follow the writable-home coordinator path, including `ensure`, in the shared [research-memory protocol](../research-mathematics/references/research-memory.md), using its [CLI](../research-mathematics/scripts/research_memory.py). A constrained destroyer remains read-only and reports back.

Default to report-only without both writable authority and a home theory.

## 1. Normalize assumptions

Rewrite the theorem precisely and split compound hypotheses into atomic,
human-semantic identifiers such as `finite-energy` or `uniform-integrability`.
Use `A1` or `Ai` only as transient local notation, never as a durable canonical
research key or card slug. Include ambient conventions, well-posedness
requirements, explicit hypotheses, premises imported by results, hidden proof
assumptions, boundary/dimensional/stochastic/convergence qualifiers,
interpretation and formalization choices, and cited-source premises.

Record implication, equivalence, incompatibility, and joint sufficiency in a transient assumption map. Freeze the original theorem. For each relaxation, diff hypotheses, conclusion, definitions, domains, quantifiers, convergence modes, and intended interpretation.

Complete this phase when every explicit or discovered assumption appears exactly once.

## 2. Map exact uses

Link each assumption to the definitions, expressions, lemmas, interchanges, existence or uniqueness claims, constants, and imported theorems that use it. Inspect every proof step for unstated assumptions.

For each assumption answer independently:

1. Is it needed for the statement to be well-defined?
2. Is it used by this proof?
3. Is it necessary for the theorem?
4. What evidence supports each answer?

Mark unused assumptions. Proof use establishes dependence of this proof, not theorem necessity.

## 3. Remove and mutate

For each semantically identified assumption:

- delete it while retaining the rest;
- check whether another assumption implies it;
- weaken it to the local property actually used;
- replace it with a nearby or incomparable condition;
- test reversals or strengthened conclusions;
- inspect interacting groups and alternative sufficient sets; and
- mutate interpretation choices to expose vacuity, triviality, or a changed question.

In standalone work, apply `$destroy-theory` in constrained mode—or execute [the sibling skill](../destroy-theory/SKILL.md)—to seek witnesses. In a full `research-mathematics` round, perform only cheap local tests and return uncovered searches to the coordinator. State the scope of every finite, symbolic, numerical, random, or literature search; failure leaves necessity unresolved.

Each nested report includes `candidate_digest` and a `requested_attacks` list, even if empty. Each request identifies the digest, removed or weakened assumptions, exact target and negation, proposed search scope, and why the general attack does not cover it.

Minimize counterexamples and verify every retained hypothesis. When practical, certify the exact conclusion failure formally.

## 4. Mine the proof for relaxations

At every use of `Ai`, extract the weakest local property sufficient for that step. Ask whether it can replace `Ai` globally, whether the conclusion or topology must change, whether constants or exceptional sets lose uniformity, whether approximation/localization/truncation/density/compactness/duality bridges the gap, or whether another proof bypasses the use. Build a weakening ladder rather than jumping to the weakest imaginable claim.

Treat every load-bearing “standard,” “classical,” “immediate,” or “well-known” claim as an imported premise. Prove it locally or verify an exact source statement; otherwise make it an open dependency.

## 5. Classify evidence

Use:

- **necessary for well-posedness:** removal makes an object or expression undefined;
- **demonstrably theorem-necessary:** a certified counterexample or no-go theorem applies;
- **needed by the current proof:** exact use located, theorem necessity undecided;
- **sufficient but apparently nonminimal:** a verified weaker property suffices;
- **redundant:** implied by other assumptions or provably unused and removable;
- **status unresolved:** available work decides neither necessity nor redundancy.

Call an assumption “technical” only after a proved alternative route removes it.

## 6. Evaluate relaxations

For each proposed weakening state the replacement, revised theorem, affected proof nodes, new obligations, obstructions and counterexamples, evidence and search scope, and status: `PROVED`, `PLAUSIBLE`, `CONJECTURAL`, or `FALSE`. Distinguish an immediate proof-supported relaxation from a research program needing a new lemma.

Audit statement fidelity separately: revised prose, formal encoding, and claimed relaxation must express the intended question rather than a convenient substitute.

## Retain only useful state

In a writable round:

- **Canonical Markdown:** exact final assumptions, accepted theorem changes, proved relaxations, and load-bearing necessity witnesses.
- **Research-memory cards:** unresolved necessity questions with next tests, parked weakenings with revival conditions, rejected relaxations with witnesses or reasons, and alternative sufficient sets worth revisiting.
- **Workpad only:** exhaustive assumption map, removal tests, mutation variants, tool logs, and superseded theorem versions.

Close once under the shared protocol. A nested specialist recommends destinations; only the coordinator writes them.

## Report

Start with:

| Semantic key | Assumption | Origin | Exact uses | Well-posedness? | Current proof? | Theorem necessary? | Evidence | Candidate weakening |
|---|---|---|---|---|---|---|---|---|

Then report hidden assumptions, implication and redundancy, witnesses and search scope, interacting or alternative sets, relaxation portfolio, revised statements, fidelity diffs, prioritized obligations, nested `requested_attacks`, and—when nested or writable—canonical/card recommendations.

Complete only when every explicit and hidden assumption is mapped, every proof use is linked or marked unused, every theorem-necessity claim has a certificate, and every relaxation has exact proof obligations.
