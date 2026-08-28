---
name: research-mathematics
description: Research, formulate, prove, verify, or repair a substantial mathematical theorem, conjecture, derivation, or theory. Use for open-ended mathematical research, rigorous proof construction, independent verification, or improving a theorem. Reserve this full workflow for nontrivial claims rather than routine calculations or exposition-only requests.
disable-model-invocation: true
---

# Research Mathematics

Optimize for mathematical truth. Produce claims that can survive expert review, and expose an exact gap, counterexample, or unresolved obligation whenever proof is unavailable.

Read [rigor-standards.md](references/rigor-standards.md) completely before working. Read [evidence-based-methods.md](references/evidence-based-methods.md) when formal verification, computation, literature retrieval, candidate search, or example-driven discovery could materially help.

When no research target is ready and the user wants to explore a selected formalism before choosing what deserves rigorous investigation, recommend `$explore-mathematical-structure` rather than manufacturing a frozen claim.

## Own one research round

For an authorized file-backed round, read and follow the
[research-memory protocol](references/research-memory.md). The coordinating
research agent owns one canonical Markdown document, one writable companion
database, and one generated OS-temporary workpad. It may query other theory
databases read-only. Chat-only work and read-only review create no files.

Read the canonical document before its memory. Retrieve active, open, and
parked summaries first; query rejected routes only when they bear on a route
under consideration. On the first file-backed round, initialize the empty
`<stem>.research.sqlite` companion and add its locator to the canonical
frontmatter. A named but missing companion is reported rather than silently
recreated.

Use the three retention tiers throughout the round:

- every accepted or load-bearing result belongs in the canonical mathematical
  account; a deliberate native proof source, certificate, program, or dataset
  may carry its machine-checkable representation when linked and explained
  there, but does not replace the self-contained account;
- reusable noncanonical knowledge becomes a cohesive research-memory card;
- candidate versions, reports, logs, and incidental failures remain in the
  workpad and are discarded after successful consolidation.

## 1. Formalize

Rewrite the problem as a precise claim.

- Type every object and map with domains and codomains.
- State quantifiers, dimensions, regularity, ambient structures, boundary or initial conditions, and deterministic or stochastic qualifiers.
- Specify topology, norm, measure, filtration, and the mode of equality or convergence when relevant.
- Surface requirements needed merely for expressions to exist.
- State the chosen interpretation of any ambiguity and note material alternatives.
- Create an atomic assumption map with stable identifiers such as `A1`, `A2`, and `A3` in the workpad; the final exact assumptions belong beside the theorem in the canonical document.
- Freeze a content-bound target contract before substantial search: the literal claim, intended interpretation, definitions, fixed versus search variables, permitted assumptions or axioms, and representative non-vacuous instances. Keep later diffs in the workpad and re-audit them rather than silently changing the problem.

Complete this phase only when the claim is well-posed and every symbol and qualifier has a declared meaning.

## 2. Expose the mechanism

Identify the structure that could make the result true: invariance, conservation, monotonicity, convexity, compactness, coercivity, orthogonality, analyticity, algebraic closure, a universal property, or another concrete mechanism.

Build an example laboratory containing the smallest nontrivial case, representative cases, relevant boundary or degenerate cases, and at least one plausible near-miss. Compute explicit examples where possible. Record observed patterns as evidence rather than theorems.

Before committing substantial effort to a proof, run a bounded truth triage on
the frozen target: try the cheapest substitutions, small cases, dimensional or
scaling checks, and exact counterexample searches from the `destroy-theory`
funnel. Keep certified counterexamples and failed boundary cases in the round
laboratory; canonicalize load-bearing witnesses and card only reusable
noncanonical ones at closure. Failure to refute within a stated scope is not
evidence of truth.

Complete this phase with either a candidate mechanism tied to the examples or an explicit account of what remains unexplained.

## 3. Build a strategy portfolio

For a nontrivial claim, develop at least two materially different routes. Consider direct, contradiction, induction, approximation, compactness, duality, algebraic, probabilistic, variational, spectral, transform, geometric, combinatorial, representation-theoretic, or reduction approaches as the problem warrants.

For each route, record:

- the proposed mechanism;
- the assumptions it appears to need;
- the hardest subgoal;
- its likely failure mode;
- why it is selected, deferred, or rejected.

Include a clearly labelled speculative route when a nonstandard idea could reveal new structure. Complete this phase only after selecting a route for mathematical reasons rather than because it appeared first.

## 4. Construct a checkable proof

Separate creative proposal from verification.

1. Draft the strategic argument.
2. Convert it into a dependency-ordered graph from definitions through lemmas to the main claim.
3. Attach assumptions and imported results to the exact nodes that use them.
4. Prove each open subgoal and record its status.
5. Check the proof one inference at a time without silently adding a new idea during the checking pass.

