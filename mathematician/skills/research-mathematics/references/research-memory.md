# Research Memory Protocol

Read this reference for an authorized file-backed round run by
`research-mathematics`, `explore-mathematical-structure`,
`explore-proof-strategies`, `destroy-theory`, or `audit-assumptions`.
Chat-only work and read-only review create no files.

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
database. Other theory databases are read-only. Different home theories may be
researched concurrently; parallel lanes for the same theory return to one
coordinator and one final database transaction.

On the first authorized file-backed round, add this frontmatter to the
canonical Markdown document and initialize the empty companion with
[`research_memory.py`](../scripts/research_memory.py):

```yaml
research_memory:
  path: ./<stem>.research.sqlite
  schema: 1
  optional_for_understanding: true
```

Use the canonical stem by default: `theory.md` pairs with
`theory.research.sqlite`. Store a relative canonical path in the database. If
the document already names a missing companion, report the loss and continue
canon-only; create a replacement only with explicit authorization.

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

Open every non-home database read-only. A foreign card is a lead, not a live
dependency. When it materially affects local work, create a self-contained
local snapshot card. Its `origin_uri` identifies the source database and
includes the foreign semantic slug as a fragment, its `origin_digest` records
the foreign card's content digest, and its detail gives an explicit mapping of
objects, hypotheses, and unmatched assumptions. Accepted cross-theory
mathematics is restated in a canonical document; databases never have
cross-file foreign keys.

## Use cohesive cards

A card is a context packet, not a normalized ledger fragment. Its summary must
state enough scope and reasoning to be useful without traversing an edge or
joining another record. Use a stable semantic slug rather than an opaque row
number.

Core fields are: kind, title, Markdown summary and optional detail, workflow
disposition, optional claim status, reason, next test, revival condition,
canonical anchor, optional foreign origin, revision, digest, and timestamps.
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

## Know schema v1

The companion uses standard SQLite features available through Python 3.9's
standard library. It deliberately avoids `STRICT` tables, FTS5, JSON1, WAL,
graph libraries, and migration frameworks. It sets `PRAGMA user_version=1`,
enables foreign keys for every writable connection, and contains three tables:

- `meta` has one row with the schema version, theory slug, canonical path
  relative to the database, last consolidated canonical SHA-256, monotonically
  increasing database revision, last applied round identifier and batch
  digest, and UTC creation/update timestamps.
- `card` uses the semantic `slug` as its primary key. It stores free-form
  `kind`, `title`, self-contained `summary_md`, optional `detail_md`,
  `disposition`, independent optional `claim_status`, `reason`, `next_test`,
  `revival_condition`, `canonical_anchor`, paired `origin_uri` and
  `origin_digest`, card `revision`, normalized-content `content_sha256`, and
  timestamps.
- `edge` stores local `source_slug`, free-form `relation`, local
  `target_slug`, and optional `note_md`. Its composite primary key is
  `(source_slug, relation, target_slug)`; both slugs are cascading foreign
  keys into `card`.

Kinds and relations remain extensible. The database constraints require a
next test for `open` and `active`, a revival condition for `parked`, a reason
for `rejected`, a canonical anchor for `integrated`, and either both origin
fields or neither.

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
apply  --db PATH --input JSON_FILE
search --db PATH [--db PATH ...] [--text TEXT]
       [--state STATE ...] [--kind KIND ...] [--limit N]
show   --db PATH --slug SLUG
check  --db PATH
```

All commands emit JSON. `search`, `show`, and `check` open databases read-only
and never create a missing file. `apply` mutates one existing home database
with one `BEGIN IMMEDIATE` transaction. Its batch carries a round identifier,
expected database revision, post-edit canonical digest, and explicit card and
edge operations. Updates and deletions require expected card revisions; there
are no implicit upserts. An immediate retry of the same round and batch digest
is idempotent.

`init` requires an existing Markdown canonical document, derives the companion
name when `--db` is omitted, refuses every existing target, and creates a
`DELETE`-journal database. `search` accepts repeated `--db` options, defaults
to `active`, `open`, and `parked`, and searches slug, title, summary, and detail
with parameterized `LIKE`; rejected and integrated cards require an explicit
state filter. `show` returns a complete card and its immediate local edges.
`check` runs schema/version, quick-integrity, foreign-key, canonical-path and
digest, card-constraint, and rollback-journal/WAL/SHM-sidecar checks. Canonical
digest staleness is reported as `requires_review`, not as mathematical
invalidity.

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
rejected. Schema v1 intentionally stores only the last applied round, so round
identifiers must be unique; an older identifier is not a durable global
deduplication key. Every operation is validated before commit; a conflict or
invalid operation rolls back the whole batch.

The tool edits neither the canonical document nor the workpad and performs no
Git operations. It never mechanically parses, imports, migrates, rewrites, or
deletes legacy ledgers. An agent may read an existing user-generated ledger as
source material during a later authorized round and semantically curate only
worthwhile content into cards. After successful consolidation, report the old
file as eligible for user-approved removal and otherwise leave it untouched.
