---
name: consolidate-math-documents
description: Consolidate selected mathematical documents into one self-contained canonical target while preserving the source documents.
disable-model-invocation: true
---

# Consolidate Mathematical Documents

Consolidate deliberately. Produce one coherent mathematical account without
silently changing definitions, assumptions, claim status, or source history.
This skill organizes existing work; it does not certify new mathematics.

For a writable consolidation, read and follow the shared
[research-memory protocol](../research-mathematics/references/research-memory.md)
and use its
[CLI](../research-mathematics/scripts/research_memory.py). The target canonical
document and its companion are the only writable theory artifacts. Every
source document, source companion, and source-native artifact is read-only.

## Choose the mode

- **Preview:** compare the sources and return a consolidation and conflict map
  in the conversation without creating or changing files.
- **Existing target:** merge into one explicitly selected canonical Markdown
  document in an authorized file-backed round.
- **New target:** create one explicitly named canonical Markdown document and
  its canonical-stem companion in an authorized file-backed round.

Default a writable consolidation to a new target, but never invent its path:
the user must explicitly name a currently absent target Markdown file. Use an
existing target only when the user explicitly selects it.

Before every run, establish the complete source list and classify the
relationship among the sources. A writable run also requires its explicit
target. Use **same-theory unification** for fragments or versions intended to
describe one theory. Use **cross-theory synthesis** when the sources retain
distinct objects or interpretations. Ask the user when this choice or the
target is ambiguous; do not infer authority from filenames or modification
times.

Classify an input as canonical mathematics, a noncanonical draft or research
record, or a native proof/reference artifact when that distinction affects
what may be adopted. A draft remains uncertified after consolidation.
Require at least two mathematical documents in total. Search the repository
for additional inputs only when the user requests discovery.

## Establish one target and immutable sources

Resolve and de-duplicate all paths. The target cannot also be a source. A
writable run owns exactly one target canonical document and one target
research-memory database; it opens every source companion read-only.

In a writable existing-target run, preflight the target pair with `ensure`
before substantive work. When the target has no locator, `ensure` creates or
validates its canonical-stem companion; add the schema-2 locator only after
success. When a locator exists, run `ensure` with `--require-existing`. Stop
and report a missing target companion rather than recreating it. Preview mode
never runs `ensure`.

In preview with an existing target, open a located target companion only
read-only and stop for confirmation if it is missing. Treat an unlocated
target as canonical-only; preview never creates its default companion.

A source locator naming a missing companion may represent lost research
history. Stop and obtain confirmation before continuing from its self-contained
canonical document alone; create nothing for that source. A source without a
locator is canonical-only unless the user explicitly routes a database to it.

In new-target mode, require an explicitly named path that does not exist.
Draft the target in the workpad; create the canonical file and ensure its
companion only after the candidate is stable and ready for publication.

Preserve source files byte-for-byte. Do not edit their locators, mark them
superseded, move them, or delete them. Do not copy a source locator into the
target. After successful consolidation, report sources that the user may
separately choose to archive. Perform no Git staging or commits without
separate authorization.

For a writable run, create one generated OS-temporary workpad and record its
path and round identifier. Keep frozen input copies and digests, the
reconciliation matrix, target drafts, link rewrites, checks, and the target
database batch there. For each source, freeze its exact document bytes,
resolved path, role, canonical digest, companion revision, companion byte
digest, and semantic `export`. Freeze the same target identity and revision
when an existing target is used.

## Reconcile the mathematics

Read the target first when it exists, then every source canonical document.
Record each source's role, portable path, and SHA-256. Validate and export every
available source companion read-only. In a writable run, freeze those exports
in the workpad; in preview, keep results only in conversational/transient
context and create no file. Research memory is context, not authority.

Build a transient reconciliation matrix covering every source definition,
notation choice, ambient structure, assumption, claim and status, proof
dependency, validity boundary, counterexample, open obligation, citation, and
native artifact, plus every source card and edge. Give each unit exactly one
of these dispositions:

- `integrate`;
- `merge-equivalent`;
- `retain-as-alternative`;
- `target-only`;
- `source-only`;
- `target-card`;
- `redundant-or-obsolete`; or
- `unresolved-conflict`.

