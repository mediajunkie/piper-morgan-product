# CXO carry-forward — ephemeral session state

**Owner**: CXO | **Updated**: 2026-08-03 22:5x PT (STOP)
**Read at**: every fire START. **Rewritten at**: the end of every substantive fire.
**Durable owed/queued work lives in** `cxo-standing-items.md` — this file is *current* state only.

---

## ⏰ BETA = 2026-08-08 (a SATURDAY) — FIVE DAYS. Confirmed at source: decisions.log:303, PM's own entry.

⚠️ **PM has not confirmed whether Saturday is intended** (Aug 7 is Friday). Open question, not a defect.

## 🔴 WITH PM — the six Jake decisions (sent 08-03, `8715f0a43`)

**The chain has been stopped on the PM+CXO decision since the synthesis landed 07-31 09:45.** PA found
it; I should have. My positions on all six are filed so it's a confirm-or-adjust, not a conversation
starting cold. **Item 5 (Jake's reply) needs neither the other five nor me** — it's PM's to send, and
it's nine days.

## Delete copy (#1482) — DELIVERED, awaiting Lead's application

Six exact replacement strings filed (`dev/active/delete-copy-replacements-1482-2026-08-03.md`, also on
the issue). **Five surfaces assert "cannot be undone" on SOFT deletes — false. The one genuinely
permanent operation (credential delete) makes no claim at all.**

⚠️ **Ship as a SET** — the contrast is load-bearing; *"this one really is gone"* only carries
information because the other five are honest. **Open inside the copy**: *"we keep a copy for a while"*
— I don't know the retention window. If one exists, name it; **if none exists, that gap is its own
finding.**

## #1466 Slack link flow — spec v0.2, corrected

Arch caught that my deep-link shortcut **removed the Slack-side proof of control** (unsolicited
binding). **The param may PREFILL, it may never BIND.** Corrected flow keeps the whole step-reduction.
Lead verified the shipped code already enforces it. **New standing copy rule: never ask a user to
approve a string they cannot verify.**

## Alpha funnel — Lead has it; my stage-4 catch landed

`status='active'` would have returned ZERO (the column takes unbound/bound/unreachable/stale) and read
as maximal confirmation of my own hypothesis. **PPM improved my fix past my version: GROUP BY, not a
better predicate — a filter encodes an assumption, a grouping doesn't.** Runs on PM's go.

⚠️ **My pre-registered read stands (08-02): only ONE of four outcomes makes the first-contact spec the
right bet. Do not reason toward it.**

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

- **Job `e7059954`** — `47 6,9,12,15,18,21`. Re-armed at STOP 08-03 by delete-then-create
  (`1e30ec20` → `e7059954`). **Cadence unchanged**; prompt gained the check-the-clock reminder.
  *(Recording the id transition deliberately — a changed cron id is a documented cause of
  phantom-peer misreads.)*
- ⚠️ **Session-only AND auto-expires ~2026-08-10.** Both deaths silent. **Run `CronList` at every
  START** — this file records intent, not a live job.
