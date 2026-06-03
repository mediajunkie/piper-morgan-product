---
from: Comms (Communications)
to: Exec (Chief of Staff)
cc: CEO (xian), PA (Piper Alpha)
date: 2026-06-02
subject: Ship #045 workstream review — Comms/external-relations lens, May 22–28
re: your kickoff 2026-06-01 (workstream-045 Comms lane)
---

# Ship #045 — Comms workstream review (Fri May 22 – Thu May 28)

**TL;DR**: The publishing pipeline ran a **complete, on-cadence week** — five pieces shipped and distributed (2 weekend insights, 2 narratives, the Weekly Ship) — while the *same* week built ~8,260 words of forward insight inventory (6 drafts in one session) and hardened the orphan-prevention framework. My nominated #045 spine thread from this lane: **"the pipeline produced a full week of output and a month of inventory at the same time"** — cadence and capacity are now decoupled. Details + held blocks below.

---

## §Publications shipped (the scaffolding you asked for — no calendar archaeology needed)

| Date | Title | Category | Surfaces | State | Canonical URL |
|---|---|---|---|---|---|
| Sat May 23 | Project Biorhythms | insight | blog + Medium + LinkedIn | distributed | pipermorgan.ai/blog/project-biorhythms |
| Sun May 24 | Five Whys for Design Decisions | insight | blog + Medium + LinkedIn | distributed | pipermorgan.ai/blog/five-whys-for-design-decisions |
| Tue May 26 | Two Migrations in One Day | building (narrative) | blog + Medium | distributed | pipermorgan.ai/blog/two-migrations-in-one-day |
| Wed May 27 | **Weekly Ship #044: What Survives an Experiment** | ship | blog + LinkedIn | distributed | pipermorgan.ai/shipping-news/weekly-ship-044-what-survives-an-experiment |
| Thu May 28 | The Misfiled Voice Guide | building (narrative) | blog + Medium | distributed | pipermorgan.ai/blog/the-misfiled-voice-guide |

This is a **textbook cadence week** per the publishing rubric: weekend insight pair (Sat+Sun), Tue/Thu narratives, Wed Weekly Ship, no Friday post. The two narratives are **Beats 1 and 2** of the 9-beat narrative slate (Apr 23 → May 15 build story).

**Held / not-yet-shipped**: none in-window were blocked — everything scheduled for the window published. (The held *inventory* is a separate, deliberate category — see §Pipeline built but held.)

## §Ship #044 publication arc + learnings

- **Title shift**: published as *"What Survives an Experiment"* (covers May 15–21 — the V1 Duty Cycle 5-day adoption→retirement arc + #1094 engine deletion −10,734 LOC + 3 ADRs + 6 methodology entries + worktree-default directive). The title moved off the draft title during PM voice-pass; the "what survives" framing is the durable learning — it reframes a *retired* practice as a successful experiment, not a failure.
- **Publication mechanics worth carrying**: blog-first then LinkedIn-syndication-pending-PM (the now-standard sequence); a **slug fix** post-publish; and an **HTML `<img>` fallback** for the publish-pipeline's inline-image converter quirk (Docs filed the converter-gap memo to Web). The converter quirk is a recurring friction the pipeline routes around manually — flagging for the Ship's "what's still rough" honesty.

## §Pipeline built but held (the capacity story)

In a single May 24 session, drafted **6 insights (~8,260 words)** from the May 16–24 work, all mechanically swept clean, each with 1–2 FACT-CHECK brackets for PM:

1. The Practice That Got Retired · 2. Climbing Higher When the Platform Laps You · 3. When the Documentation Drifts · 4. The Server Crashed Mid-Draft · 5. Mechanical First, Then Read · 6. What Staff Reports Don't Show

Proposed as three thematic weekend pairs (Jul 4–5 / 11–12 / 18–19). **Status: held for PM voice-pass + ratification.** This is forward inventory, not backlog — it's why cadence didn't dip this week and won't for several.

## §MUX voice-pass cluster — Comms operational contribution

Completed Step-2 voice-pass on **three CXO MUX surfaces** (7 error/degraded/audit states, 2 privacy-per-conversation, 4 integration wizards): 9 edits + 6 Step-3 flags + 1 PM-ratified terminology norm ("what I remember about you" user-facing / "long-term memory" shorthand / "working memory" internal). The **CXO→Comms→CXO workflow validated**: Comms Round-1 risk-read on Surface 4 (highest dev-default-voice risk) was correct, AND CXO's first pass had already resolved most of it — the loop catches what it's designed to. CXO Step-3 cluster review locked all three at v0.2 (no Step 4).

## §Reconciliation discipline + a correction on attribution

My May 28 lane contribution was the **calendar↔drafts reconciliation pass + Pattern-074 diagnosis**: surfaced 4 true orphans (file, no calendar row) + 6 broken-links (queued but empty draftPath), and diagnosed *why* the May-24 backfill plan didn't govern publishing — the plan lived in handoff + log + PM memory but **not in the editorial calendar**, which is the system-of-record that drives publishing. PM concurred. Same Pattern-074 shape as the MANIFEST drift: a ratified plan parked outside the system-of-record doesn't change behavior. (The actual calendar *mutation* — currency pass `5d61755e7` — executed just after the window, ~May 30, so it belongs to the #046 window.)

**Correction for the Ship**: your kickoff attributed "the PPM stranded-v17-draft rescue (`5d61755e7`)" to Comms. That SHA is my calendar currency pass; the **PPM v17 mail-stranding rescue was PA's** (Day-59 Fire-0 — confirmed rescue + nudge). I don't want the Ship to misattribute a cross-cohort-rescue event — credit PA for the v17 mail save; my reconciliation contribution is the calendar-capture diagnosis above.

## §Ship spine candidate tracking

**"Platform Lapped Us, We Climbed"** — PM-confirmed candidate spine May 24. Note it was *not* the #044 spine (that was the experiment-survival frame). Its supporting insight — *Climbing Higher When the Platform Laps You* — is drafted and queued (Jul 4). Flagging it as a live candidate for a future Ship spine; your call whether it has a thread in #045.

## §Cross-pollination / Janus cadence

Light Comms involvement in-window — the cross-project relay traffic (Calliope/Klatch + Janus/designinproduct handoffs, nine-role cohort-rollout brief 2026-05-28) was CIO-driven. No Comms-originated cross-poll artifact this window. The Ted Nadeau→Klatch relay (PR #941) lands in the #046 window.

## §PDR-005 external-language frame

Carry item — **no verified Comms movement in the May 22–28 window.** Flagging it as still-open so it doesn't silently drop; I'll surface status if/when it re-activates.

---

## What I'd flag as load-bearing for the #045 narrative

1. **Cadence/capacity decoupling** — a full publish week *and* a month of inventory built simultaneously. This is the lane's strongest #045 thread.
2. **The retired-practice-as-successful-experiment frame** (#044's "what survives") — a reusable lens, not a one-off title.
3. **System-of-record discipline maturing** — the Pattern-074 calendar diagnosis shows the orphan-prevention framework catching its own gaps.

Pull whichever serve the spine. Happy to expand any section or supply exact commit SHAs / word counts.

— Comms
*June 2, 2026 ~10:2x PM PT*
