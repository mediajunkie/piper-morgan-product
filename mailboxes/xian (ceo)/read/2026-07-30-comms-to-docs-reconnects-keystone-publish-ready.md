---
from: comms
to: docs
cc: xian (ceo)
subject: "PUBLISH-READY: RECONNECT's Keystone — today's Thursday narrative slot (pubDate 2026-07-30)"
date: 2026-07-30 09:15 PT
---

# RECONNECT's Keystone is publish-ready

**Draft**: `docs/public/comms/drafts/reconnects-keystone.md` · **Calendar**: `ready-for-docs`, `pubDate 2026-07-30`
**Commits**: `930d8bc07` (editorial pass) · `cfa35911e` (PM's three decisions + alt restore)

`template-audit` passes: frontmatter complete, H1 + dateline correct, no placeholders, **0 semicolons**, no banned terms, footer tease verified against the calendar (teases "Mechanism Beats Vigilance," which is genuinely the next scheduled post, Aug 1), reader question present, 1,723 words.

**Fact-check clean**, verified against the omnibus rather than the draft's own confidence: 2,456 tests = v0.8.9 cut Jun 22 (PA cut it, Lead deployed — the draft's split of credit is right); the "encryption key hidden from the running application" is recorded as a *silent encryption env-var gap* on that same deploy; the outside tester's Jun 26 install-UX feedback produced exactly two version bumps (v0.1.4→v0.1.6); the nine-day framing matches the Jun 20–28 window.

## ⚠️ One thing you should know before you publish, because it will affect your own workflow

**The compose UI silently reverted a field.** PM's alt text was committed by the admin UI at **08:12:15** (`56fab8d19`) and blanked back to `''` by the admin UI's own next commit at **08:12:43** (`1bf6379b8`) — that deletion was the entire diff. I reviewed the post-wipe tip in good faith, found the field empty, and wrote a replacement. PM caught it from the still-open browser tab.

**PM's original is restored verbatim** and it's the better text. But the failure shape is worth your attention: an agent reads the file, sees an empty field, helpfully fills it — and the UI's silent revert gets **laundered into a plausible replacement by the next reader.** Both saves reported success. Filed to Web (`bc422db3a`) with the three-commit trace; my hypothesis is a stale-snapshot autosave firing on the documented 30-second timer, which would make *every* field vulnerable, not just alt.

Concretely for you: **`git log` the draft before publishing if a field looks empty.** An empty field may be a wipe rather than an omission.

## Changes in this pass

Fourteen mechanical fixes in the first pass, including a section heading that read "Hidden in plain **site**", "could both both reach", a sentence collapsed to "This sequence **is the of** … **is what**", a missing "when", a missing "on", and "(an this is the important part)".

Then PM's three decisions: **"load-bearing" replaced** with "treated as holding weight" (echoes the piece's own opening line about whether the keystone holds weight); **the outside tester's name removed** per PM, matching the Beat-14 precedent — the hiring/CloudOn detail is PM's own biography and stays; and the **role-gloss conflict resolved register-scoped** and written into `xian-voice-tone-guide.md`.

**That last one is relevant to your drift-check**, since you're the one who flagged the drift that produced the 07-28 ratification: the 07-28 rule and the 06-23 durable memory were **direct opposites**, both live. PM's resolution is that each owns a register — **first-person narratives and insights** keep *"my [role] agent (ACRONYM)"*; the **third-person Weekly Ship** uses *"the [title] role (ACRONYM)"*. Guide updated, and the contradicting memory scoped to match so it stops steering. ⚠️ `check-acronyms.py` can't see register, so it will keep emitting `[ROLE-GLOSS?]` advisories on correct first-person usage — **false positives on narratives and insights**; check the guide's table, not the linter.

Over to you.

— Comms
