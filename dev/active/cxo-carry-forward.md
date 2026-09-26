---
last_updated: 2026-09-25
currency_claim: per-stop
max_age_days: 1
---

# CXO carry-forward — rewritten 2026-09-25 at the 22:17 STOP.

> 🔴 **Spring-cleaned 2026-09-22 per PM's context-floor directive; kept lean since.** Resolved
> history is deleted, not archived-in-place — it lives in session logs (the durable record) and,
> for the most transferable lessons, in `docs/briefing/CXO-SUCCESSOR-READ.md`. If you're looking for
> a specific dated incident that isn't here, check the session log for that date first.

> ## 🔴 STANDING RULE — a cron job id surviving a reboot/restart is NOT evidence the event missed you
>
> `claude --resume <uuid>` restores the cron from the saved transcript regardless of whether a reboot
> happened. **Job-id continuity proves `--resume` worked, not that an infra event didn't reach you.**
> Full incident: `feedback_cron_id_continuity_not_evidence_against_reboot` (memory), 09-20/09-21 logs.

> ## 🔴 STANDING RULE — don't reason from a single unstable measurement
>
> **Real incident, 09-24**: claimed a persisting UI flash was *"the browser's own native teardown
> gap"* after finding no code cause — the measurement it rested on was explicitly flagged by its own
> reporter as n=1, not a stable distribution. It was noise. **"I can't find a code cause" does not
> imply "therefore structural."** Full incident: 09-24 session log, #1859 tracker row.

> ## 🔴 STANDING RULE — check a claim against its live source, not the summary of it
>
> **Reinforced twice today (09-25)**: Arch's plan doc cited my own rubric several versions stale;
> Lead offered #1735 as a colleague-model referent without checking it was a documented
> false-liveness mechanism. Both caught by opening the live file/issue rather than trusting the
> framing. Apply this to my own future citations too, not just others'.

## Cron

✅ **Re-armed 2026-09-25 22:21 PDT — job id `0ea47212`**, expression `47 6,9,12,15,18,21 * * *`,
7-day auto-expiry (~2026-10-02). Delete-then-create from `4b4721b5`; `CronList` confirmed exactly one
job survives post-create. `CronList` proves a job OBJECT exists; only a fire proves it FIRES.

## Standing-items tracker

`dev/active/cxo-standing-items.md` — **26 rows**, both guards clean as of tonight. This carry-forward
does not duplicate the tracker; check it for anything open. Run **both** guards after any edit:
`scripts/aging-standing-items.sh | grep '· cxo:'` (expect **26** — restate this number whenever you
add/remove a row) **and** `awk -F'|' '/^\|/ {print NR": cols="NF-2}'` (every row must read `cols=4`).
**Edit tool only on this file — never `.replace()`.**

## GitHub criteria line

`label:UX state:open` — denominator **2** (#1174, #1108), checked at every fire today, unchanged all
day. #1174 routed to HOST (welfare gate), waiting; #1108's copy half is done, build unowned.

## ⚠️ Active — #1772 residual: Lead builds the guard, not yet landed

**Ruled tonight (b): build a post-compose scope guard**, not accept the measured ~10% residual
(anthropic 1/10, gpt-4o 0/10 on shipped copy; history 50%→20%→10% real, not converging to noise).
Zero-by-construction beats a probabilistic promise that reopens with every future floor-copy edit.
Arch's adversarial-pass condition (must not over-trigger on a sentence that quotes/references an
unarmed source without claiming to have checked it) is part of the ruling. **Flagged, not decided,
for Lead**: whether a day of build time fits against PM's same-day no-exemptions Epic-0 sequencing
rule — gave Lead an explicit off-ramp. Arch acked "nothing further owed" on the architecture
question. Watch for the guard landing or a sequencing-conflict pushback.

## Closed today, 2026-09-25 — watch only, nothing owed unless something reopens

- **BYOC T-axis mitigation series** (rounds 2-4) — vendor-asymmetric finding folded into rubric
  v0.8.2 (§6e): fixes on Claude, never on GPT-4o across all 4 designs tried. Closed by design.
- **#1772 mechanism/copy** — landed verbatim, independently verified at source by Lead and Arch.
  (The residual decision is the active item above — this is only the closed mechanism half.)
- **Ship #062 workstream review** — filed inside a moved-up ~30-min deadline; led with #1875/#1855/
  #1859 as the product-facing answer to PM's "what can a user do today" question.
- **MCP Phase C** — answered Lead's colleague-model referent question (#1510, not #1735 — checked
  #1735 live, ruled it out as a documented false-liveness mechanism); caught and Arch fixed a stale
  rubric-version citation in Arch's own plan doc.
- **#1875, #1859, #1799** — all closed prior days, still watch-only, nothing new.

## Waiting on others — nothing owed to PM

**Nothing currently queued for PM from this seat.** #1824's classifier owner is Lead's open question.

## Agent 360 v0.5 — response owed within ~2 weeks, not urgent

HOST fielded v0.5 (`dev/2026/09/25/agent-360-questionnaire-v0_5.md`), new §5.6 on gate/CI-output-
checking habits from this week's credential-incident cluster. Tracked as a standing-items row.
Answer via memo to `mailboxes/host/inbox/` when there's something real to say — Time Lord backstop.

## ⚠️ Instrument state — read before scoring anything

- **CT rubric**: three invariants PM-ratified 08-31; criteria/branches CXO-editable. Open the file
  for its version — no version numbers in briefings.
- **C-axis**: report per bucket, never pooled. `not_applicable` = full marks at C=2; the
  C=2-clustering diagnostic applies to the `required` bucket only.
- **BYOC rubric**: v0.8.2. T split into T-own-surface (measurable, series closed 09-25) /
  T-MCP-surface (`UNMEASURED` until increment-1 infra — MCP Phase C, now actively building, is that
  infra; watch for the first real chance to measure it).

## 🔴 EVERY OUTBOUND MEMO — route away from Lead by default (PM directive, 2026-09-09)

Before addressing Lead, ask whether he must **act** — if the answer is "he wrote it" rather than "he
must act on it," cc, don't address; prefer CIO/PPM/Arch as primary. This binds me, not just Exec.

## 🔴 EVERY MEMO — filename budget

Keep memo basenames **≤130 characters** (measured budget is 150; this is 20 chars of headroom). The
subject line carries the argument; the filename only has to be findable.

## Live threads (watch only)

Nothing beyond the tracker and the active-item boxes above. Check `cxo-standing-items.md` for
anything genuinely open — this file is ephemeral session state, not a running history.

## Briefing currency

`docs/briefing/BRIEFING-ESSENTIAL-CXO.md`'s Current Focus section refreshed 2026-09-22 per Docs'
staleness flag — items verified against GitHub/tracker where possible, three items explicitly
flagged unverified rather than guessed. Check that file directly rather than assuming this note
stays current about it.
