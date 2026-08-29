# Research Claim Resolution

Read this chain completely only when `research-mathematics` attempts to resolve
a substantial claim:

```text
TARGET -> EVIDENCE -> CHALLENGE -> VERIFY -> STATUS
```

This is the research completion process, not a suite-wide cadence. It applies
the [shared mathematical integrity](mathematical-integrity.md) while
closing a proof, refutation, or exact unresolved boundary. An exact
counterexample, a precise gap, or an unresolved result is a successful rigorous
outcome when reported at its warranted status.

## TARGET

Freeze the object being judged before trying to prove it. Record:

- the literal claim and intended interpretation;
- typed objects and maps, domains, codomains, and quantifiers;
- regularity, dimension, ambient structures, topology, measure, boundary data,
  convergence mode, and deterministic or stochastic meaning when relevant;
- conditions needed merely for expressions and objects to exist;
- atomic assumptions, permitted axioms, and representative non-vacuous cases;
  and
- a content digest for any candidate sent to another context.

Distinguish a repaired or restricted theorem from the submitted theorem. A
material change to a definition, domain, hypothesis, conclusion, or quantifier
creates a new target and invalidates downstream challenge and verification.

## EVIDENCE

Type and scope every contribution: direct proof, imported theorem, exact
enumeration, numerical experiment, executable certificate, checked witness,
or heuristic. Observed patterns and failure to refute are not proofs.

For a proof, use a dependency graph from definitions through lemmas to the
target. At each node check well-posedness, available hypotheses, conclusion
strength, circularity, topology, exceptional sets, uniformity, interchanges of
operations, and finite- versus infinite-dimensional scope. A helper that
renames the central difficulty remains open.

For an imported result, obtain the exact statement from an authoritative
source and map every hypothesis and convention. Source resemblance does not
establish applicability; failure to find prior work does not establish novelty.

For material computation or executable checking, follow
[computational-checking.md](computational-checking.md). Computation proves only
the faithfully encoded proposition over its demonstrated coverage.

## CHALLENGE

Attack the literal target and each load-bearing proof node. Adapt tests to the
mathematics: small and degenerate objects, boundary parameters, rescaling and
symmetry, loss of regularity or compactness, noncommutativity, nonuniformity,
and finite-to-infinite transitions are common starting points.

A counterexample certificate defines the object, verifies every hypothesis,
and proves the conclusion fails. Keep these outcomes distinct:

- target defeated;
- proof defeated while the theorem remains open;
- encoding or implementation defeated; and
- not falsified within the reported scope.

For assumptions, distinguish well-posedness, use by the present proof, theorem
necessity, and the evidence for each. Proof use alone does not establish
necessity.

## VERIFY

Verify the unchanged target in a fresh context. Check four separate
obligations:

1. the informal statement represents the intended question;
2. any executable or formal specification faithfully represents that
   statement;
3. the proof or checker establishes exactly the frozen specification; and
4. the complete dependency closure contains no placeholder, hidden premise,
   unsafe axiom, circularity, or silently changed target.

Useful verification includes a second proof, a fresh derivation of the crux,
an alternative characterization, independent dependency reconstruction, an
audited executable checker, or a qualified human review. A fresh same-model
critic is valuable but correlated; describe it honestly. A material repair
requires renewed challenge and verification.

## STATUS

Use exactly one truth status:

- `PROVED`: the complete target is closed and the current challenge and fresh
  verification pass;
- `INCOMPLETE`: a proof architecture has a precise open obligation;
- `CONJECTURAL`: scoped evidence exists without a closing proof;
- `REFUTED`: a certified counterexample or contradiction defeats the target; or
- `UNRESOLVED`: available work determines neither truth nor falsity.

Workflow disposition such as active, parked, rejected, or integrated is
orthogonal to truth status. Support tags such as `exact-arithmetic`,
`exhaustive-on-scope`, `certificate-checked`, `checker-audited`,
`independently-replayed`, `statement-fidelity-audited`, or
`literature-audited` record how a status is supported; they never replace it.

For research-level or AI-assisted work, report logical validity, statement
fidelity, novelty or significance, provenance or autonomy, and readable
reconstruction separately. Record material sources, tools and versions, human
hints or edits, attempts and selection, budgets, failures, abstentions, and the
scope of independent review.

Before `PROVED`, require one unchanged target to pass the complete chain:
every dependency closes, every material challenge finding is dispositioned,
external results are mapped exactly, statement fidelity is checked, and a
fresh verifier covers the central argument. Otherwise select the strongest
honest lower status and name the exact remaining obligation.
