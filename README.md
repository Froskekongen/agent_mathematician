# Agent Mathematician

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21996114.svg)](https://doi.org/10.5281/zenodo.21996114)

Eight opt-in skills for mathematical exploration, proof development, rigorous
review, explanation, and document consolidation.

## Skills

- `formalize-concepts`: select faithful mathematics for an informal idea.
- `explore-mathematical-structure`: compare candidate structures with small
  discriminating tests.
- `explore-proof-strategies`: build and pressure-test a bounded proof-route
  portfolio.
- `research-mathematics`: construct, attack, and independently verify a
  substantial result.
- `destroy-theory`: falsify a statement or locate proof and validity failures.
- `audit-assumptions`: trace hypotheses and test necessity or weakening.
- `explain-mathematics`: teach advanced mathematics across specialty
  boundaries.
- `consolidate-math-documents`: reconcile canonical accounts and safely retire
  their exact source pairs.

The usual user-controlled path is `formalize-concepts` ->
`explore-mathematical-structure` -> `explore-proof-strategies` ->
`research-mathematics`; skip settled stages. These phase changes are explicit
`$skill-name` recommendations rather than automatic continuations.

All eight skills remain directly user-invokable. Only `destroy-theory` and
`audit-assumptions` are also model-invokable: `research-mathematics` calls them
as cold, read-only workers at its mandatory challenge gate. The other six stay
user-only, so phase routing cannot silently broaden a request. Short
entrypoints contain only task-specific steps and completion gates; shared
references under `research-mathematics/references/` carry cross-suite rigor,
memory, and conditional computation contracts.
The [paired architecture pilot](mathematician/evaluations/architecture-pair/pilot-results.md)
records the measured complexity, quality, and cost tradeoffs.

## Rigor model

Every evidence-bearing workflow uses one chain:

```text
TARGET -> EVIDENCE -> CHALLENGE -> VERIFY -> STATUS
```

The target is frozen before proof or attack. Evidence is typed and scoped.
Challenge attacks the literal claim and its dependencies. Verification uses a
fresh context and separately checks intended statement, encoding, proof, and
dependency closure. The terminal status is `PROVED`, `INCOMPLETE`,
`CONJECTURAL`, `REFUTED`, or `UNRESOLVED`; workflow disposition and support tags
remain separate.

## Research memory

Authorized file-backed work has three layers:

1. self-contained canonical Markdown;
2. a bounded, indexed SQLite companion for curated noncanonical memory; and
3. one OS-temporary workpad for raw round state, deleted after valid closure.

The database can grow without entering the model context. Retrieval starts at
the canonical key outline, reads exact keys and compact linked summaries, then
uses filtered search and one selected full record only when needed. Cards may
carry controlled `field`, `subfield`, `term`, `identifier`, and `symbol`
facets. These improve local retrieval and can seed bounded literature queries.

The canonical document names its companion with a scalar locator:

```yaml
---
research_memory: ./theory.research.sqlite
---
```

Each indexed section has one visible semantic key and no generated anchor or
deep link:

```markdown
## Rank-drop obstruction

**Research key:** `rank-drop-obstruction`
```

The companion format is schema 4 only. Incompatible databases are rejected;
there is no migration or compatibility layer. One coordinator writes one home
pair, while nested specialists and foreign-theory readers remain read-only.
With no locator, `ensure` may create the canonical-stem companion and returns
the scalar to add. A declared locator whose database is missing stops for
recovery rather than being silently recreated.

The standard-library memory tool exposes four commands:

```sh
python3 mathematician/skills/research-mathematics/scripts/research_memory.py ensure theory.md
python3 mathematician/skills/research-mathematics/scripts/research_memory.py read theory.md keys
python3 mathematician/skills/research-mathematics/scripts/research_memory.py read theory.md key rank-drop-obstruction
python3 mathematician/skills/research-mathematics/scripts/research_memory.py read theory.md search "rank obstruction"
python3 mathematician/skills/research-mathematics/scripts/research_memory.py apply theory.md  # JSON on stdin
python3 mathematician/skills/research-mathematics/scripts/research_memory.py check theory.md
```

`read` also selects `meta`, `card`, `artifact`, and bounded `all` summaries;
exact selected records may request full detail. Consult CLI help for changeset
fields. The tool edits neither Markdown nor source artifacts and executes no
artifact code.

## Computational artifacts

Material computational work is conditionally dispatched to an internal role
in `discover`, `falsify`, `certify`, or `replay` mode. Load-bearing artifacts
receive a fresh replay context. Small hand-checkable calculations remain in the
calling skill.

A retained experiment or checker is a Python program whose reproducibility
metadata is a native top-level literal:

```python
RESEARCH_ARTIFACT = {
    "schema": 1,
    "slug": "rank-search-degree-6",
    "kind": "bounded-experiment",
    "mode": "falsify",
    "title": "Degree-six rank search",
    "summary": "Exact enumeration of the declared candidate family.",
    "canonical_keys": ["rank-drop-obstruction"],
    "target_digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "purpose": "Enumerate the declared candidate family through degree six.",
    "scope": "All encoded candidates of degree at most six.",
    "encoded_target": "Every valid encoded candidate of degree at most six satisfies the rank bound.",
    "evidence_ceiling": "A witness refutes the encoded target; absence is scoped only.",
    "reproduce": {
        "argv": ["python3", "artifacts/rank_search.py", "--max-degree", "6"],
        "runtime": "CPython 3.14",
        "parameters": {"max_degree": 6},
        "budget": {"candidates": 1842},
        "stopping_rule": "Exhaust the declared finite family.",
    },
    "limitations": ["No claim beyond degree six."],
}
```

The program can use the dictionary directly. Indexing uses Python's standard
AST literal inspection without importing or executing the source. There is no
sidecar manifest. Optional `references` entries bind replay-critical local
files by path and SHA-256; raw logs stay temporary. Retained artifacts require
the controlled mode, frozen target digest, encoded target, evidence ceiling,
nonempty resource budget, and explicit stopping rule shown above.
Load-bearing obligations use explicit fail-closed checks rather than removable
assertions.

## Installation

Clone the repository and install all skills:

```sh
git clone https://github.com/Froskekongen/agent_mathematician.git
cd agent_mathematician

# Codex or Cursor (both use ~/.agents/skills)
python3 mathematician/install_skills.py codex

# Claude Code (~/.claude/skills)
python3 mathematician/install_skills.py claude

# All supported locations
python3 mathematician/install_skills.py all
```

Use `--dry-run` to inspect destinations. Restart the agent if the current
session does not discover the newly installed skills.

## Releasing

Install and authenticate the [GitHub CLI](https://cli.github.com/), then release
from a clean checkout of the GitHub default branch:

```sh
make release                 # next patch version
make release BUMP=minor      # next minor version
make release BUMP=major      # next major version
make release VERSION=1.2.0   # exact version
```

The command checks the branch and remote state, updates `CITATION.cff` and the
citations below, runs the full test suite, commits and tags the release, pushes
both atomically, and publishes a GitHub release with generated notes. If the
GitHub release step fails after the push, rerun the same command to finish it.

## Citation

> Aune, E. (2026). *Agent Mathematician: Agent skills for mathematical research* (Version 0.1.0) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.21996114

```bibtex
@software{aune_agent_mathematician_2026,
  author = {Aune, Erlend},
  title = {Agent Mathematician: Agent Skills for Mathematical Research},
  version = {0.1.0},
  year = {2026},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.21996114},
  url = {https://doi.org/10.5281/zenodo.21996114}
}
```

The concept DOI in the badge and citation resolves to the latest release. For
strict reproducibility, cite the version DOI shown by Zenodo for that release.
See [`CITATION.cff`](CITATION.cff) and [`LICENSE`](LICENSE).
