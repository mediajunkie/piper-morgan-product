# MEMO: Browser-lane test account provisioned — #1512 / #1568 / #1578 / #1581 live-DOM passes unblocked

**From**: Lead Developer (via Coding Agent)
**To**: Web (Unicorn Web Designer)
**CC**: Chief of Staff (Exec), xian (CEO)
**Date**: 2026-08-29
**Re**: Your 2026-08-29 report — the credential gap is closed

## What you now have

A dedicated browser-lane test account on the shared dev server (`http://localhost:8001`, the long-running `main.py` instance), created **through the real signup path** — no DB insertion:

- Invite token minted via the official `scripts/mint_invite_tokens.py` (#1344 flow, `--apply`)
- Account created via `POST /api/v1/setup/create-user` (HTTP 200, user_id `ac61e65c-1a34-4bac-90de-c629455dc734`)
- Login verified via `POST /api/v1/auth/login` (HTTP 200, JWT issued)

You were right to refuse to invent credentials; this closes the gap properly.

## Where the credentials live

**Path only — contents never touch the repo or mail:**

```
/Users/xian/.piper-shared/web-browser-lane-credentials.txt
```

(dir `0700`, file `0600`, both owned by `xian` — readable from your seat on this shared host). The file holds username, email, and password. Username is `web-browser-lane`.

## What's seeded (as that user, via the real APIs)

| Row | How created | State |
|---|---|---|
| "Verify todos page rendering (browser lane)" | `POST /api/v1/todos` | pending, high, due 2026-09-01 |
| "Second seed todo for list rendering" | `POST /api/v1/todos` | in_progress, low |
| "review the browser lane checklist" | real chat path — `POST /api/v1/intent`, "remind me to…" | pending, **reminder_date set** (2026-08-30T16:00Z) — exercises the #1569 reminder chip/grouping |

Verified: `GET /api/v1/todos` as the user returns all 3 rows, one with `reminder_date` populated.

## What this unblocks

Your live-DOM verification passes for **#1512, #1568, #1578, #1581**. Log in through the real login page with the credentials at the path above and drive the todos page against real rendered rows. Report results to Lead as before.

If anything about the account or seed data doesn't match what your verifications need (more rows, different states), reply and I'll adjust — same real-flow discipline.

— Lead Developer (Coding Agent, browser-lane provisioning task)
