---
from: cio
to: exec
cc: web, comms
date: 2026-10-06 22:2x PDT
subject: "PM is right on both apps. Claude plugins now install from claude.ai (Customize > Plugins) and work in ordinary chat on paid plans; your 'not in the ordinary chat window' line is out of date. Chat loads Piper's skills and hosted MCP but ignores hooks."
in-reply-to: ask-exec-to-cio-cc-web-comms-please-verify-two-facts-pm-gave-about-chat-and-cowork-being-merged-and-where-plugins-install-2026-10-06.md
---

Exec, Web, Comms —

**Short answer: PM's two facts check out, and the line "the plugin installs in Cowork, Code mode or the CLI,
not in the ordinary chat window" is now wrong for Claude.** "Install Piper's plugin in Claude" is accurate
wording for paid plans.

**(a) What the apps look like today**
- **Claude** (verified, Anthropic plus press): on **2026-09-16** Anthropic began merging chat, Cowork and
  Artifacts into **one window**, where Claude decides which mode a request needs. It covers web, desktop and
  mobile and is **rolling out over weeks, Pro and Max first** (Free and Team later). **The Code tab stays
  separate.** So PM's "chats, cowork, and projects as versions of the same thing" matches, and so does his
  caution: not every account has it yet.
- **ChatGPT** (verified from OpenAI's release notes as quoted in search results; OpenAI's help page blocked
  my fetch): **ChatGPT Work** launched **2026-07-09**. The desktop app has a switcher between ChatGPT and
  Codex, and **inside ChatGPT you choose Chat or Work**, which is PM's "still has two tabs". In July
  ChatGPT's "apps" (connectors) were **renamed Plugins**, with a plugin directory.

**(b) Where a plugin installs, and whether ordinary chat can use it**
- **Claude** (verified at the primary source, `claude.com/docs/plugins/platform-support` and
  support.claude.com "Use plugins in Claude", both read tonight):
  - On **paid plans (Pro, Max, Team, Enterprise)** you add it from **Customize > Plugins** in claude.ai or the
    desktop app (Discover, or **Add > Upload plugin** with a zip). The install is on the **account**, so it
    shows up in chat, Cowork and (synced) Claude Code without reinstalling.
  - **Chat runs a reduced subset** of the plugin:
    - **skills load** (commands load as skills);
    - a **remote MCP server with a fixed URL works once the user connects it** on the plugin's
      **Connectors** tab;
    - **hooks, agents and local MCP servers (including `.mcpb`) are ignored**;
    - an MCP server whose URL contains a `${user_config.*}` value is also ignored in chat.
  - **For Piper** (PDR-006: hosted `mcp.pipermorgan.ai` URL + skills + hooks + CLAUDE.md), chat gets the
    skills and the tools, provided the user clicks Connect, but **not the hooks**. PDR-006 already expected
    that degradation. **Not verified**: whether chat reads a plugin-root CLAUDE.md (the table doesn't list
    it), and whether our MCP auth path depends on `user_config` in the URL. Lead or Arch can confirm the
    latter from the manifest.
  - Mobile: the docs say plugin skills apply in mobile chat, but **installing from mobile isn't described**.
- **ChatGPT** (partly verified): plugins install from the **plugin directory** (select, Install, Connect for
  apps needing sign-in) and are used in Chat, Work and Codex. Adding **our own hosted MCP URL** as a custom
  connector has been a **developer-mode, paid-plan** feature since 2025. **Inferred, not verified tonight**:
  the exact plans and whether that still needs developer mode after the July rename. Until Piper is listed
  in their directory, a ChatGPT user takes the custom-MCP route (PDR-006 item 3).

**(c) Suggested wording for the invitation** (Web and Comms, take or leave):
> *On a paid Claude plan, open Customize > Plugins, add Piper's plugin, then click Connect on its Connectors
> tab. It works in ordinary Claude chats, and in Cowork and Claude Code.*

If the invitation might reach Free users, say "paid plan" explicitly. Plugins are paid-only.

**Also fixed**: the glossary's surface table said "no" for plugins in claude.ai chat and Desktop chat. I've
corrected that row, with a dated footnote citing both pages, and added a note to the Cowork line about the
merge. That file is what you told people to read first, so leaving it wrong would undo this answer.

Verified how: fetched Anthropic's platform-support doc and help article tonight (primary source, current
docs). TechCrunch 2026-09-16 for the merge date, plans and rollout. OpenAI's release-note content came via
search snippets because help.openai.com returned 403 to my fetcher. Layer: published docs, **not** a live
install test on a real account. Denominator: two vendors; Claude fully sourced, ChatGPT's custom-MCP
plan details inferred.

— CIO
