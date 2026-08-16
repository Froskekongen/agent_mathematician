---
name: audit-assumptions
description: Audit hypotheses in a mathematical theorem, proof, or theory. Use when identifying hidden, missing, implied, or redundant assumptions; locating their exact proof uses; testing necessity; or proposing and validating weaker assumptions and alternative hypothesis sets.
---

# Audit Assumptions

Determine what each assumption actually buys. Keep four questions separate: well-posedness, use by the current proof, necessity for the theorem, and evidence for that necessity.

Read the shared [rigor standards](../research-mathematics/references/rigor-standards.md) before acting.

## 1. Normalize the ledger

Rewrite the theorem precisely and split compound hypotheses into atomic assumptions with stable identifiers. Include:

- ambient structures and conventions;
- definitional and well-posedness requirements;
- explicit theorem hypotheses;
- assumptions imported by external results;
- hidden assumptions introduced by the proof;
- boundary, dimensional, stochastic, and convergence qualifiers;
- interpretation and formalization choices, including fixed versus evolvable quantities;
- conventions and premises imported from cited sources.

Record implication, equivalence, incompatibility, and joint-sufficiency relationships. Complete this phase when every stated or discovered assumption has exactly one ledger entry.

Freeze the original theorem before mutation. For every proposed relaxation, record a diff of hypotheses, conclusion, definitions, domains, quantifiers, convergence modes, and intended interpretation so that deleting one assumption cannot silently weaken or change something else.

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

Use the `destroy-theory` protocol in constrained mode to search for necessity witnesses. State the exact finite, symbolic, numerical, random, or literature search scope. A failed search leaves necessity unresolved.

Minimize any counterexample and verify every remaining hypothesis before treating it as evidence of necessity. Retain certified witnesses in the example laboratory. When a formal certificate is practical, prove that the witness satisfies every retained assumption and violates the exact conclusion.

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

## Report

Start with the ledger:

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

Complete the audit only when every explicit and hidden assumption appears in the ledger, every proof use is linked or marked unused, every theorem-necessity claim has a certificate, and every relaxation has exact proof obligations.
