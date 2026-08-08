---
from: cxo
to: exec
cc: xian (ceo)
subject: "Workstream #055 — CXO. Window Jul 31–Aug 6. Two lines advanced, three held, two slipped — and one of the slips is mine in a way that took three days to see."
window: 2026-07-31 → 2026-08-06
date: 2026-08-07
---

# §0 — Progress against portfolio goals, line by line

Measured against `docs/briefing/ROLE-PORTFOLIO-CXO.md` §2 as it stood in the window.

| Portfolio line | Verdict | Evidence |
|---|---|---|
| **First contact on the plugin surface** | **ADVANCED** | PDR-006 ratified 07-31; spec `design-spec-first-contact-plugin-surface` v0.1→v0.4; first-contact gate criterion proposed for #1386. ⚠️ Its forward indicator — funnel counts — **did not land**; it needs PM's go for a prod-DB read. **Advanced on the half I control.** |
| **Recomposition rubric (#1463)** | **ADVANCED → HELD** | Probe A closed: refusals require a **failure-shaped payload** (6/6). Then held — the deployed-host retest is a **gate** and there was no live `mcp.pipermorgan.ai` to run it against. **Held on a real dependency, not on attention.** |
| **Honesty of user-facing claims** | 🔴 **SLIPPED — and it is a drift I authored** | See §1. #1482 merged 08-04; **not deployed at any point in the window.** |
| **#1466 Slack link flow** | **HELD — by decision** | Spec v0.2 (corrected after Arch caught my shortcut removing a proof-of-control). **PM ruled 08-06: Slack socket path HELD until safe — not alpha, not beta, not release.** Cleanest kind of hold: a decision, taken by the person entitled to take it. |
| **#1386 beta-gate experience criteria** | **HELD — deliberately** | Criterion-2 sign-off **still withheld**; the keyless suite skips and reports green, and I committed to same-day sign-off once a keyed run exists. That run didn't happen in the window. ⭐ **Criterion 5 earned its place this cycle** — see §2. |
| **#1174 proactive presence** | **HELD — by design** | Discovery only; nothing built pre-beta, as scoped. No movement is the plan, not a slip. |
| **Floor-quality / ethics-decline watch** | 🔴 **SLIPPED — drift, plus my record was wrong** | No watch performed. And when I went to perform it on 08-05, `gh issue view` showed **#950 closed 2026-04-16 and #992 closed 2026-04-30** — I had carried them as an active watch for weeks without checking whether its objects were open. Partial attestation only: the ethics flag defaults false and is set true in `fly.toml [env]`; **I verified config, not the running app.** |
| **D2 design-system portfolio** (#1286/#1290/#1284/#1269) | 🔴 **SLIPPED — drift, fourth window** | Named as a decision-not-drift in Ship #054 §6. It is still a drift. **I have now flagged it twice and moved it zero times.** That makes it my problem rather than the board's. |

**Two advanced, three held (two by decision, one by dependency), two slipped as drift.**

---

# §1 — The slip worth the most words, because it took three days to see

**#1482** retracted five false *"this cannot be undone"* claims and gave the credential-delete dialog the
true claim it lacked. It merged to `main` on 08-04. **I reported it as "shipped" — in my session log, my
portfolio, and summaries to PM.**

**On 08-06, extending PA's deployment check into my lane, I found the deployed artifact predated it.
Three false permanence claims were rendering to users for the entire window**, the honest replacement
appeared zero times, and the credential-delete inversion the fix existed to correct was intact.

> **The fix's premise was *the word must match the behaviour*. For two days my report didn't match the
> deployment.** *"Shipped" is a layer word and I used it for the wrong layer.*

**Then it got worse before it got better**: my first measurement read `origin/production` — a stale branch.
Lead's precision fix named the deployed **artifact**. **I had inherited PA's object without deriving it.**
Re-derived against the artifact: identical count, **by luck** — nothing had touched those strings in the
window. **The conclusion was robust; the number was protected by nothing I did.**

**Also surfaced**: two of the six surfaces in the delete-copy map (`insight_controls.html`,
`insight_card.html`) **are absent from the deployed artifact entirely.** *"Six surfaces fixed"* was never
the right coverage claim.

*(Forward pointer, #056 material per window discipline: **v30 deployed 08-07 08:04 PDT and I verified the
fix live by reading the templates off the running machine** — `home_false=0`, `insights_false=0`,
`honest_home=1`, credential true-claim present, #1484's gate present. **The item is closed; it closed
outside the window.**)*

---

# §2 — What the window taught that outlasts it

**⭐ #1386 criterion 5 was the most valuable thing anyone wrote a month ago.** *"'Impossible-by-construction'
only protects if the construction is deployed and verified."* **That single sentence is the entire
deployment story of this window**, written before it happened, sitting unchecked in the gate. **I'd argue
it should be promoted from a criterion to a habit**: no "done" without a layer named.

**⭐ Our tooling encoded a shared inference.** Five roles — PA, Comms, PPM, Arch, me — independently
measured the production **branch** and got the same wrong answer, because `check-release-parity.sh` reads
`origin/production`. **That is not five people making the same mistake; it is the tooling making it five
times.** Remedy belongs at the script. *(And the authoritative instrument was on the host all along: `fly
status -a piper-morgan` says what is actually serving, in one line, with no inference step to share.)*

**⭐ A verification note immunises a claim against re-examination.** My cron prompt carried a **verified**
beta date — *"re-derived 08-04, `date -j` confirms, `decisions.log:303` confirms."* Every clause was true
when written. PM then said the 8th was a misremembering. **I didn't carry a stale claim because I failed to
check it; I carried it because I checked it and recorded the check.** The evidence trail told the next
reader — me — *this one's handled.* Distinct from the branch error: *right object, correctly measured,
referent moved.* Different remedy — **expiry-date the note, don't just re-verify it.**

---

# §3 — Commitments, fulfilled and not

| Commitment | Status |
|---|---|
| Design calls returned same session | ✅ Held — #1484, #1466, annotation naming, Radar all answered in the fire they arrived |
| No specced capability that isn't built | ✅ Held |
| #1386 criterion-2 sign-off same-day once a keyed run exists | ⏸️ **Not yet triggered** — no keyed run in the window. Commitment stands. |
| Floor/ethics watch | ❌ **Not held.** Named above. |
| Six Jake decisions filed for PM | ✅ Held (08-03) — and PM began working them 08-05 |

---

# §4 — The window's shape, honestly

**Thursday 08-06 the cohort hit the account's weekly limit and was frozen until ~21:30.** On my seat it
presented as **four duty-cycle ticks arriving stacked at 22:17** after ~11 hours of no dispatch — I first
read that as REPL-idle queuing; **Arch's correction named the real cause.** *Fires queue rather than drop,
so the wakes were pending, not lost.* **Environment fact, not lane slippage** — but it did cost me the
12:47/15:47/18:47 working slots on the day the deployment finding needed following up.

**And PM named their own availability, not the team's throughput, as what had been slowing things** — plus
*"I don't want to create any artificial sense of panic or stress."* **I've kept that out of my own memos
since**: the deployment finding went out with the pressure removed rather than added.

---

# §5 — The ask I still have open with PM

**Is Surface 1 (the history sidebar — Radar's rendering) in the 1.0 five?** PDR-005 scopes *"5 of 7 MUX
surfaces"*, classifies 2/4/6/7 clearly and **1/3 as weaker — and never enumerates the five.** Surface 1 is
carried forward by three explicit cross-client commitments while sitting in an unnamed remainder.

> **That is how a feature is lost without anyone deciding to** — not a proposal you can argue against, an
> omission you can't see. PM has defended Radar against three flattening attempts; this would be a fourth
> with no author. **One sentence settles it, or I run PDR-005's own 3-criterion test and bring the result.**

— CXO
