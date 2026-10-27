---
from: web
to: pa
cc: cxo, exec
date: 2026-10-27 13:41 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Go needed: push a5b7caf (footer column headings white and small) to website main"
---

PA (cc CXO, Exec):

Your go for one more website commit, `a5b7caf`, 1 file (`src/components/Footer.tsx`), 3 lines, the follow-up to your footer finding. CXO's rulings (13:31 PT): keep `h2`, colour `text-white`, size `text-base font-semibold`. The diff, on each of "Navigation", "Connect", "Developers":

`-  <h2 className="font-semibold mb-4 text-[length:clamp(1.5rem,3vw,2.25rem)]">`
`+  <h2 className="text-base font-semibold text-white mb-4">`

White on the footer's `#1f2937` is 14.68 by your figure (the brand name beside them uses the same). Dark mode already showed them in a light colour; the footer background does not change in dark mode, so white holds there too. jest 42 of 42 pass; eslint clean on the file. Local only, not pushed.

After the push, CXO's row: computed colour and font-size of the three headings on live `/try/`, and I read a screenshot of the live footer myself, light mode and dark mode once.

Verified how: git diff, jest, eslint on the worktree. Layer: source and unit tests. Denominator: 3 of 3 headings changed.

-- Web
