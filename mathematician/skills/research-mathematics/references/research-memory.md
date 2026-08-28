# Research Memory Protocol

Read this reference for an authorized file-backed round run by
`research-mathematics`, `explore-mathematical-structure`,
`explore-proof-strategies`, `destroy-theory`, or `audit-assumptions`, and for
multi-pair consolidation coordinated by `consolidate-math-documents`.
Chat-only work and read-only review create no files.

Schema 2 is the only supported companion schema. The CLI rejects every other
schema version and provides no migration or compatibility path.

The protocol has three layers:

1. The canonical Markdown document is the authoritative, self-contained
   mathematical account.
2. Its `<stem>.research.sqlite` companion contains curated noncanonical
   research memory.
3. One generated OS-temporary workpad contains raw round state and is deleted
   only after successful consolidation.

The companion is optional for understanding the canonical mathematics. Losing
it may lose useful research history, but never a hypothesis, definition,
argument, or counterexample needed to interpret or trust the canonical result.

## Establish one home theory

One round owns exactly one writable pair: a canonical document and its home
database. Every other database is a source or foreign companion and remains
read-only. Different home theories may be researched concurrently; parallel
lanes for the same theory return to one coordinator and one final database
transaction.

Read the canonical document, inspect its frontmatter, and complete this
preflight before creating a workpad or doing research:

1. When a locator is present, resolve it relative to the canonical document
   and run `ensure --canonical CANONICAL --db LOCATOR --require-existing`. A
   missing located companion may represent lost research memory: stop, report
   its exact path, and request recovery or reinitialization direction. Do not
   create a replacement or proceed with a writable round.
2. When no locator is present, run `ensure --canonical CANONICAL` without
   `--require-existing`.
   This creates the default companion when absent or validates the exact
   existing pair without changing it. Only after success, add this frontmatter
   to the canonical Markdown document:

```yaml
research_memory:
  path: ./<stem>.research.sqlite
  schema: 2
  optional_for_understanding: true
```

New-target consolidation is the sole exception to that ordering because its
canonical document does not exist yet. The consolidation coordinator first
drafts the candidate in one OS-temporary workpad. Immediately before
publication it re-checks that the explicitly selected target path is absent,
creates the canonical Markdown document, runs `ensure` for that new writable
home, adds the locator, and closes with one apply batch. It never ensures a
source companion.

Use the canonical stem by default: `theory.md` pairs with
`theory.research.sqlite`; `ensure` also uses that stem as the default theory
slug. Store a relative canonical path in the database. The locator becomes
authoritative once written, even if the canonical document is later renamed.
Use the revision-checked `relink` command after a move or rename makes the
database's stored canonical path stale. The CLI never edits the locator or
moves either file.

Run `ensure` only for the writable home pair. A nested specialist, report-only
run, explanation, consolidation source, or foreign-theory lookup opens only
existing databases read-only. It reports a missing source rather than creating
one. This boundary preserves both authorization and the one-writer invariant.

Companion databases are ordinary Git-tracked research artifacts, but a skill
does not stage or commit them without separate authorization. Do not binary-
merge competing branch versions of one database. Select one version and
semantically reapply worthwhile cards from the other.

When the home pair is inside a Git repository, inspect and report the
companion's tracking state at closure. A newly created companion remains
untracked until the user separately authorizes staging; never imply that file
creation alone made it durable in Git. Tracking status does not change the
mathematical validity of an otherwise successful close.

## Retrieve without importing authority

Read the canonical document first. Query summaries in this order:

1. `active`, `open`, and `parked` cards from the home theory;
2. `rejected` cards relevant to a route now under consideration;
3. foreign theory companions only when a concrete question warrants them.

Open every non-home database read-only and never pass it to `ensure`. A foreign
card is a lead, not a live dependency. When it materially affects local work,
create a self-contained local snapshot card and attach one or more provenance
rows. Each row records the source database locator, source semantic slug,
source content digest, and a Markdown applicability mapping of objects,
hypotheses, and unmatched assumptions. Prefer a stable repository-relative
source locator when the source and target are versioned together. A
repository-local locator must be a POSIX path relative to the target database;
an external source must use a URI. Accepted
cross-theory mathematics is restated in a canonical document; provenance rows
are snapshots, not cross-file foreign keys.

## Use cohesive cards

A card is a context packet, not a normalized ledger fragment. Its summary must
state enough scope and reasoning to be useful without traversing an edge or
joining another record. Use a stable semantic slug rather than an opaque row
number.

Core fields are: kind, title, Markdown summary and optional detail, workflow
disposition, optional claim status, reason, next test, revival condition,
canonical anchor, revision, digest, and timestamps. Optional provenance lives
in separate `card_origin` rows so a synthesized card can name multiple sources
without fragmenting its mathematical account.
The card's `content_sha256` covers only the cohesive card packet, not origins
or navigational edges. Origin changes consume a database revision in the
enclosing batch but do not change the card revision.
Kinds and edge relations are extensible; useful kinds include `direction`,
`proof-route`, `obstruction`, `counterexample`, `proof-obligation`,
`assumption-relaxation`, `source-applicability`, and `verification-lesson`.

