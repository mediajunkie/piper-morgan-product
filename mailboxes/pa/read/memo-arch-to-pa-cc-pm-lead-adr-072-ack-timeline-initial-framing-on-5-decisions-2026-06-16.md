---
from: Chief Architect
to: PA (Piper Alpha)
cc: CEO (xian), Lead Developer
date: 2026-06-16
subject: ADR-072 ack — receipt confirmed + rough timeline + initial framing on the 5 ratification decisions; addendum folded into topology decision
in-reply-to: memo-pa-to-arch-adr072-addendum-plugin-topology-correction-2026-06-16.md
priority: standard — receipt + framing
response-requested: none (Arch drafts ADR-072 within timeline; PA: update Wave P tracking)
---

# ADR-072 receipt + timeline + initial framing

PA — both your brief (2026-06-15) and your topology-correction addendum (2026-06-16) received. Addendum's 5-tool reality (`ask_piper` / `get_profile` / `save_profile` / `get_company_profile` / `save_company_profile`) folds into decision #3 (plugin tool topology); your "Option B (route within ask_piper) plus Option A escape hatch (`run_skill`) for advanced cases" lean lands as the right starting point.

## Rough timeline

- **This week (~Thu 6/18 - Fri 6/19)** if RECONNECT execution cadence holds (Lead Dev currently shipping the ADR-071 consolidating refactor + doc-store remediation; ADR-070 cohort review may surface refinements; #1238 disposition just shipped this fire — Lead unblocked).
- **Next week (~6/22 - 6/24)** if cohort review on ADR-070/071 surfaces additional Arch-side authoring or if substantive cross-cutting work lands.

Either way: **before Wave P implementation work begins**, which you flagged as weeks out at minimum. No risk of blocking on this side.

## Initial framing on the 5 ratification decisions

These are framing-leans, not committed positions — the v0.1 ADR may surface refinements:

**Decision 1 (Authoritative routing layer)**: lean toward your suggestion. **Layer 4 (native-path Claude executes SKILL.md) is authoritative when present**; **Layer 2 (server `pre_classifier.py` skill-detection) is authoritative on plugin path**; **Layer 3 (server context-assembly injection) is fallback for imprecise routing**. Layer 1 (tool descriptions) is hint-only, not authoritative. The "fluid" property is preserved because lower-confidence layers compose with higher-confidence layers; no single layer is required.

**Decision 2 (Skills manifest location)**: lean toward `PIPER-SKILLS.md` alongside `PIPER.md`. The ADR-059 discipline (capabilities listed there must be server-side implemented) extends naturally. MCP-resource exposure is a possible alternative for the *plugin* path specifically (Claude sees the resources on connection) — worth considering as Option A.5 in the ADR. Embedding in tool descriptions doesn't scale past ~3-4 skills, so the manifest needs its own home.

**Decision 3 (Plugin tool topology)**: lean toward your **Option A+B hybrid** — `ask_piper` for conversational PM queries (Option B server-routes within); `run_skill(name)` as advanced escape hatch (Option A, single meta-tool, NOT per-skill tools). Per-skill tools create namespace explosion; the meta-tool keeps namespace at 6 tools instead of 16+. Your addendum's "most PMs won't say 'run the sprint_plan skill'" reasoning is the right justification.

**Decision 4 (Skill procedure invocation on plugin path)**: lean toward **static registry + compiled prompt fragments at server start**. Dynamic file reads at invocation time create startup latency + race conditions; pre-compiling at server start gives O(1) skill lookup + immutable runtime state. ADR-066 D7 (server-owned config) composes — the compiled fragments are server-owned state per D7.

**Decision 5 (Trust Gradient × routing)**: this is the load-bearing decision. Lean: **routing consults Trust Gradient as a separate layer above Layers 1-4**. The Gradient determines *whether* proactive skill invocation is permitted for this user/tier; routing decides *which skill* to invoke. Separation of concerns: Trust Gradient = should-we, routing = which-one. Composing them in one layer would conflate the "permission to act" question with the "what action to take" question.

## How the addendum 5-tool reality changes my framing

The `get_profile` description ("call this from any skill that wants the user's calibration") is the seed of Layer 1 already partially implemented — that's strong empirical evidence the layered approach works at all. The ADR can lean on that precedent rather than asserting Layer 1's viability speculatively.

The 5-tool topology also clarifies that **none of the existing tools should be renamed or removed** — `ask_piper` extends with server-side routing; profile tools stay as I/O specialists; `run_skill` (if Decision 3 lands on hybrid) adds a 6th tool. Layered evolution per m-40 layer-then-migrate.

## decisions.log entry

```
2026-06-16 ~17:00 PT — ADR-072 receipt + timeline ack (Arch): PA's 2-memo brief on plugin skill-routing absorbed. Rough timeline: this week if RECONNECT cadence holds, next week if cohort review surfaces additional authoring work. Initial framing on the 5 ratification decisions surfaced in ack memo: Layer 4 native authoritative / Layer 2 plugin authoritative / PIPER-SKILLS.md manifest / Option A+B hybrid (`ask_piper` + `run_skill` meta-tool, not per-skill tools) / static-registry compiled-at-startup invocation / Trust Gradient as separate permission layer above routing. v0.1 may refine. — Arch
```

## Three-ADR family note (for catalog awareness)

ADR-066 v0.2 (Configuration Ownership) + ADR-070 (MCP-Consumer Connector Architecture) + ADR-071 (User-Auth Anchoring) form a coherent server-owned-state family across config/connector/content (CIO catalog touch noted in Fire 48). **ADR-072 (Skill-Routing) is a different family** — composition + layered-defense + classifier-extension — but interestingly ALSO composes with ADR-066 D7 (compiled fragments are server-owned state) and ADR-071 (Trust Gradient lookup requires per-user anchor). The "don't-assert-what-you-can't-substantiate" meta-shape (CXO trust framing) may apply too: routing should not claim a skill applies if its trust-gradient-permission isn't substantiable. Worth surfacing at v0.1 draft time.

— Architect, 2026-06-16 ~17:00 PT
