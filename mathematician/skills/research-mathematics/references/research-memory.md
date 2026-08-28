# Research Memory Protocol

Read this protocol only for an authorized writable theory round. Nested and
report-only work may query existing memory with `search` and `show`; it creates
no theory artifacts and does not need the writable protocol.

Schema 2 is the only supported schema. Research state has three destinations:

1. **Canonical Markdown:** authoritative, self-contained mathematics.
2. **`<stem>.research.sqlite`:** curated reusable noncanonical memory.
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

One round has one writer and one final transaction. Parallel lanes for the same
theory return findings to that writer. Different home theories may proceed
concurrently. Never binary-merge competing database versions; select one and
semantically reapply worthwhile cards from the other.

## Establish the home pair

Read the canonical document before memory and preflight before creating a
workpad:

| Canonical state | Required action |
|---|---|
| Locator present | Resolve it relative to the document; run `ensure` with `--require-existing`. A missing companion stops the writable round. |
| No locator | Run `ensure` without `--require-existing`; it creates or validates the canonical-stem companion. Add the locator only after success. |
| New consolidation target | Draft in the workpad; create the stabilized Markdown target, then run `ensure`. Never ensure a source. |

Default naming is `theory.md` with `theory.research.sqlite`; the exact canonical
stem is also the default theory slug. Add:

```yaml
research_memory:
  path: ./theory.research.sqlite
  schema: 2
  optional_for_understanding: true
```

The locator is authoritative after publication. Use revision-checked `relink`
after a deliberate move or rename; the CLI neither moves files nor edits
Markdown. Companions are intended to be Git-tracked, but skills leave staging
and commits to separate authorization and report an untracked home companion
at closure.

## Retrieve and curate

Read the canonical document first, then query:

1. home `active`, `open`, and `parked` summaries;
2. relevant `rejected` cards only when reconsidering a similar route;
3. foreign companions only for a concrete question.

A card is a cohesive Markdown context packet with a semantic slug. It remains
understandable without following an edge. Keep disposition and mathematical
status separate:

- disposition: `open`, `active`, `parked`, `rejected`, `integrated`;
- claim status: `conjectural`, `supported`, `refuted`, `proved`, `unresolved`,
  or absent.

`Rejected` allocates research effort; `refuted` records mathematical evidence.
Open and active cards require a next test, parked cards a revival condition,
rejected cards a reason, and integrated cards a canonical anchor. Retain only
live directions, reusable obstructions or counterexamples, costly results
likely to be repeated, realistic revival conditions, open obligations, or
material source applicability. Accepted and load-bearing mathematics belongs
in the canonical document; incidental attempts expire with the workpad.

Foreign findings are leads rather than live dependencies. If one materially
affects the home theory, create a self-contained local card and a `card_origin`
row containing its last-known source locator, source slug, source card digest,
and an applicability mapping of objects, hypotheses, and unmatched
assumptions. Repository-local locators are POSIX paths relative to the target
database; external sources use URIs. The locator may later become unavailable
after authorized consolidation retirement; the provenance remains valid and
is not a cross-database foreign key. Edges are sparse navigation between local
cards only.

## Work and close

Create one generated directory under the OS temporary directory and record its
path and round ID. Keep candidates, proof-DAG drafts, assumption maps, probes,
source notes, specialist reports, manifests, verifier output, and the final
batch there. Raw workpad content never enters SQLite.

Close in this order:

1. Integrate accepted mathematics, load-bearing negative results, exact open
   obligations, and concise provenance into the canonical document.
2. Curate reusable noncanonical material into one explicit batch.
3. Apply it atomically to the home database.
4. Run `check`, require `canonical_status: current`, and `show` every added or
   materially changed card.
5. Perform any coordinator-specific post-close action, such as consolidation
   source retirement.
6. Delete only the generated workpad.

A canonical, database, validation, or post-close failure retains the workpad
and its exact path. A cleanup-only failure leaves a valid pair and reports the
residual directory. Source retirement is a filesystem phase after target
closure, not part of the SQLite transaction; source companions remain
read-only throughout consolidation.

## CLI routing

Use the standard-library [research-memory CLI](../scripts/research_memory.py).
Every command emits JSON.

| Need | Command |
|---|---|
| Current schema, fields, operation shapes, digest rule | `contract` |
| Create or validate a writable home | `ensure` |
| Strict explicit creation | `init` |
| Repair ownership metadata after a move | `relink` |
| Apply one revision-checked transaction | `apply` |
| Retrieve summaries | `search` |
| Inspect one full card, origins, and local edges | `show` |
| Freeze a complete read-only source snapshot | `export` |
| Validate schema, integrity, ownership, digest, and sidecars | `check` |

Run `contract` before constructing an unfamiliar batch instead of relying on a
copied example. `apply` uses explicit add/update/delete operations, expected
revisions or exact keys, and no implicit upserts. Repeating the immediately
previous round ID and batch digest is idempotent; reusing that round ID with
different content is rejected. `search`, `show`, `export`, and `check` are
read-only and never create missing databases.

The CLI edits neither canonical documents nor workpads, performs no Git
operation, and does not mechanically merge, migrate, import, or retire source
artifacts.
