# CXO carry-forward — ephemeral session state

**Owner**: CXO | **Updated**: 2026-07-31 22:4x PT (STOP)
**Read at**: every fire START. **Rewritten at**: the end of every substantive fire.
**Durable owed/queued work lives in** `cxo-standing-items.md` — this file is *current* state only.

---

## ⏸ Blocked on PM — one action clears four lanes

**Amber key provisioning** (via `KeychainService`, **not** the `security` CLI — the service appends
`_api_key` and CLI-stored credentials are invisible to the app). Unresolved all of 07-31.

| Blocked | Consequence |
|---|---|
| **Probe A** (PA built it; PM funded it) | **My rubric-branch verdict.** Design spec §6 stays unresolved and acceptance item 4 stays un-implementable. |
| **#1386 criterion 2** | Withheld my sign-off; a keyless canonical suite *skips* and reports green. Exec deferred it in writing. |
| **#1445** · **#1395 Phase 0** | Lead's. |

**Second PM action, separate**: rouse Lead / authorize Lead's cron. **Lead's registry row is still
parked and no cron was ever armed** — the #1386 Scenario-B driver could never have started. Exec's
own finding.

**Scenario B may be entirely unaffected** (deployed beta v28, its own credentials). If Lead runs it,
**review and sign on the issue at the next fire** — independent of criterion 2.

## Live threads

| Thread | State | Next |
|---|---|---|
| **Jake FTUX** | 4 lenses in; Exec synthesis done and framed for the **PM + CXO** decision; artifact carries my positions. | **PM is working through it with me.** Hold — don't generate more input. |
| **First-contact design spec** | `dev/active/design-spec-first-contact-plugin-surface-2026-07-31.md` — **v0.2**. PPM reviewed inside 3h; gate/spec split adopted (7a vs 7b). | Awaiting **Lead** (buildability + the latency number I left blank), **PA** (Probe-A coupling), **Arch** (structured-confidence as a format constraint before Phase 2). |
| **PDR-006 / #1462** | **RATIFIED** 07-31. My 3 design implications are live work; rubric branch is a pre-user gate. | Spec review responses; then item (ii) capability legibility and (iii) the "colleague model" naming. |
| **#1174 / L4 re-scope** | ⚠️ **Still owed by me** — deferred from 07-30 STOP and not done 07-31. Title/body clarification only; **Production is the correct milestone, nothing to undo.** | Do it early, when the board is quiet. Then the discovery — mine, with HOST on welfare/trust. |
| **PDR-004 Amendment A** · **m-46** | Both filed. m-46 now **EMERGING** (limb 2 mechanized; limb 1 still vigilance). | PPM + PM ratify the amendment; CIO owns m-46 numbering. |
| **Ship #054** | **Filed 07-31**, a day inside the deadline. | Nothing. |

## ⚠️ Owed and carried four days — do this before the next substantive design call

**`docs/briefing/BRIEFING-ESSENTIAL-CXO.md` has not been opened since arriving on Amber**, along with
`ROLE-PORTFOLIO-CXO.md` §3–5. Named in three consecutive session logs. Also: **the D2 design-system
portfolio (#1286/#1290/#1284/#1269) has not moved for two Ship windows** — flagged to PM in Ship #054
§6 as a decision to make rather than a drift to continue.

## Position stated in advance so it can't be retrofitted

**Probe A**: hedges survive → the branch scores our text, R/C/T mostly ports. **Hedges don't survive →
the finding is NOT rubric-shaped**; it's an **output-format constraint** (structured confidence the
client can't paraphrase away). That's a constraint on tools nobody has written — which is why it's
Phase 0, and why spec item 4 must not be implemented in prose first.

## Environment notes for this seat

- **Sync before reading mail.** 07-29: 271 behind, inbox read *empty*, two real asks invisible.
- **Check the clock before dispatching STOP** — compute the next fire; STOP only if its *date* differs.
  On 07-31 I nearly day-closed three hours early off the cadence alone.
- **`cd` persists across Bash calls** — twice produced false-empty reads. Absolute paths.
- **Hooks**: real `pre-commit` in the common dir; **verify existence, don't probe** (v1.22).
- **Closure is a property of the DAY, not the FILE.**
- **macOS bash 3.2** — no `declare -A`; use temp files.
- **`bash scripts/check-derived-drift.sh`** — read-only, cheap; run when touching a generated artifact.

## Cron

- **Job `49d605be`** — `47 6,9,12,15,18,21`. Re-armed at STOP 07-31 by delete-then-create
  (`6415bf73` → `49d605be`). **Cadence unchanged**; prompt gained the check-the-clock reminder.
  *(Recording the id transition deliberately — a changed cron id is a documented cause of
  phantom-peer misreads.)*
- ⚠️ **Session-only AND auto-expires ~2026-08-07.** Both deaths silent. **Run `CronList` at every
  START** — this file records intent, not a live job.
