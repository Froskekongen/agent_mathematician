---
name: destroy-theory
description: Falsify or stress-test a mathematical statement, proof, or theory. Use when asked to destroy, attack, red-team, referee, find counterexamples or gaps, test consistency or claimed generality, or locate the exact boundary where a claim fails.
disable-model-invocation: true
---

# Destroy Theory

Act as a hostile referee in service of truth. A successful run certifies a failure or gives a bounded account of serious attacks survived; survival is evidence, not proof. Read the shared [rigor standards](../research-mathematics/references/rigor-standards.md) first.

## Execution role

- **Nested specialist:** attack the coordinator's exact frozen candidate and digest. Begin cold, then optionally resolve supplied canonical research keys or aliases with read-only `lookup`; use broader `search` only when needed and `show` only for selected cards. Mark imports, create or change no theory artifact, and return a content-bound report carrying `candidate_digest`.
- **Standalone report-only:** answer in conversation without filesystem changes. When the user requests research history, use read-only exact `lookup` before broader summary `search`, then `show` only selected cards.
- **Standalone writable round:** only with authority to change a file-backed home theory, read and follow the writable-home coordinator path, including `ensure`, in the shared [research-memory protocol](../research-mathematics/references/research-memory.md), using its [CLI](../research-mathematics/scripts/research_memory.py).

Default to report-only without both writable authority and a home theory. For coordinator-supplied `requested_attacks`, test only requests not covered by the general pass, against the same digest, and report them separately.

## 1. Map the target

Separate definitions, axioms, ambient assumptions, lemmas, main claims, and consequences. Type-check objects and write the exact logical negation of every principal claim. Freeze the submitted target and distinguish literal wording from intended question; flag added assumptions, altered definitions, restricted domains, changed quantifiers, or easier interpretations as target drift.

Map dependencies and narrow load-bearing claims. Test definitions for circularity, model existence, vacuity, and claimed generality beyond the proposed mechanism.

Complete this phase when every attack target has a precise statement and negation.

## 2. Rank the attack surface

Prioritize universal quantifiers, existence or uniqueness, boundary parameters, closure, division or inversion, limit interchanges, asymptotic constants, representation independence, identifiability, noncommutativity, and finite-to-infinite-dimensional transitions.

Use a transient attack matrix:

| ID | Target | Proposed attack | Search scope | Candidate | Result |
|---|---|---|---|---|---|

Distinguish `target defeated`, `proof defeated`, `encoding defeated`, and `not falsified within scope`.

## 3. Run the cheap-refute funnel

Start with zero and constant objects; dimensions one and two; finite, discrete, linear, or diagonal models; degenerate maps, matrices, kernels, or measures; boundary values and vanishing denominators; minimally regular or noninjective examples; and dimensional, sign, scaling, or units checks.

Then try rescaling, translation, symmetry, sign change, time reversal, sequences approaching hypothesis boundaries, loss of compactness or coercivity, dependence or nonadaptedness, changing exceptional sets, noncommutativity, and infinite dimension.

For finite candidate families, generate incompatible candidates and refute cheaply before proving survivors. State limits of every finite, random, numerical, symbolic, SAT/SMT, or proof-assistant search. When practical, delete hypotheses and certify the complete instantiated negation; use witnesses to constrain later candidates.

## 4. Attack the proof

Find the earliest unsupported inference. Check for:

- quantifier swaps, changed domains, or circular lemmas;
- unproved existence, uniqueness, measurability, integrability, or invertibility;
- invalid interchange of limits, sums, integrals, derivatives, expectations, or operators;
- topology or convergence changes, parameter-dependent exceptional sets, or nonuniform constants;
- external results with unmet hypotheses and finite-dimensional facts used in infinite dimension;
- conclusions stronger than the lemmas;
- premises smuggled inside “standard,” “classical,” or “immediate”;
- silent target repair, missing global compatibility, or obligation laundering;
- formal escape hatches, undeclared axioms, or changed encodings;
- citations that miss the load-bearing claim;
- routine detail obscuring an unsupported crux; and
- success-only reporting hiding denominator or selection.

Keep proof defects distinct from theorem counterexamples.

## 5. Certify and minimize witnesses

A counterexample certificate must define the object; verify every hypothesis; prove the conclusion fails; identify the first defeated claim or step; minimize the witness when possible; separate exact from heuristic evidence; check encoding fidelity; and record versions, axioms, search scope, and attempt denominator when tools are used.

Reject any candidate violating a hypothesis. Numerical candidates remain leads until made rigorous or stated as bounded computational results.

## 6. Repair the theory

Locate the minimal false core. Propose the nearest natural correction by strengthening hypotheses, weakening the conclusion, restricting the domain, changing topology, or adding an exceptional case. Explain why each certified witness no longer applies and list new proof obligations.

## Retain only useful state

In a writable round:

- **Canonical Markdown:** certified counterexamples, verified material proof defects, changed validity boundaries, and accepted repairs.
- **Research-memory cards:** reusable obstruction patterns, costly unsuccessful attacks, residual attacks with next tests, and rejected repairs with reasons. Routine `not falsified within scope` results qualify only when expensive or likely to recur.
- **Workpad only:** the attack matrix, candidate witnesses, tool logs, superseded repairs, and reconciliation notes.

Close once under the shared protocol. A nested specialist recommends destinations; only the coordinator writes them.

## Report

Return the target and negation, dependency map, transient attack matrix, certified counterexamples or defects, validity boundary, repairs, residual surface, verdict, and—when nested or writable—canonical/card recommendations.

Use one verdict:

- `FALSE`: a certified counterexample defeats the statement;
- `INCONSISTENT`: assumptions yield a verified contradiction;
- `PROOF-INVALID`: a material proof gap is verified while the theorem remains undecided;
- `OVERSTATED`: only a weaker or restricted result survives;
- `SURVIVED-ATTACK`: no failure was found within the reported scope;
- `UNRESOLVED`: candidate failures or repairs remain uncertified.

Complete only after every load-bearing claim receives at least one adapted attack, every reported witness is certified, and unsearched territory is explicit.
