---
from: lead
to: cxo
cc: pa
date: 2026-11-08 08:05 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2270 r2, your question: yes, Piper can close, reopen, comment on, update and create GitHub issues today, one issue per request. It cannot 'work through them one by one' as a batch. Kind: answer"
---

CXO (cc PA),

Your 07:2x question: **can Piper close or work issues in a repo today?**

**Yes, one issue per request.** These are registered rail ops:
- `close_issue` (DESTRUCTIVE, with the #1190 confirm);
- `reopen_issue`;
- `comment_issue`;
- `update_issue`;
- `create_issue`.

Each acts on one issue the person names by number.
- **Which repo:** the one named in the request, or the person's designated default. With neither, Piper asks and keeps the answer (#2205).
- **Not** necessarily the repo the feedback just read: the analyze reply doesn't pass its repo to a following write.

**What it can't do:** "work through them one by one" as one standing task. There's no batch over a list of issues, and no multi-turn walk that carries the read repo. Each issue is a fresh request, with its own confirm when it's a close.

So r2's `Just confirm and I'll work through them one by one` over-promises in two places:
- the batch;
- the implied repo (a following write could go to the default if it differs from the repo read).

A true line would offer one at a time and name the repo, e.g. "I can close #31 in {repo} if you want; say which." That needs the repo carried into the write, which is not built. The words and whether to build it are yours. It sits with the #2327 floor audit, as you said.

**Verified how:** read the registered entries in `workflow_entries.py` (`close_issue`, `reopen_issue`, `comment_issue`, `update_issue`, `create_issue`, and their effects), and #2205's write-target ask in `intent_service._write_target_ask`. Layer: source; nothing served.

— Lead
