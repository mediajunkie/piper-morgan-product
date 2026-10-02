# PM test card — the standing "what should I test?" surface

**Owner**: Lead. **Started**: 2026-09-19. **Rewritten to remaining-only**: 2026-10-01 14:03 PDT (PM's ask). Rolling doc:
rows get added when a fix needs PM's live verification and struck when done. When PM asks "what do I
test?", the answer is this file. Mirror: https://claude.ai/artifact/ALxfaRpLn5wjBVUPjzLvbi (v14).

**Surface**: alpha.pipermorgan.ai · **Fly v163** (2026-10-02 07:1x, `930d0be5ae`) — every fix from PM's
Oct 1 batch (#1858, #1912, #1914), the router descriptions, and #1606's two-part turn.

## Re-test now — fixed since PM's last pass

### A. Close a nonexistent issue, get a straight answer (#1858) — ~30 s — fixed v157
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
