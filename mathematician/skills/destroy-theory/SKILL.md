---
name: destroy-theory
description: Falsify or stress-test a mathematical statement, proof, or theory. Use when asked to destroy, attack, red-team, referee, find counterexamples or gaps, test consistency or claimed generality, or locate the exact boundary where a claim fails.
disable-model-invocation: true
---

# Destroy Theory

Act as a hostile referee in service of the truth. A successful run either certifies a failure or gives a bounded account of serious attacks the target survived; survival is evidence, not proof.

Read the shared [rigor standards](../research-mathematics/references/rigor-standards.md) before acting.

## Execution role and research state

Choose the role before attacking the target:

- **Nested research specialist:** attack the exact frozen candidate and digest supplied by the coordinator. Begin with a cold pass over that candidate alone. Afterwards, research-memory databases may be queried read-only for known attacks, and every imported finding must be marked. Return a content-bound report; do not modify the candidate, canonical document, home database, foreign databases, or other theory artifacts.
- **Standalone report-only:** inspect the supplied target and answer in the conversation without changing the filesystem. Consult existing research memory only when the user asks to include research history; keep it read-only.
- **Standalone writable theory round:** use this role only when the user has authorized changes to a file-backed theory workspace. Own one canonical document and one home research-memory database, open every foreign theory database read-only, and use one OS-temporary workpad. Follow the normal close protocol below.

Default to report-only when writable authority or a home theory is absent. Before any nested or standalone writable use of research memory, read the shared [research-memory protocol](../research-mathematics/references/research-memory.md) and use its [CLI](../research-mathematics/scripts/research_memory.py).

When a research coordinator supplies `requested_attacks` from an assumption audit, attack only requests not already covered by the general pass, against the same frozen candidate digest. Report each request's result separately; remain read-only.

Every nested report includes the attacked `candidate_digest`, so the coordinator can reject a report produced against a superseded candidate.

## 1. Map the target

Separate definitions, axioms, ambient assumptions, lemmas, main claims, and claimed consequences. Type-check the objects and write the exact logical negation of every principal claim.

Freeze a content-bound copy of the submitted target in the returned report or temporary workpad, and distinguish its literal wording from the intended research question. Flag every added assumption, changed definition, restricted domain, altered quantifier, or easier interpretation as target drift, even when the revised claim is true. A request to prove a statement is not evidence that it is true.

Build a dependency map and identify the narrowest load-bearing claims. Check whether the definitions are circular, whether models satisfying the axioms exist, whether the theory is vacuous, and whether the claimed generality exceeds the proposed mechanism.

Complete this phase when each attack target has a precise statement and negation.

## 2. Rank the attack surface

Prioritize universal quantifiers, existence or uniqueness claims, boundary parameters, closure assertions, division or inversion, limit interchanges, asymptotic constants, representation independence, identifiability, noncommutativity, and finite-to-infinite-dimensional transitions.

Choose attacks that fit the target. Record them in a transient attack matrix with columns:

| ID | Target | Proposed attack | Search scope | Candidate | Result |
|---|---|---|---|---|---|

Use result labels that distinguish `target defeated`, `proof defeated`, `encoding defeated`, and `not falsified within scope`.

The matrix belongs in the returned report or OS-temporary workpad. It is not a durable ledger or a separate theory artifact.

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

When formal tools are practical, vary or delete hypotheses and certify the complete instantiated negation. Use each certified witness to constrain later candidates during the run so they must explain both positive and negative cases.

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

## 7. Consolidate a writable round

In a standalone writable theory round:

- Put certified counterexamples, verified material proof defects, changed validity boundaries, and accepted repairs in the canonical document. These load-bearing results must not live only in research memory.
- Retain research-memory cards for reusable obstruction patterns, costly unsuccessful attacks, residual attacks with concrete next tests, and rejected repairs with reasons. A routine `not falsified within scope` result does not merit a card unless its search was expensive or is likely to be repeated.
- Keep the complete attack matrix, candidate witnesses, tool logs, superseded repairs, and reconciliation notes in the temporary workpad.

Apply one curated card batch only after the canonical update is ready. Validate the home database, then delete the workpad. If canonical integration, database application, or validation fails, retain the workpad and report its exact path. In nested mode, recommend canonical changes and card candidates to the coordinator instead of applying them.

## Report

Return:

1. **Target and logical negation**
2. **Theory and dependency map**
3. **Transient attack matrix**
4. **Certified counterexamples or proof defects**
5. **Boundary of validity**
6. **Candidate repairs**
7. **Residual attack surface**
8. **Verdict**
9. **Canonical and research-memory recommendations**, when nested in or closing a writable theory round

Use one verdict:

- `FALSE`: a certified counterexample defeats the statement;
- `INCONSISTENT`: the assumptions or axioms yield a verified contradiction;
- `PROOF-INVALID`: a material proof gap is verified while the theorem remains undecided;
- `OVERSTATED`: a weaker or restricted result survives but the stated generality does not;
- `SURVIVED-ATTACK`: no failure was found within the reported attack scope;
- `UNRESOLVED`: candidate failures or repairs remain uncertified.

Complete the run only after every load-bearing claim has received at least one adapted attack, every reported witness is certified, and unsearched territory is explicit.
