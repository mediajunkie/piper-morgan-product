# Communications Director Session Log

**Date**: May 16, 2026 (Saturday)
**Start Time**: 7:10 PM PT (May 15 — sliding into May 16 publication day work)
**Role**: Communications Director (Comms)
**Model**: Claude (Opus 4.7)
**Environment**: Claude Code
**Branch**: `claude/comms-family-resemblance-prep`
**Worktree**: `/Users/xian/Development/piper-morgan/piper-morgan-product-comms-family-resemblance-prep`

---

## Session Context

PM asked me to fact-check + scrub tomorrow's (May 16) insight post: *The Family Resemblance*. First real-world application of the `draft-blog-post` skill drafted earlier today. Per worktree-default directive, working in a dedicated worktree.

Draft at `docs/public/comms/drafts/the-family-resemblance.md` (1229 words / 73 lines before edits; PM has two explicit `[CONSIDER:]` / `[ADD PERSONAL ANECDOTE:]` placeholders).

## Fact-check findings — three high-confidence corrections applied inline

1. **DECISIONS.md line count**: original "a hundred and fifty lines now" → actual 43 lines (max in history). Softened to "a few dozen entries" + FACT-CHECK NOTE.

2. **Klatch DECISIONS.md timing**: original "had already adopted DECISIONS.md six weeks earlier" → cross-pollination brief from 2026-04-18 explicitly says both Klatch and PM added DECISIONS.md on the **same day**, framed as "a convergent infrastructure move that emerged independently in both projects at the same time." Corrected inline + FACT-CHECK NOTE with brief citation.

3. **Calliope attribution**: original "Calliope, the citation-and-authority engine in the OpenLaws stack" → Calliope is a **Klatch** agent per session-log paths (`klatch/docs/logs/...calliope-opus-log.md`) and the SSH-over-443 commit attribution (`56408f0f`: "via Calliope, propagated by Dispatch"). Corrected to "one of the Klatch project's agents" + FACT-CHECK NOTE.

## Lower-confidence claims flagged

4. Handoff-memo template "six-section structure my Chief of Staff agent drafted a month ago" — not verified. FACT-CHECK NOTE.
5. Klatch / OpenLaws modifications to the handoff template — can't verify from this repo. FACT-CHECK NOTE.
6. The "Calliope's read-mostly authority graph... Calliope's ingestion pipeline" passage generalized to "a sibling project's..." to avoid attribution drift (a "read-mostly authority graph" reads as OpenLaws / citation-domain, not Klatch / entity-management). FACT-CHECK NOTE.

## Four-category opacity sweep — three role-name catches resolved

- "HOST and CIO had both used it" → "two more of my roles had both used it"
- "Chat-based agent role migrates to Code" → "an agent role migrates between work surfaces (a chat interface to a coding interface, in my setup)"
- "PA caught it" → "Another agent caught it"

## Voice sweep — five semicolons split

All public-prose semicolons split into separate sentences per the no-semicolons-in-published-prose discipline:
- Line 13 (six-weeks claim) — also corrected for fact
- Line 23 (Klatch/OpenLaws/Piper Morgan inboxes)
- Line 33 (Klatch entity model / OpenLaws citation graph)
- Line 35 (Postgres/Calliope ingestion mismatch) — also generalized for attribution
- Line 42 (vocabulary in-narrative aphorism) — extra semicolon caught during pass
- Line 53 (parallel A/B/C structure)

PM placeholders left in place at lines 31 and 62.

## Final state

- 78 lines / 1532 words including FACT-CHECK NOTE meta-content (~1200 words of published prose)
- All public-prose semicolons gone
- Four-category opacity sweep clean
- Three high-confidence fact errors corrected with FACT-CHECK NOTE breadcrumbs
- Three lower-confidence claims flagged for PM verification
- PM placeholders preserved

Ready for PM voice-pass + the two placeholder additions, then publish.

This was the first real application of the new `draft-blog-post` skill. The Phase 3 sweep (opacity + length + voice spot-check + verifiable-claims) caught all three substantive fact errors plus six semicolons plus three role-name opacities — exactly the kind of upstream-from-voice-pass discipline the skill encodes.
