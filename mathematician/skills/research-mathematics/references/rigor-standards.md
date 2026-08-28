# Mathematical Research Rigor Standards

Apply these standards across the mathematical skill suite. Mathematical truth outranks agreement, elegance, speed, and apparent completeness. An exact counterexample, gap, or unresolved status is a valid result. Scale the process: routine calculations need local checking; substantial claims need the complete research loop.

## Formalization

Before proof search, declare:

- objects, domains, codomains, and quantifiers;
- regularity, dimension, and ambient algebraic or geometric structure;
- topology, norm, metric, measure, filtration, and probability space;
- boundary and initial conditions;
- deterministic or stochastic interpretation;
- pointwise, almost-sure, in-probability, distributional, weak, strong, or `L^p` meanings;
- finite- versus infinite-dimensional setting; and
- conditions making every expression well-defined.

Choose a natural interpretation for ambiguity and identify alternatives that materially change the result. Freeze the literal source, intended question, definitions, fixed versus evolvable quantities, permitted assumptions or axioms, and representative non-vacuous instances. Any later change to hypotheses, conclusion, domain, definitions, or quantifiers is a new target requiring an explicit diff and renewed audit.

## Assumptions

Use an atomic assumption map. For each assumption, record its origin and exact statement; proof nodes that use it; whether it serves well-posedness, this proof, or the theorem; logical interactions; candidate weakenings; and any removal witness or bounded unsuccessful search.

Inspect measurability, integrability, differentiability, boundedness, invertibility, completeness, separability, compactness, adaptedness, independence, uniqueness, minimizer existence, series convergence, operator continuity, and operation interchange when relevant.

## Mechanism and examples

Identify the structure doing the work: invariance, conservation, monotonicity, convexity, compactness, coercivity, orthogonality, analyticity, closure, universality, or another mechanism.

Test the smallest nontrivial case, low dimensions, linear or discrete models, boundary cases, and adapted pathologies. Keep observed patterns, computational evidence, conjectures, and theorems epistemically distinct.

## Proof search and construction

For a nontrivial result, compare genuinely different routes. Use a generate, cheap-refute, expensive-prove funnel when candidates are numerous. Speculative ideas face the same verification standard as conventional ones.

Build a dependency graph:

`definitions -> preliminary lemmas -> structural results -> main theorem`.

For every lemma, verify:

1. it states exactly what the next node needs;
2. its hypotheses are available;
3. all expressions exist;
4. its conclusion is strong enough;
5. dependencies are acyclic;
6. limiting operations use the claimed topology;
7. sums, limits, integrals, derivatives, expectations, and operators are interchanged validly; and
8. finite-dimensional facts are not silently exported to infinite dimension.

Replace “clearly” or “standard” with the missing argument when it carries mathematical content. A helper lemma that restates the central difficulty remains open; completeness is determined by the full dependency closure.

## External results

Retrieve each imported theorem's exact statement from an authoritative source or formal identifier. Verify every hypothesis, convention, quantifier, and scope condition in the present setting. Inspect proof ideas or equivalent formulations when transfer, mechanism, or novelty matters. Resemblance to a named theorem does not establish applicability.

Verify attribution and priority against primary sources and report search coverage. Failure to locate a reference does not establish novelty.

## Computation

Use symbolic, numerical, and programmatic experiments for discovery, low-dimensional inspection, constant estimation, scaling tests, and counterexample search. Before broad search, define valid-candidate criteria, an evaluator or test suite, a useful score, fixed versus search variables, reproducibility data, total attempt denominator, selection rule, budget, and stopping condition.

Prefer exact arithmetic for certificates. State numerical tolerances and conditioning. Computation is proof only when verified exhaustiveness or a faithful formal certificate closes the logical gap.

## Adversarial testing

Seek objects satisfying every hypothesis and violating the conclusion. Test zero, constant, low-dimensional, degenerate, minimally regular, boundary, rescaled, translated, sign-changed, time-reversed, noninjective, noncompact, non-uniformly-integrable, noncommutative, and infinite-dimensional cases as relevant.

Certify a counterexample by verifying every hypothesis and the failed conclusion. Survival establishes only `not falsified within scope`. Also attack the specification for vacuity, altered quantifiers, easier interpretations, hidden restrictions, unsafe target mutations, and assumptions disguised as definitions. Distinguish `target defeated`, `proof defeated`, `encoding defeated`, and `not falsified within scope`.

## Independent verification

Check a completed argument through a second proof, fresh derivation of the crux, alternative characterization, proof assistant or trusted checker, or independent dependency reconstruction. Separate proposer and verifier contexts when possible. A same-model critic is a useful filter, not independent evidence; reset stateful critics after major revisions. Rereading the same derivation is correlated checking.

Verify four distinct obligations:

1. the informal statement matches the intended question;
2. the formal specification faithfully encodes it;
3. the proof establishes exactly the frozen specification; and
4. the complete dependency closure contains no unresolved placeholder, unsafe axiom, hidden assumption, or changed target.

For formal work, test definitions with sanity lemmas and representative examples, pin proof-assistant and library revisions, and audit permitted axioms. Kernel acceptance certifies the encoded proposition, not its semantic fidelity or significance.

Make verification local: explicit subgoals, justified transitions, stable notation, and visible dependencies. Checkability is part of rigor.

## Epistemic status and provenance

Use exact labels:

- `PROVED`: all material steps and audits pass;
- `INCOMPLETE`: a precise proof obligation remains;
- `CONJECTURAL`: evidence supports a claim without a closing proof;
- `FALSE`: a certified counterexample or contradiction exists;
- `UNRESOLVED`: the truth value is undetermined.

For a gap, state the unresolved point, why current methods fail, and what follows if it closes. Report source claims, experiments, informal arguments, and formal checks as distinct evidence types.

For research-level or AI-assisted work, disclose enough to assess the result: material prompts, model and tool versions, human interventions, retries and selection, budget, checker revisions, literature coverage, failures, abstentions, and reversals. Evaluate logical correctness, statement fidelity, novelty or significance, provenance or autonomy, and readable reconstruction separately.

## Improve and explain

After resolving the claim, test stronger conclusions, weaker hypotheses, converses, quantitative bounds, stability, uniqueness, characterizations, extensions, approximations, consequences, and connections. When false, use the counterexample to locate the nearest natural true theorem.

Present motivation, definitions, intuition, lemmas, theorem, proof, and consequences in logical order. Introduce notation before use, explain why definitions are natural, and state the proof idea before technical detail. Expose uncertainty; rhetorical confidence never upgrades evidence.

## Final theorem audit

Before using `PROVED`, check:

- **Statement and fidelity:** all objects and quantifiers are defined; the theorem, intended question, encoding, and proved conclusion agree; every change is disclosed.
- **Well-posedness and assumptions:** expressions exist, types align, every hypothesis has an exact role, and hidden assumptions are stated.
- **Proof and dependencies:** every implication, limit, topology, exceptional set, and uniformity claim is justified; the dependency graph is acyclic and closed.
- **Counterexamples:** adapted simple, boundary, degenerate, and pathological cases were actively tested.
- **External results:** exact hypotheses and citations were verified.
- **Independent check:** a genuinely fresh verification agrees.
- **Novelty:** established results, new deductions, and conjectures are separated.
- **Formal closure:** versions are pinned, definitions have sanity tests, and no forbidden escape hatch or unresolved helper remains.
- **Provenance:** attempts, selection, budgets, tools, human edits, failures, and abstentions are disclosed appropriately.
- **Exposition:** the crux and dependency mechanism survive any formal-to-human rewrite.
