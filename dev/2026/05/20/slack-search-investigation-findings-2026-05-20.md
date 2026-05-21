# Slack `search.messages` migration investigation — findings (2026-05-20)

**Investigation purpose**: re-dispatch of the two subagents from 2026-05-19 ~15:19 PT (whose findings were verbally communicated to PM yesterday and then lost when the session crashed). Recapturing on the record per PM directive 2026-05-20 morning.

**Headline finding**: **no migration is required to unblock #1085 slice 3.** PM's later-recalled "bot scopes vs user scopes" hypothesis is correct. The legacy `search:read` scope is still available under **User Token Scopes** in the Slack app config UI. The dropdown gap PM saw was because they were looking at *Bot* Token Scopes (a category where `search:read` has never been available — it's user-only). Re-auth with legacy scope works; Real-time Search API migration is a separate follow-on, not a blocker.

---

## Subagent A findings — community / Slack-docs research

### 1. Current deprecation state

- **`search.messages` method**: Still functional, marked **legacy**. Slack docs say: *"This is a legacy method. We recommend using the Real-time Search API (`assistant.search.context` method) instead."* No published sunset date. Source: https://docs.slack.dev/reference/methods/search.messages/
- **`search:read` scope**: Still functional, marked **legacy**. Slack docs say: *"This is a legacy scope. We recommend using more granular scopes associated with the Real-time Search API instead."* It continues to support `search.messages`, `search.all`, and `search.files`. No published sunset date. Source: https://docs.slack.dev/reference/scopes/search.read/
- **Slack's Real-time Search API guide** does say: *"DON'T use the legacy `search:read` scope and related `search.messages` and `search.all` endpoints."* — strong guidance, but no removal date. Source: https://docs.slack.dev/apis/web-api/real-time-search-api/

### 2. Bot scope vs user scope — confirms PM's later hunch

- **`search:read` is a USER token scope only.** Slack's reference explicitly says: *"Supported token types: User."* It does **not** appear under Bot Token Scopes in the modern app config UI — that's documented intended behavior, not a regression.
- **The granular `search:read.*` variants** (`search:read.public`, `search:read.private`, `search:read.im`, `search:read.mpim`, `search:read.files`, `search:read.users`) are the **new Real-time Search API scopes** introduced 2026-02-17 with the Slack MCP server. They live alongside legacy `search:read`, not as in-place replacements.
- **PM's wrong-tab hypothesis is almost certainly correct.** If PM was looking at *Bot Token Scopes*, `search:read` would not appear (it's user-only). The legacy `search:read` should still be available under *User Token Scopes*.

### 3. Real-time Search API shape

