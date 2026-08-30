---
name: explore-proof-strategies
description: Explore why a clear claim might be true, compare proof ideas, and identify the most promising route and its crux.
disable-model-invocation: true
---

# Explore Proof Strategies

Ask what could make the conclusion follow from the hypotheses, then develop a
few plausible answers far enough to reveal their crux. Follow the
[shared mathematical integrity](../research-mathematics/references/mathematical-integrity.md).
This skill finds a route; it does not certify a proof.

Default to chat. For authorized writable work, read the shared
[research-memory rules](../research-mathematics/references/research-memory.md).
A nested scout remains read-only and works against the supplied target version.

## 1. Fix the claim and look at revealing cases

State the exact claim and keep nearby variants separate. If the objects or
intended statement are still unsettled, recommend `$formalize-concepts` or
`$explore-mathematical-structure` before choosing a proof strategy.

Work through small, boundary, or nearly failing cases. Use them to see which
hypotheses are active, what mechanism might force the conclusion, and which
ideas already point in the wrong direction. An unsuccessful counterexample
search reports only what was searched.

## 2. Develop genuinely different mechanisms

A strategy is more than the name of a method. It should explain why this
problem has the structure the method needs. Develop a small set of routes that
differ in their governing idea: the intermediate statement they seek, the
representation they introduce, or the reduction that would make the conclusion
unavoidable.

For each serious route, describe its main mathematical move, the resulting
sequence of lemmas or reductions, the hypotheses and imported results it uses,
and the step on which it is likely to succeed or fail. Keep an alternative
because it illuminates the problem or offers a credible path around the leading
route's obstruction.

When an idea comes from another field, identify the translated objects and the
structure preserved by the translation. Explain how the desired conclusion
returns to the original setting and where the correspondence may break.

## 3. Test the mechanism and expose the crux

Give each serious route one cheap test chosen for its proposed mechanism. A
candidate invariant should survive a revealing example; a reduction should
preserve the needed hypotheses; a proposed lemma should be checked at the
boundary where it is least plausible.

When material computation could change the choice, read
[computational-checking.md](../research-mathematics/references/computational-checking.md)
and use `discover` or `falsify`. State the proposition encoded, the cases
checked, and the limit of the result.

Develop the leading routes into a lemma spine. Name the next calculation,
example, source check, estimate, construction, or lemma that would most clearly
advance or defeat each one. Stop branching once one route has a concrete crux
or the useful alternatives have been exhausted.

If an end-to-end argument appears, record the exact theorem, assumptions,
imports, fragile steps, and missing verification in the internal handoff under
`CANDIDATE FULL PROOF — NOT CERTIFIED`. Mark every part that still needs a
mathematical check, source match, adversarial challenge, or independent
verification.

## 4. Prepare the proof handoff

For each leading route, record the exact claim, guiding mechanism, lemma spine,
assumptions, imported results, tests already made, known failure points, crux,
and best next step. In reader-facing prose, name the actual missing lemma,
estimate, construction, reduction, or check. The internal proof handoff may
collect such items as conversion obligations.

## Write the result

Write a mathematical comparison. Begin with why the claim is plausible, then
explain each serious mechanism, the example or test that bears on it, and its
decisive difficulty. Rank routes only when the comparison becomes clearer.

For writable work, keep the selected route, its motivation, the important
evidence, and the next proof task in canonical Markdown. Memory may retain
reusable parked or rejected ideas; its bookkeeping stays internal.

Finish when the reader understands why the leading routes might work, where
each could fail, and which exact mathematical step should come next.
