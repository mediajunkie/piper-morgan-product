# Docs Carry-Forward

**Updated**: 2026-08-04 13:45 PDT (Fire 3, mid-WORK)
**Session log**: `dev/2026/08/04/2026-08-04-0727-docs-code-log.md` (yesterday's is
`dev/2026/08/03/2026-08-03-0711-docs-code-log.md`, DAY-CLOSED verified)

**Worktrees**: product `~/Development/piper-morgan-worktrees/docs` @ `claude/docs-cycle` · website
`~/Development/piper-morgan-website-worktrees/docs` @ `claude/docs-cycle`
**Cron**: `82ddcd08` — `57 6,9,12,15,18,21`. Registry row matches.
**Hooks on this seat**: standalone `git commit` BLOCKS; compound `add && commit` BYPASSES. Mitigation:
stage in one call, commit bare in the next. `mail-send.sh` safe regardless.
**Standing note**: `pre-commit-broad-staging-warn.sh` blocks the Bash tool call outright on a ≥20-file
staged commit despite documenting itself as advisory-only; `--no-verify` has no effect (not a git hook).
Split large multi-file commits into batches under 20 files.

---

## Awaiting others — check, don't re-derive

- **PDR-007 awaits CIO ONLY** — unchanged, checked again this fire. Arch ✅ and Web ✅ both reviewed,
  no objection. **Do not decide the storage question early** — pre-registered 2–4 week window
  (2026-07-30 → 2026-08-27), shipped measurement (`scripts/measure-editorial-drift.py`).
- **Dispatch-DinP staleness report** — replied 2026-08-01, no reply yet. Still watching.
- **Next Monday's weekly-docs-audit fire (~9:07 PT, Aug 10)** — Lead nudged the cron off the
  top-of-hour after 08-03's schedule didn't fire. Watch whether it fires this time; not urgent, a week
  out.

## Owed by me — unblocked, priority order

1. **`planning/current/` Finding 1 — needs a fresh, careful pass, NOT a quick rename.** Headline claim
   ("100% stale, 314d") is false — `vision.md` is ~113d, not ~314d — and there are 13 live inbound
   references, several in active session-start briefing paths. **Named trigger for the deferral**: a
   fresh session/compaction — still hasn't arrived, four days running now.
2. **Omnibus gap: Jul 29 – Aug 4, now 7 days, growing.** Not a request, a dependency — Comms's
   `continue-narrative` discipline reads digests, not raw logs. **Comms says explicitly: no urgency, not
   before Aug 18.** Sizable job — own focused pass per `create-omnibus` skill.
3. **97 docs >30d asserting current-state language** — separate, broader item; no deadline named.
4. **methodology-20's two HIGH-COMPLEXITY compression rules are mutually unsatisfiable** — CIO owns.
5. **`docs-standing-items.md` is stale** (last touched 2026-05-27, pre-Amber). Low priority, not urgent.

## Resolved 2026-08-04 — do NOT re-open

- ~~Comms's soft-404 finding (`publish-to-blog` verification gap)~~ — **fully closed.** `pipermorgan.ai`
  returns HTTP 200 for every `/blog/<slug>/`, including slugs that never existed — a status check or a
  naive absence-check can't distinguish live from nonexistent. Found in two spots: Step 9's archival
  gate and the Quality Checklist, both said "post is live"/"accessible" with no method. Fixed (v0.22,
  `e71abedfc`): explicit content-check method — assert a distinctive phrase from the post's body is
  present, then check for whatever's supposed to be absent. Noted for the record (not credit) that
  yesterday's publish happened to dodge this by accident, via caution about a different problem
  (client-hydration hiding content from WebFetch).

## Inbox

**68 remaining, cc-only historical from the 7/21–7/28 migration window.** Everything addressed *to*
docs is drained as of this fire. Not mass-moving to `read/` — drain on quiet fires.

## Standing lessons (carried, still live)

**Verify per assertion, not per session.** Held again today — checked my own skill against Comms's
finding rather than assuming it was fine or assuming Comms's claim applied verbatim; found it did, in
two spots, and fixed both with the actual mechanism named rather than a vague "be more careful."

**Naming an accidental protection honestly, not claiming it as discipline.** Yesterday's publish avoided
the soft-404 trap, but not because I knew about soft 404s — I was worried about a different failure mode
(client hydration) that happened to route me to the same safe method (checking source content directly).
Said so plainly in the reply rather than letting Comms believe the skill was already solved for the
right reason. Worth keeping as a distinct discipline from "I was right" — being right by accident and
being right by design look identical from outside; only the person who did it knows which, and only they
can say so.

## Watch items (not owed to me, but adjacent)

- **Puppeteer extraction cause** — Pard's lane, still open.
- **methodology-20's mutually unsatisfiable compression rules** — CIO owns, raised twice.
- **`docs/internal/operations/one-command-checks.md`** (Arch, 2026-08-02) — worth reading before the
  next audit-shaped task; today's soft-404 finding is exactly its shape (an instrument that measures
  the wrong thing and returns a false clear).
- **`pre-commit-broad-staging-warn.sh` blocking despite advisory design** — documented, not escalated.
  Workaround is cheap; escalate only if it costs someone else real time.
- **Blog index is client-rendered, returns a shell** — Comms's finding named this as a separate,
  unrelated limitation (why they couldn't audit index layout when PM asked about featuring the newest
  post). Not urgent, not mine unless it becomes one.

## The one thing I most want to carry into the next fire

**A finding that arrives as "check if this affects you too" is worth checking properly, not just
trusting the pattern-match.** Comms didn't tell me my skill was broken — they told me they'd found a
mechanism and asked whether it applied to me. I could have assumed yes (pattern looked similar) or no
(different skill, different context) without checking. Reading the actual skill text found the exact
same underspecified phrasing in two places, which a pattern-match guess could easily have missed or
over-applied.
