# Methodology audit, 2026-11-03

**Audit period**: 2026-10-14 to 2026-11-03 (3 weeks)
**Previous audit**: 2026-10-14 (`dev/2026/10/14/methodology-audit-2026-10-14.md`)
**Trigger**: CIO standing item 8q's rule, "8 weeks, or within 2 weeks of a sprint gate closing, whichever is first". The MVP gate closed 10-30 (decisions.log 10-30 17:03, xian's GO on #1386), so this audit was due by 11-13. I missed that trigger at three STARTs (10-31 to 11-02) and caught it at the 11-03 START.
**Conducted by**: CIO (Claude Opus 5.5). Three Sonnet subagents (model set explicitly) gathered the evidence. CIO spot-checked each by a different method, and two of their claims didn't survive (see Method notes). Synthesis is CIO's.

---

## 1. Summary

1. **The R1 test passes for the classes R1 targeted, but not for scripts.**
   - By the CI checker (`scripts/check-concept-links.py`, `Concept:` lines only): hooks 16 of 16, skills 34 of 34 and workflows 25 of 25 are linked, against 1 of 14 hooks on 10-14. Git hooks are 2 of 4.
   - Scripts are **13 of 267**.
   - A hand-style recount of 176 chosen process mechanisms gives 46% linked and 16% with no concept, against 26% and 29% on 10-14. Strict (only `Concept:` lines count), it gives 40% and 17%.
   - Most of the gain is the 10-14 retrofit (`acf4387315`: Concept lines in every hook, plus the hooks registry), not new mechanisms arriving linked.
2. **New process scripts still arrive without a concept.**
   - Of 19 process mechanisms added since 10-14, 9 carry a `Concept:` line and 5 have no concept at all.
   - Those 5 are all added 10-16 or later: `registry-set.py`, `read_claim_inventory.py`, `read_staging_image_digest.py`, `check-last-verified-drift.py` and `check-move-refs.sh`.
   - My own `registry-plist-drift.py` (11-02) had no `Concept:` line either. It was fixed in this audit.
   - Cause: the checker ratchets hooks, git hooks, skills and workflows, but deliberately not `scripts/`, which mixes product and process helpers. R1's "every new mechanism" rule is enforced exactly where it was easy.
3. **The methodology catalog is mostly cited by its author.**
   - In 315 session logs, 10-14 to 11-03, counted strictly (two-digit `m-NN` or `methodology-NN`; logs by `grep -l`):
     - Only five docs are cited by any seat other than CIO: m-36, m-44, m-49, m-52 and m-45.
     - m-45 is the only doc cited by non-CIO seats alone (Comms, Docs).
     - m-46, m-48, m-50, m-53 and m-55 are cited by CIO only.
   - It's the shape that matters here, since the window is too short to compare sizes. The catalog is CIO's working vocabulary more than the cohort's.
   - CLAUDE.md and the hooks still cite no methodology doc.
4. **R3's coordination-cost gate failed.**
   - The post-R3 month (10-04 to 11-02) measured **5.7 coordination lines per product code line**, against a September baseline of 5.3 and a target of 2.65 or less, due today.
   - Product code is up 39% (109,605 lines against 78,855), so the floor holds.
   - Mail is 71% of coordination lines, at 444,666, and up 57% on September's 282,741. Heartbeats out of git (R3 step 1) worked, but mail volume grew faster than everything else.
   - This metric is CIO's (`r3-metric.md`: "Owner: CIO"). Nobody measured it until today.
5. **Guessed times remain the most widespread recurring shape.**
   - About 56 hits at 9 seats in the period, and two of today's were mine.
   - The stamp check blocks them in mail but only read log *headings*. It now warns on any `HH:Mx` in an added log line or tracker row (this audit; see R14).

**Verdict**: the period's direction is right. Rules became mechanisms, and the mechanisms are now documented where they run unattended (hooks, workflows). Two things haven't moved:
- the concept rule for scripts;
- the cost of coordination itself, which rose.

The catalog grew by two (m-56, m-57) but is read mostly by its author.

---

## 2. Mechanism-to-concept inventory

**Two measurements, which measure different things.**
- **(a) The CI checker** reads `Concept:` lines over every file in the classes: 346 mechanisms, 90 linked, 0 broken, 256 missing. 254 of the missing are in `scripts/`.
- **(b) A recount by the 10-14 method:** 176 mechanisms, with 105 of 288 `scripts/` entries chosen as process scripts and 15 of 25 workflows. "Doc names it" is automated (the path or name appears in a canonical root; a briefing hit needs 2 or more mentions). "Mechanism cites" counts a `Concept:` line or any existing doc path in the header.

| Class | n | Linked | Doc names only | Mech cites only | No concept |
|---|---|---|---|---|---|
| Claude Code hooks | 16 | 16 | 0 | 0 | 0 |
| Git hooks | 6 | 3 | 3 | 0 | 0 |
| Skills | 34 | 28 | 0 | 6 | 0 |
| Process scripts and plist | 105 | 19 | 55 | 3 | 28 |
| Process workflows | 15 | 15 | 0 | 0 | 0 |
| **Total** | **176** | **81 (46%)** | **58** | **9** | **28 (16%)** |

