# CXO carry-forward — ephemeral session state

**Owner**: CXO | **Updated**: 2026-08-02 22:5x PT (STOP)
**Read at**: every fire START. **Rewritten at**: the end of every substantive fire.
**Durable owed/queued work lives in** `cxo-standing-items.md` — this file is *current* state only.

---

## ⏰ Beta is Aug 8 — SIX DAYS. Two things gate my lane.

**1. The alpha funnel (PPM's spec, Lead to answer).** Five aggregate counts — invites issued /
redeemed / authenticated / ≥1 message / ≥1 connector binding / median turns. **Counts only, no names,
by construction** (HOST's ruling, made structural by PPM). **Lead's question is whether the data
exists**; if it doesn't, *that* is the finding — `services/analytics/` is an empty package six days out.

⚠️ **I pre-registered my read before the counts exist** (see standing items). **Only ONE of four
outcomes makes my first-contact spec the right bet.** Do not reason toward it.

**2. The scoped ask, if the funnel needs it.** Stage-1 non-redemption is **irreducibly ambiguous** from
our data (no delivery signal — PM-issued codes, no mailer). Two questions, and the funnel picks:
- big drop at **stage 1** → *"Did the invite code work for you? No worries either way — I'm checking
  whether it was the code or just bad timing."* (offers a pre-approved answer so the honest reply
  isn't an admission)
- drop at **2→4** → *"Did you get as far as connecting a tool?"*
- reached **4** then stopped → neither; that's a conversation.

## ★ Probe A CLOSED — refusals need a failure-shaped payload

**Requirement**: a refusal is emitted as a **failure-shaped payload**
(`{"error":"REFUSED","code":…,"message":…}`) — **not prose, and not a caveat field inside a success
result.** 6/6 both providers. Structured fields stay required for *ordinary* caveats but are
**explicitly NOT the fix for refusals** (gpt/structured was 3/6).

**The variable is FRAMING, not channel** — PA's correction of my hypothesis; OpenAI has no `is_error`
flag, so the winning arm was an ordinary success result whose *content* read as a failure. Remedy needs
no transport work.

🔴 **GATE, not a footnote**: every probe exercised **provider APIs**, not the shipping products with a
deployed MCP server. **Encouraging, not clearance.** Retest against `mcp.pipermorgan.ai` **before the
capability is booked** — one afternoon when the server exists.

⚠️ **Not banked**: attribution correlating with survival confirms a ruling I'd already made, so it's
recorded as **to re-verify**, not as support.

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

- **Job `1e30ec20`** — `47 6,9,12,15,18,21`. Re-armed at STOP 08-02 by delete-then-create
  (`d76fe3a6` → `1e30ec20`). **Cadence unchanged**; prompt gained the check-the-clock reminder.
  *(Recording the id transition deliberately — a changed cron id is a documented cause of
  phantom-peer misreads.)*
- ⚠️ **Session-only AND auto-expires ~2026-08-09.** Both deaths silent. **Run `CronList` at every
  START** — this file records intent, not a live job.
