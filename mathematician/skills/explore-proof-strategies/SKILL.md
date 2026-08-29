---
name: explore-proof-strategies
description: Compare possible proof ideas for a clear claim and identify the most promising route and its central difficulty.
disable-model-invocation: true
---

# Explore Proof Strategies

Find several plausible ways to prove a claim and understand what makes each one
work. Follow the
[shared mathematical integrity](../research-mathematics/references/mathematical-integrity.md).
The goal is a clear route and a visible crux, not a certified proof.

Default to a conversation-only result. For authorized writable work, first read
the shared [research-memory rules](../research-mathematics/references/research-memory.md).
A nested scout remains read-only and reports against the supplied target
version.

## 1. Understand the claim

State the exact claim. If nearby versions with different assumptions or
conclusions are worth comparing, name them and say which version each strategy
addresses. If the meaning or underlying structure is unsettled, recommend
`$formalize-concepts` or `$explore-mathematical-structure` first.

Test a few small, boundary, degenerate, or scaling cases. Use them to understand
why the claim might be true and to rule out routes that already conflict with
the examples. A failed search for a counterexample is only evidence from that
search; it is not a proof.

## 2. Develop genuinely different ideas

Identify the structures already present in the problem. Develop a small set of
strategies that differ in their main idea—for example, their invariant,
representation, reduction, or central lemma.

For each strategy explain:

- the main idea and why it fits this problem;
- the likely sequence of intermediate results;
- the hardest step;
- assumptions or imported theorems it needs; and
- how or where it is most likely to fail.

For an idea imported from another field, say how the objects translate, what
structure survives the translation, how the conclusion returns to the original
problem, and where the analogy may break.

Keep a route because of mathematical promise, not merely because it is
different. Stop when the leading route has a concrete crux or when the useful
alternatives have been exhausted.

## 3. Test and deepen the leading ideas

Give every serious strategy one cheap test tailored to its proposed mechanism.
When a material computation would change the choice, read
[computational-checking.md](../research-mathematics/references/computational-checking.md)
and use `discover` or `falsify`. State only what the computation actually
checked.

Turn the leading strategies into a sequence of lemmas or reductions. For each
one, identify the next calculation, example, source check, or lemma that would
most clearly advance or defeat it.

If an end-to-end argument appears, stop branching and record the exact theorem,
argument, new assumptions, imported results, fragile steps, and unperformed
verification under:

`CANDIDATE FULL PROOF — NOT CERTIFIED`

## 4. Prepare for rigorous proof

For each leading strategy, make a compact proof handoff with the exact
claim, guiding idea, lemma sequence, assumptions, imported results, tests
already tried, known failure points, conversion obligations, central crux, and
best next step. If a candidate full proof exists, mark every part that still
needs checking, source matching, challenge, or independent verification.

`research-mathematics` will state the target afresh and decide whether the proof
is complete. This handoff does not change the claim's status.

## Write the result

Write a mathematical comparison, not a search log. Lead with why the claim is
plausible, then explain the main idea of each serious strategy, the example or
test that informs it, and the decisive difficulty. Rank the strategies in prose
or a small table only when the comparison becomes clearer.

For writable work, keep the selected route, its mathematical motivation, the
important evidence, and the next proof task in canonical Markdown. Memory may
retain reusable parked or rejected ideas, but its bookkeeping does not belong
in the document.

Complete when the reader understands why the leading strategies might work,
where each could fail, and what exact step should come next. Any heuristic that
supports a stronger claim has a conversion obligation, and every candidate
proof remains visibly uncertified. Recommend `$research-mathematics` for
rigorous resolution.
