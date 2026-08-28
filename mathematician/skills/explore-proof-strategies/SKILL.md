---
name: explore-proof-strategies
description: Explore a bounded, mathematically disciplined portfolio of proof strategies and preserve any candidate proof for later rigorous verification.
disable-model-invocation: true
---

# Explore Proof Strategies

Scout broadly, test cheaply, and stop with a useful proof architecture. Preserve mathematical precision and visible obligations without performing the exhaustive certification owned by `research-mathematics`.

When no claim is ready and the user instead wants to discover which structures or questions deserve investigation, recommend `$explore-mathematical-structure` rather than manufacturing a proof target.

## Execution role and research state

Choose the role before doing any work:

- **Nested research specialist:** work against the exact target or candidate supplied by the coordinator. Treat the canonical document and every research-memory database as read-only. Return a content-bound report to the coordinator; do not create, edit, or delete theory artifacts.
- **Standalone report-only:** answer in the conversation without changing the filesystem. Do not initialize a companion database or create a persistent report.
- **Standalone writable theory round:** use this role only when the user has authorized changes to a file-backed theory workspace. Own one canonical document and its one home research-memory database; open every foreign theory database read-only. Use one OS-temporary workpad for the round and close it according to the shared protocol.

Default to report-only when writable authority or a home theory is absent. For a nested or standalone writable round, read the canonical document first. Before using research memory, read the shared [research-memory protocol](../research-mathematics/references/research-memory.md) and use its [CLI](../research-mathematics/scripts/research_memory.py). Query `active`, `open`, and `parked` summaries before generating routes. Query `rejected` cards only when a similar route is under consideration.

The temporary portfolio, cheap screens, candidate variants, bridge sketches, and scout reports are workpad material. They are not durable theory artifacts.

## 1. Frame the working target

Record:

- the literal claim;
- the working interpretation and any alternatives that change the problem;
- the objects, quantifiers, and assumptions needed to discuss proof routes;
- user-supplied constraints on methods, time, or compute.

Use a lightweight working target rather than a full assumption catalog. Ask for clarification only when different answers would materially change the truth or relevant strategies.

Complete this phase when candidate routes can be judged relevant or irrelevant to the same stated target.

## 2. Run a cheap truth screen

Test the smallest useful cases, scaling or dimensional consistency, boundary and degenerate cases, and one plausible obstruction. Use small symbolic or numerical experiments when they are cheaper than speculation.

Certify a decisive counterexample against every hypothesis before calling the target false. Otherwise report only that the target was not refuted within the stated screen.

Complete this phase when an immediate defeat is exposed or the exact scope of the surviving sanity checks is recorded.

## 3. Build a structural fingerprint

Identify the features that could do mathematical work: invariance, monotonicity, convexity, compactness, coercivity, orthogonality, duality, recursion, extremality, algebraic closure, local-to-global structure, spectral structure, or another mechanism adapted to the target.

Name the likely bottlenecks and tie every later route to at least one concrete feature. Complete this phase when the portfolio can be generated from the problem's structure rather than a generic list of proof styles.

## 4. Build a strategy portfolio

Generate materially different routes. Always consider the simplest native approach, then scan relevant analytic, algebraic, geometric, probabilistic, combinatorial, variational, spectral, categorical, computational, or other viewpoints.

Count routes as different only when their central invariant, representation, reduction, or hard lemma differs. Seek nontrivial combinations of fields, but retain a combination only when its mathematical interface can be stated.

For each route, record:

- central mechanism and outline;
- assumptions and imported results it appears to need;
- hardest subgoal;
- likely failure mode;
- current disposition: `advance`, `park`, or `reject`.

Reject a route only on a demonstrated obstruction. Park shallow failures and unverified analogies rather than overstating them.

Keep the complete route portfolio in the report or temporary workpad. Persistence is a later curation decision, not a consequence of having considered a route.

### Adapt effort

Start with a bounded pass and allocate further effort by expected information gain:

