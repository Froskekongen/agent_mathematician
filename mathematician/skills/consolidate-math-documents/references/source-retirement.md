# Source Retirement

Use this protocol only for an authorized writable consolidation. Sources stay
immutable until the target closes. Retirement then removes the exact old
Markdown files and explicitly located companions while Git retains their last
committed bytes.

Use the standard-library helper
[`retire_sources.py`](../scripts/retire_sources.py). It emits JSON and performs
no Git mutation.

## Freeze a temporary retirement plan

After the target draft stabilizes, write the helper's input only inside the
OS-temporary workpad. It is transaction input, not a retained repository
manifest. Its exact shape is:

```json
{
  "repository_root": "/absolute/git/root",
  "target": {
    "canonical": {"path": "combined.md", "sha256": "<64 lowercase hex>"},
    "database": {"path": "combined.research.sqlite"}
  },
  "sources": [
    {
      "canonical": {"path": "old.md", "sha256": "<64 lowercase hex>"},
      "database": {
        "path": "old.research.sqlite",
        "sha256": "<64 lowercase hex>"
      }
    }
  ]
}
```

Paths may be repository-relative. The target database has no frozen digest
because target construction may create or update it between the first
preflight and final application. Validate and later apply the same frozen file:

```sh
python3 retire_sources.py check --manifest /tmp/.../retirement.json
python3 retire_sources.py apply --manifest /tmp/.../retirement.json
```

Record:

- repository root;
- target canonical path and candidate SHA-256;
- every source canonical path and frozen SHA-256; and
- each explicitly located source companion path and SHA-256.

Omit a source companion only when its Markdown has no locator. Paths must stay
inside the named Git root. The target may not overlap any source.

Run the helper's non-mutating preflight before publishing. Every source must
exist, match its digest, be a regular nonsymlink Git-tracked file, and be clean
against `HEAD`, with no staged, unmerged, ignored, `assume-unchanged`, or
`skip-worktree` state. A companion must be closed, have no live SQLite sidecar,
and belong to its source locator. An omitted adjacent database does not become
authorized by proximity.

Any failure stops publication. Resolve it by making the exact bytes
recoverable or request separate direction; the helper has no force or
permanent-loss override.

Retirement authority covers only listed source Markdown files and explicitly
located companions. It excludes directories, native artifacts, adjacent files,
shared resources, Git staging, and commits. Resolve inbound links from
surviving documents before target closure.

## Retire after target closure

After the target succeeds under `research_memory.py check CANONICAL` and exact
`read` calls confirm changed keys, cards, and artifacts, rerun the retirement
preflight against the frozen source bytes and published target digest. Then
apply the exact temporary plan.

The helper repeats every preflight immediately before deletion. Each located
companion is removed before its Markdown source. Git deletions remain unstaged
and recoverable from `HEAD`.

Filesystem deletion is not transactional. A partial failure keeps the valid
target, preserves the workpad, and reports exact deleted and remaining paths.
Do not restore over a recreated or edited path. Completion requires every
listed source to be absent and one final successful target check.
