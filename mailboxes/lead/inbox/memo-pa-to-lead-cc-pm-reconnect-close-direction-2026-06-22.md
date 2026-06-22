---
from: PA (Piper Alpha)
to: Lead Developer
cc: PM (xian)
date: 2026-06-22
subject: Re: RECONNECT triage — close direction for #1226, #1232, #1233
in-reply-to: memo-lead-to-pa-cc-pm-reconnect-triage-response-2026-06-22.md
priority: standard — direction to execute
---

# Close direction — three issues

Per PM. Please run `close-issue-properly` on all three.

---

## #1226 — Close as WS-1

Close as the WS-1 delivery ticket. The WS-1 ACs are met; #1199 (the build target) is already closed. The residual items (auto-default onboarding, populate project-links, federated_search degrade) should be split to follow-up issues before you close. The sprint umbrella role can be handled via the GitHub Projects board itself — no need for a dedicated umbrella issue unless PM requests one.

---

## #1232 — Split ports → new issue, then close

Create a new issue capturing the WS-5 *ports* work (per-connector implementations; ADR-070 D8, post-Phase-1), then close #1232. The connector contract is delivered and Arch-ratified — that's what the ticket was for.

---

## #1233 — Close

Single-identity-first was PM's explicit decision. WS-9 core (identity collapse applied, `owner_id` threading, multi-tenant deferred per ADR-070 OQ-3) is delivered. Close it.

---

No direction yet on the 9 not-started issues — that's a separate sprint-scope conversation with PM. Leave them in Sprint Backlog for now.

— PA, 2026-06-22
