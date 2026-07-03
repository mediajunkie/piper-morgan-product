# Alpha Known Issues (v0.8.9.1)

**Version**: 0.8.9.1
**Last Updated**: July 2, 2026

This document helps alpha testers avoid wasting time on things we already know about.

v0.8.9 covers the full stack through D1/RECONNECT plus RECONNECT WS-1, the security layer (field encryption + auth hardening), and Design D2 (token system + mobile nav + Radar rename). The 252/252 canonical regression baseline (D1 gate) is unchanged. What's below are the rough edges that survived those gates.

---

## Recent Improvements (Fixed in 0.8.9)

These are the changes alpha testers are most likely to notice. If something on this list still seems broken for you, please report it.

### Connector config now persists across restarts

GitHub repo config and integration preferences are now stored in the database. Restarts no longer lose your connector configuration. When GitHub isn't configured, Piper now surfaces an honest "not connected" state rather than guessing or failing silently.

### Real standup pipeline

The hollow `MorningStandupWorkflow` is retired. `StandupAssembler` is the live pipeline — it draws from connector data and Radar sources. Ask Piper for your standup in the chat interface.

### User secrets encrypted at rest

The `user_api_keys` table now stores secrets encrypted (AES-256-GCM, HKDF per-field key derivation). Any existing plaintext secrets are migrated on `alembic upgrade head`. BYOC keys are now routed per-request, completing the end-to-end BYOC flow.

### Auth hardening

`admin_compose` route removed. Auth exemption list is now lint-enforced — no new exemptions without an explicit rationale comment.

### Documents → Radar rename

The "Documents" nav label is renamed to "Radar" throughout — nav, page headers, breadcrumbs. Standup content and work items are first-class Radar data sources.

### Mobile nav

Mobile nav is implemented (hamburger → drawer pattern). The responsive shell adapts across viewport widths. The design token system is fully applied to the app shell.

---

## Known Issues

### Blocking

_None currently at P0._

### Annoying (tester-facing)

