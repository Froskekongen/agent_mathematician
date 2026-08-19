# Probe and Evidence Protocol

Read this reference when a structural-exploration round uses material
computation, search, formal checking, or agent scouts, or when a probe could
materially promote or refute a candidate.

## Separate status axes

Record each consequential claim on three independent axes.

### Mathematical status

- `DEFINITIONAL`
- `CONJECTURE`
- `SUPPORTED(scope)`
- `REFUTED(counterexample)`
- `UNRESOLVED-CONFLICT`

Reserve `REFUTED` for a checked counterexample against a precise claim.
Otherwise record the exact local failure, such as `FAILED-ON(E7)` or a scope
restriction.

### Evidence type

- `EXACT-DERIVATION(method)`
- `EXACT-FINITE(method, scope)`
- `NUMERICAL(scope, precision)`
- `OBSERVED(scope)`
- `SOURCE-LOCATED(citation)`
- `SOURCE-APPLICABLE(citation, checked assumptions)`
- `HEURISTIC`
- `ANALOGY`

Formal checking certifies the encoded statement, not semantic fidelity,
novelty, naturalness, or significance. Numerical agreement establishes
behavior on the examined scope, not structural identification.

### Workflow disposition

- `ACTIVE`
- `PARKED(reason, revival condition)`
- `SPLIT`
- `MERGED`
- `SELECTED`
- `REJECTED(reason)`

## Record decisive probes

Give every consequential probe a stable ID and record:

- candidate IDs and formalism version;
- object, family, and parameter range;
- competing predictions stated before inspection when practical;
- generation or sampling method;
- executor and implementation details;
- result and mathematical scope;
- artifact risks and checks;
- affected matrix cells, claims, and directions;
- code, data, solver input, certificate, or source artifact.

Preserve failed searches when their explored scope affects future work.

## Choose discriminating examples

Select examples because they separate candidates. Use as appropriate:

- smallest nontrivial and canonical cases;
- parameterized deformations;
- boundary, singular, degenerate, and near-miss cases;
- adversarially selected cases;
- exhaustive small instances;
- random or optimized counterexample search;
- a held-out family selected after a hypothesis was proposed;
- one-feature-at-a-time variation for attribution;
- joint scaling, noncommuting limits, and interaction tests;
- isomorphic presentations, relabelings, coordinate changes, symmetries,
  normalizations, discretizations, or equivalent representations;
- null and randomized baselines.

Pair a population scan with a microscope case when the scan locates the
phenomenon and the microscope can expose its mechanism.

## Match the executor to the uncertainty

Choose among direct derivation, exact symbolic manipulation, exhaustive
enumeration, numerical simulation, asymptotics, random or adversarial
search, optimization, SAT/SMT/finite-model search, computer algebra,
relation discovery, local proof-assistant verification, literature, or a
human semantic decision.

When computation is decisive:

- test the implementation on known cases;
- record seeds, randomness, precision, and stopping criteria;
- prefer exact arithmetic when feasible;
- distinguish implementation failure from mathematical failure;
- cross-check a critical result by an independent method.

## Use agent scouts without manufactured consensus

Enter this mode only after the first-tracer escalation conditions in
`SKILL.md` are satisfied. Parallelize independent candidate, literature,
falsifier, or computation lanes. Freeze the semantic contract and output
schema before dispatch. Centralize synthesis in the contrast matrix and
preserve disagreement.

After two critique-revision cycles without new computation, source
evidence, or mathematical insight, isolate the minimal disputed claim and
seek an independent probe. If no adequate probe is available, record
`UNRESOLVED-CONFLICT` and return it to the user. Polished exposition or
agreement among generated reviewers does not raise the evidence level.
