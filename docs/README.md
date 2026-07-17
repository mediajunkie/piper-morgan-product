<img src="assets/images/pm-logo.png" alt="Piper Morgan Logo" width="200" />

# Piper Morgan

**An AI-powered product management assistant — and an experiment in human-AI collaboration.**

Current version: **v0.8.11.0 alpha** · [pipermorgan.ai](https://pipermorgan.ai) · [GitHub](https://github.com/mediajunkie/piper-morgan-product)

---

## What Piper Morgan does

Piper Morgan is a conversational PM assistant that connects to the tools a product manager already uses — GitHub, Notion, Slack, Google Calendar — and helps make sense of them together. Ask it what's blocking the sprint, surface what needs attention today, or get a morning standup that says what's actually happening rather than what the last person to update a ticket said was happening.

It's built by a team of AI agents working alongside a human PM. That's both the product and the point.

---

## Alpha testing

Piper Morgan is currently in **invite-only alpha** at [alpha.pipermorgan.ai](https://alpha.pipermorgan.ai).

If you're part of the alpha:

- **[Alpha Quick Start](ALPHA_QUICKSTART.md)** — get running in a few minutes
- **[Testing Guide](ALPHA_TESTING_GUIDE.md)** — what to test and how to give feedback
- **[Known Issues](ALPHA_KNOWN_ISSUES.md)** — current limitations
- **[Alpha Agreement](ALPHA_AGREEMENT_v2.md)** — terms and expectations
- **[Release Notes v0.8.11.0](releases/RELEASE-NOTES-v0.8.11.0.md)** — what changed in the latest release

Not in the alpha yet? You can follow along at [pipermorgan.ai](https://pipermorgan.ai) — we publish weekly ships, building narratives, and insights about what we're learning.

---

## Current capabilities

- **Conversational interface** — natural language for PM tasks; Piper tracks context across a conversation so you don't repeat yourself
- **GitHub integration** — issue triage, status, prioritization, cross-feature patterns
- **Morning standup** — honest assembly from live sources, with explicit provenance (no hallucinated progress)
- **Integrations** — GitHub, Notion, Slack, Google Calendar; connector architecture (RECONNECT) actively extending
- **Radar** — structured display layer for the objects Piper tracks (WorkItems, Documents, People, Conversations)
- **Trust-gating** — proactive skills surface when invited; consequential actions require explicit confirmation
- **Per-user key routing and field encryption** — credentials isolated per user, secrets encrypted at rest (AES-256-GCM)

---

## Architecture

```
FastAPI server (port 8001)
  ├── Intent dispatch → workflow rail
  ├── Integration services (GitHub · Notion · Slack · Calendar)
  ├── Radar object layer (WorkItem · Document · Conversation · People)
  └── Trust + skill routing (ADR-072)

PostgreSQL 14+ (port 5433) — primary store
Redis 7+ (port 6379) — session cache
ChromaDB (port 8000) — vector search
LLM: Claude (Anthropic)
```

**Key docs:**
- [Architecture Decision Records](internal/architecture/current/adrs/adr-index.md) — 78 decisions with rationale (as of 2026-07-09)
- [Patterns catalog](internal/architecture/current/patterns/) — reusable implementation patterns
- [BRIEFING-CURRENT-STATE.md](briefing/BRIEFING-CURRENT-STATE.md) — live sprint status (agents: read this first)

---

## Running Piper locally

```bash
# 1. Clone and set up
git clone https://github.com/mediajunkie/piper-morgan-product.git
cd piper-morgan-product
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Add your API keys (Anthropic, GitHub, etc.)

# 3. Start services and launch
docker compose up -d
alembic upgrade head
python main.py   # server at localhost:8001
```

> **Note**: If launching from a Claude Code shell, strip the inherited Anthropic env vars first — see the warning in [CLAUDE.md](../CLAUDE.md).

---

## Where things live

| What | Where |
|---|---|
| Agent briefings + role assignments | `docs/briefing/` |
| Architecture decisions (ADRs) | `docs/internal/architecture/current/adrs/` |
| Product decisions (PDRs) | `docs/internal/product/pdr/` |
| Methodology + process docs | `docs/internal/development/methodology-core/` |
| Active session logs | `dev/YYYY/MM/DD/` |
| Omnibus logs (daily synthesis) | `docs/omnibus-logs/` |
| Public blog drafts | `docs/public/comms/drafts/` |

---

## What's next

**RECONNECT** — the connector refactor — is active now, replacing a patchwork setup with a clean contract (ADR-070). After that: **M4 Trust + Learning**, then **M5 Distribution + Polish**, then **0.9.0 beta** (targeting July 4, 2026).

Follow the weekly ships at [pipermorgan.ai/shipping-news](https://pipermorgan.ai/shipping-news) to see what's shipping.

---

## Support

- **Docs**: [pmorgan.tech](https://pmorgan.tech) (you're here)
- **Issues**: [GitHub Issues](https://github.com/mediajunkie/piper-morgan-product/issues)
- **Alpha support**: [support@pipermorgan.ai](mailto:support@pipermorgan.ai)
- **Blog**: [pipermorgan.ai](https://pipermorgan.ai)
