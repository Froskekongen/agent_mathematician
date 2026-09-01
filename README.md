# Agent Mathematician

Nine opt-in skills for exploring, proving, reviewing, and explaining mathematics.

## Skills

- `formalize-concepts` turns an informal idea into precise mathematics.
- `explore-mathematical-structure` compares ways to understand a phenomenon
  through exact realizations and examples.
- `explore-proof-strategies` compares possible proof mechanisms and identifies
  the most promising route.
- `research-mathematics` proves, refutes, repairs, or isolates the open step in
  a substantial claim.
- `destroy-theory` searches for counterexamples, proof gaps, failed encodings,
  and validity boundaries.
- `audit-assumptions` determines what each hypothesis contributes to a theorem
  and its proof.
- `explain-mathematics` makes advanced mathematics intuitive and exact for
  readers outside the specialty.
- `write-proof-exposition` reconstructs an established proof as a complete,
  cross-specialty account.
- `consolidate-math-documents` reconciles several mathematical documents into
  one coherent account.

## Use

Install the skills for your agent:

```sh
git clone https://github.com/Froskekongen/agent_mathematician.git
cd agent_mathematician

python3 mathematician/install_skills.py codex   # Codex or Cursor
python3 mathematician/install_skills.py claude  # Claude Code
python3 mathematician/install_skills.py all     # All supported locations
```

Restart the agent, then name the skill in your prompt:

```text
$formalize-concepts Formalize this idea: ...
$research-mathematics Prove or refute this claim: ...
$explain-mathematics Explain this proof to a graduate student: ...
```

Each skill can be used on its own. For end-to-end work, a typical sequence is
`formalize-concepts` → `explore-mathematical-structure` →
`explore-proof-strategies` → `research-mathematics` →
`write-proof-exposition`; skip any stage you do not need.

## Citation

> Aune, E. (2026). *Agent Mathematician: Agent skills for mathematical
> research* (Version 0.1.1) [Computer software]. Zenodo.
> https://doi.org/10.5281/zenodo.21996114

```bibtex
@software{aune_agent_mathematician_2026,
  author = {Aune, Erlend},
  title = {Agent Mathematician: Agent Skills for Mathematical Research},
  version = {0.1.1},
  year = {2026},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.21996114},
  url = {https://doi.org/10.5281/zenodo.21996114}
}
```

This concept DOI resolves to the latest release. For strict reproducibility,
cite the version DOI shown by Zenodo for that release. See
[`CITATION.cff`](CITATION.cff) and [`LICENSE`](LICENSE).
