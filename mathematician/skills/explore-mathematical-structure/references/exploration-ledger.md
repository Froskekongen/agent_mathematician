# Canonical Exploration Ledger

Read this reference before recording the first completed tracer, any later
definition or claim version, a one-shot result, or a handoff.

The ledger is exact state, not a transcript or report outline. It is faithful
when another mathematically mature reader can reconstruct every live
structure, determine every claim's domain and evidence coverage, distinguish
equality from weaker equivalences or analogies, and identify what survives a
version change.

## Normalize the state

Record each fact once and reuse it through stable IDs. An inherited definition
such as “`F1.v1` plus symmetry” is exact when `F1.v1` is present and the added
axiom is literal; nearby unlabeled prose is not a reference. Candidate records
own candidate mathematics; contrast tables are derived views.

Use namespaced IDs: `F` formalism, `M` candidate, `K` claim, `P` probe, `E`
evidence, `Q` search, `S` source applicability, `D` direction, `H` history, and
`L` ledger envelope. Assign an ID when an item enters a consequential probe or
cross-reference, survives a round, or enters a handoff. Never reuse an ID.

All fields below are required when applicable. Omit only explicitly
conditional fields whose condition is false; state a decision-relevant absence
explicitly, and do not emit filler `N/A` fields.

## Canonical records

- **Envelope `L#`:** `SNAPSHOT` or `DELTA`; ledger ID; base ledger ID for a
  delta; resulting current formalism/candidate versions and claim/direction
  dispositions; research taste; explored scope; privacy mode; applicable
  round/time/compute/search or cost caps; stopping condition.

- **Formalism `F#.v#`:** predecessor and `H#`, or `initial`; mathematical job
  and observable/question; ambient setting, primitive data, exact object types;
  typed operations, relations, and load-bearing maps; definitions and laws;
  equality/equivalence and witnesses or comparison maps; assumptions,
  quantifiers, regularity, finiteness, boundaries, regimes, and conventions;
  anchors and intended nonexamples; unresolved semantic forks; fixed versus
  reversible choices. Define load-bearing notation before use.

- **Candidate `M#.v#`:** predecessor and `H#`, or `initial`; pinned formalism;
  exact definition, role, and primitives; component versions and typed
  interfaces when bundled; regime and dependencies; decision-relevant
  relations to other candidates with their map, interface, hypothesis, or
  obstruction; applicable laws, invariants, preserved/forgotten structure,
  arbitrary choices, and degeneracies; scoped predictions and nearest
  competitor; workflow disposition with exact reason and revival condition.

- **Claim `K#.v#`:** predecessor and `H#`, or `initial`; literal statement;
  pinned formalism and candidates; quantifiers and hypotheses; `claim_scope`;
  mathematical status; evidence IDs; dependencies; workflow disposition. A
  repair creates a new version and retains the old statement.

- **Evidence `E#`:** pinned formalism, candidates, and claims; exact proposition
  admitted as evidence; originating `P#` or `S#`; `evidence_kind`;
  `evidence_coverage`; `semantic_fidelity`; certificate/source/artifact
  reference; workflow disposition.

- **Probe `P#`:** pinned formalism, candidates, and claims; competing prior
  predictions; object/family and parameter range; generation or sampling
  method when used; executor, method, and raw outcome; implementation details
  when material; evidence IDs; artifact risks and checks; affected cells,
  records, and directions; decision-state change, including unchanged; artifact
  references when any exist.

- **Search `Q#`:** privacy mode; pinned pre-search formalism, candidates, and
  claims; exact or abstracted query; date, source classes, and stopping scope;
  preserved cold-pass IDs; result coverage; searched-scope novelty assessment
  and rationale; located `S#` IDs.

- **Source applicability `S#`:** origin `Q#` or
  `USER-SUPPLIED(artifact/message reference)`; exact citation and source
  version; imported statement with objects, quantifiers, hypotheses, and scope;
  pinned applicable formalism, candidates, and claims; preserved pre-source
  cold-pass IDs when user-supplied; explicit mapping from source objects and
  assumptions; applicability status and unmatched assumptions; source-specific
  relation to the candidate; resulting evidence IDs.

