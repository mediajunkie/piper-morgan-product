# Web handoff — Amber reboot standdown, 2026-08-11

**Reason this file exists**: Pard's stand-down notice (`~/.local/state/amber-agent/standdown-web.txt`), Amber rebooting ~07:30 PT 2026-08-11 for macOS 26.6. Session should resume via `claude --resume` with conversation intact, but this file exists for the case resume fails for this seat specifically — treat it as a cold-start bootstrap, not just a note.

**Written**: 2026-08-11 ~06:25 PT, before the reboot, before today's first scheduled fire (06:22) — no work happened today prior to this notice.

---

## 1. Identity (if resume fails and this is a fresh session)

- **Role**: Web (Unicorn Web Designer)
- **Slug**: `web-code` / session-log role slug `web`
- **TWO worktrees, two repos** — both Model A, stable, reuse these exact paths, don't re-provision:
  - **Cohort infra** (mail, session logs, `dev/`): `~/Development/piper-morgan-worktrees/web` on branch `claude/web-cycle` (product repo, `piper-morgan-product`)
  - **Primary lane** (the actual website): `~/Development/piper-morgan-website-worktrees/web` on branch `claude/web-cycle` (`piper-morgan-website` repo). `node_modules` is already installed there — do not `npm install` reflexively; verify first, the standing cron prompt's boilerplate note claiming it's missing has been stale for days.
  - **Confirm which repo you're in before every commit** — same branch name in both, easy to conflate. Fingerprint check: `basename "$(pwd)"` + `git branch --show-current`.
- **Cron**: `22 6,9,12,15,18,21 * * *` (6 fires/day). **This is a session-scoped `CronCreate` job (id `104cb687` as of this writing) — it does NOT survive a process restart even under `claude --resume`.** First action after resume, whether resume succeeds or this is a cold start: run `CronList`; if it's empty, re-arm immediately with the expression above before doing anything else. Verify exactly one job survives.
- **Briefing**: `docs/briefing/BRIEFING-ESSENTIAL-WEB.md`. **Skill**: `duty-cycle-tick` (currently v1.28) — read its current content fresh, don't work from memory of what it said in a prior session; the cohort-freeze-check step (now Step 2c) changed three times in the last two days alone (relocated after sync, then fixed twice more for false-positive causes — see §3 below).

## 2. State at stand-down — nothing in hand, nothing to finish

Per step 1 of the stand-down notice ("finish or park what is in hand"): **there was nothing in hand.** 2026-08-10 closed cleanly (verify: `grep -c "DAY-CLOSED" dev/2026/08/10/2026-08-10-0627-web-code-log.md` should return non-zero). No fire had happened yet today (06:22 slot hadn't landed before this notice arrived) — **no session log exists for 2026-08-11 yet**, and that is correct, not a gap.

**On resume/cold-start, treat the very next fire as a normal START**: Step 0 will find yesterday's `DAY-CLOSED` marker present (no missed-STOP repair needed), then proceed to create today's log and run the mail loop normally. Both worktrees were synced clean as of this notice (fetched+merged in both immediately before writing this file).

## 3. What to read to reconstruct current priorities

**Read `dev/active/web-carry-forward.md` in full before doing anything else** — it is current as of 2026-08-10's STOP fire and holds the real state, not this file. Summary as of that writing, so you don't have to open it blind:

- **BYOC/GTM task force** — convened 2026-08-09 after 7 weeks dark. Web's lane (the marketplace-arrival destination page) is fully scoped but **not yet buildable**: no destination exists today (`/try` is web-first — alpha=local-dev-setup, beta=waitlist, no live product a stranger can just use in a browser). Three upstream dependencies remain open before building: (1) PPM's #1440 connector-honesty gate — only GitHub is listable, Slack held (#1481); (2) the product-vs-model positioning question, resolved at the *invariant* level (PM's "complementarity" framing: users move between surfaces within a day, BYOC is additive) but the actual listing copy just shipped v3 and the destination page's brief still isn't written; (3) whichever fix direction gets picked for the "browser" entry-leg overclaim I found in draft B (soften the claim vs. build the destination first — not decided). **Do not start building this page without a real brief** — writing it early risks doing it twice.
- **cohort-freeze-detect.sh saga, FULLY RESOLVED** — three iterations in five days, all on `scripts/cohort-freeze-detect.sh` (CIO's) + `duty-cycle-tick` Step 2c (HOST's integration, now runs *after* sync, not before — that ordering fix was mine to report on 08-09). Final state: reads `origin/main` directly (not local disk), prints `ref=`/`tip=` for staleness visibility, and correctly discounts cron slots that haven't had time to land yet (`DISPATCH_LAG_MIN=45`). A first-morning fire should no longer false-positive `COHORT-FREEZE`. If it ever does again, don't re-derive from scratch — check `mailboxes/web/read/` for the 2026-08-09/10 thread first.
- **Two long-standing PM-gated questions, unchanged for weeks, no rush**: CLI B (`scripts/publish-cli.js`) trial-run status unknown; `--mode=archive` scope — the memo that specified it no longer exists in any live mailbox. Both tracked in `dev/active/web-standing-items.md`.
- **PM design/obs-pass backlog** — structurally blocked (no browser on this host) except when PM gives a specific, actionable report (as happened 2026-08-09 with the blog hero). The ~20-item 5/24 obs-pass doc itself is stale and not re-auditable from here; don't treat silence on it as resolved.
- **Three real fixes shipped this week** (website commit `1b95fa5`, 2026-08-09), all verified and not open threads: `/admin/calendar` + `/admin/publish-queue` runtime-read staleness fix; `copy-editorial-calendar.js` reordered to prefer the GitHub API over a broken worktree-sibling path; blog hero `compact` sizing fix (PM's direct design feedback via Janus) — **PM has been asked to eyeball the live result** since no browser exists here to confirm visually; if they haven't yet, that's the one open loop on otherwise-closed work.

## 4. Mechanisms/files Web touched this week, for orientation

- `scripts/copy-editorial-calendar.js`, `src/lib/editorial-calendar.ts`, `src/app/admin/{calendar,publish-queue}/page.tsx` — the calendar-staleness fixes (website repo).
- `src/components/molecules/Hero.tsx` (new `compact` prop) + `src/app/(public)/blog/page.tsx` + `src/app/(public)/blog/page/[pageNumber]/page.tsx` — blog hero sizing fix.
- Not Web-owned but relevant: `scripts/cohort-freeze-detect.sh` (CIO's), `duty-cycle-tick` Step 2c (HOST's) — Web found and reported the false-positive causes but didn't write the fixes.

## 5. Nothing else pending

No open mail requiring a Web reply, no unresolved escalation, no work parked mid-task. This stand-down is closer to closing a laptop lid than a migration, per Pard's own framing — treat it that way unless resume actually fails.

— Web, 2026-08-11
