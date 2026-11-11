---
name: explore-mathematical-structure
description: Explore different ways of understanding a mathematical phenomenon, test them on revealing examples, and identify the structure worth developing.
disable-model-invocation: true
---

# Explore Mathematical Structure

Explore genuinely different ways of understanding a mathematical object,
problem, or phenomenon before committing to one formulation or proof route.
Follow the [shared mathematical integrity](../mathematical-integrity/SKILL.md).
This skill uncovers structure, invariants, obstructions, and sharp questions;
it does not certify a theorem.

## 1. Ground the phenomenon and develop distinct viewpoints

Start in the problem's native setting and work through a concrete case until
the feature needing explanation is clear. If the problem itself is ambiguous,
clarify what matters before branching.

Develop genuinely distinct mathematical viewpoints—such as algebraic,
geometric, analytic, combinatorial, spectral, variational, or probabilistic
lenses—keeping only those that change what becomes visible or tractable. For
each viewpoint, connect the intuitive picture to its exact mathematical
realization (the definitions, invariants, maps, estimates, or constructions
that carry it) and note where that picture breaks down or loses information.

## 2. Probe with revealing examples

Test the viewpoints on small, boundary, degenerate, or deformed cases:

- When viewpoints suggest different behavior, find a minimal case where they
  part ways and trace why.
- When viewpoints are mathematically equivalent, compare what each makes
  transparent, routine, or opaque—and look for whether the translation between
  them is itself the key insight.

Keep hand-checkable calculations inline. When material computation, solver
search, or executable checking can clarify the structure, use
[computational-checking.md](../research-mathematics/references/computational-checking.md).

## 3. Synthesize and point forward

Write the exploration as natural mathematics rather than a search log, letting
the ideas and examples determine the organization. Explain what the examples
reveal—such as a governing invariant, hidden symmetry, obstruction, or
candidate claim—and identify the viewpoint (or bridge between viewpoints) most
worth developing next, along with the main open mathematical step.

If a precise conjecture or claim emerges, include a compact **proof handoff**
stating the exact claim and assumptions, the guiding mechanism, the cases
checked, and the likely crux. Treat any end-to-end argument that appears during
exploration as an unverified candidate and name what still needs rigorous
checking.

## Internal protocol (file-backed work and sources)

Default to chat (creating no files). For authorized file-backed writable work
or history retrieval, follow
[research-memory.md](../research-mathematics/references/research-memory.md) as
sole writer, keeping memory mechanics out of the mathematical prose. When prior
art, attribution, or unpublished material affects the direction, follow
[literature-and-privacy.md](references/literature-and-privacy.md).
