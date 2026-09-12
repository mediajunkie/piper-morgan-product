# Blog Style Guide

**For**: Anyone drafting, voice-passing, auditing, or proofreading a blog post (Comms and Docs
both).
**Purpose**: House terminology and word-choice decisions specific to public blog content —
places where the deliberate, correct choice is NOT the conventional one, and a well-meaning
"correction" during editing or proofreading actively introduces a defect.
**Created**: 2026-09-12, after the second known instance of the same mistake (see below).

This is distinct from the three documents it complements:
- `xian-voice-tone-guide.md` — sentence structure, register, editorial moves (*how* PM writes)
- `blog-post-template.md` — structure, frontmatter, footer conventions (*shape* of a post)
- `knowledge/piper-morgan-glossary-v1.1.md` — the canonical acronym/jargon expansion authority
  for the whole project, not blog-specific

This guide exists because a fact can be correctly recorded in the glossary and still get
overridden in practice, if nothing prompts a drafter or proofreader to check it at the moment
they're tempted to "fix" something that looks wrong. **The entries below are the ones that have
already cost a real mistake — read this before assuming a term is a typo.**

---

## Terminology

### MVP = "Minimum Valuable Product," not "Minimum Viable Product"

**The house term deliberately says "Valuable," not "Viable."** This is recorded in
`knowledge/piper-morgan-glossary-v1.1.md` ("MVP: Minimum Valuable Product (our gloss; not
'Viable')") and is the correct spellout anywhere MVP is expanded in prose, including inside a
description that doesn't use the bare acronym at all (e.g. "minimum-valuable-product planning").

**Do not silently "fix" this to the conventional "viable"** — that reads as an obvious
correction to anyone who knows the standard term, which is exactly why it keeps getting
"corrected" back.

**Known incidents**:
- Pre-2026-06-10 (Comms): a Ship-edit false-unpacking incident — motivated adding MVP to the
  glossary in the first place (glossary v1.2 changelog).
- 2026-09-12 (Docs): while proofreading "Piper Morgan Eras," independently "fixed"
  "minimum-valuable-product" to "minimum-viable-product," reasoning from the conventional term
  and from `episodes.ts`'s own bare "MVP" usage — without checking the glossary first. Published
  live before catching it via the file's own git history (PM had reasserted "valuable" via the
  admin UI minutes earlier). Corrected same-morning; full account in
  `dev/2026/09/12/2026-09-12-0720-docs-code-log.md`.

**Two incidents, two different roles, both from the same root cause**: treating a term that
*looks* like a typo as one, without checking whether it's a documented deliberate choice first.
That's the reason this guide exists as its own document rather than trusting the glossary entry
alone — a fact needs to be checked at the point someone is about to override it, not just
recorded somewhere true.

---

## How to use this guide

**Before "correcting" any spelled-out acronym, unconventional phrase, or term that looks like an
error in a draft**: check this guide and the glossary first. If the term isn't listed in either
and you still believe it's wrong, flag it rather than silently fixing it — especially if PM
touched the draft directly (admin UI edits can land between your sync and your read).

**Add a new entry here** whenever a genuine house-style word choice gets "corrected" by mistake,
or whenever PM makes a deliberate terminology call that a future editor might reasonably guess
wrong. One entry per term; keep the "known incidents" list growing rather than replacing it, so
a second occurrence is visibly a *pattern*, not a first-time surprise.

---

*v1.0 — 2026-09-12. Created after the MVP/valuable incident above, per PM's direct instruction
that the fact "belongs in the blog's style guide, which also should exist."*
