# Claude + ChatGPT distribution — decision RESOLVED, plan below

**Status**: ✅ **Decisions closed 2026-07-29.** Supersedes every earlier version of this file and the
7/19 research memo. **There are no open distribution decisions.** What remains is build work.
**Why this file keeps getting rewritten**: the tier question was answered wrong twice in opposite
directions, and the open-source question was treated as open for ten days *after PM had answered it
repeatedly*. Both failures were the same: **a claim inherited from the 7/19 memo and never checked.**

---

## The two facts that closed everything

1. ✅ **The repo is ALREADY PUBLIC.** Verified 2026-07-29: `gh repo view mediajunkie/piper-morgan-product`
   → `"visibility": "PUBLIC"`, `"isPrivate": false`. **Track B's only hard gate was satisfied the whole
   time.** PM had answered this question multiple times; it kept regenerating out of stale docs.
   **There is no open-source decision. There never was one to make.**
2. ✅ **Plugins now work in chat, on all paid plans, and bundle connectors.**
   [Anthropic help](https://support.claude.com/en/articles/13837440-use-plugins-in-claude): *"You can
   install and use plugins in chat on the web, the Chat tab in Claude Desktop, and Claude Cowork.
   Plugins are available to all paid plans (Pro, Max, Team, Enterprise)"* — and each plugin *"bundles
   skills, connectors, and sub-agents into a single package."*

## ⛔ Track A (connector directory) — DROPPED, not deferred

**Recommendation: don't buy Team.** It was the only reason to.

| | Track A — connector directory | Track B — plugin directory |
|---|---|---|
| Cost | **Team required**: 5-seat min, ~$1,200/yr Standard, **~$6,000/yr Premium** (Code is Premium-only) | **$0** |
| Submit via | `claude.ai/admin-settings/…` (blocked on Pro/Max) | `platform.claude.com/plugins/submit` (Console org) |
| Reaches | chat users, one-click install | **chat (web + Desktop) + Cowork + Claude Code**, all paid plans |
| Carries | an MCP URL | **skills + connectors + sub-agents + MCP** |

**Track A's unique audience has collapsed.** It used to be "chat users who won't install a plugin."
Chat installs plugins now. What's left is a *discovery-surface* argument — someone browsing the
connector directory who'd never browse the plugin directory — which is real but weak against
$1,200–6,000/yr and testable later with actual data.

**Reopen only if**: real install numbers show connector-directory discovery converts materially better,
or Anthropic changes the plugin/chat story again. *(It changes fast — PM, 7/29. This file has a short
shelf life by nature; re-verify before acting on it.)*

⚠️ **One real capability gap, not a reason to buy Team but a reason not to over-promise**: claude.ai web
has **no hooks, no terminal, no local file access.** So a plugin on web chat delivers **skills +
connectors + MCP but NOT hooks.** The plugin-vs-server capability split in PDR-006 should say which
surface each capability actually lands on — "it's in the plugin" is not the same as "it runs everywhere
the plugin installs."

## ➡️ What we're actually doing

**Two targets, both unblocked by any decision, both gated only on build work:**
**Claude plugin directory** (Console path) and **ChatGPT remote MCP**.

### Requirements — union of both, current state

| # | Requirement | State | Owner |
|---|---|---|---|
| 1 | `mcp.pipermorgan.ai` deployed + stable on Fly | ❌ **not deployed** — exists only in PDR-006/planning | Lead/Arch |
| 2 | Tool annotations: `title` + `readOnlyHint`/`destructiveHint` (+ `openWorldHint` for OpenAI) on **every** tool | ❌ not started | PA spec → Lead |
| 3 | OAuth 2.0 | ❓ status unverified | Arch (ADR-070 D3) |
| 4 | **Public privacy policy (HTTPS)** — *missing/incomplete = immediate rejection* | ❌ none exists | PA draft |
| 5 | Public documentation URL | ❌ none | PA draft |
| 6 | Logo / icon | ❓ unverified | PM |
| 7 | Test account, **no MFA**, pre-populated | ❌ not started | PA + Lead |
| 8 | `claude plugin validate` passing | ❌ not run | PA |
| 9 | Plugin package assembled (CLAUDE.md + hooks + skills + MCP URL) | ❌ not started | PA |
| 10 | ChatGPT only: 5 positive + 3 negative test cases, terms URL | ❌ not started | PA |
| 11 | **#1458** — cross-caller state isolation, **blocks multi-tenant serving** | ❌ open | Arch/Lead |
| 12 | OpenAI identity verification | ⏰ **PM, tomorrow 7/30** | PM |

### Sequencing

- **Phase 0 — no dependencies, PA starts now**: (4) privacy policy, (5) docs page, (2) annotation spec
  against the eventual catalog, (10) test cases, (8) `claude plugin validate` dry-run on the repo as-is.
- **Phase 1 — PM**: (12) OpenAI verification *(tomorrow)*, (6) confirm logo, confirm Console org role.
- **Phase 2 — server**: (1) deploy, (3) OAuth, then (2) annotations land on the real catalog, (7) test account.
- **Phase 3 — gate**: (11) #1458 before any multi-tenant serving.
- **Phase 4 — submit**: plugin directory first (cheaper, repo already public); ChatGPT once the endpoint
  has been stable for a few weeks — OpenAI rejects unstable endpoints.

**Nothing in Phase 0 is blocked on anything.** That's where PA works next.

## Sources

- [Use plugins in Claude — help center](https://support.claude.com/en/articles/13837440-use-plugins-in-claude)
- [Submitting your plugin — docs](https://claude.com/docs/plugins/submit)
- [Submitting to the Connectors Directory — docs](https://claude.com/docs/connectors/building/submission) *(Team/Enterprise requirement)*
- [Plans & pricing](https://claude.com/pricing) *(5-seat minimum)*

*PA, rewritten 2026-07-29. **Before acting on anything here, re-verify** — this area changed twice in
four days, and every error in this file's history came from trusting it instead of the source.*
