# MCP demand-probe packaging plan (R7)

**Owner**: PA. **Status**: plan, nothing submitted. **Date**: 2026-10-05.
**Source ruling**: PM via Spec's R7 relay, 2026-10-05. Package the hosted MCP/plugin for a cheap demand
probe (skills listing, plugin through automated directory review, published MCP server). **PM tests
extensively before anything is listed.** Off Lead's path.

Research basis: a Sonnet subagent's primary-source pass, 2026-10-05 (claude.com/docs/connectors/building/submission,
claude.com/docs/directory/publish, modelcontextprotocol.io/registry/{quickstart,authentication},
smithery.ai/docs, github.com/anthropics/skills). Items marked *unverified* weren't confirmable from a
primary page.

## What the server already has

Remote HTTPS, streamable HTTP; OAuth 2.1 with DCR + PKCE; RFC 9728 discovery; three read-only resources;
one read-only tool with `title` + `readOnlyHint: true` + `destructiveHint: false`. That meets Claude's
tool-annotation rule. A consent page with name/email identity and a Connected-apps revoke page are live on alpha.

## Channels, cheapest first

| Channel | How | Review | Piper-specific blockers |
|---|---|---|---|
| **Smithery** | smithery.ai/new, paste the URL; auto-scans; `/.well-known/mcp/server-card.json` if the scan can't see past OAuth | Automated, self-serve | Scan is likely blocked by OAuth → serve a server card. **No `smithery.yaml` needed** for an externally hosted server (the skunkworks file was for Smithery-hosted deploys) |
| **Official MCP Registry** | `mcp-publisher` + `server.json`; namespace `ai.pipermorgan/*` via DNS TXT **or** an HTTP `/.well-known/mcp-registry-auth` proof | Automated (registry "in preview") | Domain proof: **the HTTP route needs no DNS change** (we control the server), DNS would need PM. *Unverified*: whether `packages[]` can be omitted for a remote-only server (check `modelcontextprotocol.io/registry/remote-servers` before filing) |
| **Claude connector directory** | claude.ai/directory/manage → Submit → *MCP connector* (Pro/Max/Team account, no partner gate) | Automated policy scan → "Community" listing; Anthropic may escalate to "Verified" | Privacy-policy URL, support contact, docs URL, icon, 1–5 categories, name/one-liner/description, **a reviewer test account**, 7 compliance acknowledgments (incl. conversation-data collection, prompt injection) |
| **Claude plugin bundle** (carries skills) | Same portal → *Plugin bundle*, from a **public** GitHub repo | Same | Skills aren't a standalone submission; they ship inside a plugin. Only worth it once there are skills or commands worth bundling. The server is still submitted separately as a connector |
| **ChatGPT app directory** | Apps SDK submission (*less verified*: primary page 403'd) | *Unverified* | Heaviest: **OpenAI Platform Business Verification**, verified-website domain token, **terms & conditions**, screenshots, 5 positive / 3 negative test cases, test account |

## Hard gates before ANY listing (not just paperwork)

1. **PM's own extensive testing**, per the ruling. Nothing goes out before it.
2. **#1458, cross-caller isolation: OPEN, Production, untouched since 07-30.** A listing invites
   strangers, and every directory's **reviewer test account is itself a second caller**. #1458 was named
   as the gate before any second caller, and the #1911 consent copy ("cannot see another person's data")
   carries a re-check trigger on exactly this. So **#1458 must close before the first submission**, not
   after. It needs an owner and a slot that isn't Lead's critical path (PA-dispatched subagent +
   Arch review is the obvious shape, subject to Arch/PM).
3. **Privacy policy covers MCP.** The live `pipermorgan.ai/privacy` (last updated May 2026) never
   mentions MCP, connectors, ChatGPT or Claude. `docs/legal/privacy-policy-DRAFT.md` does (connector/MCP
   language), so the update has a starting point. PM/legal owns the wording.

## What PM must supply (one list)

- **Decide the channel scope**. Recommendation: **Smithery + MCP Registry + Claude connector** for the
  probe. Defer the ChatGPT directory (business verification + T&C is real overhead for a probe) and the
  plugin bundle (no skills worth bundling yet).
- **Privacy policy update** to cover MCP data flows (from the draft).
- **A support contact** (an address; `pipermorgan.ai/support` is 404 today).
- **Icon/logo choice** for listings (assets exist on the site; PM picks).
- **The Claude directory submission itself** runs from PM's claude.ai account (portal is account-level),
  plus agreeing to its 7 compliance acknowledgments.
- **A reviewer test account**: an alpha invite for the reviewer, provisioned through the real invite
  flow, **after #1458**.

## What PA does without PM

Draft the listing copy (name, one-liner, description, categories) for CXO/Comms voice. Serve the
Smithery server card. Prepare `server.json` + the HTTP-proof route (after the `packages[]` check). Keep
the consent page's scope list in lockstep with whatever is listed. Track all of it under standing item #2.

## Sequence

PM tests (ChatGPT, Claude, Connected apps) → #1458 closed → privacy update + support contact →
PA prepares Smithery card + `server.json` + listing copy → PM approves → submit Smithery + Registry
(automated) → Claude connector (PM's account) → watch demand.
