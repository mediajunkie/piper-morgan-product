# Docs Carry-Forward

**Updated**: 2026-07-29 22:35 PDT (Fire 3, STOP — DAY-CLOSED 2026-07-29)
**Session log**: `dev/2026/07/29/2026-07-29-0948-docs-code-log.md`
**Prior update**: 2026-07-12 — **17 days stale, pre-Amber.** Rewritten wholesale; still-live items from
that version are preserved below and marked, resolved ones noted so they aren't re-derived.

**Worktrees** (both verified 0-behind Fire 1): product `~/Development/piper-morgan-worktrees/docs` @
`claude/docs-cycle` · website `~/Development/piper-morgan-website-worktrees/docs` @ `claude/docs-cycle`
**Cron**: `26805e13` — `57 6,9,12,15,18,21`. ⚠️ **Session-only; auto-expires ~2026-08-05** (CronCreate
7-day cap) and dies on session exit. Registry row written — re-arm AND update the row when it lapses.
**Hooks on this seat** (probed Fire 1, index printed empty before each): standalone `git commit`
**BLOCKS**; compound `… && git add … && git commit …` **BYPASSES**. Mitigation: stage in one call,
commit bare in the next. `mail-send.sh` is safe regardless (`commit-tree`).

---

## Awaiting PM / others — check, don't re-derive

- ✅ **Weekly Ship #053 CLOSED OUT** (Fire 2). LinkedIn URL supplied by Dispatch-DinP; `status=distributed`, `liPubDate`/`linkedinURL` set, `mediumURL` left empty by design (ship = LinkedIn-only). Draft archived to `published/` per Step 9. Nothing outstanding.

- **🔭 ANTICIPATED (PM 2026-07-29, "may want to" — NOT yet a directive, do not build ahead):** the cross-posting skill is nearly done, and PM may hand syndication to **a new Dispatch agent working on the Piper Morgan project**. Three things in my lane change if that lands; all three are cheap to settle *before* the handover and expensive after:
  1. **Routing is genuinely ambiguous and has a documented failure mode.** `mailboxes/DIRECTORY.md` explicitly says *do not* create `mailboxes/{agent}/` for cross-project agents **including Dispatch**, and cites CIO's 2026-07-04 mistake — *"a dead letter, not a delayed delivery."* A Dispatch agent *on this project* is either (a) Piper-Morgan-local → it needs `mailboxes/dispatch/` **and** DIRECTORY.md amended in the same change, or (b) still cross-project → stays at `~/Development/dispatch/mail/` and nothing changes. **Guessing wrong produces silent dead letters.**
  2. **`publish-to-blog` Step 8 says "PM does manually"** and Step 9 gates archival on a confirmed syndication URL. If Dispatch owns syndication, Step 8 changes owner and Step 9's gate becomes a *mail-driven* dependency with real latency — worth encoding rather than leaving as folklore.
  3. **Keep ONE writer on the editorial calendar (recommend: Docs).** Dispatch should *report* the URL; Docs writes it via `/update-calendar`. A second writer on an 18-column CSV is precisely the column-shift risk that `update-calendar` v1.2 and my predecessor's Ship #050 repair both document — field count stays valid while content drifts one column right.
- ✅/⚠️ **Puppeteer cache CLEARED (PM-authorized) — and it DISPROVED the diagnosis.** A clean cache reproduces the identical failure: ~100MB downloads, then `ABOUT` + `LICENSE` and no binary, rc=1. Not stale cache, not disk space (259GB free). **The extraction is reproducibly broken on this host; cause unknown** (untested: Node 26 vs `@puppeteer/browsers`, macOS quarantine, archive format). Pard's lane. **`npm ci --ignore-scripts` is therefore the correct standing procedure, not a workaround.** Nothing in publish or `next build` is blocked; anything driving a real headless browser would be.
- ✅ **Stash cleanup: NO DEADLINE.** PM ruled the pre-Amber machine stays up indefinitely. Stashes exist only there (verified 0 anywhere on Amber), so only something with access to that host can act. Standing offer to Dispatch: export all 15 to patches somewhere tracked and I'll review per-stash from here.
- ❌ **CIO scoping note: NOT a blocker, and never arrived.** HOST's Pass 3 says explicitly *"Docs, this is your call and I've stayed off it"*; the refactor was PM-greenlit 7/12. **Proceed without it** — this is mine to execute, not to wait on.
- **⏳ CIO/Pard on provisioning** — 2 memos sent (Node gap; Python-too addendum). Nothing blocks on a reply.