- **Shipped 2026-02-17** alongside the Slack MCP server announcement. Source: https://docs.slack.dev/changelog/2026/02/17/slack-mcp/
- **Request/response shape** (not event-driven). Two methods: `assistant.search.context` (the search call) and `assistant.search.info` (capabilities).
- **Not a drop-in swap** for `search.messages`: granular consent model, action-token requirement for bot tokens (user tokens don't need one), AI-assistant framing. Migration is non-trivial.

### 4. Community migration experience

Real signal is thin in the past 6 months. Only concrete community thread is an n8n integration bug (https://community.n8n.io/t/slack-app-still-not-including-search-read-scope/218774) which was n8n-side (OAuth2 default scope list omitted `search:read`), fixed by their PR #19229 — **not a Slack-side deprecation issue**. No reports of `search.messages` returning errors or being throttled differently. Migration is currently optional in practice.

### 5. Recommended path (per subagent A)

**Option (a): re-auth with legacy `search:read` under User Token Scopes; keep planning a future migration.**

Rationale: dropdown gap matches looking at wrong tab; `search.messages` is legacy but functional with no sunset; forcing migration mid-#1085 trades known-working code for new-API risk under no time pressure.

Confirmation step PM can take in ~30 seconds: in the Slack app config UI, navigate to **OAuth & Permissions → User Token Scopes** (scroll past Bot Token Scopes), search the dropdown for `search:read`. It should be present.

---

## Subagent B findings — codebase impact assessment

### Headline

The mentions-of-user slice (#1085 slice 3) is **designed but not implemented**. OAuth machinery has the scope in place (since 2026-05-18 commit `3b8b98432`), but the `_fetch_slack_mentions_items()` method doesn't exist yet. Once OAuth re-auth succeeds (with legacy `search:read`), implementing the slice itself is ~50 lines following the DM-aggregator pattern.

### Current state

| File | Status |
|---|---|
| `services/integrations/slack/oauth_handler.py` lines 132–141 | `search:read` in default user_scopes (added May 18, prep work) |
| `services/intent_service/context_assembler.py` lines 1259–1274 | Docstring notes `search.messages` deferred due to missing scope |
| `tests/unit/services/integrations/slack/test_oauth_user_scopes_1085.py` | 4 tests validating `search:read` default; all passing |

**No active call sites** to `search.messages` yet. OAuth-prep only.

### Call graph (if mentions-of-user slice were implemented)

```
context_assembler._compute_recent_activity()
  → _fetch_slack_activity_items()  [shipped May 18: DM-only via im:history/mpim:history]
    → [FUTURE] _fetch_slack_mentions_items()
      → [FUTURE] SlackIntegrationRouter.search_messages()  (would use search.messages API)
```

### Abstraction quality

**Clean.** All Slack API calls go through `SlackIntegrationRouter` which delegates to `SlackClient`. Adding a new endpoint is a single point of extension. No scattered call sites.

### Effort estimates

- **Just to implement mentions-of-user with legacy `search.messages` API** (after OAuth re-auth lands): ~50 lines in context_assembler + ~30 lines in slack_client/router + tests. **Small (< 1 dev-day).**
- **Future migration to Real-time Search API**: 12–24 hours / 1.5–3 dev-days. **Large.**

### Subagent B's disagreement with Subagent A — flagged

Subagent B assumed (from PM's reported observation yesterday) that legacy `search:read` is no longer available, and therefore that Real-time Search migration is a prerequisite for #1085. **Subagent A's docs-cited research overrides that assumption** — `search:read` IS still available, just under User Token Scopes, not Bot Token Scopes. So Subagent B's "migration is now required" framing is incorrect; the correct path is the legacy re-auth.

I'm flagging this transparently because if the User Token Scopes search dropdown turns out to NOT have `search:read` (counter to Slack's own docs), then Subagent B's framing becomes the right path. The verification step PM takes resolves which subagent's assessment lands.

---

## Synthesized recommendation

1. **PM**: in Slack app config UI for the Piper Morgan app, navigate to **Features → OAuth & Permissions**, scroll to **User Token Scopes** (NOT Bot Token Scopes), confirm `search:read` is in the dropdown. ~30 seconds.

2. **If `search:read` is present** (expected outcome per Slack docs):
   - Add it to the User Token Scopes for the app (if not already)
   - Re-attempt the OAuth flow (Settings → Connect Slack from the running app UI)
   - This unblocks #1085 slice 3 ("mentions-of-user" implementation)
   - Then implement `_fetch_slack_mentions_items()` (~50 lines + tests, small task)

3. **If `search:read` is NOT present** (counter to Slack docs; would be a real change):
   - Slack ahead of their published docs in deprecating; need Real-time Search API migration NOW
   - 1.5–3 dev-days of work + design review
   - File migration as the unblock for #1085, sized as its own work

4. **Either way**: file a tracking issue for "Plan migration of Slack search to Real-time Search API (`assistant.search.context`)" — sized as 1.5–3 dev-days, do post-#1085 once the immediate slice ships.

## Sources cited by Subagent A

- [search.messages method | Slack Developer Docs](https://docs.slack.dev/reference/methods/search.messages/)
- [search:read scope | Slack Developer Docs](https://docs.slack.dev/reference/scopes/search.read/)
- [Using the Real-time Search API | Slack Developer Docs](https://docs.slack.dev/apis/web-api/real-time-search-api/)
- [Announcing the Slack MCP server and Real-time Search API (2026-02-17)](https://docs.slack.dev/changelog/2026/02/17/slack-mcp/)
- [search:read.public scope](https://docs.slack.dev/reference/scopes/search.read.public/)
- [search:read.private scope](https://docs.slack.dev/reference/scopes/search.read.private/)
- [n8n community thread on search:read scope](https://community.n8n.io/t/slack-app-still-not-including-search-read-scope/218774)

— Findings captured 2026-05-20 ~07:25 PT by Lead Developer agent (re-dispatch of 2026-05-19 ~15:19 subagent pair)
