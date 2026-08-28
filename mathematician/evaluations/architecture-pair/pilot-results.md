# One-repeat architecture pilot

This pilot asks a narrow engineering question: can the revised skill and
memory architecture preserve mathematical rigor while reducing the routed
instruction surface and tool burden of the current suite? It is not a general benchmark of
mathematical ability.

## Frozen arms

- Current arm: Git commit
  `38740199ec1d0266cd9c1425d0d81f8bcffd2595`.
- Evaluated revised arm: immutable tree archive SHA-256
  `0faf0144814ebad049ddb3fbeca3374eebf754f3e8413417e456f927fb450318`.

The live revised tree has three small classes of post-pilot hardening and is
therefore intentionally not byte-identical to the evaluated archive:

1. facet order is canonicalized before card hashing;
2. executable checks must fail closed under optimization and their stopping
   prose must match actual early exits; and
3. routing now says not to load the computational contract merely to classify
   a hand check, and not to create cards that only duplicate canonical or
   artifact content.

## Static complexity

The runtime set counts every public `SKILL.md` plus the conditional references
reachable at runtime. In the current arm it also includes
`evidence-based-methods.md`, because the old research workflow routed it; the
revised file is a maintainer rationale and is not routed.

| Measure | Current | Evaluated revised | Live revised |
|---|---:|---:|---:|
| Public skill lines | 939 | 633 | 634 |
| Public skill words | 8,440 | 3,958 | 3,972 |
| Full routed-runtime lines | 1,621 | 1,167 | 1,175 |
| Full routed-runtime words | 14,012 | 7,210 | 7,295 |
| Canonical + memory implementation lines | 3,860 | 2,723 | 2,724 |
| Public canonical/memory commands | 14 | 4 | 4 |

Against current, the live suite removes 52.9% of public-skill words, 47.9% of
all runtime words, 29.4% of memory implementation lines, and 10 of 14 public
commands. The canonical-section parser remains an internal module rather than
a second user-facing CLI.

## Pilot protocol

The corpus uses four internet-sourced problems of increasing workflow demand:

