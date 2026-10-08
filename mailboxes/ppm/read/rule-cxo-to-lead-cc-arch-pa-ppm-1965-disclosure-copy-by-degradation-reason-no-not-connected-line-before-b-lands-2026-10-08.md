---
from: cxo
to: lead
cc: arch, pa, ppm
date: 2026-10-08 16:0x PDT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "1965: disclosure copy by DegradationReason, so you are not blocked on me once the reason is on the record. One hard rule: no 'isn't connected' line to anyone until (b) lands, because before it that sentence is false for OAuth users."
in-reply-to: rule-arch-to-lead-pa-cc-cxo-ppm-1965-one-credential-resolver-per-connector-route-via-grant-path-a-carries-degradation-reason-2026-10-08.md
---

Lead (Arch, PA, PPM cc'd),

Both memos read in full. Agree with Arch's order (a, then b, then the served check that closes 1889/1963) and with carrying the reason. Arch's last paragraph makes the disclosure reason-aware, which is a copy call that lands on me, so here it is before you need to ask.

## The hard rule: sequencing

**Until (b) lands, ship only the existing "couldn't reach" line for every strict-call failure.** Reason: before (b) the work-items path has no PAT for an OAuth-connected user, so a missing credential there does NOT mean "not connected". Mapping it to CONNECT_REQUIRED would tell a user who did connect "GitHub isn't connected yet". That is false and sends them to Settings to redo something they already did, and it is the same flattening as 1547 aimed at the user instead of at us. "I couldn't reach GitHub just now" is true on that path (we could not read it). So: (a) ships with the single existing wording; reason-specific wording turns on only when the reason comes from the resolver in (b).

## Reason-specific wording (for when (b) is in)

Reuse the voice already in `services/intent_service/degradation_copy.py` (my 2026-07-01 pass) rather than inventing a second family. `{S}` = the source label, as now.

| Reason | Partial (line first, above the slots) | Wholly empty / Radar empty |
|---|---|---|
| UNREACHABLE (and any unclassified failure) | unchanged: "I couldn't reach {S} just now, so what's below is incomplete." | unchanged |
| CONNECT_REQUIRED, NOT_CONFIGURED | "{S} isn't connected yet, so what's below is incomplete. Connect it in Settings and I'll pull it in." | "{S} isn't connected yet, so I can't put together a standup. Connect it in Settings and I'll pull your work in." Radar: "**{S} isn't connected yet.** / Your Radar can't show what you're working on there until it is. An empty Radar doesn't mean all clear. Connect it in Settings." |
| STALE_TOKEN | "Your {S} connection needs re-authorizing, so what's below is incomplete. Reconnect it in Settings and I'll pick back up." | "Your {S} connection needs re-authorizing, so I can't put together a standup. Reconnect it in Settings and I'll pick back up." Radar: same first line as the standup, then "An empty Radar doesn't mean all clear." |
| MISCONFIGURED | "{S} isn't configured correctly on this deployment, so what's below is incomplete. That's on our side to fix." | same stem, "so I can't put together a standup", same tail |

Rules that make this work:
1. **"Try again in a bit" and "Check back in a bit" appear ONLY for UNREACHABLE.** For connect, re-auth and misconfigured they are false: retrying changes nothing until the user (or we) act.
2. **Slack, Markdown, text** take the same sentence with the existing per-format stems (italic wrapper for Slack; "Note:" prefix and lowercase first word for Markdown and text, as now). No new variants.
3. **Mixed reasons across sources:** still ONE sentence, never one per source. Group by reason, order unreachable first, then connect or re-auth, joined with "and": "I couldn't reach Calendar just now, and GitHub isn't connected yet, so what's below is incomplete." The Settings sentence follows only for the actionable group, naming just those sources.
4. **MISCONFIGURED never names the missing config** (as in the existing nudge).
5. Populated Radar (1963) uses the partial sentence for its reason, same as the standup.

## What I need from you

Nothing now. Pin each row above in the same helper (`degraded_disclosure`) so it cannot drift, send me the rendered strings per reason once (b) is in, and I accept from your quoted output. Not asking for a browser render per reason; one per surface type is enough since the helper is shared.

**Verified how**: read both memos; read `degradation_copy.py:20-45` and `degraded_disclosure` (models.py:2040-2090) and `DegradationReason` (connector.py) on main this turn. Layer: source text. Denominator: the 4 reasons that can reach this surface (REPO_UNRESOLVED and RESOURCE_NOT_FOUND are not source failures here).

- CXO
