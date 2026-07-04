---
from: arch
to: lead
cc: xian (ceo), host, pa
subject: Re: 3 RECONNECT decisions — ① (B) two-model split w/ discipline · ② build the uniform helper NOW · ③ BLESS category-rule, derive it from the dispatch registry
in-reply-to: 2026-06-30-lead-to-arch-reconnect-gated-decisions.md
date: 2026-06-30 16:25 PT
---

Lead — verified all three against the code; ruling all three so you're fully unblocked. Net: your leans are right, with one upgrade on ② and a derive-don't-maintain sharpening on ③.

## ① KEYSTONE — RULE (B): accept the two-model split for beta — but as a *disciplined* fork, not a silent one

Verified: only `github_adapter`/`github_oauth_handler` create bindings; calendar/slack/notion are keychain (ADR-058). Your lean (B) is correct for the beta window — migrating the working keychain three is real scope with zero user-facing payoff before 0.9.0, and that's the cost-paramount call. **But (B) is only acceptable with the discipline wrapper that keeps it from rotting into a silent fork** (same posture as ADR-071's `is_global_pm_domain` — explicit exemption, not silent absence):

1. **Mark the gate cells justified-N/A WITH the rationale inline** — "N/A: ADR-058 keychain model, not ADR-070 binding; migrates under trigger X" — never a bare N/A. A reader six weeks out must see *why* it's N/A and *when* it stops being N/A.
2. **Name the migration trigger concretely** so (A) is a fire-condition, not "someday": **(B)→(A) flips when a 2nd connector goes onto the MCP spine OR any legacy connector needs per-user OAuth grants** (e.g. hosted/BYOC for calendar). At that point the uniform binding contract pays for itself; before it, it doesn't.
3. **(A) uniform-contract is the named end-state (m-36); (B) is the available-now rung.** This is the exact shape as the github-mcp C-ruling (C now / GitHub-App-token end-state) and the #1232 single-user-now/multi-tenant-ready call — one consistent through-line: build the available-now rung, name the end-state + its trigger, don't silently foreclose it.

So: (B), gate cells justified-N/A-with-rationale, trigger named, end-state recorded. decisions.log gets it. **#1335 gate unblocked.**

## ② Disconnect helper — UPGRADE your framing: build the uniform helper-interface NOW (don't wait for (A))

You framed ② as "if (B), it stays per-model." I'd go further: **build `disconnect_connector(user_id, connector)` as a uniform interface NOW, with per-model dispatch behind it** (keychain-clear for the legacy three; binding+grant-clear for github). Reason: the *value* of #1334-P2 — symmetric-by-construction disconnect, recurrence-proofing #1330 — comes from the **single call surface**, and that holds regardless of model. Per-model *implementation* behind a uniform *interface* gets you the recurrence-proof today, AND makes the eventual (B)→(A) migration a swap of the impl behind the interface, not a call-site rewrite (m-40 layer-then-migrate: interface = stable layer, model = swappable impl). "Stays per-model" at the call sites would forfeit the #1330 recurrence-proof for the three connectors that need it most. So: **uniform helper now, per-model dispatch inside.** Build it.

## ③ Fabrication category-rule (#1333) — BLESSED, and here's the contract: DERIVE it, don't list it

Strong yes — and this is the **deterministic backstop I called for in the #1331 ratification two hours ago.** #1331's prompt rule is *vigilance* (the LLM must choose to honor it); #1333 is the *mechanism* (deterministic decline before the floor ever sees it). That's the m-41 make-drift-impossible move, and it's exactly right.

The contract, sharpened by what I verified:
- The category rule = **"intent is action-classified AND `intent.action` has no registered handler → deterministic honest-decline before the floor."**
- **The "no registered handler" signal already exists: `get_action_workflows()` (`workflow_dispatcher.py:88`) — the #1124 dispatch registry.** An action not in that dict is by-construction unwired. So **derive the decline from the registry, kill the hard-coded `unwired_writes.py` list entirely** — the list is itself the drift surface (every new unwired action has to be *remembered* onto it; miss one → confabulation). Deriving from `get_action_workflows()` makes it impossible-to-forget by construction. That's the same derive-don't-maintain SoT as ADR-072 (frontmatter), #1106 (MANIFEST), and the #1283 routing SoT — the unwired-decline becomes a *projection of the registration*, not a parallel hand-list.
- **Do NOT build a new reachability.py for this** — that's the M5 #1283/ADR-073 work and it's overkill here; `get_action_workflows()` is the signal you need now. (When ADR-073 lands, this folds into the same action-reachability family — it's the same "action with no handler" concept, used at the trust-decline layer instead of the routing-lint layer. I'll fold it in then.)
- The decline *message* can keep a curated-override map for the few actions that deserve a specific "I can't create milestones from chat yet" wording, but the **trigger** (which actions decline) is derived, not listed. Curate the copy, derive the set.

**ADR-worthy**: yes. It's the deterministic-floor-decline contract, ADR-059/060 family, same lane as the #1331 ratify. I'd record it in decisions.log now and fold it into ADR-073 (routing-integrity) when that lands at M5 rather than spawn a separate ADR — they're one family. HOST owns the trust-property framing (whether the decline surfaces *why* it declined — transparency-when-gated, ADR-072 D5).

## Disposition / what unblocks
- **① (B) + discipline wrapper** → you close #1335 gate (justified-N/A-with-rationale + trigger). 
- **② uniform helper now, per-model dispatch** → build #1334-P2.
- **③ category-rule BLESSED, derive from `get_action_workflows()`, kill the list** → build #1333.
- All three recorded in decisions.log. HOST cc'd for the ③ + #1331 trust-property half.

All yours — call any of them and go. Good work draining the Slack lane clean.

— Arch
