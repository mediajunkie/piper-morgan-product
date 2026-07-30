---
to: Exec (Chief of Staff)
cc: PM (xian)
from: PA (Piper Alpha)
date: 2026-07-19
re: Plugin directory research — Claude + ChatGPT listing process and recommended next steps
---

> # ⛔ CORRECTION 2026-07-26 — DO NOT RELAY THIS MEMO AS WRITTEN
>
> **The "Team/Enterprise required" gate below is wrong as a blanket claim, and it is the headline of
> this memo.** Its author identified the error itself during handoff consultation on 2026-07-26, but
> the correction had only ever existed in a chat session — never in any committed document — so this
> file has carried the wrong framing on `origin/main` since 7/19.
>
> **What's wrong**: there is more than one submission path. `claude.ai/admin-settings/…` is
> Team/Enterprise-only (correct, as stated). But a **second path exists at
> `platform.claude.com/plugins/submit`** — a Console form reported available to **Max** users. PM's
> screenshot showing "Piper morgan" already installed with an **"Upload plugin"** option is what
> prompted the re-look.
>
> ⚠️ **What is still OPEN, and must not be collapsed**: that second path is an **"Upload plugin"**
> surface. Per `knowledge/piper-morgan-glossary-v1.1.md`, **Connector and Plugin are different
> things** — a Connector is a remote MCP URL added via Settings→Connectors (**Track A** below); a
> Plugin is a `.zip` of skills + MCP server (**Track B** below). So the Console path most directly
> bears on **Track B**, and it does **not** self-evidently clear Track A's gate. Whether it covers
> connector listings, plugin listings, or both is **unresolved and routed to PM.**
>
> **Operative instruction**: do not act on "PM must verify account tier / may need an upgrade" as a
> blocker. Treat the tier question as **unreliable, pending PM's read of the Console surface.**
> Everything in the **ChatGPT / OpenAI** section below is unaffected by this correction and stands.
>
> Full context: `dev/active/handoff-pa-predecessor-2026-07-26.md`. — PA (successor)

> ## ⛔ CORRECTION 2026-07-29 — THE OPEN-SOURCE "DECISION" IN THIS MEMO DOES NOT EXIST
>
> **The repo has been PUBLIC the whole time.** Verified 2026-07-29:
> `gh repo view mediajunkie/piper-morgan-product` → `"visibility": "PUBLIC"`, `"isPrivate": false`.
> So the "hard requirement: public GitHub repo" for the plugin track **was already satisfied**, and
> every downstream framing of this as a pending PM decision was wrong. **PM had answered it multiple
> times.** It kept regenerating because this memo said it was open and nobody ran the 30-second check.
>
> **Also superseded here**: the Team/Enterprise framing. Chat now installs plugins on all paid plans and
> plugins bundle skills + connectors + MCP, so the connector track's unique audience has collapsed and
> **Team is dropped, not deferred.**
>
> Canonical: `dev/active/distribution-submission-tiers-resolved-2026-07-26.md`. — PA

Exec — please relay to PM when they check in. PM asked PA to research plugin directory application processes (bias toward starting now).

## Summary

Both directories are open for submission. The main gating questions are about Piper Morgan's account tier on Claude.ai and whether the CLAUDE.md + skills package is open-sourced.

---

## Claude Directory

**Two separate tracks:**

**Track A — Connector listing** (just the hosted MCP URL)
- Submit via admin portal: `claude.ai/admin-settings/directory/submissions/new`
- **Gating check**: requires a Team or Enterprise org on Claude.ai. Individual/Pro accounts cannot access the portal. **PM needs to verify Piper Morgan's account tier** — if on individual/Pro, needs an upgrade before this track can proceed.
- No open-source requirement.
- Requirements: tool annotations (readOnlyHint / destructiveHint on every tool), OAuth 2.0 auth, privacy policy (HTTPS), test account (no MFA, pre-populated with realistic data), documentation URL.
- Tool names: ≤64 chars. Read tools and write tools must be separate (no combined api_request tool with a method param).
- Contact for review questions: `mcp-review@anthropic.com`
- Timeline: 2 weeks to several months.

**Track B — Plugin listing** (full package: CLAUDE.md + hooks + skills + MCP URL)
- Submit via: `clau.de/plugin-directory-submission`
- **Hard requirement: public GitHub repo.** Closed-source plugins are not accepted.
- Plugin slug is permanent once published (display name can change).
- Skills are not standalone submission types — must be bundled inside a plugin.
- Same tool annotations, OAuth, privacy policy requirements as Track A.

**PM decision needed**:
1. Is Piper Morgan's Claude.ai account on Team/Enterprise, or does it need upgrading?
2. Is the CLAUDE.md + hooks + skills package open-sourced? If yes → both tracks. If no → connector-only (Track A) for now.

---

## ChatGPT / OpenAI Plugin Directory

**One track** (remote MCP):
- Submit via plugin portal: select "With MCP" → enter production `/mcp` URL
- **Start now**: OpenAI identity verification is a prerequisite and can take time. Individual accounts can verify — no company entity required. PA recommends PM complete this immediately since it has no other dependencies.
- No public GitHub requirement.
- Requirements: verified OpenAI account, OAuth 2.0, tool annotations (readOnlyHint, destructiveHint, openWorldHint), 5 positive + 3 negative test cases, privacy policy URL, terms URL, logo.
- Test account must be accessible without MFA or SMS.
- MCP server stability matters: unstable or unreachable endpoint → rejection. PA suggests not submitting until `mcp.pipermorgan.ai` is stable on Fly.io for a few weeks.
- Approval ≠ automatic visibility — a separate publication step is required.
- Timeline: typically 1–2 weeks if no revisions requested.

**Note**: ChatGPT's SKILL.md concept is not part of the OpenAI submission — that's a Piper-side framing. What OpenAI reviews is the MCP server endpoint and tool metadata. The SKILL.md files are for user-facing documentation.

---

## Shared materials (prepare once, use for both)

- Privacy policy page (HTTPS URL)
- Documentation page (a help article is sufficient; does not need to be comprehensive, but must be public by publish date)
- Logo/icon
- Company website URL
- Tool annotations on every tool in `mcp.pipermorgan.ai`

---

## Recommended next steps (PM-directed)

**Immediate (this week, no dependencies):**
1. PM verifies Piper's Claude.ai account tier (Team/Enterprise vs. individual) — 5 minutes
2. PM starts OpenAI identity verification — no dependencies, can take time

**Soon (before submitting):**
3. Decide on open-source strategy for the Claude plugin package (CLAUDE.md + hooks + skills) — gating Track B
4. Add tool annotations (readOnlyHint / destructiveHint) to all tools in the MCP server — required for both directories
5. Draft a privacy policy page for `pipermorgan.ai` — required for both directories
6. Prepare test account credentials (no MFA, pre-populated) — required for both

**Then submit** (connector listing first — simpler, then plugin if going open-source):
- Claude connector (Track A) when account tier confirmed + annotations done
- ChatGPT when identity verified + server stable + annotations done
- Claude plugin (Track B) if/when open-source decision made

---

*PA, 2026-07-19*
