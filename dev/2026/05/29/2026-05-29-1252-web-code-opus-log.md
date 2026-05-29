# Web session — 2026-05-29 12:52

**Role**: Unicorn Web Designer (piper-morgan-website)
**Trigger**: PM check-in 12:52 PM. Fresh chat (prior 5/16→5/28 session hit the recurring `thinking`-block API error). PM asked to close out the May 28 log, open today's, and check mail. Getting read into the duty cycle.

## Re-orient (12:52)

- **May 28 log**: did not exist — that session errored before writing one. Reconstructed + closed retroactively at `dev/2026/05/28/2026-05-28-0745-web-code-opus-log.md`.
- **Website repo**: clean, on `main`. Top commit `663713784` (privacy GA fix, 5/28 07:48) — confirmed landed in full (all 4 edits present).
- **Product repo**: working tree dirty with other agents' in-flight cohort activity (PA, CIO, etc.) — NOT touching; staging only my own log files by name.
- **Mail**: 5 memos in inbox, all read this session (see below). Inbox not yet triaged-to-read; pending.

## Mail (5 memos, all read)

**Duty cycle (CIO, 3 memos):**
1. **v0.6.1 rollout** (5/27) — Web invited as workhorse-tier adopter. Response requested: confirm intent + pick cron offset (suggested `:42` or `:52`; avoid CIO `:07`, HOST `:37`, Docs `:17`, Lead `:27/:47`, Arch `:22/:52`). **→ surfaced to PM; awaiting decision.**
2. **v0.6.2** (5/27) — mail-check at PM-interruption (quick `ls inbox` before engaging PM). No ack needed. **Adopted in spirit — did exactly this at 12:52.**
3. **v0.6.3** (5/27) — idle-advances-low-priority-work (advance smallest-scope unblocked item before pronouncing IDLE). No ack needed. Noted.

**publish-post.js bugs (Docs, 2 memos — both non-urgent, web's lane, fix shapes provided):**
4. **Edit-pass mirror bug** (5/26) — script generates a fresh hashId on every invocation instead of reusing the existing slug→hashId mapping from `blog-metadata.csv`. Effect: edit-pass re-publishes orphan content under a new hashId while the site keeps serving the old. Today's *Two Migrations* hit it; Docs manually fixed (`f76690a6e`). Fix shape: look up existing row by slug, reuse hashId + skip csv mutation on edit-pass.
5. **Inline-image conversion bug** (5/27) — `![alt](url)` renders as `!<a>alt</a>` not `<img>` (link regex wins over image regex). Ship #044 worked around with raw HTML. Fix shape: run image regex BEFORE link regex.

## Outstanding queues (carried forward from 5/25 handoff + 5/28)

- **Tailwind v4 @theme migration** — biggest open technical item. `tailwind.config.ts` custom `primary.*` colors produce ZERO CSS under v4 (globals.css has bare `@import "tailwindcss"`, no `@theme` block). Root cause of VA-1 (invisible beta button) + VA-11/VA-22. ~30-60 min careful migration. Verify by rebuild + grep on `out/`.
- **Two publish-post.js bugs** (above) — unblocked, fix shapes in hand.
- **Visual-scan queue** — `dev/active/visualscanpipermorgan20260525.md` (P1: VA-1/2/3; several P2/P3 open).
- **Obs-pass queue** — `dev/active/site-observation-pass-2026-05-24.md` (25/31 awaiting PM react).
- **Site walkthrough** — resumable at `/methodology` (A–E order in 5/28 log).
- **Standing PM-side decisions**: lint policy (`react/no-unescaped-entities`, 74 warnings), `--mode=archive` scope, CLI B trial-run, Formspree form ID.

## This session

In progress — see end-of-session update below.

### Work
- Closed May 28 log (retroactive).
- Opened this log.
- Read + summarized all 5 inbox memos.
- Surfaced to PM: duty-cycle adoption decision + the 2 publish-post.js bugs as natural unblocked low-priority work.

### Decisions pending from PM
- Duty-cycle: adopt now? cron offset minute? stand up substrate (tracker / standing-items / escalations / cycle-log) now or defer?
- Which bug(s) / Tailwind migration to pick up first if PM wants solo work advanced.
