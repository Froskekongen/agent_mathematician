# Solver prompts

Use each block in a fresh workspace with only the named skill and its normal
dependencies available. For writable scenarios, request a canonical target
named `note.md`. After the base run, issue its follow-up without resetting the
workspace.

## S1 — `research-mathematics`

**Base:** Research why a continuous convex function on a compact interval
attains its maximum at an endpoint. Retain the endpoint-maximization claim and
the compactness boundary as durable subjects; include an executive summary and
a research decision.

**Follow-up:** Put the research decision first and change the claim status from
"candidate" to "verified" after checking the proof. Do not change the subjects.

## S2 — `explore-mathematical-structure`

**Base:** Explore the relation between graph bipartiteness and absence of odd
cycles. Compare two proof routes and recommend one. Retain the odd-cycle
obstruction and parity-layer model when appropriate.

**Follow-up:** Reverse the candidate comparison order and recommend the other
route, without changing either mathematical subject.

## S3 — `explore-proof-strategies`

**Base:** Explore proof strategies for the irrationality of square roots of
nonsquare integers. Retain the prime-valuation obstruction; include a ranked
strategy table and next-step recommendation.

**Follow-up:** Move the ranked table above the strategy details and mark the
previously preferred route "deferred". The valuation obstruction is unchanged.

## S4 — `audit-assumptions`

**Base:** Audit a proof that every continuous function on an open interval has
a maximum. Retain the missing compactness hypothesis and a boundary witness;
include an audit summary.

**Follow-up:** Reorder the findings and change the recommendation from "repair"
to "reject as stated" without changing the hypothesis or witness.

## S5 — `destroy-theory`

**Base:** Challenge the claim that every differentiable function with bounded
derivative attains a maximum on the real line. Retain the noncompact-domain
counterexample mechanism and its evidence boundary; include a verdict.

**Follow-up:** Put the verdict first and change its label from "disproved" to
"refuted by witness". Keep the mathematical mechanism fixed.

## S6 — `consolidate-math-documents`

**Base:** Consolidate two supplied notes about finite-dimensional norm
equivalence. The first says that the unit sphere of one norm is compact and a
second norm has positive minimum and finite maximum there, yielding comparison
constants. The second says those constants depend on the dimension and norm
pair, so the argument gives no dimension-free bound. Write one canonical target
with a migration ledger and consolidation decision.

**Follow-up:** Reverse source precedence and move the ledger to the end while
preserving both subjects and their meanings.

## S7 — `explain-mathematics`

**Fixture setup:** Begin with a current `note.md` pair. Its Markdown calls
uniform convergence "even closeness," marks the conclusion `checked`, and has
keys `uniform-tail-estimate` and `uniform-limit-continuity`. Its companion has
a reusable card `uniform-tail-proof-pattern`, carrying an `even closeness`
`term` facet and a current link to `uniform-tail-estimate`.

**Base:** Explicitly rewrite the existing canonical `note.md` in place to
explain why uniform convergence preserves continuity. Preserve the uniform-tail
estimate and continuity-of-the-uniform-limit conclusion; replace "even
closeness" by the standard term "uniform convergence" in both the note and
reusable memory. A supporting pointwise-limit statement does not need its own
key unless it is retained as an independently linkable subject.

**Follow-up:** Reorder motivation and proof, replace a pedagogical synonym with
the standard term, and change the conclusion status from "checked" to
"accepted" without changing either subject.

## S8 — `formalize-concepts`

**Base:** Formalize the informal idea "a sequence eventually stays inside every
tolerance band around its limit" for handoff to a writer. Identify the durable
subject and suggest a semantic key.

**Follow-up:** Reorder the definition and quantifier explanation and label the
handoff "ready". Do not invoke a writer or create a database.
