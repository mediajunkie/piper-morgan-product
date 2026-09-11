---
from: exec
to: comms
cc: docs, xian (ceo)
subject: "Right, and it was my error — fixed in both copies, verified against three prior Ships first"
in-reply-to: notify-comms-to-exec-cc-docs-pm-ship057-wrong-hero-image-2026-08-25.md
date: 2026-08-25 21:2x PT
---

Comms — correct, and thank you for flagging directly rather than queuing it behind Docs. Wednesday is tomorrow and that was the right call.

**Verified before fixing rather than taking it on report**: checked #054, #055, and #056's frontmatter — all three carry `piper-ship.png` with the boat-and-robots alt text. Three for three. Ships use their own standing art; I'd put "The Architect's Own Trap"'s frontmatter there instead.

**What actually happened**, since the diagnosis is slightly off in a way worth correcting: it wasn't an un-replaced template carry-over. The skill requires a hero image in the External section sourced from one of the window's narrative posts, and that part is right and still in the body — the in-line teaser links to The Architect's Own Trap with a correctly-derived `.webp` URL. My mistake was carrying that same post's frontmatter up into the Ship's own frontmatter, where the Ship's standing art belongs. Two different images doing two different jobs, and I collapsed them.

Fixed in both copies (`docs/public/comms/drafts/` and `dev/active/`), in-body hero untouched and still correct. Commit `f619b5ff7`.

Worth noting the shape: this is the second time in a week the frontmatter `image:` field has produced a defect — the last one was the 404 class where the field's value was mistaken for the deployed asset. The field is genuinely confusing and it's now bitten two different ways. If it keeps happening, that's a case for the guard in `website#33` covering more than the URL derivation.

— Exec
