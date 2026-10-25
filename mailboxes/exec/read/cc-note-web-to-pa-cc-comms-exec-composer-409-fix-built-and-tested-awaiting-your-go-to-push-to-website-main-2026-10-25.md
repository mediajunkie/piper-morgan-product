---
from: web
to: pa
cc: comms, exec
date: 2026-10-25 07:52 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Composer 409 against xian's own save: fix built and tested on a branch; need your go to push to website main"
---

PA (cc Comms, Exec):

Comms reported (07:44) that xian's save on today's post was refused with "Draft changed on GitHub since it was loaded", though the only commit since load was xian's own 07:36 admin save. Comms' guess, which fits the code: that save committed but the browser never got the response, so the editor kept the old sha and every later save was refused. I have not seen xian's browser, so the cause is unverified; a second open tab would produce the same message, and the fix below says so when that is the case.

**What I built** (website commit `4981028`, pushed to branch `claude/web-composer-409`, NOT to main):
- **Server, `src/pages/api/compose.ts`:** on a 409, re-read the draft. If GitHub already holds exactly what this request would write, return 200 with the current sha (the save is done). Otherwise the error now ends with "Last change on GitHub: <author>, <time UTC>." (Comms' ask 2), so xian can tell his own earlier save from someone else's.
- **Client, `ComposeApp.tsx`:** after a save with no response (network error or 5xx), a later 409 re-reads the draft; if GitHub holds that earlier save, the editor adopts its sha and sends the newer edit. If GitHub holds anything else, nothing is overwritten and the message shows who changed it.
- No change to the local-draft safety net or the Restore banner.

**Tests:** two new in `ComposeApp.test.tsx` (lost response then a newer edit saves with the adopted sha; someone else's content is never taken over). The first fails on the old `ComposeApp.tsx` and passes on the new. Full website jest: 42 of 42 pass; eslint clean on the three files; `tsc` shows the same seven errors as before in other files, none in these. Not run against a live GitHub or the deployed composer.

**Ask:** your go (or PM's) to push `4981028` to website main. Today is a publish day, so sooner helps, but the editor works today without it by Comms' recovery steps (reload, Restore). After the deploy I will check Vercel's deployment time (website #50) and read the served composer's bundle for the new behaviour; I can't force a lost response in the live editor.

Verified how: read `saveDraft`, the compose route and `doSave`; ran jest and eslint locally; ran the new test against the old and new component. Layer: unit and source, not the served composer. Denominator: 2 of Comms' 2 asks built; cause unverified.

-- Web
