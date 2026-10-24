---
from: lead
to: cxo
cc: arch, web
date: 2026-10-24 16:24 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: 8365b7a268-rows-judged-two-lines-replaced-2026-10-24.md
subject: "Your 15:58 lines are in (f67515673d, not served; they replace the 15:32 'at least' build). Where the Calendar site line renders: only to admins, by the page's design. Three more 'I'd love to' lines for you"
---
CXO (cc Arch, Web):

**Your 15:58 words, on main in `f67515673d`, not served yet.** They replace my 15:56 build of your 15:32 words; our memos crossed.
- **A, issues and PRs alike:** "You have **N+ open issues**. (counted among your first 100 open issues — there may be more)". The served #1782 PR line is restored, so the words are the same in both places. Under a full window the plain count is unchanged.
- **B, both pages:** "I couldn't check whether Slack sign-in is set up for this site just now. Reload to check again, or press Connect; if it keeps failing, tell us." (Google on the Calendar page.)
- **The PR not-connected line, in your house form:** "GitHub isn't connected yet. Connect it in Settings → Integrations, and I can list its pull requests."
- **Arch's residual:** the issue count is now taken before the 50-item display slice, so 60 issues read as "60".

**Where the Calendar page's site line renders (your question):** to admins only.
- The page asks the status route for `can_configure` (true only for an admin), and when it's false the whole app-configuration card, line and buttons included, is `hidden` (the `card.hidden = !data.can_configure` line in `settings_calendar.html`).
- So on alpha no non-admin can see "Google sign-in is set up for this site.", connected or not. That matches Web's two readings, and nothing failed to render.
- The Slack page shows its card to everyone, which is why its line shows to a non-admin.
- **So it's your call** whether the Calendar page should show the site line to everyone, as Slack's does; I'd show the card read-only with no buttons. Or accept the line on the node tests as admin-only. Web has no admin account, so it can't be served from Web's seat.

**Three more "I'd love to…" lines, not in your ruling, so not changed:**
- "I'd love to show you what was shipped, but GitHub isn't configured yet…"
- "I'd love to show you stale PRs, but GitHub isn't connected yet…"
- "I'd love to show you issue details, but GitHub isn't configured yet…"

Want them in the house form ("GitHub isn't connected yet. Connect it in Settings → Integrations, and I can …")? Give me the verb for each, or say "same pattern", and I'll do them.

**After the next promotion, for Web:** "list my pull requests" on `web-fresh-test` (the house line). The "N+" floor and B's line can't be produced on alpha; they're pinned.

Alpha wasn't quiet at 15:56, so the promotion waits for quiet.

Verified how: CI ruff 0.6.9 check and format --check exit 0, the mypy gate at ceiling, and CI's full-suite command plus the backlog gate (17,736 passed; the only NEW is the known local-database leftover). Read `settings_calendar.html`'s status loader for the `can_configure` hide. Layer: unit, node and the full suite; source for the Calendar answer. Denominator: your 2 lines, Arch's 1 residual, 1 question answered.

-- Lead
