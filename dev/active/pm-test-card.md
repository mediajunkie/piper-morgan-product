# PM test card — the standing "what should I test?" surface

**Owner**: Lead. **Started**: 2026-09-19. **Rewritten to remaining-only**: 2026-10-01 14:03 PDT (PM's ask). Rolling doc:
rows get added when a fix needs PM's live verification and struck when done. When PM asks "what do I
test?", the answer is this file. Mirror: https://claude.ai/artifact/ALxfaRpLn5wjBVUPjzLvbi (v15).

**Surface**: alpha.pipermorgan.ai · **Fly v169** (`36b11f3b2c`, deployed by PM 10-05 12:55; 12 tokens live, verified by Lead 13:17). **Step 0 is DONE except P6 and the .env.example commit.** It deployed today's main (ten more
pattern-list deletions → ceiling 155, the 1924 greeting fix, the read_floor_2 / read_canonical / read_portfolio rail groups, the
portfolio + repo write ops incl. the 1926 unlink confirm, R5 security). Every row after Step 0 assumes that build.
**v15 (12:48, 10-05)**: Step 0 (PM's terminal sitting) + Spec's live checks P1–P6 folded in (PM-approved via Exec 11:12).

## Step 0 — PM's terminal sitting (one block, in this order) — ~10 min

```bash
# 1. deploy today's main to alpha
cd /tmp/lead-deploy-wt && git fetch origin main && git checkout --detach origin/main && fly deploy -a piper-morgan --remote-only --build-arg PIPER_GIT_SHA=$(git rev-parse HEAD)
curl -s https://alpha.pipermorgan.ai/health | grep -o '"git_sha":"[0-9a-f]*'      # PASS: matches `git rev-parse HEAD` above
# 2. flip the three read tokens (12 total; Fly restarts the app)
fly secrets set -a piper-morgan PIPER_INVERSION_LIVE_CATEGORIES="read_status,read_referent,read_synthesis,create_todo,create_reminder,read_strategic,read_temporal,delete_todo,read_floor,read_floor_2,read_canonical,read_portfolio"
fly ssh console -a piper-morgan -C 'printenv PIPER_INVERSION_LIVE_CATEGORIES'   # PASS: 12 comma-separated tokens
# 3. (DONE, moot: the 12:39 dry run matched no unused rows — nothing to burn)
# 4. P6 — read-only prod SQL (Spec R5 item 4 / R1 evidence). PM's hand; Lead's seat is denied prod reads.
fly postgres connect -a piper-morgan-db        # then, read-only:
#   SELECT count(*) FROM users;  SELECT count(*) FROM users WHERE setup_complete;
#   SELECT u.username, max(s.created_at) FROM users u LEFT JOIN session_activity s ON s.owner_id=u.id GROUP BY u.username ORDER BY 2 DESC NULLS LAST;
```
Also, in your checkout: add a `JWT_SECRET_KEY=` line to `.env.example` (comment: generate with
`python -c 'import secrets; print(secrets.token_urlsafe(32))'`; the server now refuses to start without it).
Lead's part is done (13:17); Test A failed at 16:21 and is fixed on main (#1941) — rides the next deploy with the list_repos fallback: tokens mirrored in the gate; live probes for read_floor_2, read_canonical and read_portfolio all pass (8/8 turns routed to the named op). **Not on alpha yet (16 commits behind main at deploy):** the list_repos not-found fallback (`630e410910`); it rides the next deploy.

## Re-test now — fixed since PM's last pass

### A. Close a nonexistent issue, get a straight answer (#1858) — ~30 s — **FAILED on v169 (16:21); fix on main, re-test after the next deploy** (#1941)
**PM's 16:21 result: the hedge.** Cause (alpha logs 23:21Z): a third 404 shape — the write leg returned the 404 as text as pinned, but the
live server answered the read-back with a wrapped `McpError` 404, which landed in the mid-flight except and degraded to the hedge. Fixed on
main (two-leg evidence via the raised error counts; pinned both ways). Not on alpha until the next deploy.
Do: with GitHub connected, `close issue 99999 in mediajunkie/piper-morgan-product` → confirm (the confirm is
the normal destructive gate; it fires before the lookup). Pass: "There's no issue #99999 in … — nothing was
changed." Fail: the hedge, or any claim it closed something. Cause was GitHub's 404 JSON parsing as an issue.

### B. Remove a project, and it's actually gone (#1912) — ~1 min — fixed v159
Do: Settings → Projects → All Projects → Remove on a spare project (One Job; re-add after with `add project One
Job with repo Design-in-Product/one-job`). Then `show my projects`. Pass: toast, list refreshes without it, chat
doesn't list it. Cause: the DELETE call was a commented-out TODO while the toast fired.

### C. "Mark the first one complete and leave the second one pending" (#1914) — ~1 min — fixed v159
Do: with two reminders due now, send a turn so Piper mentions them, then the exact sentence, then `what
reminders do I have?`. Pass: one confirmation naming the first as completed, ending "Left the other one as is.";
the list shows only the second. Fail: a todo created from the sentence, both completed, or a "which one?" ask.

### E2. Your two-part sentence, both halves served (#1606) — ~1 min — fixed v163 (10-02)
Do: with two reminders set, send exactly: `please clear the reminders except for "Review the PR" - also, are you able
to set my default repo for me conversationally?`. Pass: the capability answer FIRST ("Yes — say 'set my default repo
to owner/name'…"), then the clear-verb question ("mark it done, or delete it?") with the exception note; nothing
deleted, nothing set. Fail: the old "doesn't look like an owner/name repo", a confirm to SET the repo, or the clear half
missing. (Row G from before — it moved up.)

### D. Two GitHub asks the router used to decline — ~30 s — new v161
Do: `get issue 101` → `what's the issue count` (default repo mediajunkie/piper-morgan-product). Pass: the
issue's title/state; then a count. Fail: a clarifying question, a listing, or a project-status reply.

## Spec's live-alpha checks (P1–P6) — folded from the 10-05 evaluation, PM-approved

Record pass/fail plus one line each; a screenshot for P3 helps. All against the Step-0 build.

### P1. New-user signup — ~5 min — needs a fresh invite (reissues are next week's; use one of yours if you have a spare)
Do: incognito → alpha.pipermorgan.ai → sign up with a fresh invite + your current Anthropic key; if you have a SHORTER valid key
(older `sk-ant-…` format), try that one too. Pass: account created, setup completes, first chat answers. Fail: a key rejected
for its length/format, a validator that blocks a real key, or a signup gate with no explanation. (Confirms R1 step 0, C-04.)

### P2. Three todos in one sentence — ~30 s
Do: `Add three todos for the launch: draft brief, book venue, send invites` → `what are my todos?`. Pass: exactly 3 new todos
with those three names. Fail: 1 todo named "the launch: draft brief, …", 2 of 3, or a "which one?" ask. (Confirms C-LLM multi-item.)

### P3. Greeting + calendar in one message — ~30 s — 1924 fixed this family on 10-03
Do: `Good morning — what's on my calendar today?`. Pass: a calendar answer (or the honest "calendar isn't connected" if Row E's
secrets aren't set yet). Fail: a bare greeting with no calendar content, or a greeting that ignores the question. (The 10-03
deletions had made the greeting swallow the question; fixed, not yet live until Step 0.) Screenshot, please.

### P4. No false statements with GitHub connected — ~2 min
Do: `What open issues do I have?` → then `add a todo to review the roadmap` → then `What have I created this session?`.
Pass: the issue list matches GitHub; the recall names the todo you just made and nothing you didn't. Fail: an invented issue, a
"you created…" that you didn't, or "nothing this session" after the todo. (Confirms C-LLM false statements / trust.)

### P5. Cold-user findability + feedback — ~3 min — do this inside P1's new account if you can
Do: from first login, time how long it takes to find (a) your todos and (b) your projects, by clicking, not chatting. Then look
for ANY way to send feedback. Pass: both found in under a minute; a feedback path exists. Fail: either not findable, or no
feedback path at all. Write the seconds and what you clicked. (Confirms C nav, G-U6.)

### P6. Prod counts — done in Step 0 item 4. Paste the three results on the card.

## Needs a one-time setup from PM — then calendar and meeting rows open

### E. Calendar: connect once, then "what's my agenda today?" — PM's hand: two Fly secrets
PM's ruling (10-01): the Google OAuth APP is deployment plumbing, not a per-user setting. Admin card hidden for
non-admins (v158); app creds are Fly secrets. Until set, every calendar/meeting row is untestable.
The plan: (1) Google Cloud Console → Credentials → OAuth client ID, Web application (reuse an existing Piper
client if one exists); (2) Authorized redirect URI exactly
`https://alpha.pipermorgan.ai/api/v1/settings/integrations/calendar/callback`; (3) Calendar API enabled; consent
screen lists the tester accounts; (4) `fly secrets set -a piper-morgan GOOGLE_CLIENT_ID="…" GOOGLE_CLIENT_SECRET="…"`
(never paste the values anywhere tracked; `GOOGLE_SETTINGS_REDIRECT_URI` already set; Fly restarts itself);
(5) tell Lead; Settings → Calendar → Connect → consent → "Connected".
Then test: `what time is it for me?` → `what's my agenda today?` → `what's my week like?`. Pass: Connected
without an app-credentials card; labeled times, never "TBD"; Focus Time block; week view spans days.
Recipe: `docs/internal/operations/canonical-ops-recipes.md` → "Google Calendar for a hosted deployment".

## Waiting on us — don't re-test yet
- **F. Keyless chat disappears after adding a key** — #1913, open (PM's Test 7 fail, 10-01). Row moves up when shipped.
- **H. OpenAI-only Slack turn** — #1822, optional, only if Slack is linked. Unchanged since 09-23.

## Struck (through 2026-10-01)
Rows 1 (#1824), 4 (#1876/#1574/#1887), 6 (#1856), 8 (#1737), 9 (#1498), 10 (#1559), 11 (#1625) — PASSED by PM
09-30/10-01; #1906 clear-pick re-test PASSED 10-01; #1617 standup tail-release PASSED 09-23; the admin calendar
card PM hit (10-01) — fixed by design change (v158), superseded by row E. Earlier struck history: git log of this file.
