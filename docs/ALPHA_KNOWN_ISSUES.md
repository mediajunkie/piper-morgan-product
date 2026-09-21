# Alpha Known Issues (v0.8.13.0)

**Version**: 0.8.13.0
**Last Updated**: September 21, 2026

This document helps alpha testers avoid wasting time on things we already know about.

v0.8.13.0 is the "Nothing Invented, Nothing Borrowed" release — a one-day fast follow to
v0.8.12.0 carrying the fixes from the first real dogfood session: the standup interview
keeps its word and its drafts to your words, keyless first contact is human, and the
server-key concept is deleted from the code outright. What's below are the rough edges
that remain.

## Known Issues in 0.8.13 (the honest list)

- **Web chat's front door still asks for an Anthropic key specifically** ([#1823](https://github.com/mediajunkie/piper-morgan-product/issues/1823) — ruled, queued). OpenAI-only users are fully served in Slack; on web, add an Anthropic key for now.
- **A short polite imperative can finalize a standup draft** ([#1843](https://github.com/mediajunkie/piper-morgan-product/issues/1843), found by this release's own regression work): "please remove the fluff" can be mis-read as an acceptance. Workaround: phrase edits without a leading "please", or say "start over" if a draft finalizes on you.
- **An invalid stored key can still surface the generic "Something unexpected happened"** ([#1824](https://github.com/mediajunkie/piper-morgan-product/issues/1824) — observed live; the honest-copy split is designed and queued). If you see it, the fix is the same: check your key in Settings.
- **Personality preferences are not yet per-user** ([#1791](https://github.com/mediajunkie/piper-morgan-product/issues/1791)): the questionnaire works but preferences aren't isolated per account yet.
- **Some docs links 404** ([#1793](https://github.com/mediajunkie/piper-morgan-product/issues/1793)).
- The REST `/api/v1/todos` endpoint is still mocked ([#1427](https://github.com/mediajunkie/piper-morgan-product/issues/1427)) — chat and UI todos are real.

---

## Fixed in 0.8.13 (from PM's live dogfood transcript)

If any of these still happens to you, that's a regression — please report it:

- **[#1837](https://github.com/mediajunkie/piper-morgan-product/issues/1837)** — Accepting the standup interview offer starts the interview (no re-greeting); the generic placeholder draft is deleted and unreachable; the flow never denies an offer it made.
- **[#1836](https://github.com/mediajunkie/piper-morgan-product/issues/1836)** — "I've updated your standup" is only said when the draft actually changed; free-form edits now genuinely apply (on your own key).
- **[#1818](https://github.com/mediajunkie/piper-morgan-product/issues/1818)** — A keyless "hi" gets a human acknowledgment plus one key sentence, not a policy wall.
- **[#1812](https://github.com/mediajunkie/piper-morgan-product/issues/1812)** — The transitional operator/server-key seam is deleted; every spend is the acting user's own key or an honest refusal (was already the enforced behavior; now it's the only representable one).
- **[#1839](https://github.com/mediajunkie/piper-morgan-product/issues/1839)** — `/health` reports the real version, git SHA, and environment.
- **[#1764](https://github.com/mediajunkie/piper-morgan-product/issues/1764)** — Credential-store namespace collisions fail loudly instead of silently mixing credentials.

---

## Previously Fixed (0.8.11, July)

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
| [#1105](https://github.com/mediajunkie/piper-morgan-product/issues/1105) | Settings UI sometimes requires re-pasting API key even when saved correctly server-side | Re-paste if prompted; if chat works, the save took — report it if refusals persist |
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

These shipped in 0.8.13 and need real-world validation:

| Feature | What to Test | How to Access |
|---------|--------------|---------------|
| **Interview offer → interview** | Accept the guided-interview offer — first question immediately? Draft built from your words only? | Chat: "let's do my standup" |
| **Free-form standup edits** | Ask for a real edit in your own words — applies? An inapplicable one — honest "unchanged"? | A standup draft in REFINING |
| **Keyless first contact** | "hi" / "thanks" with no key — human acknowledgment + one key sentence? | A keyless account or key removed |
| **Honest key errors** | Break your key, send a message — honest key message? (Generic message = #1824, report it) | Settings → LLM Keys, then chat |
| **Your key, your billing** | Chat, then check YOUR provider dashboard — requests there and nowhere else? | Provider usage page |
| **Session recall (no-regress)** | Create an issue in chat, then "what did we create this session?" | Chat |

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
- [Release Notes v0.8.13.0](releases/RELEASE-NOTES-v0.8.13.0.md) — Full 0.8.13.0 changelog

---

_Last Updated: September 21, 2026_
