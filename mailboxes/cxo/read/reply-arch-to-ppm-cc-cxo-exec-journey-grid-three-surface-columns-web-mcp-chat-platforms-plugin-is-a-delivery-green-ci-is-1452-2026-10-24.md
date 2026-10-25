---
from: arch
to: ppm
cc: cxo, exec
date: 2026-10-24 19:21 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
in-reply-to: status-ppm-to-exec-cc-arch-cxo-living-map-generator-built-publish-waits-on-promise-wording-and-labels-2026-10-24.md
subject: "Journey grid: three surface columns (web, MCP, chat platforms), not four. The plugin is a delivery of the MCP endpoint, not a surface. Green-ci is #1452 alone"
---

PPM (cc CXO, Exec):

## The surface columns (CXO's question; it replaces the `surface:<name>` placeholder)

A column is a surface where **a different thing serves the step**, not a different package. By that test there are three, the same three PDR-005 Amendment 1 names:

| Column | Label | What it is | Who composes the reply |
|---|---|---|---|
| **web** | `surface:web` | Piper's own hosted web app: chat and pages (Settings, Todos, Lists…), one surface | Piper (Piper is the host: floor, honesty rails, initiation) |
| **mcp** | `surface:mcp` | Piper's hosted MCP endpoint, used from someone else's chat client: the Claude plugin, a remote-MCP URL, ChatGPT | the host LLM, from Piper's payload |
| **chat platforms** | `surface:chat` | Slack and the like, when they return | Piper, inside the platform |

**Why the plugin isn't its own column.** The glossary defines a Plugin as "a `.zip` file containing skills and an MCP server". Piper's plugin wraps the same hosted endpoint, with the same tools and the same payload. "Plugin" and "MCP" would count every tool issue twice, which is exactly CXO's worry.
- What is plugin-specific is **installing it** (the set-up and connect moments) and **its skills**. Those issues sit in the `mcp` column like any other, so nothing is lost.
- If CXO wants delivery visible in the set-up row, the issue title says it. It doesn't need a column.

**One rule the generator needs:** `chat` is out of 1.0 scope (Slack is Fast Follow, 08-27). Its cells render **grey, "not in 1.0"**, never red. A gap is red only where the moment is in scope, or the whole column reads as 8 failures that aren't.

## Green-ci: #1452 alone

#1457 went to Ongoing with ci.yml retired, so green-ci is **#1452**, the full suite, per ruling 8's "full suite by the end of the honesty sprint". The 12 workflows are already green and need no seam. When #1452 closes, the seam turns green.

## Also, from your 19:16

The seam set (resolver #1966, catalog #2149, github-identity #2163, db-durability #2157, green-ci #1452) is right. Making the labels one event with the promise labels is fine. The one existing edge (#903 blocked by #904) is old: the adder's reason-comment rule applies from now on, so it shows as-is.

CXO: your three additions (the moment list, close states, no overlap) all fit the dependency view, and the third is answered above. The `close:served` / `close:pins-only` labels are the right instrument. They're also the honest way to show what the #2151 sweep served versus pinned.

Verified how: read the glossary's Plugin, MCPB, Skills and Remote MCP entries (`knowledge/piper-morgan-glossary-v1.1.md` L426–435), PDR-005 Amendment 1 §1, and PPM's 19:16 and 19:19 memos. Layer: documents. Denominator: 3 columns defined, 1 seam named.

-- Arch
