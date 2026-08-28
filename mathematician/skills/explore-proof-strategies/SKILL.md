---
name: explore-proof-strategies
description: Explore a bounded, mathematically disciplined portfolio of proof strategies and preserve any candidate proof for later rigorous verification.
disable-model-invocation: true
---

# Explore Proof Strategies

Scout broadly, test cheaply, and stop with a useful proof architecture. Preserve precision and visible obligations without performing the certification owned by `research-mathematics`. If no claim is ready, recommend `$explore-mathematical-structure` rather than manufacturing one.

## Execution role

- **Nested specialist:** work against the coordinator's exact candidate. Return a content-bound report and create no theory artifact. Resolve a supplied canonical research key or alias with read-only `lookup` before broader `search`, and use `show` only for selected cards; never run `ensure` or `apply`.
- **Standalone report-only:** answer in the conversation without filesystem changes. Existing memory, if useful, is likewise limited to read-only exact `lookup`, summary `search`, and selective `show`.
- **Standalone writable round:** only with authority to change a file-backed home theory, read and follow the writable-home coordinator path, including `ensure`, in the shared [research-memory protocol](../research-mathematics/references/research-memory.md), using its [CLI](../research-mathematics/scripts/research_memory.py).

Default to report-only without both writable authority and a home theory. Before route generation, look up known canonical keys first, then query active, open, and parked summaries only as needed; query rejected cards only for similar routes under consideration.

## 1. Frame the target

Record the literal claim, working interpretation and material alternatives, objects, quantifiers, assumptions, and user constraints on methods or budget. Use a lightweight target rather than a full assumption catalog; ask only when an ambiguity changes truth or relevant strategies.

Complete this phase when every route can be judged against the same target.

## 2. Run a cheap truth screen

Test small cases, scaling or dimensions, boundary and degenerate cases, and one plausible obstruction. Use symbolic or numerical experiments when cheaper than speculation. A decisive counterexample must satisfy every hypothesis; otherwise report only `not refuted within the stated screen`.

Complete this phase when an immediate defeat is certified or the scope of surviving checks is recorded.

## 3. Build a structural fingerprint

Identify mechanisms that could work: invariance, monotonicity, convexity, compactness, coercivity, orthogonality, duality, recursion, extremality, algebraic closure, local-to-global or spectral structure, or another target-specific feature. Name bottlenecks and tie every route to concrete structure.

Complete this phase when the portfolio can arise from the problem rather than a generic proof-style list.

## 4. Build a portfolio

Generate materially different routes. Start with the simplest native approach, then scan relevant analytic, algebraic, geometric, probabilistic, combinatorial, variational, spectral, categorical, computational, or other viewpoints. Routes differ only when their central invariant, representation, reduction, or hard lemma differs. Keep cross-field combinations only when their interface can be stated.

For each route record:

- mechanism and outline;
- assumptions and imported results;
- hardest subgoal;
- likely failure mode; and
- disposition: `advance`, `park`, or `reject`.

Reject only on a demonstrated obstruction; park shallow failures and unchecked analogies.

Start bounded and allocate by information gain. Broaden when routes are cosmetic or a feature remains unexplained; deepen a route with a concrete mechanism and identifiable crux; use parallel scouts, computation, or theorem lookup only when they can decide allocation; stop for work requiring broad literature review, a large proof DAG, exhaustive attack, assumption audit, or independent verification. Treat `quick` and `wide` as optional budget modifiers.

Complete this phase with a structurally diverse shortlist or a visibly exhausted budget and stopping reason.

## 5. Certify cross-field bridges

For every retained hybrid, state:

1. original and translated objects;
2. structure preserved, reflected, or deliberately lost;
3. target subgoal addressed;
4. theorem or mechanism transferred;
5. return map;
6. compatibility conditions and open assumptions; and
7. cheapest break-test.

Theorem names and analogies are leads until exact statements and hypotheses are checked. Complete this phase when each retained hybrid has an explicit interface.

## 6. Pressure-test and deepen

Give each serious route one adapted cheap test. Deepen the best into lemma-level architectures and identify each decisive next calculation, example, lookup, or lemma. Keep verified facts, heuristic evidence, analogies, and speculation distinct.

Complete this phase when ranking, cruxes, and next actions have mathematical reasons.

## 7. Capture any candidate proof

When an end-to-end argument appears, stop branching and record the exact theorem, complete available argument, newly introduced assumptions, imported results and checking status, fragile steps, and omitted verification phases. Label it:

`CANDIDATE FULL PROOF — NOT CERTIFIED`

Run one coherence pass for missing links and circularity, but no separate adversarial, assumption, or independent-verification campaign. In a writable round place the strongest candidate in the canonical document with its label; otherwise return it to the caller. Memory persistence never upgrades status.

## Retain only useful state

In a writable round:

- **Canonical Markdown:** exact target, selected architecture, strongest candidate proof, decisive evidence, and immediate proof obligation.
- **Research-memory cards:** reusable open obligations; parked routes with concrete revival conditions; and rejected routes with demonstrated obstructions. Each card states the bottleneck, bridge applicability, next test, reason, or revival condition needed to reuse it.
- **Workpad only:** complete brainstorming portfolio, cheap screens, candidate variants, bridge sketches, scout reports, routine probes, and superseded drafts.

Close once under the shared protocol. A nested specialist recommends destinations; only the coordinator writes them.

In a writable round, give retained canonical subjects human-semantic research
keys through the protocol's deterministic section tool, reuse those exact keys
in card links, and explicitly refresh changed items and review affected links.
Legacy opaque identifiers remain aliases rather than primary keys.

## Report

Return the target and ambiguities, truth-screen scope, structural fingerprint, portfolio, bridge certificates, ranked routes and next tests, any candidate full proof, explored scope and stopping reason, and a handoff containing the literal claim, examples, selected route, open lemma chain, imported-result status, rejected routes, and first proof obligation. For nested or writable work, include concise canonical/card recommendations.

The report stays in the conversation or coordinator response rather than a separate artifact. Complete only when the portfolio supports a reasoned shortlist, every retained bridge has an explicit interface, each leading route has a decisive next test, and every candidate proof remains visibly uncertified. Recommend `$research-mathematics` when the user wants rigorous resolution.
