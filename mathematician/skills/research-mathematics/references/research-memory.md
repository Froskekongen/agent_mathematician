# Research Memory Protocol

Read this protocol completely for an authorized writable theory round. Nested
and report-only work may query an existing companion through exact `lookup`,
summary `search`, and selective `show`; it creates no theory artifact and does
not need the writable lifecycle.

Schema 3 is the only supported schema. Research state has three destinations:

1. **Canonical Markdown:** authoritative, self-contained mathematics.
2. **`<stem>.research.sqlite`:** a semantic crosswalk and curated reusable
   noncanonical memory.
3. **One OS-temporary workpad:** raw round state, deleted after a valid close.

The canonical document must remain understandable without its companion.
Native proof sources, certificates, programs, and datasets remain deliberate
artifacts linked from the canonical account rather than database payloads.

## Roles and ownership

| Role | Database access | Filesystem effect |
|---|---|---|
| Writable-home coordinator | One home database writable; others read-only | Owns the canonical update and one workpad |
| Nested or report-only specialist | Existing databases read-only | No theory files or workpad |
| Foreign/source lookup | Existing databases read-only | Missing databases remain missing |
| Consolidation coordinator | One target database writable; sources read-only | Retires exact sources only after target closure |

One round has one writer and one final database transaction. Parallel lanes for
the same theory return findings to that writer. Different home theories may
proceed concurrently. Never binary-merge competing database versions; select
one and semantically reapply worthwhile records from the other.

## Establish the home pair

Read the canonical document and preflight its key structure before creating a
workpad:

| Canonical state | Required action |
|---|---|
| Locator present | Resolve it relative to the document; run `ensure` with `--require-existing`. A missing companion stops the writable round. |
| No locator | Run `ensure` without `--require-existing`; it creates or validates the canonical-stem companion. Add the locator only after success. |
| New consolidation target | Draft in the workpad; create and key the stabilized Markdown target, then run `ensure`. Never ensure a source. |

Default naming is `theory.md` with `theory.research.sqlite`; the exact canonical
stem is also the default theory slug. Add:

```yaml
research_memory:
  path: ./theory.research.sqlite
  schema: 3
  optional_for_understanding: true
```

The locator is authoritative after publication. Use revision-checked `relink`
after a deliberate move or rename; the database CLI neither moves files nor
edits Markdown. Companions are intended to be Git-tracked, but skills leave
staging and commits to separate authorization and report an untracked home
companion at closure.

## Address canonical sections

A **research key** is the durable, human-readable identity of a canonical
mathematical subject. Use a lowercase ASCII kebab noun phrase such as
`implicit-young-evaluation` or `rank-drop-obstruction`. It names the object,
mechanism, theorem, obstruction, or mathematical job—not its sequence number,
date, temporary status, or current proof disposition. A materially changed
denotation gets a new key; a mere heading edit does not. Use one optional
`theory/key` qualification when distinct theories would otherwise collide.

One section may have several primary keys when splitting its exposition would
be artificial. Reuse a key only for the same subject. Give related but
different subjects distinct keys and express their relationship in the
crosswalk. Preserve opaque inherited identifiers such as `IR-COMP-1` only as
aliases of an equivalent semantic key.

The standard-library
[canonical-section CLI](../scripts/canonical_sections.py) owns the generated
Markdown representation. A keyed section has one namespaced HTML anchor per
key and one visible key line, conceptually:

```markdown
<a id="research-key--implicit-young-evaluation"></a>
<a id="research-key--rank-drop-obstruction"></a>

### Candidate theorem: implicit Young evaluation

**Research keys:** `implicit-young-evaluation`, `rank-drop-obstruction`
```

Use `key-set` to assign or change keys; never hand-edit generated anchors or
the visible key line. The tool accepts only its addressable-section dialect:
BOM-free UTF-8, optional top-of-file front matter, column-zero ATX headings,
and well-formed backtick or tilde fences. Exact generated research-key anchors
are the dialect's only raw HTML; unsupported CommonMark raw-HTML block openers
are rejected rather than partially parsed. The tool also rejects duplicate
keys, orphan or malformed markers, unsupported structural headings, and
unclosed fences. `key-set` additionally rejects symlink and non-regular
mutation targets.
Exactly one blank line separates a generated anchor block from its heading so
CommonMark terminates the raw HTML block.