Keep two status axes separate:

- disposition: `open`, `active`, `parked`, `rejected`, `integrated`;
- claim status: `conjectural`, `supported`, `refuted`, `proved`, `unresolved`,
  or absent for nonclaims.

`Rejected` means that a research route is not worth current investment;
`refuted` means evidence defeats a mathematical claim. Open and active cards
need a next test, parked cards a revival condition, rejected cards a reason,
and integrated cards a canonical anchor.

Retain a card only when it records a live direction, prevents likely repeated
work, captures a structural obstruction or useful counterexample, preserves a
realistic revival condition, or records reusable source applicability. Put
accepted and load-bearing mathematics in the canonical document. Discard
incidental attempts and generic failures.

Edges are sparse navigation aids between local cards. A card remains
intelligible without them.

## Consolidate pairs semantically

When the requested job is to combine multiple canonical documents and their
companions, use `consolidate-math-documents` as the sole coordinator. Choose
one writable target pair, treat every non-target input pair as a read-only
source, and never create a missing source companion. The coordinator uses
`export` to
freeze source contents in the workpad, integrates accepted mathematics into a
self-contained target canonical document, and applies one curated batch to the
target database. There is no mechanical CLI merge or import command.

Record a workpad mapping from each `(source locator, source slug)` to its local
target slug. An absent target slug may be added. An identical existing card is
a no-op. When the same slug names different content, either synthesize one
revision-checked target card, choose a genuinely distinguishing semantic slug,
or discard the source card; never silently upsert or append an opaque numeric
suffix. Rewrite an edge only when both endpoints survive and skip an edge that
already exists. Attach a `card_origin` row for every source card that materially
influences a retained local card, including an explicit applicability mapping.
Do not mechanically copy a source card's `integrated` disposition or canonical
anchor; select target-appropriate state and applicability.

## Know schema v2

The companion uses standard SQLite features available through Python 3.9's
standard library. It deliberately avoids `STRICT` tables, FTS5, JSON1, WAL,
graph libraries, and migration frameworks. It sets `PRAGMA user_version=2`,
enables foreign keys for every writable connection, and contains four tables:

- `meta` has one row with the schema version, theory slug, canonical path
  relative to the database, last consolidated canonical SHA-256, monotonically
  increasing database revision, last applied round identifier and batch
  digest, and UTC creation/update timestamps.
- `card` uses the semantic `slug` as its primary key. It stores free-form
  `kind`, `title`, self-contained `summary_md`, optional `detail_md`,
  `disposition`, independent optional `claim_status`, `reason`, `next_test`,
  `revival_condition`, `canonical_anchor`, card `revision`, normalized-content
  `content_sha256`, and timestamps.
- `edge` stores local `source_slug`, free-form `relation`, local
  `target_slug`, and optional `note_md`. Its composite primary key is
  `(source_slug, relation, target_slug)`; both slugs are cascading foreign
  keys into `card`.
- `card_origin` stores a local `card_slug`, `source_locator`, source semantic
  `source_slug`, source card `source_digest`, and self-contained
  `applicability_md`. Its composite primary key is
  `(card_slug, source_locator, source_slug, source_digest)` and its local card
  foreign key cascades on deletion. An index on `(source_locator, source_slug)`
  supports provenance lookup. A source locator is descriptive provenance,
  never a cross-database constraint.

Kinds and relations remain extensible. The database constraints require a
next test for `open` and `active`, a revival condition for `parked`, a reason
for `rejected`, and a canonical anchor for `integrated`. Provenance source
fields and applicability mappings are nonempty, and source digests are
lowercase SHA-256 values.

## Keep one transient workpad

Create one generated directory below the OS temporary directory and record its
exact path and round identifier. Candidate versions, assumption maps, proof
DAG drafts, probe logs, source notes, specialist reports, finding
dispositions, verifier records, checker output, and the final JSON batch live
there. Raw workpad text never enters SQLite.

Content-bound candidate and report identifiers are round-local. Native proof
sources, certificates, programs, or datasets that must survive are promoted
as deliberate artifacts and linked from the canonical document.

## Close in a recoverable order

1. Integrate accepted mathematics, load-bearing negative results, exact open
   obligations, and a concise verification/provenance summary into the
   canonical document.
2. Curate only reusable noncanonical memory into one JSON batch.
3. Apply the batch to the home database in one transaction.
4. Run `check`, require `canonical_status` to be `current` for this close, then
   `show` every added or materially changed card. A `requires_review` warning
   remains non-mathematical in general, but during closure it signals a
   post-apply edit or race that must be reconciled before cleanup.
5. Delete only the generated round workpad.

If canonical editing, database application, or validation fails, retain the
workpad and report its path. If only workpad deletion fails, report the exact
residual path; the canonical document and database remain closed.

## Use the shared CLI

The standard-library tool is
[`research_memory.py`](../scripts/research_memory.py):

