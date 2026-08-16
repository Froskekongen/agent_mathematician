# Mathematical Research Rigor Standards

Apply these standards across the full skill suite.

## Truth and scope

Use mathematical truth as the objective. Treat agreement with the user, narrative elegance, speed, and apparent completeness as secondary. A rigorous negative result, exact gap, or unresolved status is a valid outcome.

Scale the process to the claim. Routine calculations need local checking; substantial theorems, conjectures, derivations, and research questions need the complete research loop.

## Formalization standard

Before proof search, declare all material features:

- objects, domains, codomains, and quantifiers;
- regularity, dimension, ambient algebraic or geometric structure;
- topology, norm, metric, measure, filtration, and probability space;
- boundary and initial conditions;
- deterministic or stochastic interpretation;
- pointwise, almost-sure, in-probability, distributional, weak, strong, or `L^p` meanings;
- finite- versus infinite-dimensional setting;
- requirements for every expression to be well-defined.

Choose and state a natural interpretation for ambiguity, then note alternatives that materially change the result.

Freeze a versioned target contract before substantial search. Preserve the literal source statement, intended research question, definitions, fixed versus evolvable quantities, permitted assumptions or axioms, and representative non-vacuous instances. Treat any later change to hypotheses, conclusion, domain, definitions, or quantifiers as a new target that requires an explicit diff and renewed audit.

## Assumption standard

Maintain an atomic assumption ledger. For each assumption, record:

- origin and exact statement;
- every proof node that uses it;
- whether it is needed for well-posedness, this proof, or the theorem itself;
- implication or interaction with other assumptions;
- a candidate weakening;
- a removal witness or the scope of an unsuccessful search.

Inspect measurability, integrability, differentiability, boundedness, invertibility, completeness, separability, compactness, adaptedness, independence, uniqueness, existence of minimizers, convergence of series, continuity of operators, and interchange of operations when relevant.

## Mechanism and examples

Identify the structure doing the work before allowing notation to obscure it. Use explicit examples to reveal invariance, conservation, monotonicity, convexity, compactness, coercivity, orthogonality, analyticity, closure, universality, or another mechanism.

Include the smallest nontrivial case, low dimensions, linear or discrete models, boundary cases, and pathologies adapted to the problem. Keep an observed pattern, computational evidence, a conjecture, and a theorem as distinct artifacts.

## Proof-search standard

For a nontrivial result, compare multiple genuinely different proof routes. Record why a route fails before abandoning it; the obstruction may identify the correct statement. Allow speculative and nonstandard ideas during the creative pass, then submit them to the same verification standard.

Use a generate, cheap-refute, expensive-prove funnel when many candidates exist. Preserve structurally diverse survivors rather than only the current favorite.

## Proof-construction standard

Build a dependency graph:

`definitions -> preliminary lemmas -> structural results -> main theorem`.

For every lemma, verify:

1. it states exactly what the next node needs;
2. its hypotheses are available;
3. all expressions exist;
4. its conclusion is strong enough;
5. dependencies are acyclic;
6. limiting operations use the claimed topology;
7. sums, limits, integrals, derivatives, expectations, and operators are interchanged under valid conditions;
8. finite-dimensional facts are not silently exported to infinite dimension.

Replace compression words such as “clearly” or “standard” with the missing argument whenever that step carries mathematical content.

Keep a proof DAG rather than only a persuasive transcript. Preserve verified nodes, failed branches, checker feedback, and unresolved obligations. Do not accept a helper lemma that merely restates or hides the central difficulty; the dependency closure, not the main-file appearance, determines whether a proof is complete.

## External-result standard

Retrieve the exact statement of every imported theorem. Record an authoritative source or formal identifier and verify all hypotheses, conventions, quantifiers, and scope conditions in the current setting. Inspect the proof idea or equivalent formulations when novelty, transfer, or mechanism matters. Resemblance to a named theorem does not establish applicability.

Verify attribution and priority claims against primary sources. Report the search scope. Absence of a located reference does not establish novelty.

## Computation standard

Use symbolic, numerical, and programmatic experiments to discover identities, inspect low-dimensional cases, estimate constants, test scaling, and find counterexamples.

Before broad computational search, define:

- valid candidate criteria;
- a deterministic evaluator or explicit test suite;
- a score that distinguishes degrees of progress when possible;
- fixed structure versus search variables;
- reproducibility data: code, versions, precision, bounds, and random seeds;
- an archive of diverse candidates and failures;
- the total attempt denominator, selection rule, budget, and stopping condition.

