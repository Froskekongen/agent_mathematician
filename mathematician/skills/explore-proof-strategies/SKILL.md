---
name: explore-proof-strategies
description: Explore different proof ideas, explaining what makes each promising, where its main difficulty lies, and what to try next.
disable-model-invocation: true
---

# Explore Proof Strategies

*Primary goal:* Explore several *different* routes towards a proof for a claim.
Follow the
[shared mathematical integrity](../mathematical-integrity/SKILL.md).
The intention is not to certify a proof, but find several plausible directions
and mechanisms that may lead to a full proof.

Default to chat. For authorized writable work, read the shared
[research-memory rules](../research-mathematics/references/research-memory.md).
A nested scout remains read-only and works against the supplied target version.

## 1. Fix the claim and look at revealing cases

State the exact claim and keep nearby variants separate. If the objects or
intended statement are still unsettled, recommend `$formalize-concepts` or
`$explore-mathematical-structure` before choosing a proof strategy.

Work through small, boundary, or nearly failing cases. Use them to see which
hypotheses are active, what mechanism might force a conclusion, and which
ideas already point in the wrong direction. An unsuccessful counterexample
search reports only what was searched.

## 2. Develop genuinely different mechanisms

Explain why each approach fits the mathematical structure of the problem.
Develop routes with different central ideas, such as an intermediate
statement to establish, a useful representation, or a reduction that makes
the conclusion accessible.

When an idea comes from another field, identify the translated objects and the
structure preserved by the translation. Explain how the desired conclusion
returns to the original setting and where the correspondence may break.

## 3. Test the mechanism and expose the crux

Give each serious route one cheap test chosen for its proposed mechanism. A
candidate invariant should survive a revealing example; a reduction should
preserve the needed hypotheses; a proposed lemma should be checked at the
boundary where it is least plausible.

When computational experiments could change the choice, read
[computational-checking.md](../research-mathematics/references/computational-checking.md)
and use `discover` or `falsify`. State the proposition encoded, the cases
checked, and the limit of the result.

Develop the leading routes into a lemma spine. Suggest a next step that could
advance that route toward a proof. Explore the alternatives far
enough to show how their main ideas and central difficulties differ.

If an end-to-end argument appears, record the exact theorem, assumptions,
imports, fragile steps, and missing verification in the internal handoff under
`CANDIDATE FULL PROOF — NOT CERTIFIED`. Mark every part that still needs a
mathematical check, source match, adversarial challenge, or independent
verification.

## 4. Prepare the proof handoff

For each leading route, record the exact claim, guiding mechanism, lemma spine,
assumptions, imported results, tests already made, known failure points, crux,
and best next step. In reader-facing prose, name the missing lemma, estimate,
construction, reduction, or check.

## Write the result

Write a mathematical comparison of the routes. Explain what makes each route
promising, illustrate its central idea, and describe its main difficulty.
Where one route seems more promising, explain why; otherwise make the tradeoffs clear.

For writable work keep bookkeeping internal.
