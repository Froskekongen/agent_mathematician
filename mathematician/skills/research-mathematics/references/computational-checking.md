# Computational Checking

Use computation in proportion to its mathematical role:

- `discover`: explore examples, patterns, or parameter regimes. Output is
  heuristic or conjectural.
- `falsify`: search for a counterexample to an exact statement. A directly
  verified witness establishes `REFUTED`; an unsuccessful search establishes
  only survival on the tested scope.
- `certify`: prove a scoped proposition via exhaustive enumeration or an
  explicit certificate check, subject to auditing that the code matches the
  mathematical statement.
- `replay`: independently re-verify a retained checker or certificate in a
  clean context.

## Running experiments and checks

1. **Be explicit about the encoding and scope.** State the mathematical
   property encoded, the domain or candidate family actually tested, any
   selection or filtering, and the stopping condition (matching actual control
   flow, including early exits).
2. **Use any appropriate tool or language.** Choose exact or interval
   arithmetic for witnesses and certificates. When floating-point approximation
   carries a claim, state tolerances and error bounds; exploratory numerical
   probing needs only clear scope.
3. **Scale verification to the claim, avoiding redundant runs:**
   - *Exploratory (`discover`):* sanity-check on a known small case and iterate
     freely.
   - *Counterexample found (`falsify`):* verify the witness itself directly
     (analytically or with a minimal exact check) against every hypothesis and
     the negated conclusion. Do not re-run or audit the search that found it.
   - *Proof-bearing check (`certify`):* test known-positive, known-negative,
     and boundary cases. Raise explicit exceptions on failed checks—never rely
     on removable `assert` statements. Prefer emitting an independently
     checkable certificate over trusting a complex search.
4. **Verify cheaply before replaying.** When verifying a load-bearing
   computational step in a fresh context, audit that the encoded check matches
   the intended theorem and verify the witness or certificate. Re-run a full
   exhaustive computation only when no compact certificate exists and runtime
   permits; otherwise state the unverified compute in the trust boundary.

## Retained Python artifacts (file-backed memory only)

Chat-only and exploratory scripts need no special wrapper. When indexing a
retained `.py` file in `research_memory.py`, include one top-level literal dict
`RESEARCH_ARTIFACT` (strings, finite numbers, booleans, `None`, lists, and
string-keyed dicts only; `schema` is integer `1`, `slug`/`kind` are
lowercase-kebab, `target_digest` is 64-hex SHA-256, and `budget` is nonempty):

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

Use only the keys shown above (`parameters`, `seeds`, and `limitations` are
optional), plus optional top-level `result` (dict) and `references` (list of
`{"role", "path", "sha256"}` entries with lowercase-kebab `role` and
repository-relative `path` for replay inputs, certificates, or checkers in
other languages). Keep raw logs in the temporary workpad.

## Reporting

State plainly what proposition was encoded, what scope or attempt denominator
was tested, what resulted, and what mathematical gap (if any) remains between
the computation and the full claim. For proof-bearing checks, note the trust
boundary (runtime, solver or libraries, and whether a certificate or full
search was independently checked).
