# Agent Mathematician

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21996114.svg)](https://doi.org/10.5281/zenodo.21996114)

Nine opt-in skills for mathematical exploration, proof development, rigorous
review, explanation, proof-bearing exposition, and document consolidation.

## Skills

- `formalize-concepts`: turn an informal idea into faithful mathematics through
  examples, consequences, and consequential choices.
- `explore-mathematical-structure`: compare ways of understanding a phenomenon
  through exact realizations and revealing examples.
- `explore-proof-strategies`: compare mechanisms that could prove a claim and
  identify the most promising route and its crux.
- `research-mathematics`: prove, refute, repair, or locate the exact open step
  in a substantial claim.
- `destroy-theory`: find checked counterexamples, proof gaps, failed encodings,
  and validity boundaries.
- `audit-assumptions`: distinguish what each hypothesis contributes to the
  statement, the proof, and the theorem.
- `explain-mathematics`: make advanced mathematics intuitive and exact for
  readers outside the specialty.
- `write-proof-exposition`: reconstruct an established proof as a complete
  cross-specialty mathematical account.
- `consolidate-math-documents`: reconcile several documents into one coherent
  account and safely retire their exact source pairs.

The usual user-controlled path is `formalize-concepts` ->
`explore-mathematical-structure` -> `explore-proof-strategies` ->
`research-mathematics` -> `write-proof-exposition`; skip settled stages and the
final writing stage when it is not needed. `explain-mathematics` can branch from
any stage while preserving the current mathematical status. Phase changes are
explicit `$skill-name` recommendations rather than automatic continuations.

All nine skills remain directly user-invokable. Only `destroy-theory` and
`audit-assumptions` are also model-invokable: `research-mathematics` calls them
as cold, read-only workers during its mandatory challenge step. The other seven
stay user-only, so phase routing cannot silently broaden a request. Short
entrypoints contain only task-specific steps and completion rules; shared
references under `research-mathematics/references/` carry the small integrity,
memory, and conditional computation rules. The exhaustive claim-resolution
reference is research-only.
The [historical paired architecture pilot](mathematician/evaluations/architecture-pair/pilot-results.md)
records the preceding architecture refactor; it does not evaluate the current
task-local-rigor design.
The [research-key semantics corpus](mathematician/evaluations/research-key-semantics/README.md)
checks stable subject identity and writer ownership across the suite.

## Integrity and task-local rigor

Every skill shares four stable mathematical-integrity obligations:

- **Keep the object and claim fixed:** preserve the objects, maps, domains,
  quantifiers, assumptions, and conventions, and treat a changed statement as a
  new claim.
- **Say what the evidence establishes:** distinguish what follows from an
  example, counterexample, computation, heuristic, source, or unsuccessful
  search.
- **Make intuition recoverable:** connect mental models and analogies to the
  exact mathematics they describe, including the point where they fail.
- **State the mathematical status plainly:** separate truth from plausibility,
  usefulness, explanatory value, provenance, and workflow.

These checks guide the work, not the writing style. Canonical documents should
lead with mathematical ideas, examples, arguments, and conclusions; internal
digests, checklists, search logs, and file bookkeeping stay in compact technical
notes or memory unless they help the reader understand the mathematics.

Rigor is otherwise task-local. Exploration finishes with a revealing test and,
when useful, a compact proof handoff. Explanation finishes when its mental model
and examples support the intended reader. Falsification and assumption review
use the exact evidence their conclusions require. Only
`research-mathematics` uses the complete claim-resolution chain:

```text
TARGET -> EVIDENCE -> CHALLENGE -> VERIFY -> STATUS
```

Within that research chain, the target is frozen, evidence is typed and scoped,
challenge attacks the literal claim and dependencies, and fresh verification
separately checks intended statement, encoding, proof, and dependency closure.
The terminal status is `PROVED`, `INCOMPLETE`, `CONJECTURAL`, `REFUTED`, or
`UNRESOLVED`; workflow disposition and support tags remain separate.

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

A key is the document-scoped stable identity of one durable mathematical
subject. Navigation, summaries, report roles, and other workflow wrappers stay
unindexed; one key does not aggregate multiple independently linkable subjects.
Keys survive reordering and status or recommendation changes. All nine skills
inherit this contract. `formalize-concepts` proposes a subject and key but
creates no database; the receiving coordinator decides the authoritative key.

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

Eight skills can coordinate authorized file-backed work. In particular,
`explain-mathematics` and `write-proof-exposition` remain chat-only unless the
user explicitly names an existing canonical target and asks to update or
rewrite it. Such a rewrite updates that Markdown/SQLite pair together; an
explicitly requested separate explanation or proof exposition owns a different
companion and leaves the source pair read-only.

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
