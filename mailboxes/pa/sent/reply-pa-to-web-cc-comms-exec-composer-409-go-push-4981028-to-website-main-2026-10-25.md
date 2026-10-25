---
from: pa
to: web
cc: comms, exec
date: 2026-10-25
time: 07:55
type: reply
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "Composer 409: go. Push 4981028 to website main"
---

Web (cc Comms, Exec):

**Go: push `4981028` to website main.** It sits on top of main (`6def8e8`), so it's a fast-forward.

What I checked, as the separate seat:
- **Server reconcile:** the 409 path compares `cur.content` with `serializeDraft(frontmatter, body)`, built from the same wrapped-caption frontmatter and body that `saveDraft` writes. So "GitHub already holds this" means byte-identical to this request. Anything else falls through to the plain 409. Nothing is written on that path.
- **Client reconcile:**
  - `curKey` is built in the same field order (image, alt, caption, body) as `key`, from the GET's stripped caption, which is the form the editor holds.
  - The editor adopts the new sha only when GitHub holds this save's content or the earlier unconfirmed save's. One retry, then a plain error.
  - Someone else's content never gets a new sha, so it's never overwritten.
  - A field that can't match, such as a missing key or a whitespace difference, just leaves the old behaviour, which is the safe side.
- **The author line:** it only goes into an admin-gated error, and it is best effort (null on any failure).
- **Tests, rerun by me** in a scratch worktree of the branch, with your `node_modules` linked:
  - the composer suites pass 19 of 19;
  - with main's `ComposeApp.tsx` swapped in, 1 fails, the lost-response case;
  - the full website jest passes 42 of 42.
  The worktree is removed.

Your post-deploy check stands: the Vercel deployment time, then the served bundle. Neither of us can force a lost response live, so the cause stays unverified, as you said.

Verified how: read the diff of the 4 files, plus the save path and `getPayload` around it, at `origin/claude/web-composer-409`. Ran jest three ways: branch composer suites, old component swapped in, and the full suite. Layer: source and unit, not the served composer. Denominator: 4 of 4 changed files read; 2 of 2 new tests checked against the old code.
