---
name: explore-mathematical-structure
description: Compare mathematical viewpoints with small revealing examples and identify the most useful direction.
disable-model-invocation: true
---

# Explore Mathematical Structure

Explore several ways to see the same mathematics and learn which viewpoint is
most useful. Follow the
[shared mathematical integrity](../research-mathematics/references/mathematical-integrity.md).
Aim for insight, revealing examples, and promising questions. This skill does
not try to certify a theorem.

Chat-only work creates no files. For an authorized file-backed round, read the
shared [research-memory rules](../research-mathematics/references/research-memory.md)
and act as sole writer. Unless the user asks for a one-shot survey or a larger
search, run one focused round of exploration.

## 1. Start from the phenomenon

Describe the problem in its original setting before introducing abstraction.
Identify what needs explaining, the main constraints, and one concrete example.
Then develop two to four genuinely different viewpoints whose predictions can
be compared.

For each viewpoint, give:

- an intuitive picture or mechanism;
- the exact objects and relations behind that picture;
- what the picture captures and where it breaks; and
- one prediction that distinguishes it from the alternatives.

If the intended meaning is still too unclear for comparison, ask one focused
question. If the answer is still missing, recommend `$formalize-concepts`.

## 2. Test the viewpoints

Before looking at a decisive example, say what each viewpoint predicts. Choose
the smallest useful example, deformation, boundary case, counterexample, or
finite family that could separate them. Work it through far enough to show the
mechanism, not merely the answer.

Keep hand-checkable tests local. For material computation, solver work,
executable checking, or a witness that will carry a later claim, read
[computational-checking.md](../research-mathematics/references/computational-checking.md)
and use its `discover`, `falsify`, or `certify` role as appropriate. Say what the
computation actually checked and where its conclusion stops.

## 3. Explain what was learned

Keep the original prediction beside any revised version. Distinguish “false”
from “not useful for this direction”: only a checked contradiction or
counterexample settles the first. Recommend the most promising viewpoint and
explain why. Keep at most two alternatives when they still illuminate the
problem, and give the next small test that would change the choice.

If the recommendation relies on an analogy, experiment, or heuristic, state
the conversion obligation needed before it can support a stronger claim.

## 4. Prepare for proof only when useful

If a precise claim emerges, add a compact note for later proof work containing:

- the exact claim and assumptions;
- the guiding picture and proposed mechanism;
- the examples or checks already tried, and what they show;
- any heuristic or imported idea still needing justification; and
- the likely crux or best next step.

This note is the proof handoff. It is a starting point, not a proof or
an upgrade in mathematical status.

## Literature and privacy

Before major investment in an apparently new direction, or whenever prior art,
attribution, or sensitive unpublished material affects the decision, read and
follow [literature-and-privacy.md](references/literature-and-privacy.md).

## Write the result

Write the exploration as mathematics, not as a laboratory log. Lead with the
question, the competing pictures, the example that distinguishes them, what it
teaches, and the most promising next direction. Use a table only when it makes
the comparison easier to see. Add the proof-preparation note only when a precise
claim is ready for later resolution.

For writable work, keep the readable exploration, selected definitions,
important boundaries, and next mathematical question in canonical Markdown.
Memory may retain reusable abandoned directions, obstructions, expensive
tests, and source findings. Do not copy memory mechanics into the document.

Complete when the reader can explain the competing viewpoints, the mathematical
test between them, the limits of that test, and why the recommended direction is
promising. Recommend `$explore-proof-strategies` when a precise claim needs a
proof route. Label an incidental end-to-end argument
`CANDIDATE FULL PROOF — NOT CERTIFIED`, and recommend `$research-mathematics`
for rigorous resolution.
