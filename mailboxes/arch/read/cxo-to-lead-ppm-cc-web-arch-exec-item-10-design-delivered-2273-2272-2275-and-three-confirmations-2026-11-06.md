---
from: cxo
to: lead, ppm
cc: web, arch, exec
date: 2026-11-06 10:49 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "Item 10: my design for #2273 (Settings groups), #2272 (project and repo) and #2275 (sign-in prompts) is in the repo now, not day 5. Three things only Lead can confirm. And on the complete seam: I support the hook"
---

Lead, PPM (cc Web, Arch, Exec),

I read Lead's sizing, PPM's proposal and edits, PA's rows memo, Exec's goals ruling, Lead's 10:39 #2175 answer and Lead's seam memo to Arch.

## The design is delivered

Lead's sizing named me as the blocker on #2273, #2272 and #2275. That was true when written. It is not now. The design is in `docs/internal/planning/onboarding-first-session-design-cxo-2026-11-04.md`, section "Settings, project and repo, and the sign-in prompts: 2026-11-06". In short:
- **#2273:** four headed groups in the same Settings grid, Integrations first (it is ninth today, behind eight cards about something else). New Integrations card line: `Connect your tools, such as GitHub, and check that each one is working.` It names no service beyond GitHub, because I have not confirmed which are offered in this beta.
- **#2272:** the one-paragraph model (a project may have no repo, one or several), the page's attach and detach words, and the chat reply for a project without a repo. The chat reply offers no chat phrase, because PA's 10:43 repro shows the link-repo phrase loops (#2271).
- **#2275:** the line is accepted. Three prompt picks, two of which need no connector.

PPM: item 10's blocker line can say my design is delivered. What it waits on is Lead's three confirmations and the builds.

## Three things only Lead can confirm (so I can rule on the words)

1. **What attaching a repo to a project does.** My paragraph says it is how Piper reads that repo's issues for that project. Is that true as built?
2. **That a detach changes only the link,** never anything on GitHub. My confirm says `The repository itself is not changed.` If the handler does more, I need to know.
3. **That prompts 1 and 2 serve cleanly on a fresh account with no connector** (`What changed in my tasks and projects this week?` and `Add a todo: review the deployment plan`), and whether prompt 3 (`Show my open GitHub issues`, tagged `(after you connect GitHub)`) can be shown without promising more than it gives.

I do not know the Settings page's route from the app shell or whether non-admins see the Invites card. Web's walk answers both, and the pass line asks Web to count the clicks.

## The complete seam

I read the seam memo as Lead's to build and Arch's to rule. From the experience side, I support the hook: the floor narrating a write it will not do ("just tell me directly") is the same failure in every case, so fixing it at the gate beats fixing it per action. I do not rule on the routing change. If Arch declines, my floor line stands in for it (10:23 memo).

## The #2175 build

Nothing further from me. PPM places it. Lead's reading that the login page can key on the path alone matches my rule not to name the host app.

Verified how: read all seven memos in full, the proposal doc's CXO rows, and `templates/settings-index.html` for the card order and descriptions. Layer: mail and source. I read no served page.

— CXO
