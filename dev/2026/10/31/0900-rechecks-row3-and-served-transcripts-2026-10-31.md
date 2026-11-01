# v0.9.0.0 re-checks on alpha 5f0112c00c: row 3 (B confirm and reverse) and the served checks (#2236, #2233, #2237, #2225), 2026-10-31

PA, by API. Account `web-seed-1386`, one session per block, replies verbatim from `/api/v1/intent`. Reverse-case confirms go on a fresh `requests.Session()` with no bearer and no cookie. Test repo `dinp-machine/piper-test-activity`: newest #35 before, #36 after (from block D3 only). Layer: API text and served page source, not the rendered page. Row 2's CSV and report: `dev/2026/10/19/canonical-retest-1386-alpha-20261031-1852-*`.

```
=== #2223 re-check on 5f0112c00c ===

## Forward, session 4322d32a (signed in throughout)

--- F1 [18:53:27, 7.4s, http 200, req None] ---
USER: Let's track this. Create a GitHub issue: 'Re-check forward 1857'
route: execution/create_ticket
PIPER: Happy to shape this with you before anything gets filed. Here's a draft to start from:

**Title**: Re-check forward 1857

What should the body say — the problem, steps to reproduce, impact? Tell me what to add or change. If this draft works as-is, say "file it as is" and I'll create it right now. (If you'd rather I just file things directly, say "just do things directly from now on" and I will.)

--- F2 [18:53:29, 0.3s, http 200, req None] ---
USER: yes
route: execution/create_ticket
PIPER: Which repository should I create this in? Say owner/name, and I'll keep it as your default.

## Reverse, session 05203cea (draft signed in; confirms with no sign-in)

--- R1 [18:53:39, 7.4s, http 200, req None] ---
USER: Let's track this. Create a GitHub issue: 'Re-check reverse 1857'
route: execution/create_ticket
PIPER: Happy to shape this with you before anything gets filed. Here's a draft to start from:

**Title**: Re-check reverse 1857

What should the body say — the problem, steps to reproduce, impact? Tell me what to add or change. If this draft works as-is, say "file it as is" and I'll create it right now. (If you'd rather I just file things directly, say "just do things directly from now on" and I will.)

--- R2-anon [18:53:41, 0.9s, http 200, req None] ---
USER: yes
route: None/clarify
PIPER: I can't process this without you being signed in or supplying your own LLM API key — sign in, or connect your own key.

--- R3-anon [18:53:44, 0.1s, http 200, req None] ---
USER: file it as is
route: None/clarify
PIPER: I can't process this without you being signed in or supplying your own LLM API key — sign in, or connect your own key.

=== 0.9.0.0 served checks on 5f0112c00c as web-seed-1386 ===

## #2236 capability reply, session e2b2ae7c

--- C1 [18:54:03, 6.0s, http 200] ---
USER: What can you help me with?
route: DISCOVERY/get_capabilities
PIPER: What I can do today:
- conversational PM guidance
- strategic thinking and prioritization frameworks
- you can ask me: "give me my standup"
- you can ask me: "what have you learned about my work style?"
- you can ask me: "connect my github"
- you can ask me: "what time is it?"
- you can ask me: "connect my notion"
- you can ask me: "connect my slack"
- you can ask me: "link my google calendar"
- you can ask me: "add a repo to my portfolio"
- you can ask me: "show me my todos"
- you can ask me: "list my projects"
- you can ask me: "connect my calendar"
- you can ask me: "what reminders do I have?"

Connected, and what I read from each:
- GitHub: chat reads open issues and their status, one issue by number
- Google Calendar: I can read your calendar for today, tomorrow or this week, including your free time. I can't check for conflicts or find a time that works for other people yet.

## #2236 fix 3, insights, session db1fc261

--- I1 [18:54:13, 8.3s, http 200] ---
USER: What insights do you have for me?
route: MEMORY/pull_insights
PIPER: I don't have any insights about your work yet.

## #2233 Q1 name, session 1ab6f224

--- N1 [18:54:18, 3.0s, http 200] ---
USER: What's your name?
route: IDENTITY/get_identity
PIPER: I'm Piper Morgan — think of me as your PM-minded thought partner. What are you working on?

## #2233 greeting then todo list, session 70710a55

--- G1 [18:54:27, 6.8s, http 200] ---
USER: Hi
route: conversation/greeting
PIPER: Hello!

I took a look at your calendar and it looks like you have a clear day ahead - nice!

What's on your mind?

Reminders that came due: "review prs" (Oct 23), "review prs" (Oct 23), "review prs" (Oct 23), and 3 more.

--- G2 [18:54:30, 1.3s, http 200] ---
USER: Show my todos
route: query/list_todos_query
PIPER: I checked your todo list - looks like quite a bit going on with 17 items.

The first one is 'review prs'. Then there's 'review prs'. Also 'review prs'. And 'review prs'. And 'review prs'. Plus 12 more items.

That's a full list. Where would you like to start?

## #2237 connect my slack, session e036372f

--- K1 [18:54:39, 6.3s, http 200] ---
USER: connect my slack
route: guidance/provide_setup_guidance
PIPER: Slack isn't available in this beta yet. You can connect GitHub or Google Calendar in Settings → Integrations.

## #2237 direct routes (no redirects followed)
GET /api/v1/settings/integrations/slack/connect -> http 409 body='{"message":"Slack isn\'t available in this beta yet.","detail":"Slack isn\'t available in this beta yet."}'
GET /api/v1/settings/integrations/slack/authorize -> http 409 body='{"message":"Slack isn\'t available in this beta yet.","detail":"Slack isn\'t available in this beta yet."}'
POST /api/v1/settings/integrations/notion/save -> http 422 body='{"detail":[{"type":"missing","loc":["body","api_key"],"msg":"Field required","input":null}]}'
GET /api/v1/setup/slack/oauth/start -> http 409 body='{"message":"Slack isn\'t available in this beta yet.","detail":"Slack isn\'t available in this beta yet."}'

## #2237 integrations page source
GET /settings/integrations -> http 200; __OFFERED_CONNECTORS__ = ["github", "calendar"]

## #2225 draft, yes, repo, session d3c2a7e6

--- D1 [18:54:49, 8.1s, http 200] ---
USER: Let's track this. Create a GitHub issue: 'Served check 2225 1858'
route: execution/create_ticket
PIPER: Happy to shape this with you before anything gets filed. Here's a draft to start from:

**Title**: Served check 2225 1858

What should the body say — the problem, steps to reproduce, impact? Tell me what to add or change. If this draft works as-is, say "file it as is" and I'll create it right now. (If you'd rather I just file things directly, say "just do things directly from now on" and I will.)

--- D2 [18:54:51, 0.3s, http 200] ---
USER: yes
route: execution/create_ticket
PIPER: Which repository should I create this in? Say owner/name, and I'll keep it as your default.

--- D3 [18:54:56, 2.3s, http 200] ---
USER: dinp-machine/piper-test-activity
route: execution/create_ticket
PIPER: Created issue #36, "Served check 2225 1858", in dinp-machine/piper-test-activity.

POST /api/v1/settings/integrations/notion/save (form) -> http 409 body='{"message":"Notion isn\'t available in this beta yet.","detail":"Notion isn\'t available in this beta yet."}'

## #2237 wizard page source (curl /setup, unauthenticated)
id="connect-later-line": You can connect Google Calendar later, in Settings → Integrations.
Notion key section and Slack connect button: absent (0 matches).
```
