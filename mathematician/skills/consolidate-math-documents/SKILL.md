---
name: consolidate-math-documents
description: Consolidate selected mathematical documents into one self-contained canonical target, then safely retire the old source documents and companions.
disable-model-invocation: true
---

# Consolidate Mathematical Documents

Produce one coherent mathematical account without silently changing
definitions, assumptions, validity boundaries, claim status, or provenance.
This skill reconciles existing work; genuinely new mathematics remains
uncertified.

## Choose the run

- **Preview:** return a consolidation, conflict, and prospective-retirement map
  in conversation; create, edit, move, and delete nothing.
- **New target:** require an explicit absent Markdown target path.
- **Existing target:** require an explicit canonical target and use it as the
  writable baseline.

Require an explicit, de-duplicated source list and at least two mathematical
documents in total. Discover repository-wide inputs only when requested. The
target is never a source. Classify the relationship as **same-theory
unification** or **cross-theory synthesis**; ask when the choice is ambiguous.
Drafts and conjectures keep their status.

For a writable run, follow the shared [research-memory
protocol](../research-mathematics/references/research-memory.md) and use its
[CLI](../research-mathematics/scripts/research_memory.py). Exactly one target
Markdown/database pair is writable. Sources remain immutable and their
companions read-only until the target closes; successful consolidation then
retires every exact source pair. Read the [source-retirement
protocol](references/source-retirement.md) before the first writable mutation
and use its helper.

## Preflight and freeze

Resolve every path without following a source symlink. For an existing target,
perform the shared writable-home preflight. For a new target, draft in the
workpad and create the pair only after the candidate stabilizes. A located but
missing target companion stops for recovery or explicit reinitialization.

For each source:

- read the Markdown before its companion;
- validate and `export` a located companion read-only;
- stop for confirmation when a locator names a missing database;
- treat a locator-less document as canonical-only; if its canonical-stem
  database exists, require explicit routing instead of guessing ownership;
- identify native artifacts and inbound links that must survive retirement.

Create one OS-temporary workpad. Freeze exact source bytes, resolved portable
paths, roles, canonical SHA-256 values, companion revisions and byte digests,
semantic exports, and the target baseline. Build an exact retirement manifest
for the explicitly selected Markdown-and-located-companion pairs and run the
retirement helper's non-mutating preflight. Any unsafe or changed source stops
the writable run before publication; preview reports the same blockers without
creating a manifest file.

## Reconcile every unit

Inventory every definition, notation choice, ambient structure, assumption,
claim and epistemic status, proof dependency, validity boundary,
counterexample, obligation, citation, relative link, native artifact,
semantic research key and alias, card, canonical link, origin, and card edge.
Give each exactly one disposition:

- `integrate`;
- `merge-equivalent`;
- `retain-as-alternative`;
- `target-only`;
- `target-card`;
- `retain-native-artifact`;
- `discard-with-source`; or
- `unresolved-conflict`.

Every disposition needs an exact target location or exclusion reason.
`discard-with-source` is an explicit decision that the unit may disappear with
the retired source; it cannot contain mathematics needed to understand or
trust the target.

Establish one target vocabulary. Equal names do not establish equal objects.
Check quantifiers, domains, assumptions, and status before merging statements.
Same-theory work may unify verified equivalents; cross-theory work keeps
distinct modules and states translations and applicability maps. Preserve
coherent alternatives and unresolved conflicts explicitly. Neither modification
time nor an existing target wins a conflict, and consolidation never upgrades
a claim to `PROVED`.

Establish human-semantic target research keys for durable mathematical
subjects. Use one primary key only for the same subject; express other
relationships as typed card links. Preserve an equivalent legacy opaque ID as
an alias, not as a target primary key. Several primary keys may address one
section when splitting the exposition would be artificial.

## Build the target pair

Draft the complete self-contained target in the workpad. Include every
accepted definition, assumption, proof or stated support, validity boundary,
load-bearing negative result, and unresolved conflict needed after source
retirement. Rewrite relative links, preserve citations, resolve anchor and
theorem-label collisions, and keep deliberate native artifacts linked in
place unless their promotion was explicitly requested.

After the target structure stabilizes, use the shared deterministic
canonical-section tool to assign its generated anchors and visible key labels;
never copy or hand-edit those markers. Scan and check the target before making
database links. Use exact key or alias lookup before broad source-memory
search, and expand only selected source cards.

Add concise consolidation provenance naming each retired source path, canonical
and companion digests, Git recovery revision when available, source role,
integrated and discarded scope, and unresolved conflicts. The reconciliation
matrix remains transient.

Curate source databases semantically rather than merging them. Accepted
mathematics belongs in Markdown. Retain only reusable obligations, revivable
directions, demonstrated obstructions, negative results, or material
source-applicability knowledge. Every materially influential source card adds
a `card_origin` with its last-known locator, semantic slug, content digest, and
target-specific applicability mapping. The target card stays self-contained;
an origin may point to a retired source.

For slugs:

1. add an absent semantic slug;
2. map equivalent content to an existing card and add its origin;
3. synthesize a revision-checked card or choose a genuinely distinguishing
   slug when meanings differ; and
4. recreate an edge only when both endpoints survive and the relation remains
   useful.

Source `integrated` state, aliases, and canonical links are never copied
mechanically. Resolve subject identity and use target-appropriate disposition,
claim status, relation, and applicability. An integrated target card requires
an explicit `integrated-at` link to a target research key.

## Publish, retire, and finish

Before publication, revalidate every frozen source digest and database
revision, the target baseline, and the complete retirement manifest. Then:

1. write or update the target canonical document;
2. check its research-key structure, ensure its schema-3 companion, and add or
   preserve the locator;
3. apply one revision-checked batch of canonical items, aliases, cards, typed
   canonical links, origins, and card edges;
4. explicitly refresh changed canonical items, review every affected card
   link at the current snapshots, run `check`, use exact lookups to verify the
   crosswalk, `show` changed cards, and `export` the final target;
5. revalidate the retirement manifest and retire its exact source pairs;
6. confirm the sources are absent and the target still validates; and
7. delete the workpad.

Tracked deletions remain unstaged; staging and commits require separate
authorization. A writable run is complete only when the target pair validates,
every source unit has a disposition, every authorized source pair is absent,
and no completed workpad or merge report remains.

If the target changes a theorem, proof, or assumption boundary rather than
reconciling existing material, mark it unresolved or uncertified and recommend
`$research-mathematics`.

On source or target drift, stop before publication. Canonical, database, or
validation failure retains the workpad and reports every changed artifact. A
retirement failure leaves the validated target in place but makes the run
incomplete: retain the workpad and report exact deleted and remaining paths.
Never restore over a recreated or concurrently edited path. A cleanup-only
failure reports the residual workpad without invalidating the closed target.
Section and link snapshot matches report curation state only; consolidation
never calls them logical or mathematical freshness.
