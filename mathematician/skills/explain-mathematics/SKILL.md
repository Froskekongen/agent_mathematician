---
name: explain-mathematics
description: Explain a mathematical theory, theorem, or proof to a mathematically mature nonspecialist. Use when teaching or unpacking prerequisites, notation, intuition, proof structure, examples, nonexamples, and connections across fields without assuming expertise in every mathematical specialty.
disable-model-invocation: true
---

# Explain Mathematics

Treat mathematical expertise as jagged: strength in one field supplies general maturity, not automatic fluency in adjacent specialties. Preserve the exact mathematics while building a bridge from the reader's known concepts to the new theory.

Read the shared [rigor standards](../research-mathematics/references/rigor-standards.md) before acting.

## Use canonical mathematics by default

Build an ordinary explanation from the self-contained canonical document,
without consulting or creating research memory. When the user
explicitly asks about research history, rejected routes, or how the theory was
developed, the existing companion databases may be queried read-only under the
[research-memory protocol](../research-mathematics/references/research-memory.md).
Label noncanonical material as research history, and never initialize or write
a companion from this skill.

## 1. Set the audience contract

Default to a professional mathematician who understands proofs, abstraction, and standard undergraduate foundations but is new to the focal specialty. Infer likely background from the request and state the inference. Ask for calibration only when the choice would materially change the exposition.

Partition prerequisites into:

- **assumed**: used without local development;
- **bridged here**: introduced before use;
- **optional**: useful for deeper study but unnecessary for the main line.

Complete this phase with an explicit audience statement and prerequisite budget.

## 2. Build a prerequisite graph

List the field-specific definitions, conventions, standard constructions, and imported theorems. Order them by dependency. Introduce every bridged prerequisite before the first use and give a compact notation and type legend.

For each imported idea, provide:

- its purpose in this theory;
- the exact definition or theorem statement;
- the minimal familiar analogue;
- the point where the analogy stops being valid.

Complete this phase when the main theorem can be parsed without an undeclared specialist dependency.

## 3. Give orientation before abstraction

Explain:

1. the problem or obstruction that motivates the theory;
2. the structure the theory introduces;
3. the mechanism that resolves the obstruction;
4. an informal version of the main result;
5. the exact theorem with all qualifiers.

Keep intuition and proof visibly distinct. Tie every abstraction to a mathematical job.

## 4. Construct an example ladder

Use the shortest ladder that exposes the full mechanism, normally:

1. a sanity or trivial case when it clarifies conventions;
2. the smallest nontrivial example;
3. a parameterized example that makes the mechanism visible;
4. a representative example exercising the full theorem;
5. a boundary case, near-miss, or counterexample after dropping one hypothesis;
6. a richer or pathological example when it reveals a genuine limitation.

Change one main complexity dimension per rung. For every rung, include:

- explicit objects and calculations;
- the assumptions it satisfies;
- the new feature introduced;
- the exact lesson;
- the link back to the formal definition or theorem;
- what the example does not establish.

Place easily confused examples or solution strategies side by side and ask what structural feature changes. Include at least one nonexample.

Complete this phase when a reader can see the mechanism appear, operate, and fail at a boundary.

## 5. Explain the proof in layers

Present three layers:

1. **Proof map**: the dependency graph and the role of each lemma.
2. **Mechanism-bearing steps**: the key derivations with assumptions annotated.
3. **Technical closure**: all remaining nontrivial details at the chosen audience level.

For each lemma, explain why it is introduced, what prerequisite it uses, and how its conclusion advances the proof. Expand transitions between fields, changes of topology, and limiting arguments even when they are standard within the specialty.

Allocate detail by proof risk rather than by line count: expand the crux, fragile reductions, cross-field transfers, and uses of imported theorems; compress genuinely routine closure. Do not let a long calculation hide the only unsupported step.

For an AI-assisted or formally verified result, reconstruct the mathematical mechanism from the proof artifact rather than paraphrasing syntax. Map the intended informal theorem to the exact encoded statement, the key formal lemmas, imported library results or axioms, and the human argument they implement. State what the checker established and which semantic, novelty, or attribution questions still require expert judgment.

Use progressive hints or subgoals before a full solution when the user wants tutoring. For a reference exposition, provide the full proof while retaining checkpoints that make it easy to verify.

## 6. Verify the teaching artifact

- Check every example symbolically, computationally, or directly.
- Confirm that simplified cases retain the stated assumptions.
- Check that every specialist term appears after its prerequisite.
- State common confusions and distinguish nearby concepts.
- Mark analogy boundaries and separate motivation from logical justification.
- Ensure the simplified explanation has not strengthened or changed the theorem.
- Verify citations and attribution for load-bearing claims.
- Compare the exposition against the checked proof after substantial rewriting; readability edits can change mathematics.
- Ask whether a mathematically mature reader outside the specialty can locate and verify the crux rather than merely follow notation.

Complete the run only when the reader can identify the hypotheses, conclusion, mechanism, proof dependencies, and limitations, and when the ladder contains both a nontrivial mechanism-bearing example and a checked boundary or nonexample.

## Report

Use this order when the theory warrants it:

1. **Audience and prerequisite contract**
2. **Orientation**
3. **Definitions, notation, and cross-field bridges**
4. **Exact theorem**
5. **Mechanism**
6. **Example ladder**
7. **Proof map and proof**
8. **Verification and provenance map**, when AI or formal tools materially contributed
9. **Boundary cases and common confusions**
10. **Optional transfer exercises or next prerequisites**
