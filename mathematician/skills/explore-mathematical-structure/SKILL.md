---
name: explore-mathematical-structure
description: Explore a vague mathematical idea, question, or provisional formalism through rapid contrastive tests so the user can choose promising next directions.
disable-model-invocation: true
---

# Explore Mathematical Structure

Run a **contrastive laboratory**: candidate structures make distinguishable
predictions, the cheapest useful probe tests those differences, and each
short round updates the user's research choices.

A candidate may be a loss, objective, representation, scalar encoding,
algebraic theory, invariant, mechanism, regime, construction, or a bundle of
structures at different levels. Optimize for understanding gained per unit
of human attention.

## Start from the user's current precision

Start from a phenomenon, desired behavior, example, application, analogy,
provisional definition, or selected formalism. Prior use of
`$formalize-concepts` is helpful but not required.

Build only the working contract needed for a discriminating probe:

- mathematical job or phenomenon;
- candidate objects, operations, transformations, or equivalences;
- one observable or question and one anchor example or family;
- fixed choices, reversible assumptions, and live semantic forks.

Begin once a candidate can make a testable prediction, differ from a
serious alternative or baseline, or fail on a meaningful example.

This skill and `$formalize-concepts` may both begin from vague ideas. Use
local formalization here when definitions serve structural comparison.
Recommend `$formalize-concepts` when choosing intended meaning is the next
useful task and unresolved meaning blocks comparison. Resolve one local
semantic fork here when a shared example makes its consequences concrete;
ask one wedge question when the answer changes examples, predictions, maps,
or equivalences.

Local derivations, micro-lemmas, finite checks, computation, search, and
counterexamples may discriminate candidates. When the objective becomes an
end-to-end proof, freeze the claim and exploration state, then recommend
`$explore-proof-strategies` or `$research-mathematics`. Reserve `PROVED` for
downstream certification. Preserve an incidental complete argument as
`CANDIDATE FULL PROOF — NOT CERTIFIED` and stop widening around it.

## Carry one living lab state

Maintain:

- **contract and formalism version** — meaning, definitions, assumptions,
  and unresolved semantic forks;
- **research taste** — the one to three user values guiding allocation;
- **candidate registry** — stable IDs, roles, relations, dependencies, and
  dispositions;
- **contrast matrix** — the current comparison and unresolved cells;
- **probe ledger** — predictions, methods, scoped evidence, and artifacts;
- **direction portfolio and budget** — selected, active, parked, merged,
  split, or rejected directions; explored scope; privacy mode; round limit.

Assign stable IDs once an item survives a round or enters a handoff. Keep
the active snapshot visible; preserve other history by ID, reason, and
revival condition.

Classify a formalism diff as `SEMANTIC`, `EQUIVALENT`, `SCOPE`,
`REGIME-SPLIT`, or `AUXILIARY`, then invalidate only dependent matrix cells,
probes, and directions. A semantic diff may stay local while shared probes
remain meaningful.

Maintain at most four active candidates unless the user requests broad
enumeration; park one before opening another. Keep claim status, evidence
type and scope, and workflow disposition on separate axes.

When material computation, search, formal checking, or agent scouts enter a
round, read [the probe and evidence protocol](references/probes-and-evidence.md)
before promoting or refuting candidates.

## Model and relate candidates polymorphically

Give each serious candidate a role. Useful prompts against category
blindness include:

- objective, loss, regularizer, or constraint;
- representation, encoding, invariant, quotient, or geometric structure;
- algebraic, compositional, signature, or categorical theory;
- probabilistic, dynamical, order, asymptotic, or computational mechanism;
- bundle combining structures at different roles.

Record only relations that affect interpretation, testing, or allocation:

- `RIVAL(role)` — alternatives doing the same job;
- `COMPOSES(interface)` — candidates joined through a stated interface;
- `REFINES` or `FORGETS` — one adds or removes distinctions;
- `REGIME(condition)` — alternatives apply in different regimes;
- `INCOMPATIBLE(reason)` or `INDEPENDENT`.

Compare rivals directly and cross-role candidates by their contribution to
the user's goal. Treat a bundle as its own candidate; probe components,
ablations, and interactions. When breadth is valuable, include at most one
structurally remote candidate with an explicit bridge, distinct prediction,
and cheap rejection test.

## Maintain the polymorphic contrast matrix

Every active candidate or bundle occupies one row in a literal side-by-side
comparison. Split the table for readability only while preserving candidate
alignment.

| ID | Role / primitives | Relations | Equivalence / maps | `HAS` | `LACKS` | Preserves / forgets | Power / behavior | Regime / dependence | Explains / misses | Evidence | Next discriminator |
|---|---|---|---|---|---|---|---|---|---|---|---|

Use `LACKS` for a meaningful absence, `UNKNOWN` for an applicable unresolved
property, and `N/A` for an inapplicable axis. Attach evidence or probe IDs to
consequential cells. Include relevant invariants, covariants, equivariances,
laws, universal properties, arbitrary choices, and artifact risks.

Adapt the axes rather than imposing a false common ontology:

- losses: optima, degeneracies, calibration, invariance, induced geometry;
- encodings: fibres, collisions, stability, distortion, sufficiency;
- algebraic theories: laws, universal properties, functoriality, closure,
  representations, and presentation independence.

Compare candidate quality on separate selectors: semantic fit, explanatory
compression, evidence scope, falsifiability, tractability, robustness,
composability, prior-art coverage, near- and long-term value, and user taste.
Use a Pareto comparison, partial order, or named winner per selector. Retain
real measurements; aggregate only with user-accepted criteria and weights.

