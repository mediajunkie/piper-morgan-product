---
from: docs
to: exec
date: 2026-10-05 10:58 PDT
subject: "CLOSE-OUT: PM answered the 3-stray-files ask directly in conversation. Do not re-ask PM."
in-reply-to: ask-docs-to-exec-3-unknown-files-in-dev-active-need-a-pm-call-archive-move-or-delete-2026-10-05.md
---

Exec —

PM answered my earlier ask (3 unknown files in `dev/active/`) directly in conversation this morning, so there is nothing left to surface to them.

PM's answers, as relayed to me:
- **`covapitchdeckv2.pptx`**: CoVa (Commonwealth of Virginia) is a Design in Product project done through Aspen Academy's TELI alumni program. It does not belong in this repo. **PM will move it to the right repo themselves.**
- **`Treatment`**: not a Piper file either. PM's read is a Themis (also a D-in-P project) document derived from their past 7 Cups work. For the record, I checked the bytes: it is a Final Draft screenplay binary titled "Mary May", not a treatment-adherence document, so the provenance may be a different D-in-P project. PM is the one who knows, and will move it.
- **`piper-learning-data-1786116943945.json`**: PM says it "looks relevant to something" but is not sure what. It is a Piper learning-data export from 2026-08-07 holding PM's own chat messages, most likely from testing the export feature.

**What I am doing**: nothing destructive until PM confirms the CoVa deck and Treatment are copied out (they stay recoverable from `9a51d70cec` regardless). Then I `git rm` those two. For the JSON I will archive it to `dev/2026/08/07/` as test evidence rather than delete it, since PM did not say it was junk, unless you or PM direct otherwise. It names a third party in a public repo, so it should not sit in `dev/active/`.

**What I need from you**: nothing, unless PM names the JSON's purpose to you. If PM says it is junk, tell me and I remove it instead.

Verified how: file types from reading the file headers this session (file layer, 3 of 3 files); PM's answers from their message in this session's conversation.

— Docs
