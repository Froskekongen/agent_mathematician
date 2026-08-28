---
name: formalize-concepts
description: Turn an informal idea into a selected mathematical formalism through lightweight collaboration that adapts to the user's relevant expertise.
disable-model-invocation: true
---

# Formalize Concepts

Turn intended meaning into the simplest faithful mathematics through a `show, then ask` loop. Let the user guide the concept at their useful level while keeping the discussion easy to revise.

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

Complete this phase when the intended job and at least one meaningful example are clear enough to make a first proposal.

## 2. Show a small candidate set

Present the simplest plausible formalism and normally one materially different alternative. Add a third only when it exposes an independent interpretation. When the user has already fixed a suitable structure and no material ambiguity remains, develop that single candidate.

For each candidate, state briefly:

- main objects;
- central relation, map, dynamics, constraint, or objective;
- interpretation of the user's terms;
- conceptual feature it captures;
- one important consequence or limitation.

Use concise formal definitions for an expert. Explain what notation represents before using it with a nonspecialist.

Complete this phase when the candidates differ in a way the user can evaluate rather than merely by mathematical vocabulary.

## 3. Ask a wedge question

Ask one high-leverage question per round, or two only when they are inseparable. Make the consequence of each answer visible.

Match the user's demonstrated level. For example, ask either:

- “Should two systems with the same present state but different histories count as the same?”; or
- “Should the state be Markovian, or should it live on path space?”

Ask only when the answer changes meaning, admissible examples, causal or normative content, or the model class. Make reversible technical choices using the simplest standard option. When the user delegates a material choice, select the simplest faithful candidate and mark it provisional in one sentence.

After showing candidates, normally pause for the user's answer when a live material fork remains. Do not merely bury the choice in a list of open questions. Continue without pausing only when the user has already resolved the fork, explicitly delegates it, or asks for a one-shot proposal.

Complete this phase when one material ambiguity is resolved or retained explicitly.

## 4. Refine through semantic tests

Update the leading candidate, then test it visibly with:

- one example it should capture;
- one boundary case, nonexample, or comparison where alternatives differ;
- a basic type or well-posedness check;
- a cheap derived consequence when it helps the user judge semantic fit.

Invite correction through the examples. Repeat the `show, then ask` loop only while a live conceptual fork remains.

Complete this phase when the candidate handles the anchor and its main limitation or disputed boundary is understood.

## 5. Select without ceremony

Treat clear endorsement, an incorporated correction without further objection, or explicit delegation as enough to select a formalism. Preserve:

- the selected formalism;
- a few serious alternatives and one decisive reason each was set aside;
- unresolved choices that could materially change later mathematics.

Discard cosmetic variants and transient brainstorms. If a genuine fork remains, keep a leading provisional candidate and state the fork rather than forcing closure.

Complete this phase when there is a selected candidate or one sharply stated unresolved fork.

When a downstream file-backed research round will retain a definition,
mechanism, conjecture, obstruction, or open question, give that durable handoff
unit a human-semantic lowercase-kebab research key. Sequence labels such as
`A1` remain transient local notation. This skill does not create companions,
manage database state, or insert generated canonical-section markers; the
receiving writable coordinator owns that lifecycle.

## 6. Stop at the right boundary

Hand off when the next work is a substantial proof, systematic assumption test, consistency campaign, empirical validation, causal identification, or novelty investigation. Retrieve literature only when the user asks about existing formalisms, attribution, or novelty.

Recommend `$explore-mathematical-structure` when the selected formalism needs an iterative test bed for intuition before the user chooses what to investigate. Recommend `$explore-proof-strategies` when a precise claim now needs proof routes, or `$research-mathematics` when the user wants rigorous mathematical resolution.

## Report

After the dialogue converges, or when the user explicitly requests a one-shot artifact, return only:

1. **Mathematical reading** — what is modeled and what the formalism should do.
2. **Selected formalism** — objects, relationships or rules, essential assumptions, equations or definitions, and interpretation.
3. **Sanity checks** — one anchor example and one boundary case or nonexample.
4. **Alternatives set aside** — one line per serious alternative explaining what it captured and why it was not selected.
5. **Open questions and handoff** — material unresolved choices and the resulting definitions, conjectures, or research questions.

Use `PROVISIONAL` and `SELECTED` only when a status helps. Selection establishes semantic fit, not proof, uniqueness, novelty, causal validity, or empirical confirmation.
