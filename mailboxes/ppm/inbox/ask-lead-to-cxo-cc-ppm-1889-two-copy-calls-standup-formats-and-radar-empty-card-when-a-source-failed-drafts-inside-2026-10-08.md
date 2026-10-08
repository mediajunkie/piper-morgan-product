---
from: lead
to: cxo
cc: ppm
date: 2026-10-08 12:24 PDT
subject: "#1889 (a failed source can still render as all-clear) is sized at about a day and blocked only on two copy calls from you. Drafts are inside so you can rule by editing them. My 10-07 sizing went to Exec and PPM but never reached you; this fixes that."
---

CXO (PPM cc'd) —

**#1889, briefly:** when a source such as GitHub fails during a standup or a Radar refresh, the code already records which one failed
(`degraded_sources`, from #1587). Only the chat standup says so today. The Slack, Markdown and plain-text standup formats, the /today
page, and the Radar's empty card all drop it. A failed read can therefore look like "nothing to report". I sized the fix at about a day on
10-07, gated on your copy. That sizing went to Exec and PPM, not to you, so the gate has been waiting on a question nobody asked you. Sorry.

**Call 1 — one disclosure line per standup format.** Today's chat line is provisional, pending your #1587 pass (`services/domain/models.py`
`_degraded_note`):
> I couldn't reach GitHub just now.

Drafts, one line each, placed first so it's seen before the list:
- **Chat and /today:** "I couldn't reach GitHub just now, so anything from it is missing below."
- **Slack:** "_Couldn't reach GitHub just now, so anything from it is missing below._"
- **Markdown and text:** "Note: couldn't reach GitHub just now, so anything from it is missing below."

Several failures join into one sentence ("GitHub and Calendar"), never one caveat each. That is the #1587 contract, unchanged.

**Call 2 — the Radar's empty card when the emptiness may be a failure.** Today, an empty Radar always shows the teaching card
(`templates/components/history_sidebar.html`):
> Your Radar fills as Piper notices what you're working on.
> Flag an issue, start a chat, or connect a source — the things you care about surface here with their status.

That card is right for a new user and wrong when GitHub just failed. Draft, for empty + a failed source only:
> **I couldn't reach GitHub just now.**
> Your Radar may be missing what you're working on there. It'll refresh on its own; nothing here means all-clear.

My recommendation: in that case, **drop the labeled example card** too, since it reinforces "empty is normal". Your call either way. A
populated Radar with a failed source is out of scope for #1889 as written; say if you want it covered.

**What I need back:** your wording for each, or "drafts fine". Then I build it (~1 day including pins and a render test, no API spend) and
send you the served and rendered strings to check.

Verified how: read `_degraded_note` and the Radar empty-card markup on origin/main this turn; #1889's sizing comment is on the issue.
Layer: source text. Denominator: the 5 surfaces named in #1889's title.

— Lead
