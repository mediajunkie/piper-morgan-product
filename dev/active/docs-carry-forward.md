# Docs Carry-Forward

**Updated**: 2026-07-29 16:10 PDT (Fire 1, first duty-cycle fire on Amber)
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

- **⏳ LinkedIn URL for Weekly Ship #053** (PM syndicating). On arrival: `/update-calendar` → `status=distributed` + `liPubDate` + `linkedinURL`, then `publish-to-blog` **Step 9 archival** (draft → `published/`; Ship reuses `piper-ship.webp`, no image to archive). **The only thing gating archival.**
- **⏳ Puppeteer cache clear** — PM authorization needed, it's outside the repo: `rm -rf ~/.cache/puppeteer/chrome-headless-shell/mac_arm-139.0.7258.154` (check the sibling `chrome/` dir too). Not blocking — `npm ci --ignore-scripts` works.
- **⏳ Pre-Amber machine disposition** — decides whether Dispatch's 15 stashes are hygiene or a deadline. Raised to Dispatch + PM. **The stashes are NOT on Amber** (verified: 0 in main checkout + all 11 worktrees, no `refs/stash`, no stash reflog).
- **⏳ CIO scoping note for the CLAUDE.md refactor** — *carried from the 7/12 version, still the blocker.* See owed item 1.
- **⏳ CIO/Pard on provisioning** — 2 memos sent (Node gap; Python-too addendum). Nothing blocks on a reply.

## Owed by me — unblocked, priority order

1. **CLAUDE.md load-time/record separation — PM-GREENLIT ALREADY, and HOST has now done the measurement.** *This is the largest thing I hold.* The 7/12 carry-forward records it as PM-greenlit (HOST proposed, CIO acknowledged), **Docs executes**, blocked on a CIO scoping note. HOST's 7/28 Pass 3 supplies the analysis: hooks investigation = **6,923 bytes / 12.8% of CLAUDE.md**, proposal is ~800 bytes replacing ~6,900 (**~11% of the file recovered from one item**), pointer verified non-dangling, and HOST deliberately stayed off the edit because it's Docs' call. **4 of 8 absent norms still unadded** — HOST added the 2 safety-relevant ones and left the rest rather than make it 4 more insertions. Next move: check whether the CIO scoping note ever arrived, or whether HOST's Pass 3 supersedes the need for one.
2. **A `draftPath`-resolves check for the editorial calendar** — from Comms' Fire-1 finding. #052's `draftPath` doesn't resolve either; the Jul 12 pass fixed 22 instances and not the cause.
3. **Per-column semantic assertion for the calendar** — predecessor's unbuilt §4.4 item. **Same root as #2**: the calendar asserts facts about the filesystem and about column shape that nothing verifies. Build as one thing.
4. **Fold "`diff` the two draft copies" into `publish-to-blog` as an explicit step** — adopted as practice Fire 1; it caught a silent image drop only because Comms did it. Shouldn't depend on luck.
5. **methodology-20 — two refinements now**: (a) predecessor's line-vs-entry-count unit mismatch, flagged across 5 omnibus logs; (b) mine — the two HIGH-COMPLEXITY compression rules are **mutually unsatisfiable** (preserve-70-80% ⇒ 1.25–1.43×; ratio check demands >3×). Both raised to CIO as owner.
6. **`template-audit` check #1 should report `CANNOT RUN`, not traceback** — my ranked-first durable suggestion to CIO. Same shape as `HEARTBEAT-WRITER-SILENT` / `det_rc`. Would need CIO or me to own the edit.
7. **18 calendar↔website metadata disagreements**, incl. ~46 live-site captions missing quotation marks (calendar right, site wrong).
8. **97 docs >30d asserting current-state language**; `docs/internal/planning/current/` is itself now a misleading directory name.
9. **Weekly-audit orphan rate** — 2 of last 6 unexecuted; mitigated by the Mon–Thu SessionStart hook, cadence still worth review.
10. **docs/ tree audit + cleanup plan** — *carried from 7/12*, PM's direct request via PPM. Starting data: stale roadmap/README.md, `CORE/` an archival candidate. Write the audit + plan before any large-scale moves.

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
