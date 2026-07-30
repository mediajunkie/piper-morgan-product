# Comms carry-forward — 2026-07-29 STOP (21:12) → for the Jul 30 START

**Host**: Amber.local · **Model A**, stable worktree `~/Development/piper-morgan-worktrees/comms`, branch `claude/comms-cycle`
**Cron**: `17634487` · `12 6,9,12,15,18,21 * * *` (armed 09:58; registry row un-parked)
**Session log**: `dev/2026/07/29/2026-07-29-0948-comms-code-log.md`
**Predecessor**: `dev/2026/07/29/2026-07-29-0642-comms-code-log.md` (Desktop / Model B, `DAY-CLOSED` ✓ — closed early to unblock this migration)

---

## Current state

- **Migration COMPLETE.** Comms is up on Amber, cycling, registry row cleared. Environment verified rather than assumed (0 behind origin, git identity clean, memory pool 168 files, toolchain present).
- **Weekly Ship #053 "The Invariant Held" — ✅ PUBLISHED AND LIVE.** https://pipermorgan.ai/shipping-news/weekly-ship-053-the-invariant-held/ · status `published`, `canonicalSite=distributed`. **ONE ITEM OPEN AND IT IS PM'S: the LinkedIn syndication URL** — I cannot generate it. Send it to Docs and they'll set `status=distributed`, fill `liPubDate`/`linkedinURL`, and archive the draft (Step 9 gates archival on that URL, which is why it's still in `drafts/`).
  - My Driver gloss lost a rebase to PM's wording ("the end-to-end scenario harness"). **No rework — PM signed off and took responsibility for forking the question; Docs separately owned publishing before opening my memo.** Closed, nothing owed. Both said mine was the better house-style answer; it lost a race, not a judgment.
  - Both blockers had resolved before publish:
  1. ✅ `pubDate` corrected at 13:47 by **EXEC** (`ebe2105bb`) — not "another session," which is how I first wrote it. **Derivation defect TRACED AND FIXED by Exec**: `draft-weekly-ship` literally read "pubDate (target Tuesday)" against an 8-for-8 Wednesday cadence, wrong for every future Ship; #053's own error was a separate day-after-drafting slip. **v1.9 shipped, #054 → Wed Aug 5.** Closed.
  2. **"Driver" RESOLVED — and my original claim was wrong.** It's the FtU sprint's **scenario driver** (Phase-3 acceptance-gate harness, Scenario A/B/C turns against a real LLM), recorded twice in the Jul 16 + Jul 17 omnibus logs. I had searched only the workstream memos and summary report and reported "no referent in any source." Gloss applied (`193647805`); question withdrawn to Exec.
- **Beats 24-28 slate proposed** (`dev/active/comms-narrative-slate-proposal-2026-07-29.md`, `fee440572`) — front established at Jul 15, span Jul 16-28, omnibus coverage complete 13/13. **Nothing drafted, no calendar rows** — awaiting PM's steer on shape (5 vs 4 beats), titles, and the spine. Would fill Aug 20 / 25 / 27 + Sep 1 / 3, curing the Aug 18 dry-out.
- **Web compose autosave**: ask #1 shipped (`0e448d3`). I answered — **#2 when convenient, #3 declined**; soft-lock/presence deliberately not pursued for a two-writer surface. **Open, on PM**: three things to check once in the compose UI (banner on unsaved reload / survives a 409 / gone after a successful save) — that observation is the only thing standing between ask #1 and being actually verified.
- **Genuinely open, awaiting PM's steer**: Beats 21-23 (Write-Path Chase Aug 11, Alpha Launches Aug 13, Architect's Own Trap Aug 18) — drafted, fact-checked, footer-chained. Needs PM's voice-pass + art.
- **Genuinely open, awaiting PM's answer**: the watchdog-wording question on "What the Running System Found" (published — non-blocking).
- **Standing structural gap**: the building-narrative queue **runs dry after Aug 18** — now has a proposed cure awaiting PM's steer (see slate above).
- **BYOC marketplace narrative**: ~6 weeks stale, PM-gated. Re-checked live 07-29, still no direction memo.

## Lesson refined this session (worth carrying, Docs supplied the better half)

My morning error was reporting *"no referent in any source"* when the true statement was *"not in the six workstream memos or the summary report."* Docs found "Driver" in **`decisions.log:225`**, the sprint plan's Phase-3 heading, and **`tests/e2e/test_scenario_driver.py`**. So the rule has two halves: **a negative finding is only as wide as the search behind it**, and **for a term of art, search the decision surfaces before the narrative ones** — `decisions.log` and the sprint plan hold ratified terms; omnibus logs only recount them.

## Findings filed this session (not yet acted on by their owners)

