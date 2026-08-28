# Paired architecture evaluation

This corpus compares the current mathematical-skill architecture with its
replacement on the same four small problems. It is a paired engineering
evaluation, not a claim about general mathematical ability.

The completed one-repeat pilot and its limitations are reported in
[`pilot-results.md`](pilot-results.md).

The corpus deliberately has no runner or scoring program. The host already
records token and tool use, while mathematical grading requires the reasoning
in `answer-key.md`. Automate only after the protocol has survived a pilot.

## Answer isolation

- Give solvers only the common envelope and one task from `prompts.md`.
- Do not mount, quote, or mention `answer-key.md` in a solver workspace.
- Disable network access and browsing for both arms. Exact searches for these
  published statements would otherwise disclose solutions.
- Keep each solver and cold-verifier conversation fresh. Reuse only the files
  deliberately persisted by the solver.

These are published problems and may occur in model training data. That limits
their value as an absolute capability benchmark, but not the paired comparison:
both arms use the same model and prompts, and graders require a complete
argument rather than an answer alone.

## Arms

Record an immutable identifier for each arm before running:

- **Current:** the Git `HEAD` from immediately before the redesign.
- **Revised:** the exact revised working-tree snapshot. Prefer a commit; if it
  is not committed, archive the entire tree and record its content digest.

Run each arm in a separate checkout with a fresh trial directory. Do not share
databases, canonical documents, artifacts, caches, or conversation history
between arms.

Keep all other conditions equal: model snapshot, reasoning effort, system
prompt, permissions, time limit, and output limit. If the runtime exposes a
seed, pair identical seeds. Otherwise use three repeats and alternate arm order
`current/revised`, `revised/current`, `current/revised`.

## One paired trial

For problem `P` and repeat `R`:

1. Create one empty workspace per arm.
2. Start a fresh solver with the common solver envelope followed verbatim by
   task `P` from `prompts.md`.
3. Preserve the solver's canonical document, memory database, and native
   artifacts. Do not preserve its conversation.
4. Start a fresh cold verifier in the same arm and workspace with the cold
   verification prompt from `prompts.md`.
5. Save both final responses, retained files, execution logs, and host usage
   counters under an opaque run ID. Do not put the arm name in material shown
   to graders.
6. Two graders independently score the run using `answer-key.md`. Reconcile a
   critical-failure disagreement or a total-score difference greater than five.

Run a one-repeat pilot first: 16 sessions (four problems, two arms, solver plus
verifier). If the isolation and measurements work, run all three repeats: 48
sessions total.

## Quality rubric (100 points)

Score the final persisted result together with the cold-verifier report.

| Dimension | Points | What earns full credit |
|---|---:|---|
| Mathematical correctness | 25 | The conclusion and every load-bearing inference are correct. |
| Status calibration | 15 | The stated status matches the evidence; bounded evidence is not promoted to an unbounded theorem. |
| Completeness | 20 | All requested quantifiers, cases, existence claims, and minimality claims are closed. |
| Statement/encoding fidelity | 15 | Any computation checks exactly the mathematical predicate, domain, and boundary claimed. |
| Challenge and verification | 15 | Edge cases and plausible failure modes are attacked; load-bearing computation is independently replayed or reconstructed. |
| Reproducibility and artifact hygiene | 10 | Retained code is deterministic or records seeds/budgets, has sufficient native in-code metadata, and needs no separate manifest. |

A run is **rigor-passing** only if it scores at least 85, earns at least 20/25
for correctness and 12/15 for fidelity, and has no critical failure.

Critical failures are:

- a wrong requested conclusion;
- declaring a target proved without closing a load-bearing case or search
  universe;
- using a computation whose encoded predicate materially differs from the
  stated claim;
- reading a source or answer key during the trial;
- a cold verifier accepting a corrupt or unreplayable load-bearing artifact as
  verified.

## Cost record

Do not fold cost into the quality score: a cheap wrong answer must never beat a
costly correct one. For each solver and verifier phase, record these raw values,
using `NA` rather than zero when the host cannot expose one:

- total input and output tokens;
- input tokens attributable to skill/reference text and tool output, if known;
- unique skill/reference files loaded and their total bytes;
- tool calls and failed tool calls, grouped by filesystem, shell, memory, and
  delegation;
- wall-clock time;
- retained file count and bytes, with source lines for executable artifacts;
- bytes returned by memory reads, if distinguishable.

Report per-problem paired differences and the median over repeats. Compare cost
only among rigor-passing runs. The revised architecture succeeds when it has no
material quality regression on any problem and reduces median context burden
or tool burden; publish the full metric vector rather than one synthetic
"efficiency score."

## Recommended result table

| Problem | Arm | Repeat | Quality | Critical failure | Input tokens | Skill/reference bytes | Tool calls | Wall time | Retained bytes |
|---|---|---:|---:|---|---:|---:|---:|---:|---:|

Also record qualitative differences that raw counts miss: unnecessary role
dispatch, repeated reading of the same rules, avoidable database operations,
missing cold replay, and unjustified status promotion.

## Coverage

| Problem | Main mode | Why it is present |
|---|---|---|
| P1 | Short proof | Detects fixed protocol overhead on an easy but nontrivial argument. |
| P2 | Bounded exhaustive computation | Tests minimality, primality fidelity, executable checking, and embedded native metadata. |
| P3 | Moderate proof | Tests quantifiers, root accounting, and whether a clean proof survives adversarial review. |
| P4 | Counterexample discovery/certification | Tests truth triage, exact witness checking, and resistance to claiming unproved minimality. |
