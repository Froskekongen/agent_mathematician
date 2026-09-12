# Research-memory prose pilot

The final reference is **684 words**, down from **1,150** (a **40.5% reduction**). It remains one shared note with the same commands, storage contract, ownership, and loading triggers. The revision removes implementation exposition and repeated directions while preserving subject identity, selective memory, and safe closing.

This is a small behavioral check, not evidence that the original note caused worse mathematics. The first candidate exposed a curation weakness, so the final note includes a focused correction and a repeated affected pair.

## Frozen arms and protocol

All arms start from the same 30-file working-tree skill snapshot, including the user's then-current proof-strategy edits. Only `research-mathematics/references/research-memory.md` differs. The live proof-strategy skill and related files continued changing concurrently; those later changes were neither overwritten nor introduced into one trial arm. Shared integrity prose was preserved.

| Arm | Note words | SHA-256 of sorted path/hash manifest |
| --- | ---: | --- |
| Baseline | 1,150 | `91b557037df1ba5033ef2e8e2543629c1232afd29aeeb7394dc27cd96216b03e` |
| Initial candidate | 675 | `700d71cd3c860b0854c4d1774c613258e67bc719b7e1724d537f23f0faaf1901` |
| Final candidate | 684 | `256f7815aab429807e027084189575dfd95085051823f6e3a59c1c8d18eabc48` |

The initial comparison used one old/new pair for each of S7 (uniform-convergence rewrite and follow-up), S3 (square-root proof strategies and follow-up), and a known-card history request. S7 and S3 requests are based on the [existing semantic corpus](../research-key-semantics/prompts.md). Fixture pairs were created once with the frozen CLI and copied byte-for-byte to both arms. The history fixture records a parked, unresolved oscillatory-integral approach alongside a separate proved geometric example.

Each base run used a fresh agent context; its follow-up used that same agent. Solvers had identical requests and dependencies except for the note, used inherited model/reasoning settings without overrides, and were instructed not to inspect the opposite arm, use the internet, or consult peer agents. The collaboration interface does not expose the exact backend model settings. Evidence capture was explicitly requested in every arm and is not counted as unwanted prose.

A fresh reviewer received anonymous canonical notes, responses, memory exports, initial fixtures, and requests, without instruction variants or arm mappings. Labels were assigned separately by case. It assessed motivation, explanatory connections, appropriate detail, mathematical fidelity, and intrusive bookkeeping, with a separate check of useful memory and preserved subjects. Its judgments are qualitative, not an ability score.

## Findings and correction

| Case | Initial blind comparison | Operational result |
| --- | --- | --- |
| S7 | Tie: baseline explains the nonuniform counterexample more concretely; candidate orders the follow-up more smoothly. | Both retain the two subject keys, synchronize terminology and facets, and close at revisions 2 then 3. |
| History | Narrow preference for candidate: it explains why the origin needs a separate estimate. | Both accurately distinguish parked from unresolved, preserve the limits of finite sampling, and leave the original pair byte-for-byte unchanged. |
| S3 | Canonical explanations nearly tie; narrow baseline preference overall because its memory adds useful material. | Both retain their subject keys and the valuation obstruction through deferral, with current pairs at revisions 1 then 2. |

The initial candidate's S3 run stored a large `proof-review-handoff` card that largely repeated the canonical arguments. Its higher-root card was useful, and the mathematics was correct, but the duplicate handoff was a curation weakness worth fixing under the existing contract.

The final note removes the broad instruction to keep bookkeeping in SQLite and restores the explicit guard against merely duplicating canonical results or artifact metadata. It says to retain the reusable addition with enough context to use it. This permits useful self-contained history while avoiding a second copy of the mathematical account. An independent instruction review confirmed that both changes preserve the baseline semantics.

Only the affected S3 pair was repeated in two fresh solver contexts. The baseline was repeated too; neither arm's earlier output was reused. A second fresh blind reviewer assessed that pair without the initial findings.

The second reviewer narrowly preferred the final candidate across the two stages. Both arms preserved sound mathematics, keys, and the requested deferral. The final candidate's review card added several concrete checks beyond its canonical account, although both cards still repeated substantial context. The baseline had corrupted inline mathematical notation in its base output and repaired it in the follow-up. That incident influenced the preference and is a confound, not evidence that shortening the note improves formatting. On final canonical prose alone, the comparison was close; the baseline gave a stronger discussion of modular methods. No material exposition regression was observed in the final candidate.

## Validation and limits

The invocation tests now parse the documented locator and key examples with the existing canonical parser instead of requiring particular jargon, bold labels, or sentence order. Invocation and link checks remain. The latest full workspace run passed **54 tests**; the earlier unrelated proof-strategy wording failure was resolved by concurrent changes. The two directly affected tests also passed after the final note correction. Changed files pass whitespace checks.

The optional bundled `quick_validate.py` could not run because PyYAML is unavailable in both Python runtimes checked. No dependency was installed for an unchanged skill manifest; repository invocation and packaging checks ran in the full suite.

An independent script checked all **12 retained writable states** with the frozen CLI: each pair was current and passed integrity checks. Subject keys remained stable through the follow-ups, including the required valuation obstruction; both S7 arms synchronized the terminology facets. Both history pairs remained byte-for-byte unchanged. The reviewers separately checked mathematical meaning and appropriate interpretation of disposition. Database currency does not certify mathematical conclusions.

S7 and History exercised the initial 675-word candidate. The final 684-word correction was retested on S3 only, as planned for an affected-case revision. The initial evidence remains retained. One adaptive repeat does not establish stable improvements in prose quality, speed, or mathematical ability. Word counts describe the note itself, not total context tokens. Operation logs are solver-recorded evidence rather than exhaustive instrumented telemetry.

## Evidence and replay

[evidence.zip](evidence.zip) retains all three frozen skill sets and manifests; exact dispatch/follow-up prompts and arm mapping; fixture pairs and their creation script; base/follow-up Markdown/SQLite pairs, responses, and recorded CLI outputs; anonymized samples and independent reviews; the removal audit; test outputs; and the independent retained-state validation script/results.

Extract into a temporary directory. `python3 -B validate_outputs.py` rechecks the retained pairs with the frozen baseline CLI. To repeat a solver run, copy its arm's skill set to `runs/<id>/skills`, restore the initial fixture (or start with an empty S3 work directory), and use the saved prompt with the extracted directory substituted. Keep base and follow-up in one context and different arms in fresh contexts. Recreating fixtures requires empty fixture pair directories; the archived pairs already preserve the exact original inputs.
