# Advanced Probe Protocol

Read this reference for material computation, solver work, formal checking, or
parallel scouts. Use the canonical `P#` and `E#` records in
[the ledger protocol](exploration-ledger.md).

## Discriminate efficiently

Choose the smallest case likely to separate the live predictions: a boundary
or degeneracy, controlled deformation, exhaustive small family, adversarial or
held-out case, equivalent presentation, null baseline, or a population scan
paired with one microscope witness. Match the executor to the uncertainty.

For computation, record exact inputs and parameter range, generation or
sampling, implementation, versions, randomness, precision, and stopping rule.
Test known cases, distinguish implementation failure from mathematical
failure, and independently cross-check a decisive result when feasible. A
computation establishes only the encoded problem on its recorded coverage; a
formal checker establishes only the encoded statement.

## Bound scouts

The first tracer normally identifies scout lanes without dispatching them.
Dispatch independent candidate, literature, falsifier, or computation lanes
only when the user asks, a one-shot result requires them, or an explicit budget
covers them. Freeze the formalism and output schema; synthesize through the
canonical records. Agent agreement is not evidence.

On surprise, verify artifacts and inspect the smallest witness. On conflict,
preserve both results and seek an independent probe. After two review cycles
without new evidence, record `UNRESOLVED-CONFLICT`. On stall, change the
representation, example family, scale, or executor, or return a semantic wedge
question.
