# Source Retirement

Use this protocol only for a writable consolidation. Sources stay immutable
until the target pair closes; retirement then removes the exact old source
pairs from the working tree while Git retains their last committed bytes.

Use the standard-library helper
[`retire_sources.py`](../scripts/retire_sources.py). It performs no Git mutation
and emits JSON.

## Freeze and preflight

Write this exact manifest in the OS-temporary workpad after the target draft is
stable. The target canonical digest is the post-edit candidate digest.

```json
{
  "repository_root": "/absolute/git/root",
  "target": {
    "canonical": {"path": "theory.md", "sha256": "<candidate-sha256>"},
    "database": {"path": "theory.research.sqlite"}
  },
  "sources": [
    {
      "canonical": {"path": "old.md", "sha256": "<sha256>"},
      "database": {"path": "old.research.sqlite", "sha256": "<sha256>"}
    }
  ]
}
```

Omit a source `database` only when that Markdown document has no explicitly
located companion. Paths may be absolute or repository-relative but must stay
inside the named Git top level. Canonical files end in `.md` or `.markdown`;
companions end in `.sqlite`.

Before publishing, run:

```text
python3 retire_sources.py check --manifest MANIFEST
```

`check` accepts a pending new target or a not-yet-published existing-target
candidate, but fully validates the retirement set. Every source must exist,
match its digest, be Git-tracked and clean against `HEAD`, and have no staged,
unstaged, unmerged, ignored, `assume-unchanged`, `skip-worktree`, symlinked,
duplicated, target-overlapping, or live SQLite-sidecar state. Any failure stops
publication. Resolve it by making the
exact bytes recoverable or obtain separate direction; this helper has no force
or permanent-loss override.

Retirement authority covers only listed Markdown files and located companions.
It excludes directories, native artifacts, adjacent files, shared resources,
and Git staging or commits. Resolve inbound links from surviving documents
before closure.

## Retire after target closure

After the target's database and canonical-section checks, exact crosswalk
lookups, changed-card `show`, and final `export` succeed, run the helper's
`check` again and require the target to be ready. Then run:

```text
python3 retire_sources.py apply --manifest MANIFEST
```

`apply` repeats every preflight, requires the target candidate digest, invokes
the research-memory validator and requires its whole-document and indexed
canonical-section matches, then immediately rechecks each source's Git state,
identity, and digest before removing it. A listed companion must be schema 3
and belong to its paired document; an omitted adjacent default companion blocks
retirement. A reviewed source companion may have document or section snapshot
mismatches, because a mismatch is not database corruption. Each located
database is removed before its Markdown document. Git deletions remain unstaged
and recoverable from `HEAD`.

Filesystem deletion is not transactional. A partial failure keeps the valid
target, preserves the workpad, and reports exact deleted and remaining paths.
Do not restore over a recreated or edited path. Completion requires every
manifest source to be absent and one final successful target check.

Run retirement while source paths are quiescent. Filesystem validation and
unlink cannot form one transaction; the just-in-time checks minimize that gap,
and Git recovery remains the hard prerequisite.