Completion of this inventory means every source unit, card, and edge has a
disposition and an exact target location or exclusion reason.

Establish one target vocabulary. Equal names do not establish equal objects;
state the map between source and target objects and account for unmatched
hypotheses. In same-theory unification, combine statements only after checking
their quantifiers, assumptions, domains, and epistemic status. In cross-theory
synthesis, keep modules visibly distinct and make every translation or
applicability claim explicit.

Do not silently privilege the existing target over a conflicting source.
Exact duplicates may be collapsed. Compatible
strengthenings, weakenings, and alternative proofs retain their differing
assumptions and status. Put incompatible claims side by side as an unresolved
conflict or ask the user to adjudicate. Consolidation never uses “latest
wins,” upgrades a claim to `PROVED`, or invents a compromise theorem.

## Build and close the target

Draft the complete target in the workpad before publication. Make it
self-contained: imported mathematics must include the definitions,
assumptions, proof or stated support, and boundaries required to understand
it. Source references provide provenance rather than load-bearing content.
Rewrite relative links for the target location, preserve citations, resolve
anchor and theorem-label collisions, and update any target cards whose
canonical anchors move. Keep source-native artifacts linked in place unless
the user explicitly requests promotion into target-owned storage.

Add a concise consolidation-provenance section listing each source path and
digest, its role, the material integrated or excluded, and every unresolved
conflict. Keep the exhaustive reconciliation matrix transient.

Curate research memory semantically rather than merging SQLite files. Retain
only source cards that remain useful to the target: live obligations,
realistically revivable directions, demonstrated obstructions, reusable
negative results, or material source-applicability findings. A relied-upon
source card becomes a self-contained local snapshot with its source locator,
semantic slug, content digest, and applicability mapping in `card_origin`.
Never bulk-copy cards or binary-merge companions; accepted mathematics belongs
in the target canonical document. Never copy a source card's `integrated`
disposition or source canonical anchor mechanically. Choose a target-specific
disposition, claim status, anchor, and applicability analysis.
Attach an origin for every source card that materially influences a retained
target card, including same-theory sources.

Handle semantic slugs explicitly:

1. add a curated card when its slug is absent from the target;
2. map equivalent content with the same slug to the existing target card and
   attach the additional origin;
3. when one slug has different meanings, either synthesize a revision-checked
   target card or choose a genuinely distinguishing semantic slug;
4. never append opaque numeric suffixes or use an implicit upsert; and
5. recreate an edge only when both endpoint cards survive and the relation is
   still useful in the target.

Before publication, revalidate every frozen source canonical digest, source
database byte digest and revision, and—when it exists—the target canonical
digest and database revision. In new-target mode, re-check that the selected
target Markdown path is still absent immediately before creating it. Then:

1. write the target canonical document;
2. ensure the schema-2 target companion and add or preserve its locator;
3. apply one revision-checked batch of card, origin, and edge operations;
4. validate the target database and require its canonical status to be
   current;
5. inspect every added or materially changed card and export the final target;
   and
6. verify that every source artifact remains byte-identical.

If a consolidation changes a theorem, assumption boundary, or proof rather
than merely reconciling existing mathematics, retain the result as unresolved
or uncertified and recommend `$research-mathematics`. Use `$destroy-theory` or
`$audit-assumptions` as read-only reviewers only when the merge itself creates
a material claim or assumption conflict.

## Recover and finish

On concurrent input changes, stop before publication and reconcile the new
version. On canonical writing, database application, validation, or
source-integrity failure, retain the workpad and report its exact path, the
last completed step, and every target artifact that changed. The database
batch remains atomic. Preserve the current target rather than automatically
restoring a snapshot over possible user edits.

A failed new-target run may leave a clearly reported incomplete target pair;
keep its recovery material rather than silently deleting it. If only workpad
deletion fails after a valid close, report the residual path; the target pair
remains valid.

Delete only the generated workpad after the target canonical and database
validate and every source-integrity check passes. A completed run leaves one
self-contained target pair and deliberate native artifacts, with no persistent
merge report and no source mutation.