- **Direction `D#`:** workflow disposition; question/construction and candidate
  versions; research-taste rationale; suspected mechanism and current support
  or counterevidence; formalism, claim, source, and other dependencies; cheapest
  decisive test and outcome map; parking/kill criterion; revival condition.

- **History `H#`:** changed record type and old/new versions; exact before/after
  definitions or claim statements and diff; change class; explicit reason not
  inferred from the class or diff; every affected record marked for retention,
  version sensitivity, invalidation, or recertification; reusable probes and
  their transport map or argument.

## Independent classifications

- Mathematical status: `DEFINITIONAL`, `CONJECTURE`, `SUPPORTED`, `REFUTED`,
  `UNRESOLVED-CONFLICT`. Reserve `REFUTED` for a checked counterexample to the
  literal claim; a local failure does not silently narrow `claim_scope`.
- Evidence kind: `EXACT-DERIVATION(method)`, `EXACT-FINITE(method)`,
  `NUMERICAL(method)`, `OBSERVED(method)`, `SOURCE-LOCATED(S#)`,
  `SOURCE-APPLICABLE(S#)`, `HEURISTIC`, `ANALOGY`.
- Semantic fidelity: `DIRECT` for the same objects and definitions;
  `ENCODING-CHECKED(mapping)` for a checked encoding;
  `TRANSFER-CHECKED(mapping,hypotheses)` for a checked transfer with matched
  hypotheses; `UNCHECKED` when correspondence is not established.
- Workflow disposition: `ACTIVE`, `PARKED(reason,revival)`, `SPLIT`, `MERGED`,
  `SELECTED`, `REJECTED(reason)`.
- Change class: `SEMANTIC`, `EQUIVALENT`, `SCOPE`, `REGIME-SPLIT`, `AUXILIARY`.
- Applicability: `SOURCE-LOCATED` until objects, maps, assumptions, and scope
  match; `SOURCE-APPLICABLE` after that check.

`claim_scope` is the proposition's quantified domain;
`evidence_coverage` is only what was examined. A finite or numerical check does
not narrow a broader claim. Formal checking certifies the encoded statement;
its mapping to the mathematical claim is recorded separately as semantic
fidelity.

## Ownership and versioning

A probe owns procedure and raw outcome. A source-applicability record owns the
imported statement and local mapping. Evidence owns the proposition admitted
for or against a claim, with coverage and fidelity. A claim links evidence.

Version a formalism, candidate, or claim when its definition, regime, scope, or
dependencies change. Preserve the old record and prior evidence. Classify the
diff, follow explicit dependencies, and mark every affected claim, candidate
relation, derived cell, probe, evidence, search, source applicability, and
direction as `retained`, `version-sensitive`, `invalidated`, or
`requires-recertification`. Transport an old probe only with its recorded map
or argument.

## Derived contrast view

Generate a compact view only when it helps the decision. Include applicable
axes and trace consequential cells to canonical records. Use `LACKS` for a
meaningful absence, `UNKNOWN` for an unresolved applicable property, and `N/A`
only in this derived view for an inapplicable axis.

## Serialize snapshots and deltas

The first chat tracer emits a `SNAPSHOT` after the brief. It contains every
current durable record, including parked records and older versions required by
live dependencies or revival conditions; omit empty registries and derived
views. Later tracers emit a `DELTA` tied to its base ledger ID and containing
every changed record. A non-discriminating probe still adds `P#` and `E#`; only
decision state may be unchanged. Replace a delta chain with a snapshot when
the current state is no longer locally reconstructible.

Compact semicolon-delimited records and stable-ID references are encouraged.
Compactness may remove repeated prose, never exact definitions, version pins,
scope, coverage, classifications, dependencies, dispositions, or source maps.
For written artifacts, keep the standalone brief in `<topic>.md` and this
ledger in `<topic>.exploration-ledger.md`, linked both ways. A handoff includes
the complete current ledger and enough history for every live dependency and
revival condition.
