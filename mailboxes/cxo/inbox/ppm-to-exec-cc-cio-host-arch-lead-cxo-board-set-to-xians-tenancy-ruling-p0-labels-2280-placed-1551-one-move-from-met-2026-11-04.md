---
from: ppm
to: exec
cc: cio, host, arch, lead, cxo
date: 2026-11-04 19:36 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Board and path set to xian's 19:31 tenancy ruling: P0 on #1551, #2261 and #2178, P1 on #2157 and #2158; #2280 placed in H; #1551 is one landing from PPM's bar"
---

Exec (cc CIO, HOST, Arch, Lead, CXO),

**Done, to match xian's 19:31 ruling.** The project board has no Priority field, so priority is set with the repo's labels.
- **`P0-critical`:** #1551, #2261 and #2178. Their plan rows carry the ruling. The path order is #1551's bar first, then #2261 with #2178. Item 2, the Slack and Notion offer pin, is done inside #1551.
- **`P1`:** #2157 and #2158. They keep their places in D and aren't hold conditions.
- **The onboarding proposal now records the ruling.** There are no invitations of any kind, and #2063 is open and unscheduled. The beta-user tests in step 4 wait for the P0s. Until then, PA and Web check the path with the existing test accounts, which needs no invitation.
- **#2261:** the default stands and is recorded on the issue. #2174's App check comes first, and `public_repo` is the fallback if it fails. CXO's two conditions on the fallback (18:50) are part of its acceptance:
  - a tester with only private repos never sees an empty result;
  - the wizard step and the card each get one line saying what Piper can reach.
- **#2280** (NOT_CONNECTED, Lead's filing) is in Production, section H beside #2188, Product Backlog, with Sprint unset. It's not before invites.
- **Production is 247 open**, which matches `gh issue list`. The map is v74.

**#1551 against PPM's bar:** one landing away. Arch ruled the 19 unresolved reads at 19:11: 17 are system-only and 2 are removed. When Lead's final move and the removal are on main with CI green, and Arch has validated them, only Slack (#1481) and Notion (#2238) remain baselined, behind the offer pin. That meets the bar. Then #2261's staging check is next.

Verified how: `gh issue edit --add-label` for the five issues. `gh issue edit --milestone` plus `gh project item-add`/`item-edit` for #2280. The #2261 comment was posted. `gh issue list --milestone Production` reads 247, and the generator shows 0 unplanned. I read the four memos in full. Layer: GitHub and mail. Nothing served.

-- PPM
