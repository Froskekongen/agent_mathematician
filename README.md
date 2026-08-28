# Agent Mathematician

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21996114.svg)](https://doi.org/10.5281/zenodo.21996114)

Agent skills for mathematical exploration and rigorous research. The suite helps agents formalize ideas, use mathematical structures as test beds for intuition, formulate and verify substantial claims, attack theories and proofs, audit assumptions, and explain advanced mathematics.

## Skills

- `research-mathematics`: research, formulate, prove, verify, or repair substantial mathematical claims.
- `explore-mathematical-structure`: iteratively explore a selected formalism through examples, viewpoints, structural patterns, and conjectures so the user can choose a direction.
- `explore-proof-strategies`: bounded exploration of diverse proof routes and cross-field bridges.
- `formalize-concepts`: lightweight development of an informal idea into a selected mathematical formalism.
- `destroy-theory`: stress-test statements and proofs, search for counterexamples, and identify failure boundaries.
- `audit-assumptions`: locate hidden assumptions, trace where hypotheses are used, and test whether they can be weakened.
- `explain-mathematics`: explain advanced mathematics to mathematically mature nonspecialists.

The typical discovery path is `formalize-concepts` -> `explore-mathematical-structure` -> `explore-proof-strategies` -> `research-mathematics`. Skip stages when the formalism, target, or proof direction is already settled.

## Research memory

Authorized file-backed research uses three information layers:

1. a self-contained canonical Markdown document;
2. a Git-tracked `<stem>.research.sqlite` companion containing curated open,
   active, parked, rejected, and integrated research-memory cards; and
3. one generated OS-temporary workpad for raw round state, deleted after
   successful consolidation.

The canonical document remains authoritative. The database preserves useful
noncanonical directions, obstructions, counterexamples, assumption
relaxations, and source-applicability notes; it never holds mathematics needed
to understand or trust the canonical result. Raw workpads and specialist
reports are not stored in the database.

`research-mathematics` and `explore-mathematical-structure` coordinate this
lifecycle directly. `explore-proof-strategies`, `destroy-theory`, and
`audit-assumptions` do so only for an authorized standalone theory round. When
nested under a coordinator, all three are read-only specialists and the
coordinator is the sole writer. `formalize-concepts` and ordinary
`explain-mathematics` do not participate in the database lifecycle.

The first file-backed round creates an empty companion and adds this locator to
the canonical frontmatter:

```yaml
research_memory:
  path: ./theory.research.sqlite
  schema: 1
  optional_for_understanding: true
```

Companions are binary Git artifacts. Different theories can advance in
parallel, but competing branch versions of the same database must be
reconciled semantically rather than binary-merged.
Skills report an untracked companion at closure and do not stage or commit it
without separate authorization.

The suite ships one standard-library CLI at
`research-mathematics/scripts/research_memory.py` with `init`, `apply`,
`search`, `show`, and `check` commands. Its complete lifecycle and card
contract live in `research-mathematics/references/research-memory.md`. These
are shared resources inside the existing skill; there is no additional
user-facing skill.

```sh
python3 mathematician/skills/research-mathematics/scripts/research_memory.py init --canonical theory.md --theory theory
python3 mathematician/skills/research-mathematics/scripts/research_memory.py search --db theory.research.sqlite
python3 mathematician/skills/research-mathematics/scripts/research_memory.py show --db theory.research.sqlite --slug a-semantic-slug
python3 mathematician/skills/research-mathematics/scripts/research_memory.py apply --db theory.research.sqlite --input round-batch.json
python3 mathematician/skills/research-mathematics/scripts/research_memory.py check --db theory.research.sqlite
```

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
