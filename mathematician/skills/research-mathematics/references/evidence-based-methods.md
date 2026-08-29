# Maintainer Evidence Rationale

Audited on **2026-08-30**. Claims about current capability below use work first public in 2026; older work appears only as methodological foundations.

This file preserves the literature behind the suite's design and evaluation.
It is maintainer rationale, not a runtime reference routed from public skills.
Runtime decisions belong in `mathematical-integrity.md`,
`claim-resolution.md`, and `computational-checking.md`. Rare successes,
benchmark scores, kernel acceptance, and institutional novelty claims do not
establish general reliability.

## Operational conclusions

1. **Separate five evidence axes:** logical validity, statement fidelity, novelty or significance, provenance or autonomy, and readable reconstruction.
2. **Freeze and test the target:** record literal source, intended meaning, definitions, fixed and evolvable variables, permitted assumptions or axioms, and representative positive, negative, and non-vacuous examples. Diff and re-audit every change; test formal definitions with sanity lemmas.
3. **Refute cheaply before proving expensively:** try substitutions, small models, hypothesis deletion, exact computation, and construction families. Certify the instantiated negation when practical. A failed bounded search means only `not falsified within scope`.
4. **Start with a minimal generator--verifier--reviser loop:** escalate to parallel, population, or evolutionary search only after a recorded bottleneck. Track the proof DAG, assumptions, sources, failures, checker errors, denominator, selection rule, budget, and stopping condition.
5. **Verify distinct obligations:** the informal claim matches the intended question; the formal specification matches that claim; the proof establishes that specification; and the full dependency closure contains no placeholder, unsafe axiom, hidden premise, or renamed central obligation.
6. **Use fresh verification:** withhold the proposer's narrative when possible. A same-model critic filters errors but is correlated evidence; high-stakes work needs a second derivation, trusted checker, different model, human specialist, or equivalent independent check.
7. **Audit literature independently:** search exact claims, equivalent formulations, constructions, and proof motifs; verify primary sources and report coverage. Failure to find prior art leaves novelty unresolved.
8. **Reconstruct the mechanism for humans:** map key lemmas and imported results from a certificate to the mathematical crux, then compare the rewrite with the checked artifact.

Evidence profiles are complementary. Independent or peer-reviewed work strengthens external validity and semantic review; certificates strongly support an encoding's logical validity; expert-author cases can provide specialist semantics but remain correlated; institutional reports are useful leads, especially with runnable artifacts, while unsupported axes stay provisional.

## Integrity, discovery, and understanding foundations

The shared integrity contract is intentionally smaller than a proof protocol.
Its four concerns—fidelity, warrant, recoverable intuition, and calibration—are
an operational synthesis of the following literature, not a claim that these
authors use the suite's terminology.

- Terence Tao's [pre-rigorous, rigorous, and post-rigorous account](https://terrytao.wordpress.com/career-advice/theres-more-to-mathematics-than-rigour-and-proofs/)
  treats mature intuition as supported by rigorous foundations and convertible
  into rigorous argument when required. The suite does not attribute that
  latent mastery to an AI system; it instead requires the exact mathematical
  referent, recovery tests, and a visible conversion obligation when a
  heuristic carries an unresolved stronger claim.