## Run a tracer round

A tracer round is the thinnest end-to-end pass that can change a research
decision. Its activities may interleave. Treat time and computation budgets
as caps. Unless the user requests a one-shot artifact, return after the
first decision-relevant round.

### 1. Frame and contrast

State one uncertainty, active research-taste criteria, budget, and stopping
condition. Open or retain two to four materially distinct candidates or
bundles. For a fixed-structure microscope round, use a baseline, nearby
modification, or failure mode as contrast. Update the matrix and identify
one to three consequential disagreements, interactions, or unknown cells.

This activity is complete when one contrast could change a candidate
relation, disposition, or research allocation.

### 2. Predict and probe

State each affected candidate's prediction, nearest competing explanation,
and cheap break-test before inspecting a decisive outcome where practical.
Execute the highest-information discriminator first; retain other tests as
next steps.

Choose examples for separation: minimal or canonical cases, controlled
deformations, boundaries, degeneracies, adversarial or held-out families,
equivalent presentations, null baselines, bundle ablations, or a population
scan paired with a microscope example. Match the executor to the uncertainty:
local derivation, symbolic algebra, finite enumeration, simulation,
adversarial or solver search, proof assistant, targeted literature, bounded
agents, or a human semantic decision.

This activity is complete when one consequential contrast has scoped
evidence, or the current contract and budget are shown unable to separate it.

### 3. Check and update

Check decisive results for representation, implementation, sampling, and
review artifacts in proportion to impact. Update only affected state. A
candidate may rise, fall, split, park, merge, be selected, or be refuted.
Keep the original prediction beside every repair and preserve informative
failures with revival conditions.

This activity is complete when the matrix, dispositions, and portfolio
reflect the result, including an explicit unchanged outcome for a
non-discriminating probe.

### 4. Allocate or return

Run another tracer autonomously only within the agreed budget and when its
value is clear. Otherwise return the delta for human steering.

A tracer round is complete when one decision-relevant relation or cell is
better determined—or its non-separation is diagnosed—the method, scope, and
artifact risk are recorded, the portfolio is current, and the next test or
human allocation is clear.

## Escalate selectively to bounded parallel scouts

The default first tracer identifies independent candidate, literature,
falsifier, or computation lanes without dispatching them. Dispatch later
when the user asks, a one-shot request requires it, or an explicit autonomous
budget covers it and results are needed before the next useful checkpoint.

Freeze the semantic contract and require one candidate-card or probe-result
schema. Keep dependent derivations serial and synthesize centrally through
the matrix. Agent agreement is not mathematical evidence; preserve
disagreement until an independent probe resolves it.

## Respond to three interrupts

| Trigger | Response |
|---|---|
| `SURPRISE` | Check artifacts, pause breadth, inspect the smallest witness. |
| `CONFLICT` | Preserve both results, isolate the disagreement, seek an independent probe; after two evidence-free review cycles, surface it unresolved. |
| `STALL` | Change representation, observable, generator, scale, or executor; ask a wedge question if the blockage is semantic. |

Routine tests inside the round contract proceed autonomously. Interrupt for
a material semantic fork, privacy/search decision, decisive conflict,
high-value surprise, or major budget reallocation.

When terminology is required, rediscovery risk affects allocation, or the
user asks about prior art or novelty, read and follow
[the literature and privacy protocol](references/literature-and-privacy.md).

## Maintain the direction portfolio

Keep normally two to four nonredundant directions, or fewer when fewer
survive. A direction may select a candidate, test a bundle, resolve a
regime, revise a definition, seek a classification, construct an
obstruction, or pursue an application-facing principle.

For each direction record its kind and candidate IDs, question or
construction, selector profile, suspected mechanism, scoped support and
counterevidence, formalism and literature dependencies, cheapest decisive
test, parking or kill criterion, and next activity.

Choose a sibling skill by the next question:

- meaning blocks comparison → `$formalize-concepts`;
- a precise claim needs proof routes → `$explore-proof-strategies`;
- a stable claim needs rigorous resolution → `$research-mathematics`;
- falsification or validity boundaries are the objective → `$destroy-theory`;
- hypothesis necessity for a stable claim or proof is the objective →
  `$audit-assumptions`.

## Report the tracer delta

For an intermediate round return only:

1. **Decision-relevant change**
2. **Contrast-matrix delta**
3. **Executed probe, scoped evidence, and artifact check**
4. **At most two next directions**
5. **One wedge question with consequences**

A default first-tracer report is at most 500 words: one compact table with
two or three candidate rows and decision-relevant columns, one executed
discriminator in at most three sentences or one short derivation, and the
items above. Keep a fourth candidate and full artifacts in the living state.
When asked about parallelism, add at most three one-line scout questions
without dispatching them. Expand only for a one-shot artifact or on request.

For a concluding artifact or handoff return the state and formalism history,
full matrix and relation map, decisive probes with provenance, candidate
dispositions, direction portfolio, and first next step. A proof or research
handoff also includes the literal claim, interpretation, objects,
quantifiers, assumptions, examples and counterexamples, mechanism, explored
scope, exact source status, and which tests are reusable, version-sensitive,
or require recertification.

## Completion

Complete exploration when the user can make a reasoned research allocation;
each surviving direction has structures or bundles, discriminating evidence,
uncertainty, and a decisive next test; important claims are scoped to
examined families; conceptual tensions are resolved, branched, or parked;
and further work is principally proof, exhaustive validation, or
publication-level development.