Prefer exact arithmetic for certificates. State numerical tolerance and conditioning. Treat computation as proof only when a verified exhaustive argument or faithful formal certificate closes the logical gap.

## Adversarial standard

Actively seek objects satisfying the hypotheses and violating the conclusion. Test zero, constant, low-dimensional, degenerate, minimally regular, boundary, rescaled, translated, sign-changed, time-reversed, noninjective, noncompact, non-uniformly-integrable, noncommutative, and infinite-dimensional cases as relevant.

Certify a counterexample by checking every hypothesis and the failed conclusion. A theorem that survives an attack remains unproved until a proof passes independently.

Attack the specification as well as the theorem: test for vacuity, altered quantifiers, easier interpretations, hidden domain restrictions, unsafe target mutations, and imported assumptions disguised as definitions. Distinguish `target defeated`, `proof defeated`, `encoding defeated`, and `not falsified within scope`.

## Independent-verification standard

Verify a completed argument through a second proof, a fresh derivation of the critical lemma, an alternative characterization, a proof assistant or trusted checker, or an independent dependency reconstruction. Separate proposer and verifier contexts when possible. A same-model critic is a useful filter, not independent evidence. Reset a stateful critic after major revisions and require a final fresh-context check for high-stakes results. Rereading the same derivation is a correlated check.

Keep the verification obligations separate:

1. the informal statement matches the intended research question;
2. the formal specification faithfully encodes that statement;
3. the proof establishes exactly the frozen specification;
4. the complete dependency closure contains no unresolved placeholder, unsafe axiom, hidden assumption, or changed target.

For formal work, test new definitions with sanity lemmas and representative examples, pin the proof-assistant and library revisions, and audit the permitted axiom set. Kernel acceptance certifies the encoded proposition only; semantic fidelity and mathematical significance require separate review.

Make the proof easy to verify: explicit subgoals, local justifications, stable notation, and visible dependencies. Checkability is part of rigor.

## Epistemic standard

Use exact labels:

- `PROVED`: all material steps and audits pass;
- `INCOMPLETE`: a precise proof obligation remains;
- `CONJECTURAL`: evidence supports a claim without a closing proof;
- `FALSE`: a certified counterexample or contradiction exists;
- `UNRESOLVED`: the truth value is undetermined.

For a gap, state: the unresolved point, why current methods do not close it, and what follows if it is established. Preserve source claims, experimental evidence, informal proof, and formal verification as distinct evidence types.

For research-level or AI-assisted work, preserve provenance: material prompts or instructions, model and tool versions, human interventions, retries, selection, failed routes, budget, checker revisions, and literature-search coverage. Report abstention and reversal rather than hiding them. Evaluate logical correctness, statement fidelity, novelty or significance, provenance or autonomy, and readable mathematical reconstruction as separate axes.

## Theorem-improvement standard

After resolving the stated claim, test whether the mathematics supports a stronger conclusion, weaker hypotheses, a converse, quantitative bounds, stability, uniqueness, characterization, extension, approximation, computational consequence, or unexpected connection.

When a claim is false, use the counterexample to locate the nearest natural true theorem.

## Exposition standard

Present motivation, definitions, intuition, lemmas, theorem, proof, and consequences in a logical progression. Introduce notation before use, explain why definitions are natural, and give the proof idea before technical detail. Use equations for mathematics and prose for logical transitions.

Expose meaningful uncertainty. Rhetorical confidence never upgrades evidence.

## Final theorem audit

Before using `PROVED`, check:

- **Statement:** all objects and quantifiers are defined and the conclusion matches the proof.
- **Target fidelity:** the final statement and any formal encoding match the frozen intended question; every change is disclosed.
- **Well-posedness:** every expression exists and types align.
- **Assumptions:** every hypothesis has an exact role; hidden assumptions are promoted into the statement.
- **Proof:** every implication, limit, topology, exceptional set, and uniformity claim is justified.
- **Dependencies:** the graph is acyclic and all open nodes are closed.
- **Counterexamples:** adapted simple, boundary, degenerate, and pathological cases were actively tested.
- **External results:** exact hypotheses and citations were verified.
- **Independent check:** a genuinely fresh verification agrees.
- **Novelty:** established results, new deductions, and conjectures are separated.
- **Formal closure:** tool and library versions are pinned; definitions have sanity tests; no forbidden escape hatch or unresolved helper lemma remains.
- **Provenance:** attempts, selection, budgets, tools, human edits, failures, and abstentions are disclosed at a level appropriate to the claim.
- **Exposition:** the proof's crux and dependency mechanism survive any formal-to-human rewrite.
