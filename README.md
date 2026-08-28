# Agent Mathematician

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21996114.svg)](https://doi.org/10.5281/zenodo.21996114)

Agent skills for mathematical exploration and rigorous research. The suite helps agents formalize ideas, use mathematical structures as test beds for intuition, formulate and verify substantial claims, consolidate mathematical documents, attack theories and proofs, audit assumptions, and explain advanced mathematics.

## Skills

- `research-mathematics`: research, formulate, prove, verify, or repair substantial mathematical claims.
- `consolidate-math-documents`: merge selected mathematical documents into one self-contained canonical target and safely retire the old source pairs.
- `explore-mathematical-structure`: iteratively explore a selected formalism through examples, viewpoints, structural patterns, and conjectures so the user can choose a direction.
- `explore-proof-strategies`: bounded exploration of diverse proof routes and cross-field bridges.
- `formalize-concepts`: lightweight development of an informal idea into a selected mathematical formalism.
- `destroy-theory`: stress-test statements and proofs, search for counterexamples, and identify failure boundaries.
- `audit-assumptions`: locate hidden assumptions, trace where hypotheses are used, and test whether they can be weakened.
- `explain-mathematics`: explain advanced mathematics to mathematically mature nonspecialists.

The typical discovery path is `formalize-concepts` -> `explore-mathematical-structure` -> `explore-proof-strategies` -> `research-mathematics`. Skip stages when the formalism, target, or proof direction is already settled.

Use `consolidate-math-documents` explicitly when several drafts, canonical
accounts, or theory branches need one target. It writes only the selected
target pair, keeps every source immutable while reconciling useful memory, and
retires the exact source Markdown/companion pairs after the target validates.

## Research memory

Authorized file-backed research uses three information layers:

1. a self-contained canonical Markdown document;
2. a Git-tracked `<stem>.research.sqlite` companion containing curated open,
   active, parked, rejected, and integrated research-memory cards plus their
   semantic crosswalk to canonical sections; and
3. one generated OS-temporary workpad for raw round state, deleted after
   successful closure.

The canonical document remains authoritative. The database preserves useful
noncanonical directions, obstructions, counterexamples, assumption
relaxations, and source-applicability notes; it never holds mathematics needed
to understand or trust the canonical result. Raw workpads and specialist
reports are not stored in the database.

Schema 3 is the only supported companion schema; earlier schemas are rejected
without migration or compatibility behavior.

| Skill | Research-memory role |
|---|---|
| `research-mathematics` | Full-round coordinator and sole writer |
| `consolidate-math-documents` | One-target consolidation and source-retirement coordinator |
| `explore-mathematical-structure` | Standalone exploration coordinator |
| `explore-proof-strategies` | Read-only when nested; standalone coordinator only with writable authority |
| `destroy-theory` | Read-only when nested; standalone coordinator only with writable authority |
| `audit-assumptions` | Read-only when nested; standalone coordinator only with writable authority |
| `formalize-concepts` | No database lifecycle |
| `explain-mathematics` | Canonical-only by default; explicit research-history queries are read-only |

Every authorized writable home round first establishes exactly one canonical
document and its companion. When the canonical document has no locator,
`ensure` creates its missing canonical-stem database or validates the exact
existing pair; the coordinator then adds this locator:

```yaml
research_memory:
  path: ./theory.research.sqlite
  schema: 3
  optional_for_understanding: true
```

A locator that names a missing home database stops the round so memory loss is
not hidden by silent reinitialization. Nested specialists, report-only runs,
and foreign-theory reads never create a database. A missing foreign companion
is reported and remains missing.

Companions are binary Git artifacts. Different theories can advance in
parallel, but competing branch versions of the same database must be
reconciled semantically rather than binary-merged.
Skills report an untracked companion at closure and do not stage or commit it
without separate authorization.

The schema-3 companion stores cohesive cards, separate card bodies, local
edges, source provenance, and a normalized many-to-many crosswalk between cards
and human-semantic canonical research keys. Opaque inherited identifiers such
as `IR-COMP-1` remain aliases. A card about exactly the same subject uses
exactly the canonical key as its slug; related but different subjects use
distinct semantic identifiers and a typed link.

The standard-library `canonical_sections.py` tool deterministically scans,
checks, and selectively reads keyed sections, and owns their generated HTML
anchors plus visible `Research keys` lines. Several primary keys may address
one section. Its metadata-only `scan` does not return section bodies, and
`show` returns one exact section. The companion CLI's exact `lookup` returns
linked card summaries without card bodies; broad `search` follows only when
exact lookup is insufficient, and `show` expands one selected card.

The suite ships both tools under
`research-mathematics/scripts/`. The database CLI commands are `contract`,
`init`, `ensure`, `relink`, `apply`, `lookup`, `search`, `show`, `export`, and
`check`. The compact lifecycle lives in
`research-mathematics/references/research-memory.md`; `contract` emits the
current schema and batch shapes on demand. All database-aware skills reuse
these resources, and none performs a mechanical database merge.

```sh
python3 mathematician/skills/research-mathematics/scripts/canonical_sections.py scan --canonical theory.md
python3 mathematician/skills/research-mathematics/scripts/canonical_sections.py check --canonical theory.md
python3 mathematician/skills/research-mathematics/scripts/canonical_sections.py show --canonical theory.md --key implicit-young-evaluation
python3 mathematician/skills/research-mathematics/scripts/canonical_sections.py key-set --canonical theory.md --heading-line 42 --key implicit-young-evaluation --expected-canonical-sha256 "$CANONICAL_SHA256"
python3 mathematician/skills/research-mathematics/scripts/research_memory.py contract
python3 mathematician/skills/research-mathematics/scripts/research_memory.py init --canonical theory.md --theory theory
python3 mathematician/skills/research-mathematics/scripts/research_memory.py ensure --canonical theory.md
python3 mathematician/skills/research-mathematics/scripts/research_memory.py lookup --db theory.research.sqlite --canonical implicit-young-evaluation
python3 mathematician/skills/research-mathematics/scripts/research_memory.py search --db theory.research.sqlite
python3 mathematician/skills/research-mathematics/scripts/research_memory.py show --db theory.research.sqlite --slug a-semantic-slug
python3 mathematician/skills/research-mathematics/scripts/research_memory.py export --db theory.research.sqlite
python3 mathematician/skills/research-mathematics/scripts/research_memory.py apply --db theory.research.sqlite --input round-batch.json
python3 mathematician/skills/research-mathematics/scripts/research_memory.py relink --db theory.research.sqlite --canonical renamed-theory.md --expected-canonical theory.md --expected-database-revision 3
python3 mathematician/skills/research-mathematics/scripts/research_memory.py check --db theory.research.sqlite
```

Canonical-item refresh and card-link review record which document, section,
and card revisions a curator considered. They do not establish logical or
mathematical freshness.

A writable consolidation freezes an exact retirement manifest before changing
the target. After target validation, the consolidation-specific
`scripts/retire_sources.py` removes only source Markdown files and explicitly
located companions that are Git-tracked and clean against `HEAD`; it leaves the
deletions unstaged. Dirty, staged, untracked, ignored, or non-Git sources stop
for explicit direction, as do paths hidden behind `assume-unchanged` or
`skip-worktree`. Native artifacts, directories, and adjacent files are outside
retirement authority.

All skills are opt-in and carry manual-only metadata for all supported hosts. Invoke them explicitly with `$skill-name` in Codex or `/skill-name` in Cursor and Claude Code.

Manual-only metadata prevents the host from selecting a skill merely because a prompt resembles its description. It does not prevent an invoked skill from explicitly applying another skill: for example, `$research-mathematics` delegates adversarial review to `$destroy-theory` and hypothesis review to `$audit-assumptions`.

## Installation

Clone the repository:

```sh
git clone https://github.com/Froskekongen/agent_mathematician.git
cd agent_mathematician
```

Install all skills for your agent:

```sh
# Codex or Cursor (both use ~/.agents/skills)
python3 mathematician/install_skills.py codex

# Claude Code (~/.claude/skills)
python3 mathematician/install_skills.py claude

# All supported locations
python3 mathematician/install_skills.py all
```

Use `--dry-run` to inspect the destinations without changing anything:

```sh
python3 mathematician/install_skills.py all --dry-run
```

Restart the agent if it does not discover the newly installed skills in the current session.

## Citation

If these skills contribute to your research, please cite them as research software:

> Aune, E. (2026). *Agent Mathematician: Agent skills for mathematical research* (Version 0.1.0) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.21996115

BibTeX:

```bibtex
@software{aune_agent_mathematician_2026,
  author = {Aune, Erlend},
  title = {Agent Mathematician: Agent Skills for Mathematical Research},
  version = {0.1.0},
  year = {2026},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.21996115},
  url = {https://doi.org/10.5281/zenodo.21996115}
}
```

The repository also includes [`CITATION.cff`](CITATION.cff), which GitHub and compatible reference tools can use to generate citations. The badge uses the [concept DOI](https://doi.org/10.5281/zenodo.21996114) for all releases; cite the version DOI above for reproducibility.

## License

MIT. See [`LICENSE`](LICENSE).