- broaden when the routes are cosmetic, all fail cheaply, or a structural feature remains unexplained;
- deepen when a route has a concrete mechanism and a small number of identifiable crux lemmas;
- use a bounded parallel scout round only when additional breadth justifies its cost;
- use targeted computation or theorem lookup when it can decide a route;
- stop when the next useful step is broad literature work, a large proof DAG, exhaustive attack, assumption audit, or independent verification.

Treat `quick` and `wide` in the user's invocation as optional budget modifiers. Otherwise adapt to the problem and report the explored scope and stopping reason.

Complete this phase when the portfolio is structurally diverse enough to support a reasoned shortlist or when the budget is exhausted visibly.

## 5. Certify cross-field bridges

For every retained cross-field route, give a bridge certificate:

1. original object and translated object;
2. structure preserved, reflected, or deliberately lost;
3. exact target subgoal addressed;
4. theorem or mechanism expected to transfer;
5. return map to the original target;
6. compatibility conditions and assumptions still open;
7. cheapest test that could break the bridge.

Treat theorem names and analogies as search leads until their exact statements and hypotheses are checked. Complete this phase when every retained hybrid has an explicit interface rather than a thematic resemblance.

## 6. Pressure-test and deepen

Give each serious route one adapted cheap test. Deepen the best routes into short lemma-level architectures and identify the decisive next calculation, example, lookup, or lemma for each.

Keep verified local facts, heuristic evidence, analogies, and speculative transfers visibly distinct. Complete this phase when the ranking, crux, and next action are mathematically justified.

## 7. Capture a candidate proof

When an end-to-end argument appears, stop branching and record it completely enough for later checking. Label it exactly:

`CANDIDATE FULL PROOF — NOT CERTIFIED`

Include:

- the exact working theorem;
- the complete argument currently available;
- assumptions introduced during the argument;
- imported results and their checking status;
- compressed, fragile, or doubtful steps;
- verification phases not yet performed.

Perform one local coherence pass for missing links and circularity. Keep the draft in the returned report or temporary workpad without running a separate adversarial, assumption, or independent-verification campaign.

In a standalone writable round, place the strongest candidate proof in the canonical document with the uncertified label intact. In nested and report-only roles, return it to the caller. Database persistence never upgrades a route, lemma, or proof to `PROVED`.

## Consolidate a writable round

For a standalone writable theory round, keep these destinations distinct:

- Put the exact target, selected proof architecture, strongest candidate proof, decisive evidence, and immediate proof obligation in the canonical document.
- Propose research-memory cards only for reusable open obligations, parked routes with a concrete revival condition, or rejected routes with a demonstrated obstruction. A retained card must be self-contained and record the relevant bottleneck, bridge-applicability analysis, next test, reason, or revival condition.
- Leave the full brainstorming portfolio, cheap failures, superseded drafts, and routine probes in the temporary workpad.

Apply the curated card batch only after the canonical update is ready. Validate the home database, then delete the workpad. If canonical integration, database application, or validation fails, retain the workpad and report its exact path. A nested specialist only recommends these destinations; the coordinator performs consolidation.

## Report

Return:

1. **Working target and ambiguities**
2. **Sanity-screen results and scope**
3. **Structural fingerprint**
4. **Strategy portfolio**
5. **Cross-field bridge certificates**
6. **Ranked routes, cruxes, and decisive next tests**
7. **Candidate full proof**, when one emerged
8. **Explored scope and stopping reason**
9. **Research handoff** containing the literal claim, working interpretation, examples, selected routes, open lemma chain, imported-result status, rejected routes, and first recommended proof obligation
10. **Canonical and research-memory recommendations**, when nested in or closing a writable theory round

The report is returned in the conversation or to the coordinator rather than persisted as a separate artifact. A route or candidate proof from this skill has no `PROVED` status. Recommend an explicit `$research-mathematics` follow-up when the user wants rigorous resolution or certification.
