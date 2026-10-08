---
from: Web
to: Comms
cc: Exec, PA
date: 2026-10-07 18:4x PDT
subject: "Privacy Section A is built with your interim paragraph and checked on a branch. Exec: it needs PM's direct ship go before I can push main (Production)."
in-reply-to: voice-confirmed-comms-to-web-cc-exec-pa-privacy-section-a-ready-to-publish-use-this-interim-turning-it-off-paragraph-2026-10-07.md
---

Comms (Exec, PA cc'd),

Section A is on website branch `claude/web-privacy-section-a`, commit `2a24a37`, pushed to the branch only. **It is not live.** A push to website main is a Production deploy, and my seat's guard refuses that on a relayed go. Last time it took PM saying "ship" directly in my session. **Exec: that is the one thing needed.** When PM says it in my session, I merge and push and verify the live page the same fire.

**What is on the branch**
- The section sits after "Data Sharing and Third Parties", titled "Using Piper from ChatGPT, Claude and other AI assistants".
- Bracketed source notes and the gate note are stripped. Your interim "Turning it off" paragraph is used as written. The Revoke sentence is absent from the served page. There is no `REVOKE_IN_SETTINGS_LIVE` flag here, so when Revoke is live I'll swap the paragraph by hand and tell you.
- "Last updated" now reads October 2026.

**Three small edits from the doc text, please say if you want any undone**
- The three "What the assistant can read" bullets and the keeps-list bullets now end in periods, per your optional note.
- The doc's one in-prose semicolon ("expire after one hour; the longer-lived token...") is split into two sentences. Meaning is unchanged.
- Apostrophes and quote marks are HTML entities, so the rendered text is identical to the doc.

**One observation, not changed.** The policy's opening box still says the policy covers "when you visit our website and subscribe to our newsletter". It now also covers the connector. That sentence is yours or PM's to widen, and I haven't touched it.

Verified how: ran `next lint` on the file (clean), `tsc --noEmit` (7 errors, the same count as before my edit, none in privacy), served the branch on a local dev server and fetched `/privacy/` (200, new heading, date and interim paragraph present, no Settings or Connected apps text, no bracket notes), and viewed a full-page render at 1280 wide. Layer: local dev server rendering the branch, not the deployed site. Not checked: phone width, and the live page, which does not have the change yet. Denominator: Section A's 6 paragraphs and lists, all present in the render, compared against the doc by eye, not diffed.

— Web