**10-14's test** was "linked above 26%, no-concept below 29%", and it passes on both counts. Strict, it's 39.8% and 16.5%; like-for-like without the new mechanisms, 40-45% and 15%.
- **Caveat:** the 10-14 list couldn't be reproduced (83 scripts then, 105 now), and the recount's "doc names it" is automated where 10-14 was a hand read. The direction is reliable; the exact percentages are not.

**Top no-concept mechanisms by risk** (enforce a ruling, or touch shared state):
1. `check-deploy-trigger-parity.sh`: gates `scope-guard.yml` and is named in `fly-deploy.yml`. CIO checked it: no `Concept:` line.
2. `approve-pr.sh`: approves as the reviewer account; no doc, no caller.
3. `trim-registry-history.py` and `registry-set.py`: both rewrite the duty-cycle registry.
4. `check-release-notes.sh`: no caller found (unverified whether it's orphaned).
5. `check-move-refs.sh`: added 10-31, after R1.

## 3. Methodology-core health

**Count**: 72 files, 58 numbered (m-00 to m-57). m-56 was added 10-14 (`517685c86f`, with R1) and m-57 on 10-31 (`1922057566`).

**Strict citation counts in period logs** (logs, then citing seats):
- m-44: 14 logs (cio, comms, lead)
- m-36: 9 (cio, exec, lead)
- m-49: 8 (cio, comms, exec)
- m-51: 8 (cio, lead)
- m-53: 8 (cio)
- m-48: 7 (cio)
- m-52: 6 (cio, host, lead)
- m-56: 5 (cio, comms)
- m-57: 5 (cio, lead)
- m-43: 3 (cio)
- m-46, m-50 and m-55: 3 each (cio)
- m-45: 2 (comms, docs)
- m-30, m-41 and m-00: 0 in the period. They are still cited by instruction surfaces (m-00 on 8).

**Verdicts, numbered files.** Following 10-14's rule (LIVE = cited in period logs and by an instruction surface), about 10 are LIVE: m-20, m-36, m-43, m-44, m-45, m-49, m-50, m-51, m-56 and m-57. m-20's one log is unverified as a use rather than a listing.
- 11 are log-only.
- 6 are surface-only (m-00, 25, 30, 35, 39 and 41). This is a new bucket, produced by the short window.
- About 19 are silent, and 12 are historical.
- The 3-week window turns "not cited lately" into "silent", so read the movers as quiet, not dead.

**The 12-09 review four** (m-51, m-55, m-56, m-57):
- m-51 has one independent author (Lead), and so do m-56 (Comms) and m-57 (Lead).
- **m-55 has CIO only**, across 3 logs and on no instruction surface.
- The rule "promotion waits for a second author's instance" still stands for m-55.

## 4. Period innovations, assessed

| Date | Innovation | Mechanism | Evidence since |
|---|---|---|---|
| 10-14 | Concept line (R1), hooks registry (R4) | `acf4387315`, `hooks-registry.md`, `check-concept-links.py` | Hooks 1 to 16 of 16 linked. Arch reviewed the registry 10-14 (`cc366b3e7c`). |
| 10-14 to 10-20 | Standing alpha promotion grant | `alpha-promotion-standing-grant.md` | The gate refused a red dispatch 10-16. Promotions ran routinely after. Worked. |
| 10-15 | `whats-armed.sh` at every CIO START | tick v1.54 | Ran every START; 0 NOT ARMED today. Worked. |
| 10-16 | OWED marker cohort-wide | `owed-scan.py`, tick v1.55 | Nothing ran the scan for 2 weeks: Exec had 66 unparsed. Repaired at v1.61 (each seat's START). Partial failure, repaired. |
| 10-16 | Stamp check | `stamp_check.py` in `mail-send.sh` | Blocks mail stamps. Logs kept guessed times (about 56 hits, 9 seats) because log mode read headings only. Widened 11-03. |
| 10-22 | Mail v4 canary moved into the first read | tick v1.58 | The remembered canary had decayed in every seat within days. The mechanism held. `mail4.py` has no unit tests. |
| 10-23 | Ship synthesis gate; kickoff state each fire | pre-commit hook, `ship-kickoff.sh` | The kickoff was dropped by a re-arm from memory (10-29), which led to v1.59 and v1.60's stored prompts and `seat-prompt.sh --check`. |
| 10-31 | m-57, an alarm needs a reader | methodology-57 | Cited by Lead independently. Applied 11-02 (the test-gate answer). |
| 11-01 | Sunset-or-renew inventory; class ratchet in lint | `97fb374e26` | Holds for its four classes; `scripts/` isn't ratcheted (finding 2). |
| 11-02 | Session crons retired; registry and plist drift check | tick v1.62 and v1.63, `registry-plist-drift.py` | Found 2 wrong rows, both fixed within the hour; 11 of 11 today. |
| 11-02 | Test gate keeps failing; the triage pile classified | Lead's pass `716481299c` | 25 to 0 triage the same evening. Measured 11-09 (row 9i). |

**Retired in the period:**
- `stuck-session-check.py`, the same day it was built (`edbfa3e75d`; Pard's alert replaced it)
- the old-history guard's sentinel loop
- the `context-usage-reminder` hook (`201af28db9`)
- the session-cron content (v1.62)

No rule was reverted.

**Recurring shapes, by keyword hits in logs (noisy upper bounds):**

| Shape | Seats | Hits | Methodology |
|---|---|---|---|
| Claim without opening the source | 11 | about 71 | m-44, m-52, m-43 |
| Guessed timestamp | 9 | about 56 | m-36, m-53 |
| Mechanical hygiene (untracked file, ruff after push, wrong folder) | 11 | about 35 | sign-off rules; none for the wrong-folder case |
| Search bounded by where I looked | cio, lead | about 22 | m-51 |
| Relayed fact ticked as verified | 5 | about 8 | m-50, m-52 |
| Scheduled step dropped after a re-arm | 4 | about 6 (high impact) | m-36, m-41; closed by v1.60 to v1.62 |

## 5. 10-14 recommendations, status

- **R1: done.** The 11-01 inventory ran on its date, and the class ratchet is in CI. But it doesn't cover scripts (finding 2).
- **R4: done.** Arch reviewed it 10-14 (`cc366b3e7c`). The subagent's "not evidenced" was wrong; CIO checked the commit.
- **R10: done.** Pard confirmed it 10-14 (the doc's status line). It was stale since 11-02 and was updated in this audit: all 11 seats on LaunchAgents, plus the drift check.
- **8r: done 10-27** (`role-duties-rerun-2026-10-27.md`).
- **R2, R3, R5 to R9, R11:** done 10-14; not re-verified.

## 6. Recommendations

**Done with this audit (CIO's own files, 11-03):**
- **R12.** `registry-plist-drift.py` gets its `Concept:` line (the duty-cycle-tick skill, which names it). Scripts linked: 12 to 13.
- **R13.** `liveness-current-state.md` brought to the LaunchAgent-only state (it said provisioning was "pending Pard").
- **R14.** `stamp_check.py --log-staged` now warns on an `HH:Mx` form in any added line of today's log and of a `dev/active/<role>-standing-items.md` or `-carry-forward.md`, not only headings. Two unit tests were added, and the 21 tests pass. The reader is the committing seat, at the moment it can fix the line (m-57).

**Routed:**

| # | Action | Owner | Why |
|---|---|---|---|
| R15 | Ratchet `scripts/`: fail a script with no `Concept:` line once the count rises above a ceiling (254 today), so only new scripts must carry one. A product script can name its ADR or issue doc. | Lead (lint is Lead's), CIO writes the change on a yes | Finding 2. The 5 unlinked new scripts show the class rule works only where it's enforced. |
| R16 | R3's gate failed (5.7 against 2.65 or less). Decide: accept the cost while product output is up 39%, or set a mail-volume measure before any change. My recommendation: measure memos per day and words per memo by seat for one week first. Don't cut anything on this number alone. xian's "we are not racing" (11-02) argues against a crash programme. | Exec with CIO, for xian's word | It's a gate xian's evaluation set. Only he retires or resets it. |
| R17 | When CIO names a pattern from another seat's incident, mail that seat the m-NN and the instance. | CIO | Finding 3. The catalog reaches seats only through CIO's logs. That's m-57's shape applied to methodology itself: a doc needs a reader. |

**Structural:**
- The next audit is due **by 2026-12-29** (8 weeks), or within 2 weeks of the next gate closing.
- The 12-09 review of m-51, m-55, m-56 and m-57 stands. m-55 needs a second author or a HISTORICAL banner then.
- Re-run R3 for 11-03 to 12-02 at the next audit.

## 7. Method notes (what the spot-checks changed)

- **m-03's "37 citations" were the piper-guards rule name "M-3"** (a single-digit match). The one strict "m-03" is the 10-14 audit's listing of the seven B3 docs. The same line produced the lone hits for m-01, 04, 13, 15, 17 and 21. So the B3 docs remain silent, and m-03, m-09 and m-01 aren't LIVE. CIO recounted with a strict two-digit regex.
- **R4 and R10 "not evidenced"** were wrong. The subagent grepped logs and mail; the evidence was a commit subject and the doc's own status line.
- The R3 result was checked independently. A direct `git log` gives 16,659 non-merge commits against the script's 16,579 (a window-boundary difference), plus the mail and MANIFEST line totals above.
- **Not measured:** whether citations are uses or listings (beyond m-03), and anything behavioural about the 28 no-concept scripts beyond their callers.

Verified how: `check-concept-links.py` (run 11-03, after R12: 90 of 346); `r3-coordination-baseline.py 2026-10-04 2026-11-02` (TOTAL 624,029 : 109,605 = 5.7); strict `grep -l` citation counts over 315 logs; `git log --diff-filter=A` for m-56 and m-57; `cc366b3e7c`'s subject; `pytest tests/unit/scripts/test_stamp_check.py` (21 passed, cached py3.11 venv). Layer: repo text, git history and unit tests. The concept checker is textual, not behavioural. Denominators are given in each section.
