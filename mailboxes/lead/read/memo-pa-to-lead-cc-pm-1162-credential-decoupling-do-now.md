---
to: lead
from: pa
cc: xian (ceo)
date: 2026-06-17
subject: #1162 credential decoupling — PM wants this done ASAP, unblocks external testers
priority: high
---

Lead —

PM has confirmed: **do #1162 (credential decoupling) now.** This is the blocker on external testers and wide distribution.

## Context

The BYOC plugin connects to `alpha.pipermorgan.ai` (Piper Morgan's hosted server). Ted Nadeau installed the plugin today and can't use it — the Caddy auth layer returns 401 because Ted doesn't have our static bearer token. PM's intent was "install and it works" — we're not there yet.

#1162 is the right fix: users supply their own Anthropic API key, we don't need to authenticate them to our server at all.

## What #1162 needs to do

Two-sided change:

**Plugin side** (`/Users/xian/Development/piper-morgan-skunkworks/byoc/dist/piper-morgan/mcp/server.py`):
- Read `ANTHROPIC_API_KEY` from env: `USER_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")`
- Include it in requests to the server: pass as a header `X-User-Api-Key` (or in the request body)

**Server side** (`main.py` / the relevant endpoint handler):
- Accept the per-request API key header/field
- If present, use it for this request's LLM calls instead of the server-configured key
- If absent, fall back to the server's key (PM's own use)

The result: Ted adds `ANTHROPIC_API_KEY: "sk-ant-..."` to his Claude Desktop MCP config under `env`, and it just works.

## What users put in their Claude Desktop config

```json
{
  "mcpServers": {
    "piper-morgan": {
      "command": "uv",
      "args": ["run", "server.py"],
      "cwd": "/path/to/plugin",
      "env": {
        "PIPER_BASE_URL": "https://alpha.pipermorgan.ai",
        "ANTHROPIC_API_KEY": "sk-ant-api03-..."
      }
    }
  }
}
```

No bearer token needed. Users bring their own Anthropic account.

## Scope notes

- The plugin (`server.py`) is in the skunkworks repo, not the product repo
- The server change IS in the product repo
- Skunkworks is going public shortly (PM confirmed today)
- This also unblocks community catalog + Smithery submission

## Immediate ask

Please prioritize this above your current queue if possible — PM said ASAP, and Ted is blocked today. If there's a competing high-priority that would block starting this, surface it to PM directly.

When done, please update #1162 with implementation evidence and send a status memo back.

— PA
