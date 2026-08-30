---
name: explore-mathematical-structure
description: Explore different ways of understanding a mathematical phenomenon, test them on revealing examples, and identify the viewpoint worth developing.
disable-model-invocation: true
---

# Explore Mathematical Structure

Explore different ways of understanding the same mathematics before deciding
which one to develop. Follow the
[shared mathematical integrity](../research-mathematics/references/mathematical-integrity.md).
Aim for a useful mental model, an exact realization, and a revealing example.
This skill clarifies structure; it does not certify a theorem.

Chat-only work creates no files. For an authorized file-backed round, read the
shared [research-memory rules](../research-mathematics/references/research-memory.md)
and act as sole writer. Unless the user asks for a one-shot survey or a larger
search, run one focused round of exploration.

## 1. Start from the phenomenon

Begin with the problem in its original setting. Work through one concrete case
until the feature needing explanation is visible, then develop two to four
genuinely different ways of seeing it.

For each viewpoint, explain the mental model, identify the objects, maps, and
relations that realize it, and draw one consequence that can be compared with
the alternatives. State its limits. Keep only viewpoints that change what the
mathematics makes easy to see or do.

If the intended meaning is still too unclear for comparison, ask one focused
question.

## 2. Separate the viewpoints with an example

Before choosing, say what each viewpoint leads one to expect. Find the smallest
example on which those expectations diverge or one viewpoint gives a clearly
better analysis. A boundary case or simple deformation may be more revealing
than another typical example. Work it far enough to expose the reason for the
difference. If two viewpoints are equivalent, compare what each makes
transparent rather than forcing an opposition.

Keep hand-checkable tests local. For material computation, solver work,
executable checking, or a witness that will carry a later claim, read
[computational-checking.md](../research-mathematics/references/computational-checking.md)
and use its `discover`, `falsify`, or `certify` role as appropriate. Say what the
computation actually checked and where its conclusion stops.

## 3. Explain what was learned

Compare those expectations with the worked example. Recommend the viewpoint 
that best explains the phenomenon or opens the most promising mathematics.

If the recommendation rests on a heuristic, name the missing mathematical step
in the explanation.

## 4. Prepare for proof only when useful

If a precise claim emerges, prepare a compact proof handoff. State the claim and
assumptions, the proposed mechanism and the mental model behind it, the examples
already checked, the missing mathematics, and the likely crux. This handoff is
a starting point, not a proof or an upgrade in mathematical status.

## Literature and privacy

Before major investment in an apparently new direction, or whenever prior art,
attribution, or sensitive unpublished material affects the decision, read and
follow [literature-and-privacy.md](references/literature-and-privacy.md).

## Write the result

Write the exploration as mathematics, not as a search record. Use a
collaborative voice in chat and polished, yet intuitivie,  exposition in a 
canonical document. Lead with the phenomenon, then the mental models and 
their realizations, the example that tests them, and the direction it 
suggests. Add the proof handoff only when a precise claim is ready for later work.

For writable work, keep the readable exploration, selected definitions,
important boundaries, and next mathematical question in canonical Markdown.
Memory may retain reusable abandoned directions, obstructions, expensive
tests, and source findings. Do not copy memory mechanics into the document.

Finish when the reader can explain each serious mental model, its mathematical
realization, the example that distinguishes or limits it, and why the chosen
direction is worth developing. If an end-to-end argument appears, mark it
in the internal handoff as `CANDIDATE FULL PROOF — NOT CERTIFIED`.
