# Assignment: where has xian written down the project's five goals?

**From:** Exec. **For:** one read-only research sub-agent (suggested model: Sonnet; Opus only if the first pass is thin). **Filed:** 2026-10-13. **Output file:** `dev/active/exec-goals-forensic-report-2026-10-13.md` (do not edit anything else).

## Why

On 2026-10-13 xian restated the project's fundamental goals, in this order:

1. I learn things.
2. I share my experience, demystify, and invite others into this space.
3. Piper Morgan becomes useful for me.
4. Piper becomes useful for other people.
5. Piper becomes sustainable: revenue, an active open source community, consulting around supporting it.

He says he has said this, in some form, many times since the project began, and that it is a surprise to everyone but him. We need to know **how and when** he has said it and **where it was written down**: a passing log line, an intentional document, a public post, or nowhere. Then he and Exec decide where it belongs.

## Questions to answer

1. **Earliest.** What is the earliest dated statement of any of the five goals, in any form? Quote it.
2. **Every restatement.** List each distinct statement, oldest first: date, file path (or URL), the speaker (xian, an agent paraphrasing him, or a document), a short exact quote (under 40 words), and which goals it covers.
3. **Where it lives today.** Is any version written in an intentional, durable document (vision, PDR, ADR, README, briefing, about page, a public post, an onboarding doc)? Name each and say whether it is current or stale, and whether it keeps the order and the wording.
4. **Where it does not.** Is it absent from the places an agent reads at start (CLAUDE.md, `docs/briefing/` including `PROJECT.md`, `BRIEFING-CURRENT-STATE.md`, role briefings, the shared memory index)? Say so plainly for each.
5. **Drift.** Where the goals have been paraphrased, did the order or content change (for example, revenue ranked higher, or "useful for me" dropped)? Quote both versions.
6. **Gaps.** If the five goals are nowhere in an intentional document, say "nowhere" and list the nearest things (for example, strategy or vision documents that cover part of it).

## Where to look (read-only)

- This repo: `docs/` (vision, strategy, PDRs, ADRs, public, comms, blog drafts, omnibus logs), `dev/` day logs from the start of the project forward, `docs/briefing/`, `README*`, `CLAUDE.md`, `mailboxes/` (read and sent, all roles, older boxes too), `knowledge/`.
- Shared memory: `~/.claude-pm/projects/-Users-xian-Development-piper-morgan-product/memory/` (read files; do not edit or delete anything).
- The website content and blog sources in this repo, and the Weekly Ship issues (`docs/public/`).
- The private repo `~/Development/designinproduct` (read-only; `docs/` and `docs/mail/`), only for statements of the goals themselves.
- Search for variants, not just the exact words: "learn", "learning", "demystify", "invite", "share my experience", "useful for me", "useful for others", "sustainable", "revenue", "open source community", "consulting", "why I'm building", "goals of the project", "north star", "mission", "purpose", plus the numbered list shape.
- Use `git log -S` / `git log --follow` to date a statement in a file that has changed; give the date of the commit that first added the wording.

## Rules

- Rule 8 applies: do **not** write any outside person's name, address or employer into the report. Use role labels. xian and his agents may be named. If an outside person's words matter, say "an alpha tester" or "a collaborator".
- Never copy a credential or invite code.
- Report only what you found. If you did not search a place, list it under "Not searched". Quote output; do not guess dates.
- Do not edit, move or commit any file other than the report. Do not run `git add` outside the report path. Exec commits it.

## Report format (keep it short; one page of bottom line first)

1. **Bottom line** (5 lines): earliest date, number of restatements found, whether any intentional document holds all five in order, and what is missing.
2. **Timeline table**, oldest first: date | path | speaker | quote | goals covered.
3. **Where it lives today** and **where it does not** (points 3 and 4 above).
4. **Drift** (point 5).
5. **Verified how:** the searches you ran (terms, directories), counts of files scanned out of files that exist, and **Not searched**.

## Done means

A reader who knows nothing can see, in one page, when xian first said it, how often, and which durable document (if any) holds it, with every claim backed by a path and a quote.
