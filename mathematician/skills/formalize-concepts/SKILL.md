---
name: formalize-concepts
description: Turn an informal idea into a selected mathematical formalism through lightweight collaboration that adapts to the user's relevant expertise.
disable-model-invocation: true
---

# Formalize Concepts

Turn intended meaning into the simplest faithful mathematics through a `show, then ask` loop. Let the user guide the concept at their useful level while keeping the discussion easy to revise.

Follow the
[shared mathematical integrity](../research-mathematics/references/mathematical-integrity.md).

## Adapt to local expertise

Infer relevant expertise from the user's definitions, notation, examples, constraints, and corrections rather than requesting a mathematical biography. Expertise may vary by topic.

- Work directly with supplied mathematical structures and results when the user uses them precisely.
- Express choices through examples and consequences when the user reasons conceptually.
- Clarify an ambiguous specialist term locally rather than lowering the whole discussion.
- Do not infer lack of expertise from informal writing.

Offer this invitation near the start when it would help:

> If you want to steer the mathematical machinery directly, give any structures, constraints, or results you want considered. Otherwise, guide the intended behavior and I will propose the mathematics.

## 1. Identify the mathematical job

Restate the idea compactly and determine what the formalism should do: describe, distinguish, explain, predict, classify, optimize, control, or support a theorem.

Separate descriptive, causal, and normative claims when they would lead to different mathematics. Ask for a concrete anchor only when the request lacks one.

Show the first proposal once the intended job and one meaningful example are
clear.

## 2. Show a small candidate set

Present the simplest plausible formalism and normally one materially different alternative. Add a third only when it exposes an independent interpretation. When the user has already fixed a suitable structure and no material ambiguity remains, develop that single candidate.

For each candidate, state briefly:

- main objects;
- central relation, map, dynamics, constraint, or objective;
- interpretation of the user's terms;
- conceptual feature it captures;
- one important consequence or limitation.

Use concise formal definitions for an expert. Explain what notation represents before using it with a nonspecialist.

Keep alternatives only when their differences are meaningful to the user, not
merely changes of mathematical vocabulary.

## 3. Ask a wedge question

Ask one high-leverage question per round, or two only when they are inseparable. Make the consequence of each answer visible.

Match the user's demonstrated level. For example, ask either:

- “Should two systems with the same present state but different histories count as the same?”; or
- “Should the state be Markovian, or should it live on path space?”

Ask only when the answer changes meaning, admissible examples, causal or normative content, or the model class. Make reversible technical choices using the simplest standard option. When the user delegates a material choice, select the simplest faithful candidate and mark it provisional in one sentence.

After showing candidates, normally pause for the user's answer when a live material fork remains. Do not merely bury the choice in a list of open questions. Continue without pausing only when the user has already resolved the fork, explicitly delegates it, or asks for a one-shot proposal.

Move on once one important ambiguity has been resolved or stated clearly.

## 4. Refine through examples

Update the leading candidate, then test it visibly with:

- one example it should capture;
- one boundary case, nonexample, or comparison where alternatives differ;
- a basic type or well-posedness check;
- a cheap derived consequence when it helps the user judge whether the
  formalism captures the intended meaning.

Invite correction through the examples. Repeat the `show, then ask` loop only while a live conceptual fork remains.

Refine until the candidate handles the anchor and its main limitation or
disputed boundary is understood.

## 5. Select without ceremony

Treat clear endorsement, an incorporated correction without further objection, or explicit delegation as enough to select a formalism. Preserve:

- the selected formalism;
- a few serious alternatives and one decisive reason each was set aside;
- unresolved choices that could materially change later mathematics.

Discard cosmetic variants and transient brainstorms. If a genuine fork remains, keep a leading provisional candidate and state the fork rather than forcing closure.

Finish selection with either a chosen formalism or one sharply stated remaining
choice.

If the result will be saved for later work, read the shared
[research-memory rules](../research-mathematics/references/research-memory.md).
Hand off a plain description of the mathematical subject and a suggested
research key. The next writable skill decides whether to reuse that key or make
a new one. This skill does not create companions, manage database state, or add
canonical-section markers. Keep these storage details out of the mathematical
account.

## 6. Stop at the right boundary

Hand off when the next work is a substantial proof, systematic assumption test, consistency campaign, empirical validation, causal identification, or novelty investigation. Retrieve literature only when the user asks about existing formalisms, attribution, or novelty.

Recommend `$explore-mathematical-structure` when the selected formalism needs an iterative test bed for intuition before the user chooses what to investigate. Recommend `$explore-proof-strategies` when a precise claim now needs proof routes, or `$research-mathematics` when the user wants rigorous mathematical resolution.

## Report

Write the result as a short mathematical account rather than a process log.
Lead with what is being modeled and why the chosen formalism fits. Then give its
objects, relationships, assumptions, and equations or definitions. Work through
an anchor example and a useful boundary case. Mention rejected alternatives
only when the comparison improves understanding, and end with any genuine open
choice or next mathematical question.

Use `PROVISIONAL` and `SELECTED` only when the distinction helps the reader.
Selection means that the formalism captures the intended meaning; it does not
by itself prove uniqueness, novelty, causal validity, or empirical correctness.