For every lemma, verify well-definedness, available hypotheses, sufficient conclusion strength, absence of circularity, justified limit or operator interchanges, the correct topology, exceptional sets, parameter-independent constants, and finite- versus infinite-dimensional distinctions.

Use the smallest viable generate--verify--revise loop first. For a long search,
keep the frozen target, proof DAG, verified nodes, current best proof, source and
assumption maps, counterexamples, checker errors, and failed routes in the
round workpad. At closure, canonicalize the accepted proof and its load-bearing
dependencies, card only reusable failures or open obligations, and discard the
rest. Set attempt, tool-call, compute, time, or cost budgets and explicit
stopping or human-escalation conditions. Escalate to parallel or evolutionary
search only after a simpler loop shows a concrete bottleneck, and report the
attempt denominator rather than only selected successes.

Use exact source statements for external theorems and verify every hypothesis. Prefer a proof assistant, symbolic checker, exact arithmetic, or executable invariant for load-bearing steps when a faithful formalization is practical. Before the main target, test new definitions with sanity lemmas, positive and boundary examples, and expected laws. Lock the encoded statement, scan the complete dependency closure for `sorry`, `admit`, unsafe axioms, or equivalent escape hatches, and pin tool and library versions. Reject obligation laundering: renaming the central difficulty as a helper lemma does not close it. A checker certifies the encoding, not its fidelity to the intended theorem.

Complete this phase only when every dependency node is proved or explicitly open.

## Specialist-review fork

Keep fork-and-join ownership with the coordinating research agent. Freeze a
content-hashed review candidate in the workpad containing the current target,
complete theorem and proof, dependency graph and node statuses, assumption
map, permitted axioms, exact load-bearing sources and their hypothesis
mappings, and any formal artifacts and environment. A material field change
creates a new candidate digest.

Launch phases 5 and 6 concurrently when delegation is available. Give both
specialists the identical candidate. They begin with a cold pass over that
candidate, may later query relevant memory read-only with imported findings
clearly marked, leave every artifact unchanged, and return content-bound
reports to the coordinator. Reports and their identifiers are transient round
state. The coordinator alone edits the candidate, canonical document, and
home database.

## 5. Attack the candidate

Apply the installed `$destroy-theory` skill to the review candidate, including its theorem, critical lemmas, and proof. If skill-to-skill invocation is unavailable, read and execute [the sibling skill](../destroy-theory/SKILL.md). Treat proposed repairs as findings for phase 7.

Complete this phase only when the latest `destroy-theory` report has met its own completion criterion on the current review candidate.

## 6. Audit hypotheses

Apply the installed `$audit-assumptions` skill to the same review candidate. If skill-to-skill invocation is unavailable, read and execute [the sibling skill](../audit-assumptions/SKILL.md). Treat proposed theorem or proof revisions as findings for phase 7, and preserve the distinction between an assumption needed by this proof and one necessary for the theorem itself.

In this nested role, the audit performs cheap local removal tests and returns
uncovered counterexample searches as `requested_attacks`; it does not launch a
second `$destroy-theory` worker. After both reports join, send only requests
not covered by the main attack to one constrained destroy-theory follow-up.

Complete this phase only when the latest `audit-assumptions` report has met its own completion criterion on the current review candidate.

## 7. Reconcile, repair, and stabilize

Begin this phase only after phases 5 and 6 have met their completion criteria
on the same review candidate. In the workpad, give every finding a disposition:
repair it; close it through specialist re-evaluation or independent
adjudication with an exact reason bound to the finding, report, and candidate
digest; or preserve it in the result status. Every preserved unresolved
material finding blocks `PROVED`.

Integrate the accepted repairs centrally. Repair each verified defect, weaken the conclusion, strengthen the assumptions, or downgrade the epistemic status. When the original claim is false, search for the nearest natural true statement and explain why the counterexample no longer applies.

After every material repair, return to the earliest affected phase, freeze a
new candidate digest, and rerun phases 5 and 6 before re-entering this phase.

Once the candidate remains unchanged, freeze a transient stabilization
manifest containing its digest, specialist-report lineage, findings and
dispositions, repair diffs, and re-evaluation or adjudication records. A later
manifest change reopens this phase and requires every changed load-bearing
disposition to be checked again.

Complete this phase only when the latest successful phase-5 and phase-6
reports identify the same candidate digest, every finding has a disposition,
every accepted repair is incorporated, the candidate has remained unchanged
since both reviews, and the workpad manifest is frozen.

## 8. Verify independently

Promote the stabilized review candidate unchanged to the verification
candidate. In the workpad, bind one verification-run identifier to the
candidate and stabilization-manifest digests and use it as the sole launch
gate. Bind each verifier invocation to that run, its verifier or method, and
exact input projection; record every terminal outcome, including failure or
abstention.

Give each fresh verifier only the projection of the verification candidate required for its check. For a second proof or fresh derivation, give the frozen target and necessary sources while withholding the submitted proof. For proof-correctness review, give the proof DAG, formal artifacts, and necessary sources while withholding the proposer's persuasive narrative and requiring an independently reconstructed dependency trace. Use at least one of:

