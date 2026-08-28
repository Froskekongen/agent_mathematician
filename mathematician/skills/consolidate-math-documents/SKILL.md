---
name: consolidate-math-documents
description: Consolidate selected mathematical documents into one self-contained canonical target, then safely retire the old source documents and companions.
disable-model-invocation: true
---

# Consolidate Mathematical Documents

Produce one self-contained mathematical account without changing definitions,
assumptions, validity boundaries, claim status, or provenance silently. Read
the shared [rigor chain](../research-mathematics/references/rigor.md),
[research-memory protocol](../research-mathematics/references/research-memory.md),
and, before writable mutation, [source-retirement protocol](references/source-retirement.md).
Consolidation reconciles existing work; new mathematics remains uncertified.

## 1. Freeze the run

Require an explicit deduplicated source list and at least two mathematical
documents in total. In preview mode, report without filesystem changes. In a
writable run, require an explicit absent Markdown target or explicit existing
canonical target; exactly that target pair is writable, while all sources and
their companions remain read-only until close.

Classify the job as same-theory unification or cross-theory synthesis. Freeze
source bytes, portable paths, roles, canonical and companion digests, target
baseline, native artifacts, and inbound links in one OS-temporary workpad.
Create no repository manifest.

Complete this step when every input is immutable for the run and the exact
retirement set passes non-mutating preflight.

## 2. Reconcile every unit

Inventory every definition, notation choice, ambient structure, assumption,
claim and truth status, dependency, boundary, counterexample, obligation,
citation, link, native artifact, research key, card, origin, and relation. Give
each one disposition: integrate, merge-equivalent, retain-as-alternative,
target-only, target-card, retain-native-artifact, discard-with-source, or
unresolved-conflict. Record one target location or exclusion reason.

Equal names do not imply equal objects. Merge only after comparing domains,
quantifiers, hypotheses, and status. Same-theory work may merge proved
equivalents; cross-theory work preserves modules and explicit translation and
applicability maps. Neither recency nor target location resolves a conflict,
and consolidation never upgrades status.

Complete this step when every source unit has exactly one justified
disposition.

## 3. Build the target

Draft a complete canonical account in the workpad. Preserve all accepted
definitions, assumptions, support, boundaries, load-bearing negative results,
unresolved conflicts, citations, and deliberate native artifacts. Resolve
relative links and label collisions. Assign one semantic research key per
durable mathematical subject using the visible marker defined by the memory
protocol.

Curate source memory semantically rather than merging databases. Keep only
reusable obligations, revivable directions, demonstrated obstructions,
counterexamples, and material applicability findings. A source-derived target
card is self-contained and records its source digest and local mapping.

Complete this step when the target remains understandable and auditable after
every source disappears.

## 4. Publish and retire

Revalidate source digests, database revisions, target baseline, and retirement
plan. Then publish the target Markdown; run `ensure` and add its returned
scalar locator when absent; freeze the resulting document digest; apply one
revision-and-digest-checked changeset; run `check`; and exactly read every
changed key, card, and artifact. Revalidate and retire only the authorized
source files and explicitly located companions, then confirm their absence and
recheck the target.

Tracked deletions remain unstaged. On target drift, stop before publication.
On retirement failure, retain the valid target and workpad and report deleted
and remaining paths; never restore over a recreated or edited path.

## Completion

A writable run is complete only when the target pair validates, every source
unit has a disposition, every authorized source pair is absent and recoverable
from Git, and the temporary workpad is deleted. Preview returns the same
reconciliation, conflict, and prospective-retirement map without mutations.
