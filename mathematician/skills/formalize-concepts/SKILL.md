---
name: formalize-concepts
description: Turn an informal idea into faithful mathematics by comparing concrete consequences and resolving the choices that matter.
disable-model-invocation: true
---

# Formalize Concepts

Find the simplest mathematics that captures the intended behavior. Work in a
`show, then ask` rhythm: propose something concrete, show what it means in an
example, then ask one question whose answer would change the formalism.

Follow the
[shared mathematical integrity](../research-mathematics/references/mathematical-integrity.md).

## Adapt to the mathematics the user knows

Infer relevant expertise from the user's notation, examples, constraints, and
corrections. Work directly with a structure they use precisely; when they
reason informally, express the mathematical choices through examples and
consequences. Clarify a local ambiguity without lowering the level of the whole
discussion. Informal writing is not evidence of mathematical inexperience.

When useful, invite the user to steer either the mathematics or its intended
behavior:

> Give any structures, constraints, or results you want built in. Otherwise,
> describe how the concept should behave and I will propose the mathematics.

## 1. Begin with the intended distinction

Restate what the concept is meant to describe or distinguish, and what later
work—explanation, prediction, classification, optimization, control, or a
theorem—should depend on it. Find one concrete instance it should capture and,
when possible, a nearby instance it should treat differently. Separate
descriptive, causal, and normative readings when they lead to different
mathematical objects.

If the user has already supplied a suitable structure, develop it. Otherwise,
show the first candidate once the intended job and one revealing example are
clear.

## 2. Put candidate mathematics on the table

Begin with the simplest plausible formalism. Add one genuinely different
alternative when the examples admit two interpretations; add a third only for
an independent conceptual fork.

For each candidate, identify the objects and admissible transformations, the
relation, map, dynamics, constraint, or objective that carries the idea, and
the user's intended terms in that language. Then derive one consequence on the
anchor example and one limitation or boundary. Alternatives earn their place
by changing the mathematics, not by renaming it.

Use concise definitions with an expert. Introduce notation through the object
it denotes when the user is working more conceptually.

## 3. Ask the consequential question

Expose the live fork and ask one question per round, or two only when they
cannot be separated. State what each answer changes. For example, whether two
systems with the same present state but different histories are identical
decides whether the state can be Markovian or must retain path information.

Pause after the candidates when the answer would change the meaning, admissible
examples, or model class. Continue when the user has already answered,
delegates the choice, or asks for a one-shot proposal. Make reversible
technical choices by the simplest standard convention; mark a delegated
conceptual choice as provisional.

## 4. Refine through consequences

Update the leading candidate and work through the anchor example. Check a
boundary case or nonexample on which the alternatives differ, verify that the
objects and operations are well-typed, and derive a simple consequence when it
helps reveal the meaning of the definition.

Let these examples carry the conversation. Repeat `show, then ask` only while
a genuine conceptual fork remains. The formalism is ready when it handles the
anchor and its important boundary is understood.

## 5. Select and explain

Clear endorsement, an incorporated correction with no remaining objection, or
explicit delegation is enough to select a formalism. If a real fork survives,
keep a leading `PROVISIONAL` candidate and state the choice that remains.
Otherwise use `SELECTED` only when the label helps.

Write a short mathematical account: what is being modeled, why this formalism
fits, its objects and relations, the anchor example, and a useful boundary.
Mention a rejected alternative only when the comparison improves
understanding. Selection says that the formalism captures the intended
meaning; it does not prove uniqueness, novelty, causal validity, or empirical
correctness.

## Internal handoff

If the result will support later file-backed work, read the shared
[research-memory rules](../research-mathematics/references/research-memory.md).
Hand off a plain description of the mathematical subject and a suggested
research key. The next writable skill decides whether to reuse that key or
make a new one. This skill does not create companions, manage database state,
or add canonical-section markers.
