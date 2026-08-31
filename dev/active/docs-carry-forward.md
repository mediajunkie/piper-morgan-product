# Docs Carry-Forward

**Updated**: 2026-08-31 ~13:4x PDT (a very high-volume fire — #1708 verified+SETUP.md fixed,
scheduled-workflow defect found+filed+worked around, standing-items dated, B3 at 15/81)
**Session log**: `dev/2026/08/31/2026-08-31-0728-docs-code-log.md` (open).
**Cron**: `cfdd5f76`, `57 6,9,12,15,18,21 * * *`, healthy through ~09-06.

## ⭐ Weekly Docs Audit (#1712) — GENERATED, real work owed, deliberately deferred to a fresh fire

Found a real infrastructure defect: neither of this repo's two Monday-scheduled GH Actions
(weekly-docs-audit, monthly-housekeeping-audit) fired on schedule today — 4.5 hours late, zero
runs, while `push`-triggered workflows fired normally throughout (ruling out a general Actions
outage). Filed **#1713** with the full evidence trail. Manually dispatched `weekly-docs-audit.yml`
to unblock myself — succeeded immediately, produced **#1712** (today's real audit, 74 unchecked
items). Did NOT manually dispatch the monthly one, since #1486 (last month's) is still open and a
second one would compound rather than close a gap — left that call to whoever owns #1486.

**#1712 itself is genuinely deferred, not avoided**: 74 items is comparable to prior weeks' full
audits (#1643, #1681), and this fire has already delivered a lot of real, verified work — picking
it up fresh next fire is quality-banking against an explicit trigger (checklist-scale work
deserves undivided attention), not the "no rush" antipattern. Named here so it isn't silently
dropped.

## #1708 (ALPHA_QUICKSTART hosted-primary) — MY SHARE DONE, verified independently

PM blessed the plan in-conversation; PPM landed the main rewrite (`013d5a0cd`) while I was
mid-heads-up-memo — a genuine same-fire race, no actual collision (caught before I'd touched any
file). **Verified PPM's landed work independently rather than trust the summary**: confirmed
`piper-morgan.fly.dev` responds live, confirmed the 4 remaining "production" mentions are all
contextual/explanatory not instructional, read `CONTRIBUTING.md`'s new §1b against Lead's probe
report line-by-line — clean match.

**Picked up the flagged residual PPM couldn't finish**: `SETUP.md` had 3 real defects Lead's probe
found (nonexistent `config/PIPER.example.md` path, wrong psql port/user for the Docker path, wrong
server entry point `uvicorn web.app:app` instead of `main.py`) — verified each claim independently
against the actual codebase before fixing (didn't just trust Lead's memo), then fixed all 3 plus
their echoes elsewhere in the same doc (Python version claim, Quick Reference table, Troubleshooting
section) rather than just the first instance of each. Flagged the SETUP.md/CONTRIBUTING.md overlap
honestly at the top of the doc rather than unilaterally consolidate — real decision, not mine alone.
**Not touched**: `ALPHA_TESTING_GUIDE.md` (PPM's other flagged residual) — more entangled, deserves
its own pass rather than a rushed one riding this fire.

## B3 corpus-disposition — IN PROGRESS, 15/81 patterns dispositioned

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

## Monthly Housekeeping Audit (#1486) — still deliberately sequenced behind B3

Checked directly earlier today: titled "2026-08", created 2026-08-05, 33 unchecked items, zero
progress in 26 days, not "due today." September's won't auto-generate until ~09-07 (and given
today's scheduled-workflow defect, may need a manual dispatch when the time comes too — watch for
it). B3 + #1712 both take priority; #1486 picked up when they leave room, or later this week.

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
