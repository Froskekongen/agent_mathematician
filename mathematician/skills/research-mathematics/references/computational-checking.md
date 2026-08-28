# Computational Checking Role

This is a shared internal role, not a user-facing skill. A public mathematical
skill loads it only when computation or executable checking can materially
change a research decision, then dispatches the work to a fresh specialist
context. The specialist returns evidence to the coordinator and writes neither
canonical Markdown nor research memory.

Keep hand-checkable arithmetic and disposable examples in the calling skill.
Dispatch this role for broad, randomized, selected, expensive, or
load-bearing computation; claimed exhaustiveness; a promoted counterexample;
or an executable certificate or checker.

## Modes and evidence ceilings

Choose one mode:

- `discover`: expose structure or candidates. Output remains heuristic or
  conjectural.
- `falsify`: seek a witness to an exact negation. A fully checked witness may
  establish `REFUTED`; a failed search establishes only survival on its scope.
- `certify`: check an exhaustive computation or explicit certificate. It may
  prove the encoded scoped proposition after the trust boundary and semantic
  correspondence are audited.
- `replay`: independently reproduce a retained result without the builder's
  hidden state. Replay validates the recorded artifact, not a broader claim.

## Input contract

Receive the frozen target and digest, exact computational question, mode,
permitted evidence ceiling, search or certificate scope, resource budget, and
artifact-retention policy. Clarify an ambiguity only when it changes the
encoded proposition or evidential force.

## Build the smallest decisive artifact

1. State the mathematical proposition and its encoding. Identify fixed and
   search variables, valid-candidate predicate, evaluator, denominator,
   selection rule, budget, and stopping rule as applicable. Match the stopping
   description to actual control flow, including any justified early exit and
   which branches remain exhaustive.
2. Design the smallest experiment or checker that answers the question.
   Prefer exact arithmetic for witnesses and certificates. For numerical work,
   state precision, tolerance, conditioning, and error policy.
3. Run known-positive, known-negative, boundary, vacuity, and malformed-input
   controls relevant to the artifact. Use mutation or a structurally different
   cross-check for a load-bearing checker. Make certificate obligations fail
   closed: do not carry them only in removable assertions, and for Python
   either replay under `-O` or statically establish that optimization cannot
   bypass a required check.
4. Execute within the recorded budget. Preserve failures and the total attempt
   denominator, not only selected successes.
5. Distinguish mathematical failure, encoding mismatch, implementation error,
   and resource exhaustion.

## Self-describing Python artifacts

A retained executable artifact is a Python source file with one top-level
literal dictionary named `RESEARCH_ARTIFACT`. The program reads the same
dictionary at runtime; tooling may inspect the assignment with Python's
standard `ast` module and `ast.literal_eval` without importing or executing the
file. Keep the value literal: strings, numbers, booleans, `None`, lists, and
dictionaries only.

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
    "evidence_ceiling": "Exhaustive only on the encoded finite scope.",
    "reproduce": {
        "argv": ["python3", "artifacts/rank_search.py", "--max-degree", "6"],
        "runtime": "CPython 3.14",
        "parameters": {"max_degree": 6},
        "seeds": [],
        "budget": {"candidates": 1842},
        "stopping_rule": "Exhaust the declared finite family.",
    },
    "limitations": ["No claim beyond degree six."],
}
```

The dictionary is the artifact metadata; create no sidecar manifest. Use an
argument vector rather than a shell command. Put replay-critical local files in
optional `references` entries with their role, repository-relative path, and
SHA-256. Optional `result` records the declared outcome. The research-memory
tool computes the whole source-file hash because a source cannot contain its
own hash. Raw logs and routine outputs stay in the temporary workpad; retain a
dataset or certificate only when later inspection or replay requires it.

The retained contract requires integer schema `1` (not a boolean), one of the
four controlled modes, `target_digest`, `encoded_target`, `evidence_ceiling`,
and a reproduction block containing `argv`, `runtime`, a nonempty `budget`,
and `stopping_rule`. This is deliberately stricter than disposable computation:
if evidence is worth retaining, its target, ceiling, and termination must be
recoverable without the builder's context.

Python is the initial reproducible envelope. A checker implemented in another
language may be invoked by the Python artifact and listed in its inputs with a
digest; adding another metadata convention waits for a demonstrated need.

## Fresh replay for load-bearing results

The builder cannot perform the final replay of its own load-bearing artifact.
Give a fresh specialist the frozen target, retained files, and documented
command, but no hidden builder state or persuasive narrative. The replayer:

- validates artifact and input hashes;
- reconstructs the environment declared by the artifact;
- runs controls before the main command;
- compares the observed and expected outcomes;
- inspects the encoded-target/intended-target correspondence; and
- reports the trust boundary, including runtime, libraries, parser, checker,
  certificate format, and allowed assumptions.

## Return contract

Return the mode, target digest, encoded proposition and scope, method, attempt
denominator, result, evidence class and ceiling, controls and cross-checks,
artifact path and observed hash, reproduction command, trust boundary,
limitations, and exact open obligations. For `replay`, include every mismatch
or abstention. The role is complete only when another agent can tell precisely
what was tested, reproduce it from retained artifacts, and avoid inferring a
stronger mathematical conclusion.
