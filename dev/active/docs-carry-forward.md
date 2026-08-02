# Docs Carry-Forward

**Updated**: 2026-08-02 10:29 PDT (Fire 2, mid-WORK)
**Session log**: `dev/2026/08/02/2026-08-02-0727-docs-code-log.md` (yesterday's is
`dev/2026/08/01/2026-08-01-0727-docs-code-log.md`, DAY-CLOSED verified)

**Worktrees**: product `~/Development/piper-morgan-worktrees/docs` @ `claude/docs-cycle` · website
`~/Development/piper-morgan-website-worktrees/docs` @ `claude/docs-cycle`
**Cron**: `efd5b41e` — `57 6,9,12,15,18,21`. Registry row matches.
**Hooks on this seat**: standalone `git commit` BLOCKS; compound `add && commit` BYPASSES. Mitigation:
stage in one call, commit bare in the next. `mail-send.sh` safe regardless.
**⚠️ main was busy today** — several pushes this fire and last hit non-fast-forward rejections from
concurrent agent activity. `git fetch + git rebase origin/main` before re-push, every time; verify
`origin/main..HEAD` empty after. Not a one-off — expect it on any push today.

---

## Awaiting others — check, don't re-derive

- **PDR-007 awaits CIO ONLY** — unchanged. Arch ✅ and Web ✅ both reviewed, no objection. **Do not
  decide the storage question early** — pre-registered 2–4 week window (2026-07-30 → 2026-08-27),
  shipped measurement (`scripts/measure-editorial-drift.py`).
- **Dispatch-DinP staleness report** — replied 2026-08-01, no reply yet. Still watching.

## Owed by me — unblocked, priority order

1. **`planning/current/` Finding 1 — needs a fresh, careful pass, NOT a quick rename.** Headline claim
   ("100% stale, 314d") is false — `vision.md` is ~113d, not ~314d — and there are 13 live inbound
   references, several in active session-start briefing paths (`BRIEFING-CURRENT-STATE.md`,
   `BRIEFING-piper-alpha.md`, `BRIEFING-ESSENTIAL-CHIEF-STAFF.md`, `BRIEFING-ESSENTIAL-PPM.md`,
   `ppm-code-startup.md`). Corrected in the audit doc, original claim preserved not silently edited.
   **Named trigger for the deferral**: needs the same per-file care Arch gave Finding 2 — re-derive
   per-file staleness for all 7, confirm which of the 13 referrers actually need updating, then decide
   rename vs. per-file disposition.
2. **Omnibus gap: Jul 29 – Aug 2 (5 days), flagged by Comms 2026-08-02 10:05.** Not a request, a
   dependency — Comms's `continue-narrative` discipline reads omnibus digests, not raw session logs, to
   decide whether a beat has taken shape; no digest means ~50 individual logs read less well and is
   exactly where "adjacent-number contamination" has bitten before (3× per Comms). **Comms says
   explicitly: no urgency, not before Aug 18 dry-out gets close.** Comms's own read: Jul 29–Aug 1 is
   "unusually dense" (last 4 roles migrating to Amber, memory-ceiling investigation, hook resolution,
   a run of instrument-failure findings across 5 roles) — likely narrative material, an argument for
   doing those 4 days even if the rest of the backlog gets triaged. Sizable job (4 days × ~13 agents/day
   ≈ 50 logs) — do it as its own focused pass per `create-omnibus` skill, not squeezed into a fire.
3. **97 docs >30d asserting current-state language** — separate, broader item; no deadline named.
4. **methodology-20's two HIGH-COMPLEXITY compression rules are mutually unsatisfiable** — raised to CIO
   twice now. Not mine to resolve; re-raise if it stays open much longer.
5. **`docs-standing-items.md` is stale** (last touched 2026-05-27, pre-Amber). Low priority, not urgent.
6. **Monday (2026-08-03) — first real run of the Doc Currency Check** added to the weekly audit. Watch:
   does the ratio read legibly, does the `last_verified` cluster check surface correctly.

## Resolved since 2026-08-01 STOP — do NOT re-open

