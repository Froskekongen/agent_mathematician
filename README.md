# Agent Mathematician

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21996114.svg)](https://doi.org/10.5281/zenodo.21996114)

Agent skills for rigorous mathematical research. The suite helps agents formulate and verify substantial claims, attack theories and proofs, audit assumptions, and explain advanced mathematics.

## Skills

- `research-mathematics`: research, formulate, prove, verify, or repair substantial mathematical claims.
- `explore-proof-strategies`: bounded exploration of diverse proof routes and cross-field bridges.
- `formalize-concepts`: lightweight development of an informal idea into a selected mathematical formalism.
- `destroy-theory`: stress-test statements and proofs, search for counterexamples, and identify failure boundaries.
- `audit-assumptions`: locate hidden assumptions, trace where hypotheses are used, and test whether they can be weakened.
- `explain-mathematics`: explain advanced mathematics to mathematically mature nonspecialists.

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