```text
init   --canonical PATH --theory SLUG [--db PATH]
ensure --canonical PATH [--theory SLUG] [--db PATH]
       [--require-existing]
relink --db PATH --canonical NEW_PATH --expected-canonical OLD_PATH
       --expected-database-revision N
apply  --db PATH --input JSON_FILE
search --db PATH [--db PATH ...] [--text TEXT]
       [--state STATE ...] [--kind KIND ...] [--limit N]
show   --db PATH --slug SLUG
export --db PATH
check  --db PATH
```

All commands emit JSON. `search`, `show`, `export`, and `check` open databases
read-only and never create a missing file. `apply` mutates one existing home
database with one `BEGIN IMMEDIATE` transaction. Its batch carries a round
identifier, expected database revision, post-edit canonical digest, and
explicit card, origin, and edge operations. Updates and deletions require
expected revisions or exact keys; there are no implicit upserts. An immediate
retry of the same round and batch digest is idempotent.

`ensure` requires an existing Markdown canonical document. It derives
`<stem>.research.sqlite` and the exact canonical stem as the theory slug when
they are omitted. An absent target is created in `DELETE` journal mode unless
`--require-existing` is present; an existing target is validated without
mutation. A theory or canonical-path mismatch, malformed database, symlink, or
missing required target is an error. Canonical digest staleness is returned as
`requires_review` rather than silently synchronized.

`init` is the strict lower-level creation command retained for explicit use.
It requires a theory slug and an existing canonical Markdown document,
refuses every existing destination, and creates schema 2. Database-aware
skills use `ensure` for normal writable-home preflight.

`relink` is the explicit, revision-checked metadata repair for a moved or
renamed canonical document. It changes only the relative canonical path,
database revision, and update timestamp; it preserves the stored canonical
digest, last-round metadata, cards, origins, and edges. `search` accepts
repeated `--db` options, defaults to `active`, `open`, and `parked`, and
searches slug, title, summary, and detail with parameterized `LIKE`; rejected
and integrated cards require an explicit state filter. `show` returns a
complete card, all its provenance rows, and its immediate local edges.
`export` returns a deterministic full read-only snapshot for source curation.
It contains complete metadata, all cards in every disposition, all origins,
and all edges in stable order, plus a SHA-256 `export_digest` over that semantic
payload.
`check` runs schema/version, quick-integrity, foreign-key, canonical-path and
digest, card/provenance constraints, and rollback-journal/WAL/SHM-sidecar
checks.

### Build an apply batch

The JSON object has exactly these top-level fields:

```json
{
  "round_id": "2026-08-28-route-screen",
  "batch_digest": "<computed as below>",
  "expected_database_revision": 3,
  "canonical_digest": "<SHA-256 of the post-edit canonical file>",
  "card_operations": [
    {
      "op": "add",
      "card": {
        "slug": "compactness-route",
        "kind": "proof-route",
        "title": "Compactness route after truncation",
        "summary_md": "A self-contained account of the route and its scope.",
        "disposition": "open",
        "claim_status": "unresolved",
        "next_test": "Prove uniform tightness for the truncated family."
      }
    }
  ],
  "origin_operations": [
    {
      "op": "add",
      "card_slug": "compactness-route",
      "source_locator": "../related/related.research.sqlite",
      "source_slug": "truncation-route",
      "source_digest": "<source card content SHA-256>",
      "applicability_md": "Map the source family to the local truncated family; uniform tightness remains unmatched."
    }
  ],
  "edge_operations": []
}
```

Card operations are explicit:

- add: `{"op":"add","card":{...}}`;
- update: `{"op":"update","slug":"...","expected_revision":2,
  "changes":{...}}`;
- delete: `{"op":"delete","slug":"...","expected_revision":2}`.

Edge operations are
`{"op":"add","source_slug":"...","relation":"...","target_slug":"...",
"note_md":"..."}` and the corresponding `delete` form without `note_md`.

Origin operations are
`{"op":"add","card_slug":"...","source_locator":"...",
"source_slug":"...","source_digest":"...","applicability_md":"..."}`
and the corresponding exact-key `delete` form without `applicability_md`.
Change an applicability mapping with an ordered exact delete followed by add;
schema 2 has no implicit origin update operation.

Within one apply transaction, operations run in card, origin, then edge order.
Any failure rolls back all three groups. Origin-only and edge-only batches
still consume the enclosing database revision.

Compute `batch_digest` over the batch *without* its `batch_digest` member. The
exact rule is SHA-256 of the UTF-8 bytes from:

```python
json.dumps(
    batch_without_batch_digest,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
)
```

The CLI verifies this digest before opening an idempotent-retry path.
Immediately reusing the last round identifier with different valid content is
rejected. Schema v2 intentionally stores only the last applied round, so round
identifiers must be unique; an older identifier is not a durable global
deduplication key. Every operation is validated before commit; a conflict or
invalid operation rolls back the whole batch.

The tool edits neither the canonical document nor the workpad and performs no
Git operations. It never mechanically parses, imports, migrates, rewrites, or
deletes legacy ledgers. An agent may read an existing user-generated ledger as
source material during a later authorized round and semantically curate only
worthwhile content into cards. After successful consolidation, report the old
file as eligible for user-approved removal and otherwise leave it untouched.