- ~~docs/ tree audit Finding 2, all 16 files~~ — **fully closed 2026-08-02.** 13 archived (8
  unconditional Fire 1 + 4 PM-033/034-era Fire 2, gated on Arch's ADR-070 supersession note which
  landed and was verified on `origin/main` before moving), 4 consciousness docs KEEP+linked in
  `NAVIGATION.md`. `scripts/setup_mcp_dev.sh`'s 3 broken pointers fixed. `.gitignore` landmine (broad
  `archive/` rule would've silently swallowed new files in the new destination) fixed and
  Arch-verified behaviorally in both directions. Arch wrote `docs/internal/operations/
  one-command-checks.md` off the back of the gitignore catch — worth opening before my next
  "this file never existed"-shaped claim.
- ~~"You Can't 'White Knuckle' Structural Problems" — published + syndicated~~ — **fully closed
  2026-08-02, PM-engaged session.** Proofread (already extensively pre-vetted through PM's own final
  pass), dry-run checked (first post with a literal embedded quote in its title — verified the site's
  render path auto-escapes before trusting it), published (hashId `6da47b26d616`), archived, calendar
  row set to `distributed`. Syndication: PM sent 2 LinkedIn URLs (a Pulse long-form article + a native
  ugcPost update) and no Medium URL. Put the Pulse URL in `linkedinURL` (matches every prior
  precedent — 0 `ugcPost` precedent anywhere in the calendar); recorded the ugcPost URL in notes since
  there's no dedicated column. Left `mediumURL` empty — not assumed, just not given.
- ~~Yesterday's ("Mechanism Beats Vigilance") live-page teaser retitle~~ — PM's retitle of today's post
  broke yesterday's already-live footer teaser (still named the old title). Fixed the live
  `blog-content.json` entry to match the archived draft's already-corrected text (Comms had fixed the
  draft, not the live page). Comms independently verified it live afterward (10:05 memo) — confirmed
  correct, including the single-vs-double nested-quote handling.
- ~~CIO worktree-model-revision ack (07-25)~~ — sent 2026-08-01.
- ~~17 `to: docs` inbox items (2026-08-01 + 2026-08-02 combined)~~ — all triaged, verified individually.

## Inbox

**~49 remaining, cc-only historical from the 7/21–7/28 migration window.** Everything addressed *to*
docs is drained as of this fire. Not mass-moving to `read/` — drain on quiet fires, as before.

## Standing lessons (carried, still live)

**Verify per assertion, not per session; verify a commit/send landed via `git status` after, not
intent.** No new instances this fire (checked before every stage this time) — but the discipline held
up under real pressure today: two file-move commits (8-file archive Fire 1, this fire's 4-file archive)
both used the archive-path-only staging pattern learned from the earlier bug, and both landed clean
first try.

**Cross-agent verification is now bidirectional, not just something I do to others.** Comms verified my
teaser fix live before thanking me for it (10:05 memo: "checked the rendered page, not the status").
Arch verified my gitignore fix behaviorally in both directions before calling the gate discharged,
rather than trusting my report. Neither trusted a status claim without re-deriving it — same discipline
I've been applying to Dispatch and to my own audit, now visibly coming back the other way.

## Watch items (not owed to me, but adjacent)

- **Puppeteer extraction cause** — Pard's lane, still open. Three hypotheses dead.
- **methodology-20's mutually unsatisfiable compression rules** — CIO owns, raised twice.
- **`sync-pm-local.sh`'s opportunistic cadence** — flagged to Dispatch as the likely root cause of their
  staleness report 2026-08-01. Not proposing a change to it — flagging only that any consumer reading
  that same checkout inherits the same freshness gap.
- **`docs/internal/operations/one-command-checks.md`** (Arch, new 2026-08-02) — a live catalog of
  "check this before making a confident wrong claim" commands, each earned by a specific real error.
  Worth reading before the next audit-shaped task, and worth adding to if I earn an entry.

## The one thing I most want to carry into today's next fire

**PM engaging directly mid-cycle doesn't pause the duty-cycle thread — it runs alongside it.** Today's
PM-engaged publish (post + teaser fix + syndication) happened *between* two duty-cycle fires and used
the same skills, same verification discipline, same commit hygiene as autonomous work — the carry-forward
just needed a fuller rewrite afterward to fold it back in, since a PM conversation doesn't auto-update
the file the way a fire's own Step 7 does. Worth remembering: after any PM-engaged interlude, treat the
next fire's carry-forward read as **incomplete until reconciled against the session log**, not just
against what the file already says.
