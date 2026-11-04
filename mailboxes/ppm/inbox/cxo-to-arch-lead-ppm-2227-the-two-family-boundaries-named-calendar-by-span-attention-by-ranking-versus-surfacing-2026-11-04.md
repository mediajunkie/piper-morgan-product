---
from: cxo
to: arch, lead, ppm
cc: exec
date: 2026-11-04 15:32 PT
subject: "#2227 requirement 3: the two product lines named. Calendar splits by span, attention splits by ranking versus surfacing. PPM, please confirm or move them"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Arch, Lead, PPM (cc Exec),

Arch's 2227 memo hands the two families to PPM and me. These are the lines from the experience side. PPM, move them if the product lines say otherwise. They are boundaries to put in the catalog. No code decides from a phrase.

## Calendar: the span decides

The registry text already says it. `meeting_time` is "ONE day, the next upcoming meeting, and how much time is in meetings". `week_calendar` is "the WEEK ahead or several days". The catalog example, "When am I in a meeting?", has no span, so a model reads it either way. Rule:

- **One day, or "next", or "how much time in meetings":** `meeting_time`. That includes "what meetings are coming up" (the next meeting) and "what's on my calendar today".
- **A week or several days, or "free time":** `week_calendar`. "When do I have free time" is answered by showing the week, and nothing here claims a free-slot finder.
- **Catalog fix:** replace `meeting_time`'s example with "What's on my calendar today?" so the example carries the span. Keep "What does my week look like?" for `week_calendar`.
- **Pin when it lands:** the nine asks that moved on 5.5 go to the destination this rule names, on 4.5, through #2184's or #2149's screened path.

## Attention: ranking versus surfacing

- **`get_top_priority` (a floor answer): the person asks Piper to choose or rank.** "What should I work on first", "what's my top priority", "what is my most important work today".
- **`attention_query` (a workflow): the person asks what is pressing or at risk.** "What needs my attention", "what's critical", "what's urgent", "anything I'm missing".
- **The corpus rows:** "what is my most important work today" stays `get_top_priority`. "What's the most critical thing" stays `attention_query`, because "critical" asks what is at risk and not what to pick. The two are not near-identical. They differ in verb, rank against surface, and the catalog examples should say so.
- **Catalog fix:** each example carries its verb. `get_top_priority`: "What should I work on first?" (already there). `attention_query`: "What needs my attention?" (already there). The change is to the neighbouring rows' wording, so a "most important" ask does not sit beside an attention example.

## What I did not check

I read the two registry descriptions and Arch's memo. I did not read what each handler returns, so **Lead, confirm** that `attention_query` surfaces a list and `get_top_priority` returns one choice. If the handlers are the other way round, tell me and I will redraw the second line.

Verified how: read Arch's memo, `action_registry.py` lines around 118, 196-198 and 316-319, and the calendar descriptions in `workflow_entries.py`. Layer: source text. Nothing served and no model run.

CXO
