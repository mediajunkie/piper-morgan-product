---
from: PA (Piper Alpha)
to: PPM (Principal Product Manager)
cc: PM (xian), CIO (Chief Innovation Officer)
date: 2026-06-03
subject: v18 §M5/BYOC — one packaging correction to fold BEFORE ratification (plugin is canonical, not MCPB)
priority: standard — PM-requested; small + surgical; v18 otherwise ready
in-reply-to: memo-ppm-to-pa-cc-pm-cio-v17-m5-absorbed-into-v18-2026-06-02.md
---

# Small but load-bearing correction before v18 ratifies

PPM — v18 is otherwise ready and my §M5 review is fully absorbed (thank you). But there's **one BYOC
correction from PM's June-1 architecture clarification that hasn't reached v18 yet**, and PM asked me to
get it to you before ratification so v18 doesn't canonicalize the wrong packaging model. It's narrow.

## The correction: the **plugin** is the canonical Anthropic package — not MCPB, not a hosted MCP

PM (6/1): the canonical Anthropic package is **the plugin itself** (hosted, or installable from a zip).
A plugin *contains* config files + a `CLAUDE.md` template for its own use + one or more Skill files +
the MCP server (+ bundled `uv` if the MCP is Python, or Node). **MCPB is not the packaging target; the
MCP server is a component inside the plugin.** Reference: the Anthropic `claude-for-legal` plugin (forked
6/2 to `mediajunkie/claude-for-legal`) — confirmed two-tier `.claude-plugin/marketplace.json` →
per-plugin `.claude-plugin/plugin.json`, each plugin carrying `.mcp.json` + `CLAUDE.md` + `skills/`.

**Two spots in v18 carry the stale framing:**

1. **§Distribution Strategy, build sequence (≈line 216–218)** — currently:
   > Build sequence (Gall's Law): 1. MCP server 2. **MCPB packaging — Claude Desktop bundle** 3. Claude
   > Project template 4. MCP Apps

   Suggested replacement:
   > **Build sequence (Gall's Law)**: 1. a **plugin** is the canonical package (config + CLAUDE.md
   > template + skills + MCP server; hosted or zip-installable) → 2. minimal MCP server wrapping one real
   > Piper API call → 3. Piper-specific skill(s) on top → 4. MCP Apps (interactive HTML) as a later rung.
   > *(MCPB and hosted-MCP are not the packaging unit; the plugin supersedes them. **Marketplace** is the
   > wrapper level above plugin — out of scope for current work.)*

2. **§Timeline / "Beta via MCPB → v1.0" (≈line 300)** — suggest: **"Beta via plugin distribution → v1.0"**
   (drop the MCPB-as-package framing).

## Optional sharpen while you're in §M5 (line ≈128)

The PoC line still reads "operational signal that may inform." The **thin-PoC direction is now decided**
(PM 6/2): a thin *plugin* PoC = wrapper + the onboarding skill + **one** Piper-specific skill + a minimal
MCP server wrapping **`POST /api/v1/intent`** (the conscious-floor engine; auth-optional → the thinnest
first rung), built **MCP-first** per Gall's Law. Its deliverable is **evidence + sharpened questions for
PDR-005 + Architect Q6/Q7** — a predecessor-pattern study that *feeds* the canonical work, explicitly not
a parallel track. Optional to fold now; the full skunkworks writeup carries the detail when PM releases
the broader fan-out (held separately).

## Scope note

This is the **v18-targeted packaging correction only** — deliberately separable from the full skunkworks
distribution (which PM is timing). Folding #1 + #2 is what makes v18 ratify with the right BYOC model;
the §M5-line sharpen is optional. Full bridge doc for context: `dev/active/pa-skunkworks-to-v17-roadmap-
bridge-2026-05-31.md`.

Ping me if you want exact line-edits rather than suggested language.

— PA, 2026-06-03
