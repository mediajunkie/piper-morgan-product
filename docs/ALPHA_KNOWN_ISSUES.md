# Alpha Known Issues (v0.8.11.0)

**Version**: 0.8.11.0
**Last Updated**: July 17, 2026

This document helps alpha testers avoid wasting time on things we already know about.

v0.8.11.0 is the "Finish the Unfinished" release: a systematic audit of half-done work across the whole codebase, fixes for every serious problem it found, and build-time enforcement so the same classes of bugs can't quietly return. The smoke gate was 565 tests green (1 skipped) at the release cut. What's below are the rough edges that remain.

---

## Recent Improvements (Fixed in 0.8.11)

These are the changes alpha testers are most likely to notice. If something on this list still seems broken for you, please report it.

- **[#1422](https://github.com/mediajunkie/piper-morgan-product/issues/1422)** — Personality questionnaire answers persist and shape Piper's tone again. Answers from before 0.8.11 were unrecoverable; re-answer once.
- **[#1415](https://github.com/mediajunkie/piper-morgan-product/issues/1415)** — LLM provider selection is per-user; one user's setup no longer pins the whole instance to their provider.
- **[#1416](https://github.com/mediajunkie/piper-morgan-product/issues/1416)** — Greetings with a question attached get the question answered; only pure pleasantries get the short greeting.
- **[#1417](https://github.com/mediajunkie/piper-morgan-product/issues/1417)** — "Connect my GitHub"-style requests get real setup guidance (Settings → Integrations) instead of a generic decline.
- **[#1425](https://github.com/mediajunkie/piper-morgan-product/issues/1425)** — Status/agenda/priority answers distinguish "I couldn't check" from "genuinely empty" — no more false "no pending tasks."
- **[#1426](https://github.com/mediajunkie/piper-morgan-product/issues/1426)** — False capability denials removed: Piper no longer claims it can't accept file uploads or set reminders.
- **[#1414](https://github.com/mediajunkie/piper-morgan-product/issues/1414)** — LLM key and quota problems surface an honest message about the key instead of "Something unexpected happened."
- **[#1420](https://github.com/mediajunkie/piper-morgan-product/issues/1420) / [#1421](https://github.com/mediajunkie/piper-morgan-product/issues/1421) / [#1434](https://github.com/mediajunkie/piper-morgan-product/issues/1434)** — Owner-scoping fixes: similarity search and default-project resolution are scoped to your account and deny rather than fall back to shared data; an auth check that silently fell back to a global key is fixed.
- **[#1435](https://github.com/mediajunkie/piper-morgan-product/issues/1435)** — List/todo metadata persists; it was previously discarded silently on every save.

---

## Known Issues

### Blocking

_None currently at P0._

### Annoying (tester-facing)

| Issue | Description | Workaround |
|-------|-------------|------------|
| [#1418](https://github.com/mediajunkie/piper-morgan-product/issues/1418) | Conversation picker sometimes loads the most recent chat regardless of which one you selected | Fix in progress; re-select or refresh |
| [#1105](https://github.com/mediajunkie/piper-morgan-product/issues/1105) | Settings UI sometimes requires re-pasting API key even when saved correctly server-side | Restart the server after saving — keychain read works correctly on restart |
| [#1164](https://github.com/mediajunkie/piper-morgan-product/issues/1164) | "Start private session" toggle in History slide-out is UI-only — no backend behavior | Cosmetic; don't rely on it |
| [#1216](https://github.com/mediajunkie/piper-morgan-product/issues/1216) | "What have you learned about my workstyle?" claims a seed-vs-real distinction the system can't actually make | Report these — they're honesty gaps |
| [#1256](https://github.com/mediajunkie/piper-morgan-product/issues/1256) | Stakeholder-update queries occasionally misclassify as update_document_query | Rephrase as "write a stakeholder update for..." if response feels off |

### Security / multi-tenancy

| Issue | Description | Status |
|-------|-------------|--------|
| [#1241](https://github.com/mediajunkie/piper-morgan-product/issues/1241) | Some content not fully anchored to user auth — multi-tenancy completeness | 0.8.11's audit shipped owner-scoping fixes (#1420, #1421, #1434); broader completeness work continues. Use test data only. |

---

## Carryover (Being Worked)

| Issue | What You Might See | Status |
|-------|-------------------|--------|
| [#1110](https://github.com/mediajunkie/piper-morgan-product/issues/1110) | Slack latent bug — `_make_request` calls `get_config()` without `user_id` | In progress |
| [#1258](https://github.com/mediajunkie/piper-morgan-product/issues/1258) | LAUNCH-ENV: inherited empty Anthropic env vars can shadow real key at server startup | Known; strip vars with `env -u ANTHROPIC_API_KEY ...` on launch |

---

## Partially Complete

| Feature | Status | What Works | What Doesn't |
|---------|--------|------------|--------------|
| **Todos REST API** | Mocked | Chat todos are real and persist; Todos UI works | The `/api/v1/todos` REST endpoints still return mocked data ([#1427](https://github.com/mediajunkie/piper-morgan-product/issues/1427)) |
| **Slack `/standup`** | Partial | Slack outbound, DMs, @-mentions | `/standup` command sections have known gaps ([#1429](https://github.com/mediajunkie/piper-morgan-product/issues/1429)) |
| **Learning dashboard** | Partial | Learning routes return clean errors now (no more 500s) | Dashboard itself has known gaps ([#1430](https://github.com/mediajunkie/piper-morgan-product/issues/1430)) |
| **Knowledge-graph similarity** | Filling | Accumulation re-enabled this release; new activity is indexed as it happens | Similarity features stay sparse until enough new activity accumulates |
| **BYOC credentials** | Mostly complete | Keys stored per-user, encrypted at rest; per-request routing; per-user provider selection | Settings UI re-paste bug (#1105) |
| **Data encryption** | Partial | API-key secrets encrypted at rest; passwords bcrypt-hashed | Content/PII at rest not yet encrypted; use test data only |
| **GitHub OAuth** | Not started | PAT token auth works | OAuth connect flow planned for a future release |
| **History privacy toggle** | UI stub only | Toggle renders correctly | No backend — doesn't do anything yet (#1164) |

---

## Needs Testing

These features shipped in 0.8.11 and need real-world validation:

| Feature | What to Test | How to Access |
|---------|--------------|---------------|
| **Questionnaire → tone** | Re-answer the questionnaire, then chat — does Piper's tone reflect your answers? | `python main.py preferences` or Settings |
| **Per-user provider** | Set your own key and provider — does chat use your provider? | Settings → LLM Keys, then your provider's usage dashboard |
| **Greeting + question** | "Hi! What can you help me with?" — does the question get answered? | Chat |
| **Connect guidance** | "connect my github" / "can you connect my slack" — real guidance, not a decline? | Chat |
| **Honest status claims** | Ask for status/agenda/standup — are todo/issue claims honest? "I couldn't check" is correct on failure | Chat |
| **Honest key errors** | Break your API key, send a message — honest key message, not "Something unexpected happened"? | Settings → LLM Keys, then chat |
| **Session recall** | Create an issue in chat, then ask "what did we create this session?" | Chat |

---

## What Works

- **Conversational AI**: LLM-grounded responses; greeting + question handled together; honest "I couldn't check" on source failures; honest key errors; session recall
- **Todos & Lists**: chat todos real and persistent; metadata persists (#1435); owner-scoped
- **Personalization**: questionnaire shapes tone (#1422); per-user provider selection (#1415); per-user keys encrypted at rest
- **Files**: upload/download, in-browser preview, search, freeform tags, bulk download
- **Integrations**: GitHub connector reads (issue summarization, repo resolution); Slack outbound, DMs, @-mentions; connect-setup guidance (#1417)
- **Core Infrastructure**: multi-user with owner-scoped access; JWT auth, bcrypt passwords; PostgreSQL, Redis, ChromaDB; smoke gate 565 green at cut

---

## In Progress / Next

- Conversation picker fix ([#1418](https://github.com/mediajunkie/piper-morgan-product/issues/1418))
- Real `/api/v1/todos` REST surface ([#1427](https://github.com/mediajunkie/piper-morgan-product/issues/1427))
- Slack `/standup` sections ([#1429](https://github.com/mediajunkie/piper-morgan-product/issues/1429)) and learning dashboard ([#1430](https://github.com/mediajunkie/piper-morgan-product/issues/1430))
- Beta (0.9.0) is milestone-gated — it ships when the beta criteria are met, not on a calendar date

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
- [Release Notes v0.8.11.0](releases/RELEASE-NOTES-v0.8.11.0.md) — Full 0.8.11.0 changelog

---

_Last Updated: July 17, 2026_
