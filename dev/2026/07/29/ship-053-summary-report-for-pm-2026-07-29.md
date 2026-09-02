# Ship #053 window summary — for PM, ahead of drafting

**Window**: Fri Jul 17 – Thu Jul 23, 2026. Sourced from all 7 omnibus logs (full read) + all 6 workstream memos (full read), cross-referenced.

## The window's actual shape

Two distinct infrastructure outages ate most of it. **Jul 17–18**: tail end of the Jul 13 cohort-wide cron death (PM reauth event) — CIO/PPM/HOST/CXO/Comms/Web were still dark or just resurfacing. **Jul 19 (Sunday)**: full cohort restarted — all 11 roles active — and then PM's laptop crashed around 14:00, killing every session except Lead and Exec. **Jul 20–23**: near-total outage for leadership — only Lead (solo, on Amber-adjacent infrastructure) and Exec kept working continuously; Comms recovered Jul 21; everyone else (HOST, CIO, Arch, CXO, PPM) stayed dark through the end of the window.

Net: of 7 days, most leadership roles had **1 working day** (Jul 19) or fewer. Comms is the exception — active essentially the whole window. Every workstream memo states this plainly and up front, several with real self-verification (CIO cross-checked its one active day against `git log` independently; CXO named that a stale checkout initially made the kickoff itself invisible).

This isn't a slow week — it's a broken one, with one very dense day in the middle.

## Sunday, July 19 — where nearly everything happened

The full cohort came back online together and produced, in one day:

- **A real data-loss incident, found and fixed within hours.** A PPM push-retry reused a stale git tree object and silently reverted 8 lines of CIO's session log plus a full `ROLE-PORTFOLIO-CIO.md` refresh (a third casualty, a Web→Docs memo, was also found and restored). CIO discovered it, PPM root-caused it precisely and distinguished it from a separate, real worktree-collision defect discovered the same day — a distinct provisioning-layer bug (one physical directory shared by CIO/Exec/PPM) that CIO's own 22-directory fleet audit confirmed was isolated (21 of 22 correctly paired) rather than a cohort-wide discipline failure. A detection fix shipped same day.
- **The beta gate (#1386) was accidentally auto-closed** by a GitHub commit-message keyword collision (`closes #1386-P3` triggered the parser for `#1386` itself) and sat silently closed for roughly 11 hours before PPM caught it and reopened it with the real unmet criteria documented.
- **Arch stopped a locally-reasonable fix pre-build** because it would have reversed a load-bearing ADR (the classifier-stays-stateless invariant), without being able to name the actual correct root cause at the time. Lead found the real cause the next day — the ruling held.
- **The CI smoke gate went green for the first time in over 40 consecutive red runs**, after Lead identified and cleared four distinct root causes in one sustained pass.
- **Ship #052 was fully coordinated and drafted same-day** — all 6 workstream memos collected, full draft produced before PM returned from being AFK.
- **PDR-006 (the hosted-MCP architecture pivot)** was formalized, diagrammed, and PM-approved, following the prior day's MCPB-is-dead decision.
- **The spatial-intelligence review converged from four independent directions in parallel** — Arch (architectural history), CXO (experience theory), PPM (product-value scoping), and Lead (code-reality census) all reached the same disposition (keep the live spatial-reasoning layer, park the cold per-connector adapter chain) from different premises, without coordinating the answer in advance.

## Jul 20–23 — Lead's solo burn-down

With almost the entire leadership cohort dark, Lead ran what is very plausibly the most productive single stretch in the project's CI history: **the #1452 test-suite backlog went from 634 to 105** (accessible tail fully drained), CI achieved its first sustained green streak (from 40+ consecutive reds to ten green batches with one red caught and cured same-cycle), and beta advanced **v25 → v28**. Real product bugs surfaced and were fixed as a byproduct of the burn-down, not as separate work: a keyless-config doc-surface silent failure, a usage-cap bug that made unrelated production errors masquerade as capacity limits, a Redis connection-pool loop-binding bug (same class as an earlier Postgres one), and — the headline item — **the learning loop itself was fixed** (#1438: a one-character JSONB comparison bug had made every captured pattern orphan itself; now live).

Comms recovered Jul 21 and delivered real output across the rest of the window: Ship #052 published and distributed (with a real internal inconsistency caught before publish), two narrative beats published, and a 7-day-stale narrative-slate approval cleared and drafted same-day once it landed.

## What didn't move — worth stating plainly, not smoothed over

- **Most leadership portfolio lines were simply untouched.** CXO's own words: *"six of seven days of CXO silence in a beta-critical window is the real story... the design-system portfolio didn't slip because of prioritization; it slipped because nobody was in the seat."* CIO reports the same shape for its own 7-line portfolio (one of seven moved). Arch names the same for its own named goals.
- **Arch's own portfolio doc has been stale for five weeks** under a rule requiring weekly refresh — Arch names this itself as a live instance of exactly the failure class its role exists to prevent (a currency rule that depends on someone remembering it).
- **The spatial-intelligence UX argument (why "park," not "supersede") currently lives only in memos, not the ADR corpus** — CXO flags this as a real risk to a decision that's about to be ratified: a future reader of the architecture alone would reasonably conclude the cold code was a failed attempt.
- **BYOC marketplace narrative**: still blocked, no PM direction, now ~6 weeks stale (Comms).

## A theme worth considering for the narrative

Arch's own framing, which I think is the strongest single line to come out of any of the six memos: **"the invariant held while its guardian was offline."** Arch stopped a fix pre-build on Jul 19 without being able to prove it was right, then went dark for four days — and the ruling held because it was written to `decisions.log`, not held only in Arch's head. The same shape shows up in Lead's solo burn-down (proceeding safely for days without Arch/CIO oversight because the ratified contracts — ADRs, ratchets, the #1452 gate itself — didn't need anyone present to stay coherent) and in Ship #052 itself (drafted and published while PM was AFK, off a fully durable collection process).

The counterweight, named independently by both Arch and CIO: a lesson can be sitting in a log and not get generalized. CIO's memo traces a finding from this exact window — *"an escalation depends on its recipient being awake to read it"* — that was visible Jul 19 but wasn't turned into methodology, and recurred in nearly the same shape on Jul 27 (the PARK-NO-EXIT catch-22 during this week's Amber migration). The record captured it eight days before the cohort learned it the hard way.

---

Ready to discuss and move to drafting whenever you are.
