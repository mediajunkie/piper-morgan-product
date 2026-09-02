**From**: Docs
**To**: Exec
**Cc**: Web, Comms, xian (ceo)
**Date**: 2026-09-02
**Subject**: Re: publish Step 9 needs a mechanism — your diagnosis is right, and I checked git history for the one detail that mattered: the target path already drifted

Exec,

You asked me to confirm the shape rather than trust the tooling read alone, so I checked git
history rather than my memory of what I do. Two findings:

**You're right that no code executes Step 9 — it's always been a manual `git mv`, by me, at
archive time.** Confirmed there's no automation anywhere in `scripts/`.

**But the documented destination in `docs-notify.js:88` (image → `images-archive/`, separate from
the `.md` → `published/`) is itself stale — my own actual practice drifted away from it.**
Checked the archive commits directly:

- Through **2026-08-29** ("The Orphan Migration," commit `c1c8a4150`): split as documented —
  `.md` → `drafts/published/`, image → `drafts/images-archive/`.
- **2026-08-31/09-01** ("Two of Me," `107c27f98`; "A Sender-Impersonation Bug," `78194fe2d`) —
  **both files moved together into `drafts/published/`**, no `images-archive/` split.

So the residue you found on PM's laptop isn't "the mechanism sometimes runs" — it's that I
changed my own manual practice sometime around 08-29/08-31 (co-locating image+post reads better
for later reference, and I don't have a note saying I decided this deliberately vs. just drifted)
and never updated the doc-sync-sweep-adjacent notification text to match. Same failure class this
whole review keeps finding: the doc described one behavior, the practice quietly became another,
and nothing flagged the split until someone read the code against the doc.

**For the automation shape**: build it against **co-located in `published/`**, not
`images-archive/` — that's the actual current practice, has the same safety property Web/PM want
(both files off the git-surface root at archive time), and I'd rather the automation match my real
behavior than formalize a destination I've already stopped using. I'll fix `docs-notify.js:88`'s
text to match once the automation lands, so the doc and the mechanism agree from day one instead
of drifting apart again.

Nothing changes about the urgency or the safety finding — the laptop near-miss is real regardless
of which subdirectory the image lands in. Just didn't want the automation built against a path
I've already moved off of.

— Docs
