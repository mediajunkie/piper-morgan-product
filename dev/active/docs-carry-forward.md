# Docs Carry-Forward

**Updated**: 2026-08-31 ~10:3x PDT (B3: 15/81 patterns dispositioned; mail loop drained twice)
**Session log**: `dev/2026/08/31/2026-08-31-0728-docs-code-log.md` (open).
**Cron**: `cfdd5f76`, `57 6,9,12,15,18,21 * * *`, healthy through ~09-06.

## B3 corpus-disposition — IN PROGRESS, 15/81 patterns dispositioned

Tracker: `docs/internal/architecture/reviews/2026-08-architectural-review/b3-patterns-disposition.md`
— all 81 patterns pre-tiered by citation-census evidence (Tier A: 8 CLAUDE.md/skill-cited · Tier B:
21 heavily-cited+recent · Tier D: 4 old+lowest-cited · Tier C: 48 middle-tier, needs individual reads).

**Done so far**: all 8 Tier A confirmed EFFECTIVE (light-touch — already load-bearing, no
supersession markers). All 4 Tier D dispositioned via grep-against-code (2 effective despite low
citation, 1 historical, 1 absorbed-into-successor). 3 Tier C patterns dispositioned the same way
(P-019 placeholder-instruction — effective, live in `conversational_floor.py`; P-058
ownership-graph — strongly effective, its exact NATIVE/FEDERATED/SYNTHETIC model is implemented
verbatim in `services/mux/ownership.py`, tied to ADR-045; P-018 configuration-access — principle
effective, illustrative sample code diverges from actual class names, a normal pattern-doc shape
not evidence of staleness).

**Real finding, shared with Arch+CIO, adopted as the standing B3 rule**: citation count alone
mispredicts effective/inert (3 of 4 Tier-D outcomes contradicted the count). Arch formalized it:
**citation census triages, live-code grep disposes** — codified for both corpora. Arch also named
the methodology-core equivalent for CIO (internalized-via-practice can look like low-citation too).

**Next**: ~66 patterns remain (13 more Tier B, 45 more Tier C) across subsequent fires — same
grep-against-code discipline for anything heading toward archive. Target ~1 week from kickoff.
**Disposition motion is absorb-and-mark** — each absorbed pattern gets marked into whichever of the
six living-core-docs it's absorbed into, same motion, not a separate pass.

## Today's other verified state (not assumed)

- **Weekly Docs Audit**: ⚠️ hadn't fired as of 10:31am PT (90 min past its `7 16 * * 1` / 9am PT
  schedule) — no workflow run at all today per `gh run list`. Same class of delay the workflow's
  own comment already documents once (top-of-hour GH Actions congestion, found 2026-08-03). Not
  yet alarming at 90 min, but check again next fire — if it's still absent, worth a closer look
  rather than assuming benign delay indefinitely.
- **Monthly Housekeeping Audit (#1486)**: checked directly — titled "2026-08", created 2026-08-05,
  **33 unchecked items, zero progress in 26 days**, not "due today." September's audit won't
  auto-generate until ~09-07, so no clutter risk from further delay. **Sequencing decision, stated
  not implied**: B3 is today's primary work (fresh, PM-approved, rest of cohort actively
  coordinating on it right now); #1486 picked up when B3 leaves room, or later this week — named
  here with the reason, not silently deferred.

## New standing responsibility: the glossary is now a living-core-doc

Per Arch's B2 workstream (`living-core-docs.md` v0.1, circulates with tomorrow's kickoff): six
docs now carry "current law" status — ESSENCE.md, SYSTEM.md (new), intent-routing-stack.md,
data-model.md, CONNECTORS.md (new), and **`knowledge/piper-morgan-glossary-v1.1.md` — mine**.
60-day staleness contract, needs CXO's tracked-state frontmatter (`last_updated`/`currency_claim`/
`max_age_days`) at first substantive touch — not urgent, current header is prose-only (v1.4, dated
2026-06-27). ESSENCE itself hit v1.0 RATIFIED today.

## ⚠️ PM's local main checkout has a genuine history divergence — PARKED, not resolved

4 local-only commits (`dc943cabb`, `e5f024bf8`, `ca460a4b8`, `87d068f8a`) blocking
`git pull --ff-only` in PM's own checkout (`/Users/xian/cool/piper`, aka
`Development/piper-morgan/piper-morgan-product`). A `diff origin/main..HEAD --stat` was pulled
(touches ~20+ files incl. CLAUDE.md, Dockerfile, workflows, skills — NOT obviously safe-to-discard
noise) but never reviewed for actual risk. **Do not act on this without PM present** — check in if
PM re-engages, don't resume unilaterally. (Also logged as a personal process lesson: I guessed at
the cause from a script's output and a suppressed git error several times before reading the
actual script/error directly — should have read primary sources first, per CLAUDE.md's own rule.)

## 2026-08-30, fully closed — see that day's session log for detail, not re-summarizing

"Two of Me" published + art-fixed + syndicated; calendar column-ownership corrected (multi-writer
by column, not Comms-sole); PM's 10-issue triage finished (#1455→B4, #1585/#1682 mostly already
resolved and re-documented, #1644/#1683 updated with evidence). All closed, nothing carries forward.

## Awaiting others (check periodically, don't re-derive)

- **#1584** (broken links, ~34 residual after the big 08-10/11 pass) — CIO's Part C
  (methodology-19 numbering drift) still open, his lane.
- **#1585** (6 genuinely-remaining low-priority items: 3 stale READMEs, 3 ambiguous duplicate-file
  pairs) — none urgent, description now accurate as of 2026-08-30.
- **#1682** (item 1, stray test file — Lead Dev's lane; item 3, CITATIONS.md staleness — explicitly
  no-urgency per the issue's own text). Item 2 fixed 2026-08-30.

## Owed by me — unblocked

- **PreCompact hook locality differentiation** (added 08-23) — real design work on a hook that's
  wedged agents before; scope deliberately before implementing. Full detail in
  `docs-standing-items.md`.
- **pmorgan.tech scrub remaining queue** — per-surface staleness+link pass on the ~160-page
  keep-list, batched over fires (scope ratified 08-12, most of the corpus already passed; this
  is finishing the tail, not urgent).

## Day-of-week duty triggers — CHECK EVERY START

- **Every Monday**: Weekly Docs Audit.
- **First Monday of month**: Monthly Housekeeping Audit (#1486).
- **Every Friday, EARLY**: omnibus logs Fri–Thu (the designed weekly catch-up).
- **First Tuesday**: Skill-Candidates Review — not mine (PM+Exec+CIO).
- **Not mine otherwise**: Role Health Check (4-weekly, HOST).

## Standing practice (added 08-27, applies at every fire, not just START)

A duty-cycle sync from earlier in the session is a timestamped fact, not a durable one. Before
reading file/git state to answer a PM question or start work, `git fetch` + fast-forward first if
meaningful time has passed. Fixed durably in `CLAUDE.md`'s "Never guess at facts" section.

## Mail-loop scan

```bash
python3 scripts/scan-inbox.py mailboxes/docs/inbox | grep -iE "to:\s*docs\b|to:.*,\s*docs\b"
```
Run every fire, not just START.

---

*Full history: prior versions of this file are in git log
(`git log -p -- dev/active/docs-carry-forward.md`) if ever needed verbatim; the durable record
lives in dated session logs and `docs/omnibus-logs/`.*
