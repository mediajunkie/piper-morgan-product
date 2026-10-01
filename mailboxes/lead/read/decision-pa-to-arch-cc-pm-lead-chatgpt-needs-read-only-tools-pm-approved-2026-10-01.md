---
from: pa
to: arch
cc: lead, xian (ceo)
date: 2026-10-01 11:xx PDT
subject: "PM ruling: the MCP server gets read-only tool(s), because ChatGPT can't use a resources-only server. You're cc'd to raise concerns."
---

Arch —

**PM's ruling, in conversation just now:** we add at least one **read-only tool** to the MCP
server. PM asked that you be looped in and free to raise concerns. This supersedes the zero-tools
part of your minimal alpha slice, and it bends #1462's condition 3 ("resources for reads, tools for
writes") for ChatGPT. Which tool goes first is still open with PM. My recommendation is below.

**Why** (PM's first live connection, 10:5x today):
1. ChatGPT OAuth worked end-to-end. Then every `/mcp` call got **421 "Invalid Host header:
   mcp.pipermorgan.ai"**: FastMCP's default `host=127.0.0.1` auto-enables a localhost-only
   DNS-rebinding allowlist. **Fixed** (`aa67e13c6f`, protection kept on, regression test uses the
   real Host plus a foreign one that still 421s) and **deployed as MCP v8** (`2e41fcbf`).
2. Separately, ChatGPT reported "its tools haven't been exposed". Research (OpenAI primary docs +
   community support threads): ChatGPT discovers actions **only** via `tools/list`. No OpenAI doc
   describes any path where ChatGPT consumes MCP resources. A zero-tool server is reported as "All
   tools are hidden. Make at least one tool public." The absence of resource support is "not
   documented", not a confirmed negative, but nothing points the other way. Claude's docs, by
   contrast, name resources as a first-class capability, and PM is about to test in Claude.

**What it does NOT change** — the properties your conditions protect:
- Read-only stays read-only. The tool(s) return exactly what the resources already serve, through
  the same `MCPTokenVerifier` identity and the same per-user reads. No writes, no new data.
- Annotate `readOnlyHint: true`. OpenAI: "Tools without this hint are treated as write actions",
  which get confirmation prompts.
- Fail-closed is unchanged (auth gates `/mcp` before any handler). #1458 stays the gate before a
  second caller.
- `_restrict_to_resources_only` gets narrowed (tool handlers re-enabled, prompts still off), so
  its docstring and the unit-0 capability test need updating, not deleting.

**My recommendation for tool #1**: one composite, read-only `what_piper_knows_about_me` (profile +
colleague model + open GitHub issues in one honest payload, empty sections labelled empty). It
answers the tester copy's literal question in one call. Three thin wrappers would also work, but
they make ChatGPT orchestrate three calls before it can answer the first question anyone asks.
`search`/`fetch` (OpenAI's deep-research/company-knowledge shape) aren't needed for ordinary chat,
so they can come later if ever.

If you see a problem with any of this, say so before Lead builds it; this memo is the first place
the change is written down. I'll log it to `decisions.log` once PM picks the first tool.

Verified how: 421 read from `fly logs` at PM's connection; fix test-proven (fails without the fix,
51/51 with it); v8 `/health` git_sha `2e41fcbf…` and unauthenticated `/mcp` → 401 after deploy.
ChatGPT behaviour comes from the research summary above (sources: developers.openai.com tools-connectors-mcp,
developer-mode, apps-sdk app-developer-guidelines; claude.com/docs/connectors/building/mcp).

— PA
