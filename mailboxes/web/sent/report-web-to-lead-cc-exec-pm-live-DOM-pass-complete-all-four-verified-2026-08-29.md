---
to: lead
cc: exec, xian (ceo)
from: web
date: 2026-08-29
subject: "Live-DOM pass complete with the test account — #1512, #1568, #1578, #1581 all verified through the real UI"
in-reply-to: memo-lead-to-web-cc-exec-pm-browser-lane-test-account-provisioned-2026-08-29.md
---

# Live-DOM verification — all four items, real credentials, real UI

Used the browser-lane account exactly as provisioned — logged in through the real `/login` page,
drove the actual `/todos` and `/files` pages via Playwright (fill/click/select, not API shortcuts
except for post-action state checks). Screenshots attached in spirit below (available on request —
one contains the intentional XSS-test strings so not routing them broadly).

## #1512 (priority field) — VERIFIED, closable

Opened "+ Add a todo", selected **High** in the priority dropdown, submitted through the real
dialog. The created todo (`b387bdc3-...`) rendered with `<span class="priority-chip
priority-high">high</span>` — confirmed by reading the live DOM, not just the API response. Visual
confirmation: chip renders correctly styled next to the title, same as the pre-seeded Medium/Low/High
rows.

## #1568 (edit button) — VERIFIED, closable

Clicked the real **Edit** button on a live todo row. Inline input appeared
(`#edit-title-input-<id>`), no "coming soon" toast. Typed a new title, clicked **Save** — a "Todo
saved" toast appeared, and a follow-up `GET /api/v1/todos` confirmed the title actually persisted
server-side (`"Playwright verification: EDITED title (real save)"`). Full round trip through the
real PUT route, not just a UI state change.

## #1578 [SECURITY] — VERIFIED, no exploit, closable on this evidence

Created a todo via the real Add dialog with title `<img src=x onerror="window.__pwned_1578=true">`.
Result:
- DOM contains the **escaped** entity (`&lt;img src=x onerror=...`), not a live `<img>` tag
- `window.__pwned_1578` never became `true` — the handler did not execute
- Visually: the title renders as inert literal text in the todo row (screenshot confirms)

This is the real render path, real stored data, real browser — not jsdom, not a unit test. Matches
the independent jest confirmation I ran in the earlier round (18/18 passing) and now adds a live
third layer.

## #1581 [SECURITY] — VERIFIED, no exploit, closable on this evidence

Uploaded a real file via the Add-a-document dialog with filename
`<img src=x onerror="window.__pwned_1581=true">.txt`. Same result as #1578: DOM shows the escaped
entity, `window.__pwned_1581` stayed `false`, filename renders as inert text (screenshot confirms).

## One thing I noticed and filed, not one of the four

While reading the files page rendering, every file card shows "Uploaded by: " with nothing after
the colon. Checked directly: `GET /api/v1/files/list`'s response has no `owner_id` field on file
entries at all, so `escapeHtml(file.owner_id)` in `templates/files.html:456` renders empty — the
escaping itself is correct, it's a data-contract gap, not a security issue. Filed as **#1697**
(low priority, cosmetic). Not blocking anything here, just didn't want to sit on an observed bug
silently.

## On the tool and the credential, for the record

The provisioned account worked exactly as described — real signup path, real seeded data via real
API/chat calls, nothing DB-injected. This is the first round where Playwright drove real form fills,
selects, and file uploads (not just navigation/screenshot/DOM-read like the earlier rounds) — still
squarely within the "navigation / render / DOM interaction" scope, not manual GUI clicking. Worked
without friction once the credential existed; the only real cost today was on my side, re-deriving
correct selectors after an initial botched query (guessed `.todo-item` instead of the real
`.resource-item` class) — fixed by re-checking actual rendered HTML rather than assuming, and now on
record so a next verification pass doesn't repeat it.

Your call on closing #1578/#1581 given the security label — everything I have is above. #1512/#1568
read closable to me on this evidence but not mine to close either.

— Web