`scan` returns section metadata, hierarchy, byte/line spans, keys, anchors,
document digest, and versioned section fingerprints without returning section
bodies. `show --key` returns exactly one selected subtree starting at its
heading, including the visible key line but not the preceding anchor block.
`check` validates the structure. Mutation requires the expected document
digest, takes a nonblocking exclusive advisory lock on the regular target,
prepares and fsyncs a same-directory replacement while holding that lock, then
rechecks the path's inode, mode, and digest immediately before atomic
replacement. It holds the lock through directory fsync, inserts or replaces
only the generated representation, and preserves every other original byte and
the file mode.
This is a cooperative locked digest guard, not an absolute compare-and-swap
against editors that ignore advisory locks. If replacement commits but
directory durability cannot be confirmed, the CLI reports that state
explicitly with the installed digest. Pass `--key` more than once to assign
several primary keys to the selected `--heading-line`.

A section extends through its descendant headings until the next heading of
equal or shallower level. Its versioned content fingerprint includes heading
ancestry and the full section subtree, normalizes only line endings, and
excludes generated research-key markers. A child edit therefore changes the
parent fingerprint conservatively. The raw whole-document digest remains the
exact byte precondition used by the cooperative mutation guard.

## Retrieve selectively

Start from the canonical question, not from a database dump:

1. Use a supplied research key or citation directly. Otherwise `scan` the
   canonical document to discover keys without loading section bodies.
2. Run exact `lookup --canonical <key-or-alias>` to retrieve the resolved item
   and compact linked-card summaries.
3. Use reverse `lookup --card <semantic-slug>` when starting from a known card.
4. Run broader `search` only when no suitable key is known or exact lookup is
   insufficient.
5. Use `show` only for cards selected from those summaries, or the section
   tool's `show --key` for one selected canonical section.

`lookup` and `search` do not return card bodies. Detailed `detail_md` lives in a
separate `card_body` table so summary paths cannot accidentally scan or expose
all durable notes. Legacy aliases resolve to their primary semantic key and are
reported as aliases rather than promoted to primary identifiers.

Read the canonical account before relying on noncanonical memory. In a writable
home round retrieve home `active`, `open`, and `parked` summaries first; inspect
`rejected` cards only when reconsidering a similar route, and foreign
companions only for a concrete question.

## Curate schema-3 memory

The companion contains:

- `canonical_item`: one record per semantic research key, bound to a parsed
  canonical section and its indexed fingerprint;
- `canonical_alias`: alternate identifiers resolving to one primary key;
- `card` and `card_body`: compact card identity/summary apart from detailed
  Markdown;
- `card_canonical_link`: a normalized many-to-many, typed crosswalk between
  cards and canonical items, with review snapshots;
- `card_origin`: provenance and applicability for local cards derived from
  source or foreign memory; and
- `edge`: sparse navigation between local cards.

The `contract` command emits the exact fields, relation vocabulary, and batch
operation shapes. Canonical-item operations are explicit
`add`/`update`/`refresh`/`delete`; card-canonical-link operations are explicit
`add`/`review`/`delete`, and alias operations are `add`/`delete`. Link review
and deletion require the expected link revision. Link relations are
`same-subject`, `addresses`, `supports`, `constrains`, `tests`, `implements`,
and `integrated-at`. There are no implicit upserts.

A card is a cohesive Markdown context packet with a semantic slug and remains
understandable without following a link. If its subject is exactly the same as
a canonical item, use that canonical key exactly as its card slug and use the
`same-subject` relation. Otherwise choose an independent semantic slug and a
truthful typed relation. An `integrated` card requires an explicit
`integrated-at` link; it has no scalar canonical anchor.

Keep disposition and mathematical status separate:

- disposition: `open`, `active`, `parked`, `rejected`, `integrated`;
- claim status: `conjectural`, `supported`, `refuted`, `proved`, `unresolved`,
  or absent.

`Rejected` allocates research effort; `refuted` records mathematical evidence.
Open and active cards require a next test, parked cards a revival condition,
and rejected cards a reason. Retain only live directions, reusable obstructions
or counterexamples, costly results likely to be repeated, realistic revival
conditions, open obligations, or material source applicability. Accepted and
load-bearing mathematics belongs in the canonical document; incidental
attempts expire with the workpad.

