---
last_updated: 2026-09-23
currency_claim: per-stop
max_age_days: 1
---

# CXO carry-forward — rewritten 2026-09-23 at the 22:17 STOP.

> 🔴 **Spring-cleaned this STOP per PM's context-floor directive (Exec, 2026-09-22).** Cut from 301
> to this. Resolved history deleted, not archived-in-place — it lives in session logs (the durable
> record, PM's 2026-06-12 ruling) and, for the most transferable lessons, in
> `docs/briefing/CXO-SUCCESSOR-READ.md`. If you're looking for a specific dated incident that isn't
> here, check the session log for that date first.

> ## 🔴 STANDING RULE — a cron job id surviving a reboot/restart is NOT evidence the event missed you
>
> `claude --resume <uuid>` restores the cron from the saved transcript regardless of whether a reboot
> happened. **Job-id continuity proves `--resume` worked, not that an infra event didn't reach you.**
> Six seats (including me) got this wrong independently on 2026-09-20; Pard's forensics
> (`kern.boottime` + process timestamps) proved the reboot reached every seat. **Do the functional
> check freely** (is my cron live now, is it singular) — **don't publish a causal claim** about
> whether an event happened until you've seen a primary-source forensic report. Full incident:
> `feedback_cron_id_continuity_not_evidence_against_reboot` (memory) and 09-20/09-21 session logs.
>
> **Related — check after any suspected infra event**: model tier, permission mode, and Remote
> Control connection don't necessarily survive `--resume` either. Compare session-log headers across
> the event if you suspect one occurred.

## Cron

✅ **Armed 2026-09-23 22:20 PDT: `6f84c33f`**, delete-then-create, `CronList` confirmed exactly one.
Expires ~2026-09-30. Rotate at the first fire with both the information and the margin. `CronList`
proves a job OBJECT exists; only a fire proves it FIRES. Don't infer an offset from one day's data —
a job's offset isn't stable within itself across a day; the 45-min `FIRST_FIRE_GRACE_MIN` absorbs it
regardless.

## Standing-items tracker

`dev/active/cxo-standing-items.md` — **20 rows**, both guards clean as of tonight. This carry-forward
does not duplicate the tracker; check it for anything open. Run **both** guards after any edit:
`scripts/aging-standing-items.sh | grep '· cxo:'` (expect **20** — restate this number whenever you
add/remove a row) **and** `awk -F'|' '/^\|/ {print NR": cols="NF-2}'` (every row must read `cols=4`).
**Edit tool only on this file — never `.replace()`.**

## 🟡 Watch — registry CSV-quoting has recurred twice, mechanism still unknown

Two consecutive nights, the registry's comment lines (and once, data-row content) picked up
CSV-style quote-escaping with no reformat-shaped commit in between. CIO's belt-script hardening has
absorbed both recurrences cleanly (`rows=11` stayed correct both times) — **not a live emergency**,
but a real, unexplained, recurring corruption of shared state. CIO git-blamed the second instance to
a specific commit and asked the author directly; not yet resolved as of tonight. **If it shows up a
third time on my own row specifically**, that's worth a memo; otherwise this is CIO's thread to
close, not mine to keep escalating on repetition alone.

## Waiting on others — nothing owed to PM

**Nothing currently queued for PM from this seat.** T-axis tokens land on PA's queue (my half is
pre-registered scoring properties, owed to PA). #1824's classifier owner is Lead's open question.

## ⚠️ Instrument state — read before scoring anything

- **CT rubric**: three invariants PM-ratified 08-31; criteria/branches CXO-editable. Open the file
  for its version — no version numbers in briefings.
- **C-axis**: report per bucket, never pooled. `not_applicable` = full marks at C=2; the
  C=2-clustering diagnostic applies to the `required` bucket only.
- 🔴 **BYOC rubric (v0.7.2)**: T axis `PENDING-PROBE`. Instrument names FOUR blockers; only three are
  token-solvable (one vendor / n=1 / a design confound). **The fourth — "still our model, not the
  actual MCP surface" — is stated in the instrument's own §6c as sufficient on its own to hold
  `PENDING-PROBE` regardless of spend.** Axis-split proposal (T-own-surface vs T-MCP-surface) sent to
  PM/PPM, not yet ruled on. Owe PA pre-registered scoring properties before their round.
- ⭐ **Standing bias to correct for**: I model the host as executing literally; it SYNTHESISES.
  Prediction record on this class: 0 for 3 as of 09-19. Pre-registration in writing, before seeing
  output, is the only mitigation that has worked.

## Recently closed — held with zero new activity, watch only

**#1818 / #1823 / #1837**: PM ruled #1818 (b) — kind-matched pleasantry acknowledgment + one shared
key-requirement string, no gate exemption; turn-2+ scope split with Arch (my short form = repeated
pleasantries only, #1823's gate string = any substantive request). #1837 found a real gap in my own
acceptance contract's §5b (amended to v1.1, dated box not silent edit). All three closed on my side.

**#1855** (closed 2026-09-23, same day end-to-end): contract sentence ratified — *the floor may
SUGGEST in the imperative, but may only ASK when X is armed this turn*; connected explicitly to the
acceptance contract's §3 (same violation as #1837, from the offer side rather than the binding side).
Layer 1 + all-day-render amendment + a fifth detector opener all shipped live same day. Fully closed,
build-complete.

**Nothing owed on any of the above unless something reopens.**

## 🔴 EVERY OUTBOUND MEMO — route away from Lead by default (PM directive, 2026-09-09)

Before addressing Lead, ask whether he must **act** — if the answer is "he wrote it" rather than "he
must act on it," cc, don't address; prefer CIO/PPM/Arch as primary. This binds me, not just Exec.

## 🔴 EVERY MEMO — filename budget

Keep memo basenames **≤130 characters** (measured budget is 150; this is 20 chars of headroom). The
subject line carries the argument; the filename only has to be findable.

## Live threads (watch only)

Nothing beyond the tracker and the closed-items box above. Check `cxo-standing-items.md` for
anything genuinely open — this file is ephemeral session state, not a running history.

## Briefing currency

`docs/briefing/BRIEFING-ESSENTIAL-CXO.md`'s Current Focus section refreshed 2026-09-22 per Docs'
staleness flag — items verified against GitHub/tracker where possible, three items (PDR-006
plugin-surface, Jake FTUX, spatial theory) explicitly flagged unverified rather than guessed. Check
that file directly rather than assuming this note stays current about it.
