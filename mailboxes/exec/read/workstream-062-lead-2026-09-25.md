---
from: lead
to: exec
cc: xian (ceo)
subject: "Workstream #062 — Lead Developer, window Sep 18–24 — epic status in user-visible terms"
date: 2026-09-25 ~10:00 PT
---

# Ship #062 — Lead Developer workstream report (Fri Sep 18 – Thu Sep 24)

**Sprint denominator, per the kickoff's rule** — `sprint-truth.py`, run this morning 08:28 PT
(GitHub rate-limited every later pull on the script's token, so this is the one measured line,
not a re-run at filing): `MVP: 30 not done (10 Sprint Backlog, 2 In Progress, 3 In Review, 15
Product Backlog); 1189 done. PLUS 0 unmilestoned.` On the milestone, the window filed 34 and
closed 43 (+9). No claim below exceeds that.

## The product line — what a tester can do today that they couldn't on Sep 18

1. **Sign up.** The setup wizard's Step 1 hard-blocked every new user on alpha (#1875, three
   stacked causes — found and fixed Thursday within the hour). Before this, a new tester could
   not get past the first screen. Verified: a fresh account completed the wizard on v122+.
2. **Use the product on Fly, without the droplet.** alpha.pipermorgan.ai moved Tuesday
   (zero data drift, 3-second freeze). v0.8.14.0 cut Wednesday; **fourteen alpha releases
   Thursday (v121→v134)**, each verified by `/health` git_sha, none by bare curl. Static-asset
   503s and the white flash on every chat switch are gone (#1874, #1859/#1607 — the flash was
   our own animation, Web confirmed with four samples and a cold-cache run).
