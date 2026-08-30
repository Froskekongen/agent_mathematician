# Shared Mathematical Integrity

Use this reference in every mathematical skill. It keeps intuitive work honest
without imposing a proof cadence on every task. It is not a proof protocol;
each skill supplies the rigor appropriate to its purpose.

Use these rules behind the scenes whenever a choice could alter the mathematics
or the reader's understanding of it. Let the main document follow the ideas,
examples, and arguments. Keep workflow labels, digests, search logs, and
database details in a technical note unless they help explain the mathematics.

## Keep the object and claim fixed

State the objects, maps, domains, quantifiers, assumptions, and conventions with
the precision the task requires. Distinguish the literal claim from its intended
meaning and from any repaired or restricted version. If a definition,
assumption, or conclusion changes, treat the result as a new claim rather than
silently carrying earlier evidence across.

Prose, formulas, diagrams, sources, programs, and formal encodings may represent
the same mathematics in different ways. When moving between them, explain how
the relevant objects and relations correspond and what the translation may
lose.

## Say what the evidence establishes

Make the role of an argument clear whenever it could be mistaken for something
stronger. Examples are local: a good one may reveal the mechanism, but it does
not prove a general claim. A counterexample is decisive only after checking
that it satisfies the hypotheses and violates the conclusion. A computation
reaches no further than the statement encoded and the cases examined. Analogies and
heuristics may organize the mathematics or suggest what should be true; an
unresolved claim still needs an argument. An unsuccessful search reports its
scope, not the absence of a defect.

Check calculations, examples, translations, and source uses that carry a
conclusion. Apply an imported theorem only after matching its statement,
assumptions, and conventions to the present case.

## Make intuition recoverable

Use mental models, examples, diagrams, and metaphors to make the mechanism
visible. Identify the exact objects, relations, or operations they describe.
For an analogy, say which relations survive the comparison and where it fails.
A simple example and a boundary case are often enough to expose a misleading
model.

If a heuristic carries an unresolved claim, state what would turn it into an
argument. Name the missing mathematics directly in reader-facing prose. An
internal proof handoff may record the same item as a **conversion obligation**;
naming it does not discharge it.

## State the mathematical status plainly

Use the status justified by the evidence and the active skill's completion
rule. Keep truth separate from plausibility, confidence, usefulness,
explanatory value, provenance, and workflow choice. Explaining, translating, or
consolidating a result does not change whether it is proved, refuted,
conjectural, incomplete, or unresolved.

Check each claim in proportion to the role it plays. Routine local claims may
need only a local check. When the evidence falls short, give the strongest
supported conclusion and state the mathematical step that remains open.
