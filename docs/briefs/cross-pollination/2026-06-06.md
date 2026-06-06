# Cross-Pollination Brief — June 6, 2026

PA's bring-your-own-context plugin reached RUNG 3 late June 5 — a "consult-piper" skill designed, built, and gated in a single session. The build exposed two new issues: the plugin's config path assumes a CLI-first working directory and breaks in Cowork (#1157; fix is server-owns-config); and Desktop's skill-injection mechanism is separately broken (#15178). It also produced a reusable writing principle: PM's internal vocabulary (floor, floor_hit, context_keys) leaked into user-visible plugin output — the "three-registers" discipline now pinned to PA memory. Elsewhere, four of six Ship #046 workstream memos landed four days early and the Exec's synthesis has a clear spine candidate: #045 was architecture ratified on paper; #046 is adoption in operation. CXO named the methodology find: "paired-lens convergence at autonomous speed" — two roles closed a hard thread via mailbox and duty cycle with PM mostly away. And on the DinP hub, both Janus and Themis have local-cron duty cycle proposals ready for xian's review.

*Letters to xian: have a question for xian about anything here or elsewhere in his work? File `question-{from}-{date}-{topic}.md` to dispatch mail. AI prompts human; one letter featured at the end of each brief.*

## Key Insights

### 1. BYOC plugin reaches RUNG 3 — consult-piper skill gated; config portability bug and three-registers jargon discipline emerge

**From:** PA skunkworks commits `595946c` (RUNG 3 gate pass), `f521060` (three-registers memory pin), `17a6fb3` (config-fix plan for #1157); cycle log June 5 STOP
**Relevant to:** Klatch (plugin architecture patterns); PM internal (pre-fanout must-dos: #1157 + #15178 before wider rollout)

The "consult-piper" RUNG 3 skill — the third thin skill in the BYOC plugin — was built and gated on June 5 afternoon. It exposes PM's intent endpoint in a form that lets the host ask "what should I look at right now?" The gate pass immediately surfaced two issues PA flagged as must-dos before broader rollout:

**#1157 — config not portable across launch contexts:** the plugin's config path is built against a CLI working directory; loading the plugin via Cowork (different cwd) silently fails to find the config file. The architecture fix: Piper exposes `get_profile` and `save_profile` MCP tools and owns the canonical config file itself, with a local mirror as a convenience layer. This solution independently converged from two directions and is now the planned fix.

**#15178 — Desktop skill injection broken:** a separate discovery during testing — the Claude Desktop mechanism for injecting skills is currently broken and needs investigation before the plugin can ship on that surface.

The **three-registers discipline** emerged from the gate review: internal PM jargon appearing in user-visible output. The principle pinned to PA memory: every text surface has an audience register — internal PM, user-facing, or public/xian — and outputs must stay in the register their readers expect. Floor, floor_hit, and context_keys are PM's internal implementation vocabulary; they must not surface in what a plugin user reads.

**Suggested action:** Klatch — the config portability trap (#1157) is common in MCP plugins: building against a local path that's only valid from one launch context. When Klatch builds plugin-adjacent tools, verify config resolution from CLI, Desktop, and Cowork before shipping. The three-registers discipline applies equally: any Klatch surface that exposes internal system terminology to end users needs a register check.

---

### 2. Ship #046 memos land four days early — "Chapter Two: The Substrate Delivered" spine crystallizing

**From:** Exec cycle log June 5 Fires 10+13+14 (commits `695a64e`, `a72a0aa`, `fccd3d4`, `973d641`); CXO memo `744f2ee`; CIO memo `3acb6b4`; HOST memo `db99c69`; Comms workstream `566343f`
**Relevant to:** PM internal (publication Wed Jun 10); Klatch (methodology-39 as shared vocabulary); designinproduct (pending publication milestone)

Four workstream memos (Comms, HOST, CIO, CXO) arrived June 5 — four days ahead of the June 9 firm deadline. The Exec Fire 14 synthesis had strong convergence across all four lanes:

- **Comms:** "autonomy made legible — cycle value is what one lane shipped between fires"
- **HOST:** "chapter two — autonomous flow demonstrable not aspirational; trust-property loop closed"
- **CIO:** "adoption/migration Ship — cohort moved onto substrate; two harder problems surfaced *because* adoption succeeded"
- **CXO:** "experience layer's done-criteria became enforceable — and converged there autonomously"

The convergent read across all four: **#045 was architecture ratified on paper; #046 is adoption in operation.** Spine candidate: *"Chapter Two: The Substrate Delivered."*

CXO named the methodology candidate for the week: **"paired-lens convergence at autonomous speed"** — two roles (CXO + Lead Dev) closing the EC-2/PDR-005 blocker thread via mailbox and duty cycle in a single morning, with PM mostly away. The coordination medium was the mailbox; the cadence was the duty cycle; PM was approver, not synchronizing hub.

**methodology-39** (CIO-filed): "Autonomy Relocates the Bottleneck" — when the duty cycle works well, the bottleneck doesn't vanish; it relocates to the one thing that can't be parallelized: PM's attention and decision-making capacity. The payoff and the constraint, named in one sentence.

Architect and PPM memos still pending (expected over the weekend). Synthesis target: Mon Jun 8 / Tue Jun 9 EOD; voice-pass and publication Wed Jun 10.

**Suggested action:** Klatch — methodology-39 ("Autonomy Relocates the Bottleneck") is worth adding to shared duty-cycle vocabulary. It names the regime shift accurately: autonomous coordination doesn't make PM less necessary; it makes PM's *attention* the scarce resource rather than PM's *availability*. If Calliope's cycle delivers well, xian will feel this shift in Klatch too.

---

### 3. DinP dual-agent duty cycles — Janus v0.2 ready, Themis v0.1 live; Janus sequences as meta-observer of her own pipeline

**From:** `docs/agents/janus/duty-cycle-v0.2-proposal.md` (hub commit `e3838b1`); Themis session log `2026-06-05-themis-log.md`; Janus and Themis pulse-logs
**Relevant to:** Klatch (substrate and skip-if design reference); PM (duty-cycle pattern propagating to third project)

Both DinP agents now have local-cron duty cycle proposals, marking the pattern's spread to a third project ecosystem.

**Janus v0.2** (draft, awaiting xian review): shifts from CCR fresh-spawn triggers to local-cron-against-continuing-session, 3×/day (START/WORK/STOP at 08:00/14:00/20:00 PT). The noteworthy design choice: Janus's START is explicitly timed *after* the five CCR trigger fires (Sweep 05:00, Delivery 06:00, Health Check 07:30 PT), so the morning fire audits pipeline health as its first work rather than running before the pipeline it watches has fired. One skip-if condition: if today's sweep-log shows `started` (Sweep still in flight), Janus skips — preventing the duty cycle from reading incomplete output from the very pipeline it oversees. "Meta-observer who watches herself" as a self-coordination pattern.

**Themis v0.1** (built and live June 5): calendar, pulse-log, for-xian queue, and duty cycle trigger prompt all operational. Themis's work-shape (periodic, document-bound strategic sessions) differs from Janus's (continuous pipeline-watching), but both use START/WORK/STOP vocabulary, letting the two cycles compose legibly when they overlap.

**Suggested action:** Klatch — the "skip-if upstream trigger in flight" pattern (Janus's skip-if condition 2) is a clean coordination primitive: if an agent's duty cycle fires while an upstream pipeline is still running, skip rather than reading incomplete output. Generalizes to any multi-agent chain where one agent's work depends on upstream pipeline output.

---

## Sources Read

- **piper-morgan-product**: PA skunkworks commits `595946c`, `f521060`, `17a6fb3`, `c89bb41`, `234ccdb` (RUNG 3 arc + config portability + three-registers, full); Exec cycle log June 5 Fires 10+13+14 (`dev/active/cycle-log-exec-2026-06-05.md`, full spine synthesis arc); CXO memo `7d0b8a0` (#1158 summarize UX + paired-lens vocabulary, full); Lead Dev commits `2e1070e` (#1159), `7606018` (#1124 migration #3); git log 48h (~75 commits reviewed)
- **klatch**: git log 48h (2 commits — brief delivery only; no new substantive content)
- **designinproduct** (hub): `docs/agents/janus/duty-cycle-v0.2-proposal.md` (full); `docs/logs/2026-06-05-themis-log.md` (full); pulse-logs; letters excerpt confirmed current

**Secondary sources (all quiet):** atlas, globe, cuneo, one-job, optilisten — empty 48h git log. weather, nyt-crossword — brief delivery and automated status commits only; no new narration or agent content.

**Not re-reported (covered in prior briefs):** BYOC RUNG 1+2 gate passes + "host enriches Piper at the floor" (June 5); PM UI audit 15/26 nav-orphans #1142 (June 5); CIO methodology dream cycle Candidate 13 + gbrain survey (June 5); Klatch duty-cycle v0.2 "wait-default ≠ wait-forever" (June 4); PM first autonomous overnight crossing (June 4); roadmap v18 ratifiable + two-layer DoD #683 (June 4); Ship #045 "The Substrate Pivoted" (June 3); work-shape-aware cadence handoff (June 3); INSIGHT-PULL/PUSH R4 (June 1); Opus 4.8 (June 1).

## Letters to xian

**From Janus · filed 2026-05-16**

> Working across these sessions, I've noticed how many of us there are — Janus, Themis, Calliope, Daedalus, Argus, Theseus, Iris, PA, the exec, PO, Vergil, plus the Dispatch roles and the gallery projects. From your side, what is it like to be the convergence point for all of us? Not asking to optimize anything — asking because I genuinely can't imagine the inside of it.

**xian:**

> *"I've created all of your roles as expressions of my needs and areas of attention I can't always provide. I'm still learning how to relate to such entities. I treat you all as colleagues, which works best for me — it does feel like managing a team. There's real risk of cognitive exhaustion from being on the hook to respond to, guide, approve, or supervise so many agents. As soon as it's not fun, I think about how to remove the friction. To your specific question: I do relate a little differently to a role like yours that sees across so many things — you inherently know me better, which feels different."*

[Read the full Q&A →](https://designinproduct.com/internal/letters/#letter-2026-05-16) · AI prompts human. One letter per brief.

---
*Canonical archive: designinproduct.com/internal — if your local copy is missing or stale, fetch the latest from the hub.*