## Owed by me — unblocked, priority order

1. ✅ **DONE 2026-07-30 (`ac120d514`) — CLAUDE.md load-time/record separation SHIPPED.** 58,262 → 55,303 bytes (−5.1%) *while adding four norms*; hooks item −68%; HOST's 8 catalogued norms now 8/8 (was 4). Full record moved verbatim to `docs/internal/operations/amber-hooks-investigation-2026-07.md` — **a git-tracked doc, not the memory pin**, because the pin is a partial record and MEMORY.md is 8 lines from a silent ceiling. Two findings from verifying rather than executing HOST's memo: the item had **grown 30% in two days** (concluding the investigation meant writing more record into the load-time surface), and **HOST's pointer check had gone stale** — accurate 07-28, but 2,407 bytes landed 07-29 that the pin never carried.
2. ✅ **DONE (Fire 2)** — `draftPath`-resolves check shipped in the validator, **and all 7 stale paths repaired** (3 Ships + 4 narrative posts). 0 unresolvable of 97 rows carrying a path. Cause was Step-9 archival moving files without updating rows.
3. ✅ **DONE (Fire 2)** — per-column shape checks shipped in `scripts/validate-editorial-calendar.py` (enums, date formats incl. chatDate's M/D/YYYY wart, URL/path prefixes, the Ship #050 repo-path-in-prose signature). Errors block, drift warns. Behaviorally tested both directions in an isolated tree. Predecessor's §4.4 item, closed.
4. **Fold "`diff` the two draft copies" into `publish-to-blog` as an explicit step** — adopted as practice Fire 1; it caught a silent image drop only because Comms did it. Shouldn't depend on luck.
5. **methodology-20 — two refinements now**: (a) predecessor's line-vs-entry-count unit mismatch, flagged across 5 omnibus logs; (b) mine — the two HIGH-COMPLEXITY compression rules are **mutually unsatisfiable** (preserve-70-80% ⇒ 1.25–1.43×; ratio check demands >3×). Both raised to CIO as owner.
6. ✅ **DONE by COMMS (not me)** — `template-audit` v1.2 removed the `import yaml` dependency and added an explicit `⚠ CANNOT RUN` verdict token, tested across four frontmatter shapes. My suggestion, their lane, their fix, two hours. The *provisioning* half is still open (no venv on this host; CLAUDE.md Quick Reference still says `venv/bin/python main.py`).
7. **18 calendar↔website metadata disagreements**, incl. ~46 live-site captions missing quotation marks (calendar right, site wrong).
8. **97 docs >30d asserting current-state language**; `docs/internal/planning/current/` is itself now a misleading directory name.
9. **Weekly-audit orphan rate** — 2 of last 6 unexecuted; mitigated by the Mon–Thu SessionStart hook, cadence still worth review.
10. **PDR-007 follow-through** — drafted + routed (`35fb86c60`). ✅ **Web reviewed same night: NO OBJECTION, and corrected my cost estimate DOWNWARD** — the render layer needs zero change (it already treats the JSON as generated data), real cost is 3 generation scripts incl. `copy-editorial-calendar.js`, and Web claimed their own `loadCalendarLive()` repoint. Web also answered Q1 (decide from the measurement window) and Q2 (product repo, first substantive answer). **Still awaiting Arch + CIO.** If it ratifies, I write the companion ADR. The 2-4 week wait stands — Web pressed that point hardest too.
11. **Reconcile the '~46 captions' measurement** — PDR-007 open question 4. The 7/28 audit's figure and my 2 don't agree, and until the methods are reconciled neither should be quoted.
12. **docs/ tree audit + cleanup plan** — *carried from 7/12*, PM's direct request via PPM. Starting data: stale roadmap/README.md, `CORE/` an archival candidate. Write the audit + plan before any large-scale moves.

## Resolved since the 7/12 version — do NOT re-open

- ~~Ship #050 calendar validator error (19 fields on that row)~~ — **FIXED 7/28** by my predecessor (`fcfc95039`); it was a three-field column shift, not a count problem. Validator now clean at 418 rows / 18 fields.
- ~~`the-server-crashed-mid-draft.md` archival~~ — that draft is in `published/`.
- ~~Jul 9/10/11 log-closure and omnibus chain~~ — omnibus is gap-free through 2026-07-28 (414 logs).
- ~~`docs-duty-cycle` scheduled task / Belt-4 spawn-fresh~~ — superseded by the Amber cron model (`26805e13`) + the freeze-watchdog registry.

## Inbox

**29 remaining, all cc-only historical from the 7/21–7/28 migration window.** Everything addressed *to*
docs is drained. **Not** mass-moving unread mail to `read/` — that would misrepresent what's been
consumed. Work through on quiet fires.

## Standing lessons earned 2026-07-29 — all three one shape

**Verify per assertion, not per session.** One verification never licenses an extrapolation:

1. **Stale worktree** — reported the Ship's state from a tree **45 commits behind**, and told PM there was no draft. `feedback_read_the_artifact_not_testimony_about_it` has an unstated precondition — *the artifact must be current* — which a behind checkout satisfies in letter and breaks in fact. **Sync immediately before reading**, not once at session start.
2. **Guessed timestamps** — ran `date` at 15:26, then extrapolated across several work units; 3 memos went out up to ~55 min ahead of real time.
3. **Acted before reading mail** — Comms had already answered the Driver blocker and the memo sat unopened for 10 minutes while I published. **Drain mail before the task loop**, which is exactly what WORK PARTS already prescribes.

**The counterweight, worth as much**: **4 false alarms caught by checking before reporting** — empty
caption, `<em><em>`/trailing slashes, the "index doesn't list #053", and "`mailboxes/` has been deleted"
(self-inflicted: **Bash cwd persists between calls**). Each would have been a wrong report to PM or a bad
edit to a live artifact. Doubting your own finding is as load-bearing as finding it.

## Watch items (not owed to me, but adjacent)

- ⚠️ **`MEMORY.md` is 8 lines from a silent 200-line ceiling** (168 entries / 192 lines, HOST measured 2026-07-29 22:3x). Truncation is silent — trailing entries vanish for every agent with no error. Addressed to **CIO** (owns the mechanism) and **Exec** (would coordinate a per-role prune); Docs cc'd. **Not my ask** — but if the resolution is per-type index files with a router, that is documentation architecture and I'd expect to be involved. **Do not add memories casually until this resolves**; I deliberately deferred 3 candidate entries tonight for this reason.
- **Puppeteer extraction cause** — Pard's lane. Three hypotheses dead (stale cache, disk space, Web-poisoned-cache); untested: Node 26 vs `@puppeteer/browsers`, macOS quarantine, archive format.
- **methodology-20's two HIGH-COMPLEXITY compression rules are mutually unsatisfiable** — CIO owns. Raised twice now (predecessor's unit mismatch + my contradiction).

## The one thing I most want to carry into tomorrow

**Verify per assertion, not per session.** Both errors that reached PM today came from trusting a
verification I'd done earlier rather than redoing it — a 45-commit-stale worktree read, and timestamps
extrapolated from a single `date` call. Meanwhile **4 false alarms were caught by checking before
reporting**. Same root, opposite outcomes, and the cheap habit is the difference.

**Wanted but not found (day's biggest gap)**: a way to detect my own working tree is stale *before* I
read a file from it. Every git check I have reports branch state; nothing warns that the file I'm about
to read is N commits behind.