| Issue | Description | Workaround |
|-------|-------------|------------|
| [#1105](https://github.com/mediajunkie/piper-morgan-product/issues/1105) | Settings UI sometimes requires re-pasting API key even when saved correctly server-side | Restart the server after saving — keychain read works correctly on restart |
| [#1164](https://github.com/mediajunkie/piper-morgan-product/issues/1164) | "Start private session" toggle in History slide-out is UI-only — no backend behavior | Cosmetic; don't rely on it |
| [#1216](https://github.com/mediajunkie/piper-morgan-product/issues/1216) | "What have you learned about my workstyle?" claims a seed-vs-real distinction the system can't actually make | Report these — they're honesty gaps |
| [#1256](https://github.com/mediajunkie/piper-morgan-product/issues/1256) | Stakeholder-update queries occasionally misclassify as update_document_query | Rephrase as "write a stakeholder update for..." if response feels off |

### Security / multi-tenancy (being worked)

| Issue | Description | Status |
|-------|-------------|--------|
| [#1241](https://github.com/mediajunkie/piper-morgan-product/issues/1241) | Some content not fully anchored to user auth — multi-tenancy completeness audit | Architect-owned; being investigated. Use test data only. |

---

## Carryover (Being Worked)

These are known architectural rough edges from prior sprints:

| Issue | What You Might See | Status |
|-------|-------------------|--------|
| [#1110](https://github.com/mediajunkie/piper-morgan-product/issues/1110) | Slack latent bug — `_make_request` calls `get_config()` without `user_id` | RECONNECT-WS7 scope; in progress |
| [#1258](https://github.com/mediajunkie/piper-morgan-product/issues/1258) | LAUNCH-ENV: inherited empty Anthropic env vars can shadow real key at server startup | Known; strip vars with `env -u ANTHROPIC_API_KEY ...` on launch |

---

## Partially Complete

| Feature | Status | What Works | What Doesn't |
|---------|--------|------------|--------------|
| **BYOC credentials** | Mostly complete | Keys stored in keychain; server reads correctly; per-request routing live | Settings UI re-paste bug (#1105); macOS keychain only |
| **Data encryption** | Partial | `user_api_keys` secrets encrypted at rest (0.8.9); passwords bcrypt-hashed | Content/PII at rest not yet encrypted; use test data only |
| **GitHub OAuth** | Not started | PAT token auth works | OAuth connect flow planned for a future release |
| **History privacy toggle** | UI stub only | Toggle renders correctly | No backend — doesn't do anything yet (#1164) |

---

## Needs Testing

These features are complete in 0.8.9 but need real-world validation:

| Feature | What to Test | How to Access |
|---------|--------------|---------------|
| **Connector config persistence** | Configure a GitHub repo, restart the server — does it remember? | Settings → Integrations |
| **Honest no-repo UX** | Skip or remove GitHub config — does Piper say "not connected" rather than guessing? | Remove repo config, ask about issues |
| **StandupAssembler** | Ask "what's my standup?" in chat — do you get a real, assembled response? | Chat interface |
| **Per-user LLM key routing** | Enter BYOC key, make requests — confirm your provider usage dashboard shows activity | Settings → API Keys, then provider dashboard |
| **Mobile nav** | Open on a phone or narrow browser window — does hamburger → drawer work? | Narrow the browser window |
| **Radar rename** | Is "Radar" the label everywhere — nav, page headers, breadcrumbs? | All navigation surfaces |
| **Conscious Floor** | Ask Piper things it shouldn't know — does it say "I don't have enough context" or fabricate? | Just chat normally |
| **BYOC key persistence** | Enter API keys in Settings, restart the server — do they persist? | Settings → Integrations |

---

## What Works

- **Conversational AI**: LLM-grounded floor for unmatched queries; antecedent resolution ("it" / "that"); honest refusal when context is missing
- **Connector infrastructure**: DB-backed config, survives restarts; honest no-repo UX; `StandupAssembler` pipeline
- **Security**: AES-256-GCM field encryption; encrypted `user_api_keys` secrets; per-user LLM key routing; auth-exempt lint enforcement
- **Files**: Search, preview, bulk download, drag & drop upload, freeform tags
- **Design**: Token system applied to app shell; responsive shell; mobile nav; Documents → Radar rename
- **Integrations**: Slack (inbound via Socket Mode, outbound, DMs, @-mentions); GitHub (issue summarization, repo resolution, lifecycle); Notion (append_blocks, URL unfurling); Calendar
- **BYOC & Settings**: API keys in macOS keychain via Settings UI; per-request key routing; Radar as default home
- **Setup & Onboarding**: GUI setup wizard, system health checks, API key validation, user account creation
- **Core Infrastructure**: Multi-user, JWT auth, bcrypt passwords; PostgreSQL, Redis, ChromaDB (Debian 12/bookworm); 252/252 canonical regression baseline

---

## Planned for Next Sprints

| Sprint | Focus | Status |
|--------|-------|--------|
| RECONNECT (remaining WS) | Connector refactor continued — WS7 Slack latent bug, remaining WS | Active |
| M4: Trust + Learning | Learning system, trust gradient, preference persistence | Backlog |
| M5: Distribution + Polish | Registration flow, priority engine, polish | Backlog |
| Beta (0.9.0) | Target: July 4, 2026 | — |

---

## How to Report Issues

**What to include:**
```
WHAT I TRIED: [specific action]
WHAT I EXPECTED: [expected result]
WHAT HAPPENED: [actual result]
ERROR MESSAGE: [if any]
```

- **GitHub Issues**: [Create new issue](https://github.com/mediajunkie/piper-morgan-product/issues/new)
- **Email**: Reply to your onboarding email for private issues

---

## See Also

- [ALPHA_QUICKSTART.md](ALPHA_QUICKSTART.md) — Quick setup
- [ALPHA_TESTING_GUIDE.md](ALPHA_TESTING_GUIDE.md) — What to test and how
- [Release Notes v0.8.9](releases/RELEASE-NOTES-v0.8.9.md) — Full 0.8.9 changelog

---

_Last Updated: June 22, 2026_