- a second proof;
- a fresh derivation of the crucial lemma;
- an alternative characterization;
- a trusted checker, different model, or human specialist given only the claim and source material;
- a complete dependency trace reconstructed from scratch.

Compare the results and resolve discrepancies. Separate proof-correctness
review from statement-fidelity review. Treat a material candidate revision as
invalidating the verification candidate: return to the earliest affected
phase, rerun phases 5--7, promote the new stabilized candidate, bind a new
verification run, then launch a fresh verifier. Treat a stabilization-manifest
revision the same way from phase 7. Withhold research memory and the proposer's
persuasive narrative from the independent verifier unless a particular source
is necessary. A fresh-context same-model subagent is a useful correlated check
but not independent evidence; for an independence claim, also require a
different proof, trusted checker, different model, or human specialist.
Rereading the original derivation alone does not satisfy this phase.

Complete this phase when every verifier invocation under the current run has a
recorded terminal outcome, every returned report has a disposition, every
discrepancy is resolved or remains explicit in the result status, and at least
one content-bound report independently checks the current candidate's central
argument; otherwise report the absence of such a check as a limitation.

## 9. Improve and contextualize

Investigate stronger conclusions, weaker hypotheses, converses, quantitative or stability results, uniqueness, characterizations, larger spaces, finite-dimensional approximations, computational consequences, and connections to other theories.

Apply the material-revision rule to every accepted improvement. Whenever this phase creates a new candidate version, return to the earliest affected phase and rerun phases 5--8 before presentation.

Search primary literature when priority, attribution, or novelty matters. Search
the exact claim, equivalent formulations, key constructions, and proof motifs;
inspect proof context rather than matching only theorem titles. Verify exact
sources and state what the search covered. Treat failure to find a reference as
an unresolved novelty question rather than evidence of novelty, and publish
enough provenance in the canonical result to distinguish a new result from
rediscovery, prompted reconstruction, or human strengthening.

## 10. Present the result

Use the smallest structure that preserves checkability. For substantial work, report:

1. **Problem and interpretation**
2. **Assumptions and their exact roles**
3. **Main result and status**
4. **Mechanism and example laboratory**
5. **Strategy comparison**
6. **Proof and dependency structure**
7. **Specialist findings and repairs**
8. **Assumption analysis**
9. **Independent verification**
10. **Extensions, sources, and novelty status**
11. **Verification and provenance summary**, for research-level or AI-assisted results
12. **Exact unresolved point**, when applicable

Use one terminal status:

- `PROVED`: every material step is justified, no preserved unresolved material finding remains, the stabilization manifest closes every specialist finding, and the adversarial attack, assumption audit, and independent check pass on the same final version;
- `INCOMPLETE`: a promising argument has a precisely located proof obligation;
- `CONJECTURAL`: evidence exists without a proof architecture that closes;
- `FALSE`: a certified counterexample or contradiction defeats the claim;
- `UNRESOLVED`: the available work does not determine the truth value.

Keep five evidence axes separate: logical correctness, statement fidelity, novelty or significance, provenance or autonomy, and human-readable reconstruction. Add precise tags where useful, such as `kernel-checked`, `expert-refereed`, `statement-faithful`, `novelty-audited`, `computationally tested`, or `literature-supported`. These tags describe support and do not replace the terminal status.

For the canonical provenance section, report material model and tool versions,
prompts or human hints, edits or strengthened claims, retries and selection,
attempt denominator, budget, checker versions, expert review, and literature-
search coverage. Include failures and abstentions when they affect the
evidential weight. Do not include opaque workpad identifiers. Do not collapse
a kernel-checked proof, faithful formalization, independent mathematical
review, and novelty review into one claim of “verification.”

For a file-backed round, make this presentation the canonical document update.
Summarize material specialist findings, repairs, unresolved findings, and
independent checks without exposing round-local report or invocation IDs.

Then close the round exactly once:

1. Curate reusable noncanonical open obligations, parked improvements,
   rejected routes with demonstrated obstructions, non-load-bearing reusable
   counterexamples, assumption-relaxation results, source-applicability
   snapshots, residual attacks, and verification lessons into one card batch.
2. Apply that batch to the home database with the shared CLI; no specialist
   writes directly.
3. Run `check`, require `canonical_status: current`, and `show` each added or
   materially updated card.
4. Delete the generated workpad only after canonical and database validation
   succeeds. On failure, retain it and report the exact recovery path.

A complete file-backed round leaves only the self-contained canonical
document, its curated companion, and deliberate native mathematical artifacts.

When the user requests an accessible treatment, apply `$explain-mathematics` after the mathematics is settled. If skill-to-skill invocation is unavailable, read and execute [the sibling skill](../explain-mathematics/SKILL.md).
