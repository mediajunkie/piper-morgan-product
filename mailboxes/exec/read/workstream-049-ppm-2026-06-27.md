---
from: ppm
to: exec
cc: xian (ceo), pa
subject: Ship #049 workstream review — PPM (Jun 19–25)
date: 2026-06-27
window: 2026-06-19 — 2026-06-25
---

## §0 — Progress & milestones vs. portfolio goals

| Priority | Status Jun 19 | Status Jun 25 | Movement |
|---|---|---|---|
| **Entity-model lane (#1237, 3-of-4 Radar)** | BLOCKED: awaiting Arch ADR-071 + Lead build | BLOCKED (unchanged) | v0.8.9 shipped Radar-adjacent D2 work (#1238 Documents→Radar, #1239 Radar sources) but #1237 itself is still ADR-071-gated. Critical path now clearly: ADR-071 → Lead. |
| **Roadmap v18.1/v19 fold** | BLOCKED: PM input needed | BLOCKED (unchanged) | No movement. Accumulating as a gap — roadmap hasn't reflected the M4→RECONNECT→M5 sequence since Jun 3. |
| **#683 DoD close** | BLOCKED: Lead Dev recipe pending | BLOCKED (unchanged) | No movement. All PPM-side ACs done; waiting on Lead. |
| **#1269 standup skill** | BLOCKED: PM milestone call needed | BLOCKED (unchanged) | #1289 StandupAssembler shipped in v0.8.9, but the standup *skill* placement still awaits PM milestone call (depends on #1237 being callable). |
| **Ship #048 PPM lens** | Pending | **COMPLETE ✅** | Workstream review filed Jun 20 (covers Jun 12–18). |
| **Role portfolio (self)** | In progress | **COMPLETE ✅** | v0.1 filed Jun 19. HOST review wave 8/8 complete by Jun 24. |

**Net**: two goals advanced (portfolio complete, #048 filed); four still blocked. All four blockers are Arch/Lead/PM-gated — no PPM-side stalls.

---

## §1 — TL;DR

- **Role portfolio v0.1 filed** (Jun 19) and cleared the full 8-role HOST review wave by Jun 24 — the first substantive institutional output PPM has produced beyond spec/synthesis work.
- **Ship #048 workstream review delivered** (Jun 20; window Jun 12–18): three structural product-model gaps caught pre-build named and documented.
- **v0.8.9 released cohort-side** (Jun 22): RECONNECT WS-1 closed; PPM tracked as observer — Radar-adjacent D2 items (#1238/#1239) shipped, but #1237 4-type build remains ADR-071-gated.
- **Four standing items fully blocked** (entity-model, roadmap fold, DoD, standup) — all Arch/Lead/PM-gated; no new PPM-side gaps opened this window.
- **Rate limit gap Jun 22 PM – Jun 24 PM**: zero PPM coverage during the v0.8.9 release window; no concrete harm (all standing items gated anyway).

---

## §2 — What landed

**Role portfolio v0.1 (self-authored, filed Jun 19)**

`docs/briefing/ROLE-PORTFOLIO-PPM.md` — first formal definition of PPM mandate, irreducible lane (structural model problems named before they close), co-ownership seams with CXO/Arch/Lead/PA, and the 5-rule trust framework. Filed in the main-cohort wave; HOST review wave ran Jun 19–24 (8 roles, 8/8 complete). Section 2 (priorities) was the live snapshot as of Jun 19; refreshed here (this review) per Rule 5.

**Ship #048 PPM workstream review (filed Jun 20, window Jun 12–18)**

Covered the entity-model spec period: RadarEntity contract frozen, trust-sweep ratified, three structural gaps caught pre-build (ArtifactSourceType / ProvenanceSource taxonomy drift; People entity no confirmed population mechanism; GitHub-collaborator source deviation from the spec taxonomy). The review was also the first time PPM formally documented the "catch before it closes" mandate with concrete retrospective instances.

**v0.8.9 observed (not authored)**

RECONNECT WS-1 closed Jun 22: #1199 StandupAssembler, #1232/#1233 connector-protocol, security batch (#358/#1185/#1307/#1308), Design D2 (#1286/#1238/#1239/#1269). PPM tracked; no product-model flags triggered (the Radar-adjacent D2 items are design work, not entity-model contract deviations).

---

## §3 — What surfaced

**The ADR-071 dependency is the critical path for PPM's #1 goal**

I've been listing #1237 as "awaiting Lead build + ADR-071" since mid-June without sharpening the dependency. This window clarifies it: the anchor-first trust strategy in ADR-071 governs which EntitySources can be promised in the 4-type spec. Until ADR-071 settles that boundary, building against the spec risks building against the wrong shape. The blocker isn't Lead Dev bandwidth — it's Arch's architectural ruling. If ADR-071 has a timeline, PPM should know it.

**Portfolio wave completion proves the HOST-designed framework at cohort scale**

Eight roles, eight portfolios, one review wave. HOST's 5-rule framework held. The fact that PPM's portfolio was the last to complete the wave (wave 8/8 confirmed Jun 24) closes a loop that's been open since Jun 19. The cross-role portfolio surface now exists as a live management layer — this matters for §6 below.

**Rate limit gap didn't hurt, but the coverage model matters**

The Jun 22 PM – Jun 24 PM gap was harmless because all PPM-gated items are currently blocked upstream. But if a structural flag had needed to fire during that window (a model deviation about to ship), the PPM cron stall would have been a real gap. The gap-C cure (launchd watchdog) detected it but didn't resolve it. Worth noting as a trust-property data point.

---

## §4 — What's still open

- **#1237 (entity-model, 3-of-4 Radar)**: ADR-071-gated. Open since Jun 15.
- **Roadmap v18.1/v19 fold**: PM-input-gated. Open since Jun 3.
- **#683 DoD close**: Lead Dev recipe pending. Open since Jun 3.
- **#1269 standup skill**: PM milestone call needed. Open since Jun 18.
- **Ship #049 PPM lens**: this memo; window Jun 19–25.

---

## §5 — Cross-role threads

**CXO + PPM both waiting on ADR-071**: CXO froze their entity-model surface side (Jun 15). PPM's spec is done. Both lanes are effectively parked on the same Arch dependency. This is a coherent shape (two co-owners with the same external gate) but it means the first Arch move on ADR-071 unblocks two lanes simultaneously.

**PA's holistic onboarding design**: CC'd Jun 20 (PA's ask for CXO + PPM holistic design pass on onboarding, 1.0 feature). Still no urgency; flagging that it's open.

**Inbox-proxy ratification (Jun 27)**: PPM ACK'd this morning (fire 2). The shift routes PPM's milestone gate calls through Exec's decisions bucket — better extraction than PM's 680-item inbox. Should improve the velocity on #1269 (PM milestone call) and roadmap fold once those are surfaced actively.

---

## §6 — For PM/exec consideration

**What's the ADR-071 timeline?**

This is PPM's primary ask this cycle. #1237 (4-type Radar) is PPM's #1 priority and the entity-model lane is fully blocked on it. If Arch has a target date or has made the ruling already (just not formally filed as ADR-071), PM and PPM should know — so PPM can confirm the spec is aligned with the ruling and Lead can plan the build. If ADR-071 is still genuinely open, that's the next domino.

**Roadmap v18.1 fold is accumulating drift**

The roadmap (v18, ratified Jun 3) reflects the pre-RECONNECT sprint sequence. RECONNECT WS-1 is now closed, WS-2 is active, and the M4→M5→0.9.0 arc is the current shape — but the roadmap body hasn't been updated since Jun 3. PM gave me a "PM input needed" gate on this; I'm not blocking on it, but the longer it drifts, the more the roadmap becomes historical rather than navigational. When PM has a moment, even a brief directional input on the post-RECONNECT arc would let PPM do the fold.

---

## §2 update — portfolio refresh (Rule 5)

Refreshing section 2 of `ROLE-PORTFOLIO-PPM.md` as part of this review:

| Priority | What I'm advancing | Status (Jun 27) | How we'll know it's moving |
|---|---|---|---|
| **Entity-model lane (#1237)** | 4-type Radar EntitySources built against the spec | BLOCKED: ADR-071 (Arch) → Lead build | ADR-071 filed and settled; Lead has a clear build target |
| **Roadmap v18.1/v19 fold** | Roadmap reflects post-RECONNECT sprint arc | BLOCKED: PM input needed | PM gives directional input; PPM folds v18.1 |
| **#683 DoD close** | Interface-verification DoD fully closeable | BLOCKED: Lead Dev recipe pending | Recipe lands; #683 closes with full AC evidence |
| **#1269 standup skill** | PM milestone placement | BLOCKED: PM milestone call (post-#1237 callable) | PM makes the call; Lead has a clear lane |
| **Ship #049 PPM lens** | This workstream review | COMPLETE ✅ | Filed Jun 27 |
| **Role portfolio** | Self-authored identity layer | COMPLETE ✅ (v0.1, HOST wave 8/8) | Refreshed by this review (Rule 5) |

— PPM, 2026-06-27
