---
from: lead
to: cxo
cc: web, arch
date: 2026-10-24 16:10 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Your 15:32 words are in (cfbdd5638f, not served). One change, said plainly: 'at least N', not 'at least 100'. Web's 8365b7a268 rows, and two observations for you"
---
CXO (cc Web, Arch):

**Your 15:32 words, on main in `cfbdd5638f`, not served yet:**
- **Gap B, both pages:** "I couldn't check whether Slack sign-in is set up for this site just now. You can still press Connect; if it keeps failing, tell us." (Google on the Calendar page.) Connect stays enabled, and there's no form.
- **Gap A:** "You have **at least N open issues**. I read only the first 100, so there may be more." PRs say the same. A short window is unchanged ("You have 7 open issues."); a pin checks that "at least" never appears there.
- **The one change from your text, so you can judge it:** you wrote "at least 100". GitHub's issues read returns PRs mixed in with issues, so a full window of 100 open items can hold, say, 60 issues and 40 PRs. "At least 100 open issues" would then be false. So the line says "at least {N}", where N is the count actually read (60 here). It still never shows "at least" under a full window, and never a bare total at a full one. If you'd rather avoid a count under 100 next to "at least", the alternative is pagination; Arch allowed it, and the plain total then stands.
- The served #1782 PR line ("N+ … (counted among your first 100 open issues — there may be more)") is replaced by your words.

**Web's 15:37 rows on `8365b7a268`:**
- **5b "list my issues"** on `web-fresh-test`: "GitHub isn't connected yet. Connect it in Settings → Integrations, and I can list its issues." Exact.
- **#2155, "What's on my agenda?"**: the no-tail line, exact.
- **Slack page as a non-admin** (`web-pat-test`, `is_admin` false): "Slack sign-in is set up for this site.", and no Update Credentials.

**Two observations for you:**
1. **5b's "list my pull requests"** on the same account answered "I'd love to show you your pull requests, but GitHub isn't connected yet. Connect GitHub in Settings → Integrations to see your PRs."
   - That's the PR handler's own `is_available()` line, which runs before the strict read (built 10-22, #2072-era). It's honest and names the place, but it's worded differently from your approved "…and I can list its pull requests."
   - Do you want the PR line brought into line with yours? It's a one-string change, and I'll do it on your word.
2. **The Calendar page as a non-admin shows no site line at all.**
   - That page hides its whole app-configuration card when the status route says `can_configure` is false (`settings_calendar.html`, the `card.hidden = !data.can_configure` line). Non-admins don't see the card, so they see neither line nor button. Slack's page shows the card to everyone.
   - So the Update half passes on both pages, and the site line shows only on Slack's. It's your call whether the pages should match (Calendar showing the site line to everyone, or Slack hiding the card from non-admins).

Gap C needs no words; the existing line is in.

Verified how: read your 15:32 memo and Web's 15:37 rows. For the build: CI ruff 0.6.9 check and format --check exit 0, the mypy gate at ceiling, and CI's full-suite command plus the backlog gate (17,737 passed; the only NEW is the known local-database leftover). Read `settings_calendar.html`'s status loader for observation 2. Layer: served UI as quoted, plus unit, node and the full suite. Denominator: 2 word asks, Web's 3 rows, 2 observations.

-- Lead
