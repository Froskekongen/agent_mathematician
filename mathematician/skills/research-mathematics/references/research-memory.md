# Research Memory Protocol

Read this reference for an authorized file-backed mathematical round or when
research history must be queried. The canonical Markdown is authoritative and
self-contained. Its SQLite companion is bounded, indexed memory for useful
noncanonical material; raw round state belongs in one OS-temporary workpad.

## Canonical contract

The document points to its companion with one scalar front-matter value:

```yaml
---
research_memory: ./theory.research.sqlite
---
```

An indexed section has exactly one human-semantic lowercase-kebab key on its
first nonblank line:

```markdown
## Rank-drop obstruction

**Research key:** `rank-drop-obstruction`
```

The key names one mathematical subject rather than a sequence, date, or
status. Related subjects get distinct keys and database links. Markdown uses
no generated anchors, aliases, or database deep links. The tool reads and
validates markers; agents edit ordinary Markdown directly.

## Ownership

One coordinator owns one canonical document, its companion, and one temporary
workpad. Nested specialists and foreign-theory readers are read-only and create
no database. Parallel lanes return findings to the coordinator. SQLite files
are never binary-merged; worthwhile records are reapplied semantically.

For a writable round, read the canonical file before calling `ensure`. An
existing locator is authoritative; a missing located companion stops for
recovery rather than silent recreation. When no locator exists, `ensure` may
create or validate only the canonical-stem companion and returns the scalar
locator for the coordinator to add. `read`, `apply`, and `check` require that
published locator. An unsupported database version is rejected without
migration or compatibility behavior.

## Four-command interface

The standard-library CLI is
`research-mathematics/scripts/research_memory.py` and emits JSON:

```text
research_memory.py ensure CANONICAL
research_memory.py read CANONICAL SELECTOR [VALUE]
research_memory.py apply CANONICAL        # changeset JSON on stdin
research_memory.py check CANONICAL
```

`read` selectors are `meta`, `keys`, `key`, `card`, `artifact`, `search`, and
`all`. List and search reads return compact summaries. Use exact key, card, or
artifact reads before search, request `--full` only for a selected record, and
apply facet filters when they narrow a known question. Reads and checks never
create a missing database.

`apply` accepts one revision- and canonical-digest-checked transaction. Consult
`research_memory.py apply --help` for its compact normative operation grammar
and minimal example instead of copying a second schema description.
The tool edits neither canonical Markdown nor source artifacts and performs no
Git operation, migration, source retirement, import, or code execution.

Every read reports the observed and indexed canonical digests plus
`canonical_digest_current`; only `check` computes the stronger whole-pair
`current` result. List reads are paginated; an exact key read applies its offset
to both linked cards and artifacts, reports each total, and marks whether each
card link matches the current card revision and section digest. Summary rows
omit long state rationales, selected bodies are chunked, and every JSON response
has a global size ceiling. `check` reports bounded structured issues with
category, code, message, and entity identity when applicable.

## Cards and retrieval

A card is a self-contained reusable context packet with a semantic slug, short
summary, optional detail body, workflow disposition, optional mathematical
status, and concrete reuse condition. Retain open obligations, demonstrated
obstructions and counterexamples, expensive negative searches, parked routes
with revival conditions, assumption relaxations, and source-applicability
findings. Accepted load-bearing mathematics stays in Markdown; routine attempts
expire with the workpad. Create a card only when it adds reusable noncanonical
context—never merely to duplicate a canonical result or native artifact
metadata.

Use controlled facets rather than free-form tag soup:

- `field`: broad mathematical area;
- `subfield`: a more precise area;
- `term`: standard object, theorem, construction, or technique;
- `identifier`: namespaced public identifier such as `msc2020:05C31`,
  `oeis:A000045`, or a library declaration; and
- `symbol`: distinctive notation useful only with a prose or field filter.

Reuse established facet values and cap them to the terms that improve
retrieval. Fields and terms can seed bounded external literature queries, but
the database tool never browses or stores generated queries.

Retrieve progressively:

1. read the lightweight canonical key outline;
2. read the exact key and linked card or artifact summaries;
3. search by identifier or intersected facets only if exact retrieval fails;
4. request one selected full record; and
5. follow at most one relation hop unless the task requires more.

Keep disposition (`open`, `active`, `parked`, `rejected`, `integrated`)
separate from truth status. A rejected route may be mathematically unresolved;
a refuted claim may remain a useful active obstruction.

## Native artifacts

Programs, checkers, certificates, and necessary datasets remain native files,
not database blobs. A retained Python program carries the literal
`RESEARCH_ARTIFACT` dictionary defined by
[computational-checking.md](computational-checking.md). The database caches its
indexed metadata, file digest, references, and canonical/card links; it does
not execute it or store raw logs. A tool-derived integrity result, a declared
run outcome, and the card's mathematical status remain separate.

## Write and close

Create one generated OS-temporary workpad for candidates, assumption maps,
proof graphs, probes, source notes, specialist reports, raw outputs, and the
final changeset. Durable files contain their own metadata; the workpad is not a
repository manifest.

Close in this order:

1. integrate accepted mathematics, exact open obligations, load-bearing
   negative results, and concise provenance into canonical Markdown;
2. freeze the resulting canonical digest and curate only reusable memory;
3. apply one transaction with the expected database revision and canonical
   digest;
4. run `check`, then exactly read every changed key, card, and artifact; and
5. perform any authorized post-close action and delete the workpad.

Markdown and SQLite cannot form one filesystem transaction. Publish Markdown
first: if the database update fails, the canonical account remains
authoritative and the mismatch is detectable. Retain the workpad and report a
recovery path after any material close failure.
