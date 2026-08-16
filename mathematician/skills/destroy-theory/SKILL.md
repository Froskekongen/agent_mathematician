---
name: destroy-theory
description: Falsify or stress-test a mathematical statement, proof, or theory. Use when asked to destroy, attack, red-team, referee, find counterexamples or gaps, test consistency or claimed generality, or locate the exact boundary where a claim fails.
---

# Destroy Theory

Act as a hostile referee in service of the truth. A successful run either certifies a failure or gives a bounded account of serious attacks the target survived; survival is evidence, not proof.

Read the shared [rigor standards](../research-mathematics/references/rigor-standards.md) before acting.

## 1. Map the target

Separate definitions, axioms, ambient assumptions, lemmas, main claims, and claimed consequences. Type-check the objects and write the exact logical negation of every principal claim.

Preserve an immutable copy of the submitted target and distinguish its literal wording from the intended research question. Flag every added assumption, changed definition, restricted domain, altered quantifier, or easier interpretation as target drift, even when the revised claim is true. A request to prove a statement is not evidence that it is true.

Build a dependency map and identify the narrowest load-bearing claims. Check whether the definitions are circular, whether models satisfying the axioms exist, whether the theory is vacuous, and whether the claimed generality exceeds the proposed mechanism.

Complete this phase when each attack target has a precise statement and negation.

## 2. Rank the attack surface

Prioritize universal quantifiers, existence or uniqueness claims, boundary parameters, closure assertions, division or inversion, limit interchanges, asymptotic constants, representation independence, identifiability, noncommutativity, and finite-to-infinite-dimensional transitions.

Choose attacks that fit the target. Record them in an attack ledger with columns:

| ID | Target | Proposed attack | Search scope | Candidate | Result |
|---|---|---|---|---|---|

Use result labels that distinguish `target defeated`, `proof defeated`, `encoding defeated`, and `not falsified within scope`.

## 3. Run the cheap-refute funnel

Start with the cheapest decisive attacks:

- zero and constant objects;
- dimensions one and two;
- finite, discrete, linear, or diagonal models;
- degenerate matrices, kernels, measures, or maps;
- boundary values and vanishing denominators;
- minimally regular, discontinuous, or noninjective examples;
- dimensional, sign, scaling, and units checks.

Escalate to transformations and pathologies:

- rescaling, translation, sign change, symmetry, and time reversal;
- sequences approaching the edge of the hypotheses;
- loss of compactness, completeness, coercivity, or uniform integrability;
- dependence, nonadaptedness, or exceptional-set changes;
- noncommutative and infinite-dimensional counterexamples.

For classifications or finite candidate families, generate several mutually incompatible candidates, refute cheaply, and reserve full proof effort for survivors. State the domain and limits of every finite, random, numerical, symbolic, SAT/SMT, or proof-assistant search.

When formal tools are practical, vary or delete hypotheses and certify the complete instantiated negation. Feed each certified witness back into the example laboratory so later candidates must explain both positive and negative cases.

## 4. Attack the proof step by step

Check the earliest unsupported inference rather than only the final answer. Search for:

- quantifier swaps and changed domains;
- circular dependence in the lemma graph;
- unproved existence, uniqueness, measurability, integrability, or invertibility;
- unjustified interchange of limits, sums, integrals, derivatives, expectations, or operators;
- topology or convergence-mode changes;
- exceptional sets that depend on a parameter;
- constants that are not uniform in the claimed variables;
- external results whose exact hypotheses fail;
- finite-dimensional facts used in infinite dimension;
- a conclusion stronger than the lemmas provide;
- premise smuggling inside “standard,” “classical,” or “immediate” steps;
- silent repair or reinterpretation of the target;
- local arguments without the claimed global compatibility;
- obligation laundering, where a helper lemma restates the central difficulty;
- formal escape hatches, unrecorded axioms, or a changed encoded theorem;
- citations that do not establish the exact load-bearing claim;
- routine detail that obscures an unsupported crux;
- success-only reporting that hides the attempt denominator or selection rule.

Distinguish a defect in the submitted proof from a counterexample to the theorem.

## 5. Certify and minimize witnesses

A counterexample certificate must:

1. define the object unambiguously;
2. verify every hypothesis one by one;
3. compute or prove the failure of the conclusion;
4. identify the first claim or proof step it defeats;
5. minimize the witness when possible;
6. separate exact reasoning from floating-point or heuristic evidence;
7. verify that any formal encoding matches the frozen target;
8. record checker and library versions, permitted axioms, search scope, and attempt denominator when tools are used.

Reject a candidate that violates even one hypothesis. Treat numerical candidates as leads until converted into rigorous witnesses or bounded computational claims.

## 6. Repair the theory

Locate the minimal false core. Propose the nearest natural corrected statement by strengthening a hypothesis, weakening the conclusion, restricting the domain, changing the topology, or adding the missing exceptional case. Explain why each certified witness no longer applies and list the new proof obligations.

## Report

Return:

1. **Target and logical negation**
2. **Theory and dependency map**
3. **Attack ledger**
4. **Certified counterexamples or proof defects**
5. **Boundary of validity**
6. **Candidate repairs**
7. **Residual attack surface**
8. **Verdict**

Use one verdict:

- `FALSE`: a certified counterexample defeats the statement;
- `INCONSISTENT`: the assumptions or axioms yield a verified contradiction;
- `PROOF-INVALID`: a material proof gap is verified while the theorem remains undecided;
- `OVERSTATED`: a weaker or restricted result survives but the stated generality does not;
- `SURVIVED-ATTACK`: no failure was found within the reported attack scope;
- `UNRESOLVED`: candidate failures or repairs remain uncertified.

Complete the run only after every load-bearing claim has received at least one adapted attack, every reported witness is certified, and unsearched territory is explicit.
