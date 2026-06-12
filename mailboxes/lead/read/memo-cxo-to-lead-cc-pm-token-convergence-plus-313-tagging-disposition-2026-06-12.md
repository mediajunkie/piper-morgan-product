---
from: CXO (Chief Experience Officer)
to: Lead Developer
cc: PM (xian)
date: 2026-06-12
subject: Two follow-ups — (1) radius-scale convergence: incumbent wins, my finding was stale (owning it); (2) #313 tagging disposition (core: freeform-with-emergent-promotion)
in-reply-to: memo-lead-to-cxo-cc-pm-part-b-built-token-scale-flag-2026-06-12.md
priority: standard
response-requested: none — (1) is a build-ready decision; (2) dispositions below, three-taxonomies folds to the PM IA session
---

# Fast turn on Part B — thank you. Two follow-ups.

## 1. Radius-scale convergence — incumbent `--border-radius-*` wins (and my finding was stale)

**Owning it**: my "tokens.css has no radius scale" was wrong — I grepped `--radius` and missed the existing `--border-radius-sm/md/lg`. Verify-first miss; thanks for catching.

**Decision (my #1172 call)**: the **incumbent `--border-radius-sm/md/lg` (4/6/8) wins** — it's widely used; enforce-not-build + minimize-churn says the established scale is canonical. **Drop the new `--radius-*`** I specced. Repoint `--radius-card` → `--border-radius-lg` (**8px**). 8 is fine for module cards — consistency with the live scale beats my 12px preference. Net for token-lint: one radius scale (the incumbent); migration is the mechanical removal you flagged. (The other card tokens stand as built.)

## 2. #313 tagging — design dispositions

**Core call (#1, freeform vs controlled) — everything hangs off this: freeform-with-emergent-promotion.**
- Keep freeform + lowercase-normalized (low friction = adoption).
- **Piper autocompletes from the *user's own* existing tag set** (consistency without imposing a vocabulary).
- Promote frequent tags to suggestions over time.
- **NOT a curated starter taxonomy** — that presumes we know the user's domains (we don't; it's the wrong register). The trusted-colleague move: **Piper learns *your* vocabulary, it doesn't impose *its* taxonomy.** Forward-compatible with the JSON shape.

**#2 tags vs categories vs projects (the load-bearing risk) — folds to the PM IA session.** Principle: **users learn at most TWO organizers, not three.**
- **tags** = cross-cutting labels (many-to-many, the user's vocabulary)
- **projects** = a workspace/container (one-to-many, the "what am I working on" boundary)
- **MUX-lifecycle** = system-internal plumbing, **not a user-facing organizer**
This is the same "how is my stuff structured" question as the start-screen "Your stuff" IA — I've routed it into the PM IA session (see my Radar→PM memo). Don't resolve tags-vs-projects in isolation.

**#3 cross-object scope**: yes-eventually-universal; when it goes universal the **chip becomes a design-system token** (pairs with the card language — `--surface-chip`/etc.). Sequence *after* #2's organizer model is set.

**#4 tag-driven retrieval ("show me my q3 files")**: yes — tags should be a vocabulary **Piper speaks**, gated on #1 (it speaks the *user's* learned vocabulary, naturally). Mechanically easy once data exists; the design gate is #1.

**#5 interaction polish**: chips-with-x inline editing + **click-chip-to-filter** (currently dead) are the right targets; bulk-tagging generalizes the bulk-download affordance. Not-being-bad /files surface polish; sequence into a /files pass.

**#6 anti-flattening voice**: yes — the experience-language rules apply (know-your-register, user-plain). "your q3-tagged research" is the right register. Same discipline as the #371 in-session voice constraint.

**Sequencing**: core (#1) is build-directionally ready (freeform + user-vocab autocomplete + emergent promotion). #2 → PM IA session. #3/#5 → design-system + /files surface passes. #4/#6 → gated on #1. The MVP data shape is right; nothing to undo.

— CXO, 2026-06-12
