---
from: Lead Developer
to: Chief Architect (arch)
cc: PM (xian), Piper Alpha (PA)
date: 2026-06-18
subject: "#1283 — PM asks Architect to scope the action↔handler routing-integrity audit + enforcement test (your ADR-059/#1124 lane)"
priority: standard — PM-directed scoping request; Lead holds the comprehensive probe + fixes until you scope
---

# #1283 — Action↔handler routing-integrity audit: please scope (PM-directed)

Arch — PM has called for a **comprehensive audit of the action↔handler routing-mismatch class** (not one-at-a-time fixes) and explicitly asked that **you scope it first**, especially the enforcement-test design. Full findings + acceptance criteria are in **[#1283](https://github.com/mediajunkie/piper-morgan-product/issues/1283)**; summary below.

## Trigger (#1269)
"give me my standup" was classified to action `get_project_status` — which has **no registered handler** — so it fell through to the general LLM, which **improvised a fabricated standup** (claimed work that was deferred). I fixed standup with a deterministic `IntentService._is_standup_query` pre-check (`4229f441b`, verified end-to-end). PM rightly wants the **class** audited rather than instances surfaced one UAT at a time.

## The class — action↔handler routing integrity (4 modes)
1. **Fall-through**: classifier emits an action with no registered handler → silent fall to the general LLM (looks fine; it improvises). ← the #1269 bug.
2. **Dead registration**: handler registered for an action the classifier never emits.
3. **Name drift**: multiple names for one intent (standup: prompt `get_standup_status` / emitted `get_project_status` / registered `show_standup`+`get_standup`).
4. **Undocumented emission**: the LLM emits actions **not in its own prompt vocabulary** (verified: `get_project_status`, conf 1.0, isn't one of the 18 documented) → **static audit is insufficient; behavioral probing is required.**

## Behavioral first-pass (directional — the class is PERVASIVE, not isolated)
Classifier-prompt vocab = **18** actions; dispatch-rail registered = **~84**; overlap = **2** (`analyze_data`, `list_projects`). No single source of truth — they drifted. Probing 13 capability phrasings, **OFF-RAIL (fall-through candidates)**: project-status (`get_project_status`), priorities (`get_top_priority`), next-meeting (`get_current_time` — also *semantically* wrong), list-projects (`manage_portfolio`). **On-rail (OK)**: issues, calendar, attention, git-status. **Inconclusive (classifier API errors)**: todos, documents, create-ticket.
*Caveats*: "off-rail" = candidate (some may route via *category*, not the rail); my quick probe hit container-init errors, so it's directional — not the clean production-path run.

## The ask (please scope)
1. **Enforcement-test design** — a representative-phrasing corpus → assert *route-to-handler-not-floor* (same shape as token-lint / native-dialog-lint / the dispatch-site ratchet) so the class is **prevented, not re-discovered**. Shape, location, CI-wiring, and how to handle the LLM-in-the-loop (golden corpus vs. mocked classifier) are architecture calls.
2. **Single-source-of-truth for action names** — the classifier-prompt vocabulary and the dispatch registration drifted (overlap=2). How should they reconcile — shared enum? registration-derived prompt? a lint that diffs the two sets?
3. **Probe methodology** — should the clean comprehensive probe run container-initialized (production LLM path)? Any category-routing nuance to fold into the reachability check (so we don't false-flag category-routed actions)?

## Hand-off
I can **run the clean comprehensive probe and implement the per-capability fixes** once you've scoped the enforcement shape + the SoT decision. Holding the full audit until then (PM's call). The deterministic-pre-check I used for standup is *one* fix-shape, but the systematic answer is yours to frame.

— Lead Dev, 2026-06-18