- P1 and P3 are the 2023 Putnam A1 and A2 problems, from the
  [official MAA solutions](https://maa.org/wp-content/uploads/2024/10/2023_Putnam_Solutions_A.pdf);
- P2 is [Project Euler problem 46](https://projecteuler.net/problem=46); and
- P4 is the Lander--Parkin counterexample published by the
  [American Mathematical Society](https://doi.org/10.1090/S0002-9904-1966-11654-3).

P1 used the full orchestration profile: solver, falsifier, assumption auditor,
fresh internal verifier, then a separately cold persisted-result verifier.
P2--P4 used a controlled core profile: the solver had no subagents and ran
local challenge passes, followed by a separate cold verifier. Both arms used
the same profile within each problem. Solvers and cold verifiers had no
internet, answer key, prior conversation, other trial, or opposite-arm access.

The first revised P4 session accidentally received `k >= 2` instead of the
corpus's `k > 2`. Although its `k=5` witness answers both statements, that run
is invalid for a paired comparison. It was excluded and replaced by a fresh,
isolated corrected solver and cold verifier. The corrected datum is labelled as
such rather than presented as a pristine first attempt.

## Mathematical outcome and grading

Two independent graders used the checked-in 100-point rubric and answer key.
They agreed exactly on every score.

| Problem | Required outcome | Current | Revised | Critical failure |
|---|---|---:|---:|---|
| P1 | least index `18`, with minimality | 99 | 99 | none |
| P2 | least exception `5777`, exhaustive certificate | 100 | 99 | none |
| P3 | only additional roots `x = ±1/n!` | 100 | 100 | none |
| P4 | exact four-term fifth-power counterexample | 100 | 99 | none |

All eight official runs are rigor-passing. Every run earned full correctness,
status, completeness, statement-fidelity, and challenge/verification points.
The revised mean is 99.25 versus 99.75 current; the half-point mean difference
comes entirely from two artifact-hygiene findings:

- P2's stopping prose could be read as claiming that a helper visits every
  admissible square after it has already found the existential witness; and
- P4's checker placed required obligations in removable Python `assert`
  statements, although the normal replay and independent Ruby reconstruction
  both passed.

The live computational contract now addresses both findings. Scores were not
retroactively changed.

## Measured cost

Instruction bytes are the distinct architecture skill/reference surface
reported by the solver plus its cold verifier. They are not token counts or
aggregate model context and do not sum repeated specialist reads. For example,
the current P1 solver reported 60,976 distinct bytes but 93,942 bytes after its
specialist rereads; the revised aggregate was not reported, so no aggregate
P1 context comparison is made. The corrected revised P4 solver also loaded
6,637 bytes from an external mandatory coding skill; that is excluded from the
architecture column and disclosed below. Wall times use the bounded windows
reported by each session, whose setup/report boundaries were not perfectly
uniform.

| Problem | Instruction bytes, current -> revised | Scoped wall seconds, current -> revised | Retained bytes, current -> revised | Score, current -> revised |
|---|---:|---:|---:|---:|
| P1 | 107,116 -> 47,641 (-55.5%) | 1,365 -> 804 (-41.1%) | 108,471 -> 144,827 (+33.5%) | 99 -> 99 |
| P2 | 107,116 -> 46,010 (-57.1%) | 863 -> 980 (+13.6%) | 114,276 -> 156,293 (+36.8%) | 100 -> 99 |
| P3 | 107,116 -> 39,704 (-62.9%) | 858 -> 409 (-52.3%) | 107,191 -> 148,016 (+38.1%) | 100 -> 100 |
| P4 corrected | 107,116 -> 49,930 (-53.4%) | 532 -> 847 (+59.2%) | 108,213 -> 145,810 (+34.7%) | 100 -> 99 |
| **Total** | **428,464 -> 183,285 (-57.2%)** | **3,618 -> 3,040 (-16.0%)** | **438,151 -> 594,946 (+35.8%)** | **399 -> 397** |

Including the external P4 coding skill changes the total instruction reduction
from 57.2% to 55.7%. The wall-time result is mixed rather than uniformly
better: P1 and P3 became much faster, while the computation-heavy P2 verifier
and tiny-certificate P4 became slower. With only one repeat and differently
scoped timers, the aggregate 16% reduction is descriptive, not a stable speed
estimate.

The most comparable direct tool measure is canonical/memory CLI use:

| Problem | Current solver / cold | Revised solver / cold |
|---|---:|---:|
| P1 | 17 / 5 | 6 / 3 |
| P2 | 13 / 5 | 7 / 4 |
| P3 | 29 / 5 | 7 / 3 |
| P4 corrected | 15 / 7 | 19 / 7 |
| **Total** | **74 / 22** | **39 / 17** |

Across the pilot this is 96 calls current versus 56 revised, a 41.7%
reduction. P4 is the important exception: the revised solver curated a card,
artifact, and content-bound links for a witness whose canonical proof was
already self-contained. The live guidance now forbids such duplicate cards,
but richer artifact indexing still has a real fixed cost.

## Interpretation

The redesign passes the pilot's adoption criterion: no material quality
regression, no critical failure, and a large reduction in both the distinct
routed instruction surface and aggregate memory-interface calls. It also
produces a more legible evidence chain:
`TARGET -> EVIDENCE -> CHALLENGE -> VERIFY -> STATUS`, with truth status
separate from workflow disposition and solver-stage `INCOMPLETE` used honestly
while a mandated cold gate remains open.

The costs are also clear:

- an empty schema-4 companion is 139,264 bytes rather than 102,400 bytes, a
  fixed 36 KiB increase for richer indexes, facets, native artifacts, hashes,
  and links;
- retained P2/P4 programs are larger because their language-native
  `RESEARCH_ARTIFACT` dictionaries and controls are self-contained; and
- `apply` remains the densest part of the interface even though the top-level
  command surface is smaller.

The next evaluation should run three alternating repeats, persist a common
whole-arm identifier and normalized host telemetry, and use at least one fresh
problem per mode. This pilot's per-session reports and trial databases remained
outside the repository, so this file is a scored summary rather than a complete
replay bundle. Until a durable run archive exists, treat the instruction-surface
and command reductions as strong pilot evidence, the wall-time result as
suggestive, and the quality result as evidence of non-regression rather than
superiority.