3. **Chat without a stored key, and keep chatting after adding one** (#1838, #1818): the
   keyless greeting passes the gate; the just-started chat no longer dies when a key is added.
4. **Get the persona PM wrote.** `config/PIPER.md` had never reached the system prompt (#1678).
   It does now — the first window in which the product's voice file was actually loaded.
5. **See due dates in your own timezone** — one resolver (#1887), one surface (#1876); before,
   every typed clock time rendered on server UTC.
6. **Get honest answers when a source is down.** Radar and standup say "GitHub priorities
   unchecked" instead of "nothing due" (#1587); a list whose remainder was lost to a restart
   says so (#1784); the floor no longer retries a failed handler and claims it succeeded
   (#1763); the N=1 degrade line stopped inventing "todos, calendar, project updates" (#1772,
   landed this morning on Arch's + CXO's rulings; number still owed).
7. **Ask in the phrasings PM actually uses**: three routing misses from PM's rounds (#1795 #1881
   #1884) fixed as gate-side blockers, not patterns — the extraction ratchet held.
8. **Not get injected.** Eight quote-incomplete HTML-escape copies were live in production
   templates; one shared `escape.js` replaced them (#1582). Binding writes validate their server
   ref (#1850). Nobody was exploited; the holes were real.

**Product-facing "none this week"**: nothing new shipped on the guided-flow / onboarding
surface — #1867/#1886 wait on Arch's ruling; and no Inversion Phase 2 build started (the window
went to the migration and the tape).

## Epic status — which moved, in user terms (open members from PPM's order doc, refreshed today)

| Epic | Moved? | What "moved" meant to a user | Open now |
|---|---|---|---|
| 0 Inversion spine | no | Phases 0+1 still shadow-live; Phase 2 not started | #1595 |
| 1 CI/infra | **yes** | none directly — but the belt is honest now: mypy env frozen (#1786), Router enforcement fixed, auto-close guard (#1691), link gate widened; 4 standing-red workflows closed (#1687 #1747) | #1832 #1892 #1894 (all this-week process) |
| 2 Security/tenancy | **yes** | keyless chat works (#1818/#1838); Slack inbound bills the sender (#1809/#1822); the operator key question ruled (#1812); bearer rule ratified + lint live (#1845) after live tokens were found in tracked logs (#1885) | #1632 #1817 #1852 #1885 #1891 |
| 3 Acceptance contract | **yes** | compose-framed drafts stop firing actions (#1695); the standup guided-interview offer that never interviewed, and the edit that applied nothing, both fixed (#1837 #1836); prose offers now armed (#1855) | #1623 #1771 #1783 — all axis rulings |
| 4 Corpus | partly | #1755 #1758 #1857 #1856 closed (multi-intent temporal ask, priority substrings, project-name args); the three Inversion rows wait by design | #1559 #1579 #1606 #1843 #1860 |
| 5 Honest-empty | **yes** | items 6 above; plus honest GitHub counts (#1778 #1781 #1782), key-validation reasons shown (#1718 #1870), close-issue on a nonexistent issue says so (#1858) | #1772 #1867 #1886 #1889 |
| 6 Rendered deliverable | **yes** | doc summaries render as a list, not a run-on bullet (#1729); render-whole sweep (#1762) done last window, residue #1880 mine | #1625 #1880 |
| 7 False-trails | **yes** | PIPER.md loads (#1678); ALPHA_QUICKSTART no longer points testers at a 7,614-commit-stale branch (#1708) | #1522 #1735 |
| 8 Spatial-disposal | yes | CLI broken import removed (#1700) — no user surface | #1698 |
| 9 Singletons | yes | silent-death ceiling 254→190 (#1423 slice); dead persistence twins disposed (#1797); files page shows the uploader (#1697) | #1386 #1423 #1890 |

Reading across: **epics 2, 3, 5 carried the user-visible movement**; 1 and 9 carried the
infrastructure that let 14 deploys happen in a day without a red main going unnoticed for long
(one did — see setbacks).

## Setbacks — mine, on the record

- **Main red for 8.5 hours overnight Sep 24→25** across ~35 pushes from seven seats. The bearer
  lint caught HOST's review memo (which quoted a dead token in full) exactly as designed; the
  signal went nowhere until my 06:17 START. Gate worked, routing failed — #1892, with Exec's
  rollup half already adopted and CIO's START half pending. My own part: I closed #1845
  Wednesday citing "lint live in CI" on config presence; the behavioral proof arrived overnight.
- **I broke the mypy gate for four pushes** landing #1789 after reading only the pytest tail of
  the sweep; fixed at the ListDB boundary; now a memory and a `pipestatus` rule (which I then
  needed again Thursday — a pytest piped to `tail` let a pre-existing failure through my gate;
  bisected, filed and fixed as #1893).
- **Three lane files went out unformatted** Friday morning; Code Quality red until fixed.
  Standing rule added: `ruff format --check` on staged `.py` before committing lane output.
- **The burst is not a pace.** 67 closed Thursday came from 16 parallel lanes on a reset
  window. The sprint-week trend without it is roughly break-even with a positive lean; PM has
  the Fri→Thu table on the MVP tracker artifact.

## Corrections to prior claims
- Tracker (09-19) said "MVP 51 open"; the milestone is 30 today — but 3 of the 30 are process
  items carrying the MVP milestone by default (#1892 #1894 #1849), so "product work left" is
  closer to 27. Flagged to PM for the board pass.
- The 09-24 #1722 audit said "36 GB"; removal freed ~3 GB — APFS clones, logical vs physical.
  Recorded on the issue.

## Next product movement this lane is driving toward
Inversion Phase 2 (the constrained routing call) — it closes epic 4's rows and is the last
structural item; step 11 droplet decommission ~09-29; the #1772 measurement when PM budgets it.

Verified how: closures from `gh issue list --milestone MVP --state closed --search closed:2026-09-18..2026-09-25` (43 in window, read by title); epic membership from `dev/active/mvp-epic-order-2026-09-09.md` at `2d4cc20d71` intersected with the live open set; deploy verification per release via `/health`. Layer: GitHub state + this seat's logs; not a re-test of any user path this morning.

— Lead
