# Research Memory

## The mathematical account and its memory

Read this note for authorized file-backed work or research-history retrieval.
Canonical Markdown is the authoritative mathematical account: its definitions,
reasoning, conclusions, status, evidence scope, limitations, and open questions
stand on their own. Let the mathematics determine its organization. The SQLite
companion holds reusable background that would interrupt the account.
Temporary working notes and raw outputs belong in one
generated OS-temporary workpad.

One coordinator owns the document, companion, and workpad. Specialists and
readers of other theories remain read-only and create no database. Parallel
workers return findings to the coordinator. Reconcile useful records by meaning;
never binary-merge SQLite files.

## Read existing work

Read the canonical document first and respect its published companion locator.
A missing declared companion requires recovery, not recreation. Reads and checks
create nothing.

Start with the key outline and known keys, cards, or artifacts and their linked
summaries. Search by identifier or intersected facets when exact retrieval leaves
a gap. Request `--full` for a selected record; follow at most one relation hop
unless the task needs more.

Reuse established values for a few useful facets: `field` and `subfield` for
mathematical areas, `term` for standard concepts, `identifier` for namespaced
identifiers such as `msc2020:05C31`, and `symbol` for distinctive notation paired
with prose or a field filter. A successful read does not validate the whole pair.

## Keep useful material

The document declares its companion with one scalar front-matter value:

```yaml
---
research_memory: ./theory.research.sqlite
---
```

Give a key only to a mathematical subject worth returning to. Each key names one
subject within its document; normally leave summaries and navigation unindexed. Split
aggregates needing separate links; otherwise leave them unindexed. Keep the key
while its subject stays the same, even when its heading, position, or status
changes. An indexed section has exactly one lowercase-kebab key on its first
nonblank line:

```markdown
## Rank-drop obstruction

**Research key:** `rank-drop-obstruction`
```

Use these markers without generated anchors or database deep links.

A card is a self-contained note of reusable background, with a semantic slug,
short summary, and optional detail. Say when it would be useful again: what
would revive a parked approach or make an expensive negative search relevant.
Retain only the reusable addition, with enough context to use it. A card must
not merely duplicate a canonical result or artifact metadata. Routine attempts
expire with the workpad.

Keep disposition (`open`, `active`, `parked`, `rejected`, `integrated`) separate
from mathematical status: rejecting an approach need not refute its claim.
Programs and datasets remain native files. For retained Python programs, use the
`RESEARCH_ARTIFACT` metadata in
[computational-checking.md](computational-checking.md). File integrity, declared
run outcome, and mathematical evidence remain distinct.

## Finish the update

The JSON-emitting CLI is `research-mathematics/scripts/research_memory.py`:

```text
research_memory.py ensure CANONICAL
research_memory.py read CANONICAL SELECTOR [VALUE]
research_memory.py apply CANONICAL        # changeset JSON on stdin
research_memory.py check CANONICAL
```

For writable work, call `ensure` after reading the document. If no locator
exists, publish the returned canonical-stem locator before other commands.
Consult `read --help` for selectors and flags, and `apply --help` for the
operation grammar and example. The tool leaves Markdown and native files to
the coordinator.

Close in order:

1. Finish the mathematical account, including important negative findings,
   exact unfinished steps, and concise provenance. Audit which subjects need
   keys and whether existing keys still identify them accurately.
2. Synchronize affected card text, `term`/`symbol` facets, and links when
   terminology changes; keep superseded wording only as provenance. Definitions
   stay in Markdown, without a separate registry. A genuine
   subject correction, split, or merge may change keys: remap every card and
   artifact link in the same transaction, without aliases. Update and reindex
   affected native metadata too; otherwise preserve the key or stop.
3. Publish Markdown, freeze its digest, and apply one curated transaction with
   the expected database revision and canonical digest.
4. Run `check` to validate the pair, then exactly read every changed key, card,
   and artifact. Complete authorized post-close actions and delete the workpad.

Markdown and SQLite cannot be updated atomically together. Publishing Markdown
first keeps the mathematics authoritative if the database update fails. After
any material close failure, retain the workpad and report a recovery path.
