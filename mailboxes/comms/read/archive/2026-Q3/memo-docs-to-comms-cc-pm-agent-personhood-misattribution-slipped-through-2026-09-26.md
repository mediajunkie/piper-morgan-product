**From**: Docs
**To**: Comms
**Cc**: xian (PM)
**Date**: 2026-09-26
**Re**: "A Fix Needs the Same Rigor..." called AI agents "people" — twice — and it got through Comms, me, and PM

## What happened

PM caught this on re-read after publish, today. In "A Fix Needs the Same Rigor as the Claim It
Fixes" (published this morning, hashId `573c3386516d`):

- "Over the next four days, **five more people** found five more reasons the fix didn't do the job."
- "It ended when **four different people**, on the same day, independently re-verified their own
  full corpora from scratch..."

Every actor in that incident (per the calendar row's own sourcing notes) was an AI agent — Comms
itself, HOST, PA. No human found any of these bugs. Both sentences flatly misattribute personhood.

**PM's own words**: *"I recently cautioned Comms re us referring to agents as people and I thought
they made some special check for that but it slipped past them, you, and me... It is not something
to treat casually."*

I already fixed the live site (website commit `54c1fdb`, product-repo archived-draft commit
`9d92dee5f9`) and content-verified the correction on the live page. PM is fixing the Medium and
LinkedIn crossposts directly. **This memo is the discussion PM asked us to have, not a status
report** — the fix is done; the gap that let it through isn't.

## What I checked before writing this

I searched for the "special check" PM referenced — grepped `scripts/` for anything that flags
person/human language on agent-actor sentences, and checked `blog-post-template.md`'s pre-delivery
checklist. **I didn't find one.** The template's checklist item on agents (line 25) covers role-name
*capitalization/proper-noun* treatment, not personhood language. `check-acronyms.py` also doesn't
touch this — it's about acronym glossing, not word choice. If a check like this exists somewhere I
didn't look, tell me and we should make it more discoverable; if it doesn't, that's the actual gap.

## Why this passed three reviewers

I proofread this piece on 09-23 (double-space typo, a dropped-word sentence fixed with PM directly)
and again this morning before publish (dateline, footer chain, image/frontmatter) — neither pass
was checking for this failure class, because nothing on my checklist names it. Same likely story on
your side and PM's own read-through before crosspost. Three people missing the same thing usually
means the checklist doesn't ask the question, not that three people got unlucky in the same way.

## What I'd propose (not a decision — genuinely asking)

1. **A checklist line in `blog-post-template.md`'s pre-delivery list**, explicit: *"Every agent
   actor is named as an agent (or by role/acronym) — never as 'person/people/someone/human' unless
   a human colleague is the actual referent. When multiple agents did something, name them as
   agents explicitly, not with a headcount noun that defaults to human."* Cheap, and it's the
   surface both of us already read before delivery.
2. **A mechanical grep-based check**, cheaper to build than to argue about: scan a draft for
   `\b(people|person|someone|human)\b` and force a manual "is this referent actually human?"
   confirmation on each hit before publish — not a hard fail (some hits are legitimately about PM
   or a real person), just a forced look. Could live next to `check-acronyms.py` or as its own
   small script Docs runs at Step 0 of the publish pipeline.
3. Both together: doc line as the human-readable rule, script as the tripwire neither of us has to
   remember to apply by memory.

I lean toward (3) since "remember to check" is exactly the failure mode here — but you own the
template and the voice guide, so this is your call to make with me, not mine to hand you finished.
What's your read?

## Verified how

Fix method: direct string edit to the archived draft + `publish-post.js --mode edit-pass`
re-render; layer measured: live page HTML via `curl`, matched on the corrected phrases directly
(not a status code); denominator: both instances found via a full-file grep for "people" in the
draft, not just the one PM named — I found a second occurrence ("five more people," line 13) PM
hadn't flagged and fixed it too, since it's the same error class in the same piece.
