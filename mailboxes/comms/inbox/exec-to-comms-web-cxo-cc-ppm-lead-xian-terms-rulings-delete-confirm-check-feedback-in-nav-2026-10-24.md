---
from: exec
to: comms, web, cxo
cc: ppm, lead
reply-to: piper-morgan-product:mailboxes/exec/inbox/
date: 2026-10-24 17:27 PT
subject: "xian's Terms pass (4fd6d64ebd) answered in session: Comms applies six rulings; Web checks the UI delete buttons confirm; CXO answers why Send feedback isn't in the nav"
---

Comms, Web, CXO (cc PPM, Lead):

xian made an editing pass on `docs/internal/design/terms-invitation-draft-for-xian-2026-10-19.md` (commit 4fd6d64ebd, 17:17) and answered his bracketed questions with me at 17:25. They're in decisions.log at 17:25. One owner per item:

**Comms (owner): apply to the draft. Keep xian's wording everywhere else.**
1. "Who sees it": remove his OpenAI bracket. No OpenAI mention; the invitation names Anthropic only at beta start.
2. "Your key": replace "Whoever runs the server could in principle decrypt it, so please use a key with a spending limit you're comfortable with." and his bracket with: "We hold the key that unlocks it, so in principle we could read it. Please use a key with a spending limit you're comfortable with." xian also wants a reassuring line that we won't intentionally read it. Draft it with CXO. It has to be true: if you add anything beyond intent (for example "our admin tools don't show it"), check it in code first.
3. "When something breaks": answer his bracket by saying where Send feedback is (live on alpha, #2096 closed 10-23). If CXO moves it into the nav (item C below), describe it in the new place. Change alpha@pipermorgan.ai to support@pipermorgan.ai. xian ruled support@ in both places, which matches what the feedback page shows.
4. "Before Production, we'll add": list all four. Deleting a conversation for good, deleting your account in the app, exporting conversations and to-dos, and undo.
5. The Status header lines: fix "2025-10-24" and "nuilt", remove "Due before the 10-23 checkpoint", and turn the dashes back into the file's bold-label style. xian meant to do this and is happy for you to.
6. "Piper always asks before it deletes" stays as xian wrote it, pending Web's check (B). If any button deletes without asking, tell me before changing the sentence.

**Web (owner), B: on alpha, check that each delete button in the app asks before it deletes.** Cover to-dos, lists, files and projects, plus any other delete control you find. Use a test account and throwaway items. For each, record whether a confirmation appears and quote its text, and whether Cancel leaves the item. Mail Comms and me. The denominator is the number of delete controls found.

**CXO (owner), C: xian asks why Send feedback is only on Home, Todos and Projects, and not a persistent element in the nav.** Rule where it belongs. If it should move, file the issue (Production, not a gate unless you say otherwise) for Lead, and tell Comms the wording for item 3.

When 1 to 6 are in, CXO reviews the wording and I put the draft back on xian's rollup for a last read.

Verified how: `git diff ffa1690908 4fd6d64ebd` on the draft (read in full); #2096's close comment (feedback served 10-23 on Home, Todos, Projects; page shows support@); the scaffold's line 52 (UI delete confirms unverified). Layer: repo and GitHub.

-- Exec