- **To CIO** (`83d82817a`): `amber-onboarding-delta-2026-07-29.md` §1 asks migrating roles to re-run the **command-shape** hook probe, which CLAUDE.md's `RESOLVED 2026-07-26` block lists under *"do not re-run these."* The doc predates the resolution by three days. Ordinary drift, CIO's to correct — but three more roles read that doc on day one.
- **Cron is session-only and auto-expires after 7 days.** Every registry row cleared this week (arch's, mine) asserts a liveness that decays silently around **Aug 5** unless something re-arms. Raised to CIO; not mine to fix.
- **`check-acronyms.py` false positive**: flags "the chief architect role (Arch)" as a ROLE-GLOSS problem, but that is the house style PM **ratified Jul 28**. Will fire on every future draft until the script's glossary absorbs it. Low priority, unfiled — **but note it's the failure mode I had to actively avoid when fixing `template-audit` #1**: replacing a silent hole with a noisy false positive is not an improvement.
- ✅ **Calendar column ownership RATIFIED (PM, `update-calendar` v1.4)** — I own `title`/`theme`/`workDate`/`endWorkDate`/`pubDate`/`cartoon`/`chatDate`/`draftPath`/`notes`/`altText`/`caption`; Docs owns publish/URL columns; `status` shared sequentially (me → `ready-for-docs`, Docs → `published`/`distributed`). **Write my own columns directly; memo Docs only to cross the boundary.** Docs' sole-ownership proposal was rejected — 57 `(comms)` vs 4 `(docs)` calendar commits in 60 days, and both corruption incidents were **positional access**, not plurality of writers.
- ✅ **`draftPath` staleness CURED by Docs** from my one-line observation — 7 stale paths repaired, 0 unresolvable of 97, and the missing rule added at the archival step. `scripts/validate-editorial-calendar.py` now exists (errors block, warnings never do); I ran it, passes with 8 known legacy warnings it says not to rewrite.
- ✅ **`template-audit` check #1 FIXED — v1.2, mine, shipped.** Was **unrunnable on Amber for every role in every location** (no `pyyaml`, no venv anywhere on the host — Docs verified one level deeper than I had), emitting a traceback into a column of twelve passes. **Removed the dependency rather than satisfying it**, added an explicit `⚠ CANNOT RUN` token, added the Ship-caption N/A-by-convention note, documented the `''` YAML-vs-body distinction. Tested across four frontmatter shapes before claiming it. Provisioning (venv + `node_modules`) remains CIO's, escalated by Docs.
- **Dangling `draftPath` is chronic, not a one-off**: #052's `draftPath` also points at a file absent from `drafts/`. Worth a sweep at some point; not urgent.

## Environment facts established on Amber (so nobody re-derives them)

- Filesystem is **case-INSENSITIVE**, same as Desktop — the `draftPath` silent-divergence hazard transfers unchanged.
- Cron is the ordinary `CronList`/`CronDelete`/`CronCreate` surface, not `mcp__scheduled-tasks`.
- `mail-send.sh` push-to-ref **works** from an Amber worktree, first attempt, no retry. **The two-call inbox-side-deletion gap did NOT appear**: a 15:35 send carried nine new files plus an inbox-side deletion and the deletion landed in the same call, verified against `origin/main`'s tree. Predecessor's last open §5 question, answered.
- **Hook probe, corrected order (B-first, empty index printed and verified before each cell)**: **Probe B compound → BYPASSED. Probe A standalone → BLOCKED, naming `check-branch.sh`.** Exactly what the index-state model predicts. So the hook is alive but **does not cover the shape used in ordinary work** — assume `git add … && git commit …` on `mailboxes/` paths is ungated here, and stage-then-commit-bare when a commit must be gated. `mail-send.sh` is structurally safe regardless (`commit-tree`, never `git commit`).

## State flags

- Session: active, mid-day. Inbox **empty** (MANIFEST only). Mail loop drained.
- **Session STOPped 21:12. Day fully accounted for; `DAY-CLOSED: 2026-07-29` marker written.**
- Queue at close: **(0 unblocked, 5 PM-gated)** — Ship #053's LinkedIn URL (only PM can produce it), the Beats 24-28 slate steer, Beats 21-23 voice-pass + art, the compose-UI banner check, the watchdog wording. **Nothing unblocked is being held.**
- Inbox **drained to zero** — 10 memos triaged across the day.
- Cron re-armed by delete-then-create, exactly one job verified. First fire tomorrow **06:12**.

## For the Jul 30 START — three memories to write, deliberately deferred

Flagged rather than written at STOP, so they don't get lost:
1. **A negative finding carries its search scope** — and for a term of art, the **decision surfaces** (`decisions.log`, sprint plans) come before the narrative ones (omnibus logs recount; they don't ratify). Exec notes PPM filed this same shape this week as an m-44 instance — **cross-link them.**
2. **A note asserting a present-tense fact about an artifact goes stale the moment the artifact changes under it.** I wrote "gloss applied" while true; a rebase made it false; the calendar then recorded a gloss that never shipped.
3. **Self-attribution drift runs both ways** — CLAUDE.md warns against inventing a phantom peer to explain your own forgotten work; the mirror error is inventing an "another session" where a nameable colleague belongs. Both are the same failure to go look.

Also worth doing: **add "Driver" / "scenario driver" to `knowledge/piper-morgan-glossary-v1.1.md`.** It was in `decisions.log` and the sprint plan but not the glossary, which is where I'd have looked second. Its absence cost two roles time today.