- William Thurston's
  [On Proof and Progress in Mathematics](https://arxiv.org/abs/math/9404236)
  argues that mathematical progress and communication depend on mental models,
  multiple representations, and ways of thinking that theorem-proof prose does
  not transmit by itself. This supports treating mechanism-bearing intuition as
  a first-class output rather than proof noise.
- George Pólya's
  [Mathematics and Plausible Reasoning](https://www.jstor.org/stable/j.ctv14164db)
  develops induction, analogy, and checked consequences as instruments of
  discovery. Andrew Aberdein's
  [Evidence, Proofs, and Derivations](https://arxiv.org/abs/1904.02593)
  likewise distinguishes mathematical evidence from completed derivation. The
  runtime consequence is an evidence ceiling, not exclusion of plausible
  reasoning.
- Dedre Gentner's
  [structure-mapping account of analogy](https://doi.org/10.1207/s15516709cog0702_3)
  emphasizes systems of relations rather than superficial shared attributes.
  The runtime analogy check therefore asks what relation is mapped and what
  relevant structure fails to transfer.
- The proof-comprehension model of
  [Mejía-Ramos et al.](https://doi.org/10.1007/s10649-011-9349-7)
  separates local meaning, logical status, and justification from holistic
  ideas, modules, methods, and examples. Explanation and proof exposition need
  both levels; routine line-by-line expansion alone is not comprehension.
- Rebecca Lea Morris's
  [motivated-proof account](https://arxiv.org/abs/2001.02657)
  asks what task each step performs and where it could reasonably have come
  from. This supports crux-weighted proof exposition and the ban on hiding a
  central step beneath detailed routine algebra.

The conversion obligation is therefore narrow. It is triggered only when an
unresolved claim materially relies on heuristic support. An analogy used to
explain an already established theorem instead needs recoverable referents and
a breakpoint, not a redundant demand to re-prove the theorem.

## Evidence since 2026

### Research-level contribution

- [Towards Autonomous Mathematics Research](https://arxiv.org/abs/2602.10177) reports Aletheia's generator--verifier--reviser system, public transcripts, case studies, and a 700-problem Erdős audit. Of 200 proposed resolutions audited by humans, 137 were fundamentally flawed, 63 technically correct, and only 13 meaningful resolutions of the intended problem. This directly supports separate validity, fidelity, and significance gates, explicit Human--AI Interaction records, abstention, and novelty checks.

- [Eigenweights for arithmetic Hirzebruch Proportionality](https://academic.oup.com/pnasnexus/article/5/5/pgag143/8671739) reports Aletheia-generated mathematics validated by a responsible expert author, including discovery of a failed commutativity assumption in prior work. It establishes substantial contribution in one specialist setting, not broad autonomy.

- OpenAI's [unit-distance conjecture report](https://openai.com/index/model-disproves-discrete-geometry-conjecture/) and the mathematicians' [companion analysis](https://arxiv.org/abs/2605.20695) document a model-generated counterexample that experts checked, simplified, and generalized using transferred algebraic-number-theory machinery. This supports exact-negation and cross-field construction search followed by independent mathematical digestion.

- [Lift-independence in the p-adic Simpson correspondence](https://arxiv.org/abs/2605.29947) reports model-assisted extensions, removed hypotheses, sharper bounds, and counterexamples to further relaxation, checked by expert authors. This supports atomic assumption maps, deletion tests, thresholds, and witness search, while remaining collaborative case evidence.

### Formal search and statement fidelity

- [AlphaProof Nexus](https://arxiv.org/abs/2605.22763) reports public Lean certificates for 9 of 353 formalized open Erdős problems and 44 of 492 OEIS conjectures, sometimes co-searching constructions and proofs. A simpler language-model-plus-Lean agent later solved all nine selected Erdős targets, while evolutionary search was cheaper on some hard cases. The evidence supports compiler feedback, checkpointed lessons, joint parameter/proof search, and escalation only after a simple loop stalls; low solve rates, formalizability selection, variance, and cost remain material.

- [Formal Conjectures](https://arxiv.org/abs/2605.13171) contains 2,615 Lean statements and reports 291 corrected misformalizations; 48% involved misrepresentation and 35% semantic errors. Its manual fidelity audits, definition tests, and API sanity lemmas show that statement fidelity is a separate theorem obligation.

- [Automated Conjecture Resolution with Formal Verification](https://arxiv.org/abs/2604.03789) reports a commutative-algebra counterexample with a large Lean development checked against a shorter human-reviewed specification and explicit axiom audit. It also documents obligation laundering into an unproved helper lemma. Freeze a compact target, compare it to the full artifact, and inspect the entire dependency closure.

- [LEAP](https://arxiv.org/abs/2606.03303) uses proof decomposition, memoized verified nodes, backtracking, and Lean feedback. [Discover and Prove](https://aclanthology.org/2026.acl-long.3/) separates discovery, informal checking, and formal proof, with a “Hard Mode” that hides the desired answer. Together they support explicit DAGs and evaluation that distinguishes finding a witness from certifying it.

- [Learning to Disprove](https://arxiv.org/abs/2603.19514) scales hypothesis deletion and Lean-verifiable counterexample proofs. Its synthetic tasks reinforce early certified refutation without establishing uniform transfer to open research.

### Critics, evaluation, and exposition

- [First Proof, Second Batch](https://arxiv.org/abs/2606.18119) evaluates four systems on ten fresh unpublished lemmas, with logs, costs, and two or three expert referees per output. Seven problems received at least one passing solution. Reviewers found citation and phrase-reuse concerns and a characteristic exposition error: routine detail obscuring the crux. This supports fresh problems, attempt-level reporting, independent review, and crux-weighted exposition.

- [ProofCouncil](https://arxiv.org/abs/2607.09474) reports target drift and critic path dependence. In one incomplete-proof case, a stateful critic accepted seven revisions while fresh critics rejected them. Reset verification after major revisions and finish with a fresh audit against the frozen target.

- [The Simplicity of the Hodge Bundle](https://arxiv.org/abs/2603.19052) reports an Aletheia-generated proof needing expert expansion of a “standard” lemma; a later version corrects a factor lost during human rewriting. Exposition is a mathematical transformation that needs comparison with the checked proof.

- OpenAI's [Ten Advances](https://openai.com/index/ten-advances-in-mathematics/) supplies [public Lean artifacts](https://github.com/openai/ten-proofs). They are reproducible objects, but their recent institutional reporting leaves advertised semantic, novelty, and significance claims provisional pending independent review.

## Reporting standard

For a research-level result report:

- final frozen target and material target changes;
- terminal truth status and exact open obligations;
- proof support, checker and library versions, and permitted axioms;
- statement-fidelity audit and representative sanity tests;
- literature coverage, novelty status, and significance status;
- model and tool versions, material prompts or hints, human interventions and edits;
- attempt denominator, selection rule, reversals or abstentions, and total budget;
- independent experts or fresh verifiers and their scope; and
- a readable, mechanism-centered account linked to any machine artifact.

## Earlier foundations retained

Current evidence reinforces these mechanisms rather than replacing them:

- formal environments and premise retrieval: [AlphaProof](https://www.nature.com/articles/s41586-025-09833-y), [LeanDojo](https://proceedings.neurips.cc/paper_files/paper/2023/hash/4441469427094f8873d0fecb0c4e1cee-Abstract-Datasets_and_Benchmarks.html);
- creative proposal plus checking: [AlphaGeometry](https://www.nature.com/articles/s41586-023-06747-5), [Draft, Sketch, and Prove](https://openreview.net/forum?id=SMa9EAovKMC), [Prover-Verifier Games](https://arxiv.org/abs/2407.13692);
- evaluator-guided discovery: [FunSearch](https://www.nature.com/articles/s41586-023-06924-6), [AlphaEvolve](https://arxiv.org/abs/2506.13131);
- example laboratories: [Davies et al.](https://www.nature.com/articles/s41586-021-04086-x);
- diverse candidates and process checking: [Self-Consistency](https://openreview.net/forum?id=1PL1NIMMrw), [Let's Verify Step by Step](https://arxiv.org/abs/2305.20050);
- hypothesis mutation and bounded model finding: [Nitpick](https://www21.in.tum.de/~nipkow/pubs/itp10.html); and
- worked examples and comparison: [Chi et al.](https://doi.org/10.1207/s15516709cog1302_1), [Rittle-Johnson and Star](https://doi.org/10.1037/a0014224).

The pedagogical studies remain relevant because 2026 systems do not replace causal evidence about how mathematicians learn; the newer work instead shows why checked examples and comparative explanation remain necessary for machine-generated or formalized proofs.