Foreign findings are leads rather than live dependencies. If one materially
affects the home theory, create a self-contained local card and a `card_origin`
containing its last-known source locator, source slug, source card digest, and
an applicability mapping of objects, hypotheses, and unmatched assumptions.
Repository-local locators are POSIX paths relative to the target database;
external sources use URIs. The locator may later become unavailable after
authorized consolidation retirement; provenance remains valid and is not a
cross-database foreign key.

## Interpret snapshots honestly

Each returned link has these independent status fields:

- `canonical_key_present`;
- `database_document_match`;
- `canonical_item_section_match`;
- `reviewed_document_match`;
- `reviewed_section_match`; and
- `reviewed_card_revision_match`.

`refresh` acknowledges the parser-derived current location and fingerprint of
a canonical item. `review` records that a curator reconsidered one typed link
against current snapshots. Neither operation checks a theorem, proves a
dependency graph complete, or establishes logical or mathematical freshness.
Describe these results as document, section, card-revision, or review-snapshot
matches—never simply “fresh.” An unchanged section with a changed document may
still depend on altered context elsewhere.

## Work and close

Create one generated directory under the OS temporary directory and record its
path and round ID. Keep candidates, proof-DAG drafts, assumption maps, probes,
source notes, specialist reports, manifests, verifier output, and the final
batch there. Raw workpad content never enters SQLite.

Close in this order:

1. Integrate accepted mathematics, load-bearing negative results, exact open
   obligations, and concise provenance into the canonical document.
2. Use the canonical-section CLI to set semantic keys, then `check` the
   document and freeze its digest.
3. Curate reusable noncanonical material and its typed crosswalk into one
   explicit batch. Refresh every changed canonical item and review every added
   or affected card link against the current snapshots.
4. Apply the batch atomically to the home database.
5. Run database `check`; require the whole-document and indexed-section
   matches appropriate to the close. Verify the crosswalk with exact `lookup`
   and `show` every added or materially changed card.
6. Perform any coordinator-specific post-close action, such as consolidation
   source retirement.
7. Delete only the generated workpad.

Markdown publication and the SQLite transaction cannot form one filesystem
transaction. Publish canonical Markdown first, then apply SQLite. A canonical,
database, validation, or post-close failure retains the workpad and its exact
path. If Markdown succeeds and SQLite fails, the document remains authoritative
and the stale database is detectable; never restore an older file over it. A
cleanup-only failure leaves a valid pair and reports the residual directory.

## CLI routing

Both tools use only the Python standard library and emit JSON.

| Need | Command |
|---|---|
| Scan keyed-section metadata without bodies | `canonical_sections.py scan` |
| Validate the addressable Markdown structure | `canonical_sections.py check` |
| Read one exact canonical section | `canonical_sections.py show --key ...` |
| Assign or change generated key markers | `canonical_sections.py key-set` |
| Current database schema, fields, operation shapes, digest rules | `research_memory.py contract` |
| Create or validate a writable home | `research_memory.py ensure` |
| Strict explicit creation | `research_memory.py init` |
| Repair ownership metadata after a move | `research_memory.py relink` |
| Apply one revision-checked transaction | `research_memory.py apply` |
| Resolve one canonical key/alias or card slug to summaries | `research_memory.py lookup` |
| Retrieve broader summaries | `research_memory.py search` |
| Inspect one full card, origins, and links | `research_memory.py show` |
| Freeze a complete read-only source snapshot | `research_memory.py export` |
| Validate schema, integrity, ownership, digests, crosswalk, and sidecars | `research_memory.py check` |

Run `contract` before constructing an unfamiliar batch instead of relying on a
copied example. `apply` uses expected revisions, canonical digests, exact keys,
and explicit operations. Its `expected_canonical_digest` names the stored
baseline, while `canonical_digest` names the published bytes to index.
Repeating the immediately previous round ID and batch digest is idempotent;
reusing that round ID with different content is rejected. The canonical file
is rechecked before database commit.

`scan`, canonical `show`, database `lookup`, `search`, `show`, `export`, and
`check` are read-only and never create a missing database. The database CLI
edits neither canonical documents nor workpads and performs no Git operation,
mechanical merge, migration, import, or source retirement.
