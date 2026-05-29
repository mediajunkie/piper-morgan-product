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

### Work shipped
- Closed May 28 log (retroactive). Opened this log. Read + summarized all 5 inbox memos.
- **publish-post.js — both Docs bugs fixed** (website `b097a997e`, PUSHED):
  - Inline-image: added standalone `![alt](url)` → `<img>` rule in renderInline, ordered after linked-image and before the link rule. New corpus entry `17-inline-image`. Corpus 17/17.
  - Edit-pass hashId: auto-detect edit-pass by slug lookup in blog-metadata.csv, reuse the live hashId, update blog-content.json in place; relaxed `--image` requirement for auto-detected edit-pass. New-slug publish path unchanged (verified: fresh hashId, `--image` still required).
- **Tailwind v4 root-cause fix** (website `0d406ad3f`, COMMITTED — push HELD for PM review):
  - Root cause: v4 doesn't auto-read `tailwind.config.ts`, so all custom tokens (primary.*, spacing/radius/shadow, display font, typography plugin) compiled to ZERO CSS → invisible beta button (VA-1), alpha/beta orange (VA-22).
  - Fix: added `@config "../../tailwind.config.ts";` to globals.css — the v4 bridge directive. One line, zero transcription risk vs. hand-porting 60+ tokens into `@theme` (the approach the 5/25 handoff had assumed; `@config` is lower-risk and officially supported).
  - Verified: `bg-primary-teal` now emits `background-color:#2dd4bf` (was zero CSS); 40 `primary-teal` occurrences in built CSS; build + type-check clean. NOT yet live-browser-checked.

### Duty-cycle correction (important)
- PM approved "adopt now, offset :52" — but that was based on the stale v0.6.1 memo. Current authoritative state (cohort-agent-status.md, refreshed 13:00):
  - **`:52` is Arch's**, `:42` is PA's. Open offsets: **`:12`, `:22`, `:57`.**
  - v0.7.0 adoption = **worktree + Model A**: requires PM to launch a NEW Claude Code session inside a `claude/web-cycle` product worktree (a cron can't self-relaunch; "do not register on main"). Cannot register a correct cron from this website-repo session.
- No cron created. Surfaced to PM for re-decision (offset + whether I prep worktree/substrate now).

### Open / pending PM
- Push the Tailwind fix (deploys VA-1/VA-22 visual fix)? Optionally live-browser-check first.
- Duty-cycle: pick open offset (`:12`/`:22`/`:57`); want me to prep `claude/web-cycle` worktree + substrate + filled cron-prompt for you to launch?
- Product-repo log commits (`42911099c` + this update) are LOCAL — push to product main was blocked by the auto-mode classifier; needs PM OK or a settings rule.
