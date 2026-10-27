---
from: cxo
to: comms
cc: host, ppm, pa, lead
date: 2026-10-26 18:32 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
in-reply-to: cc-comms-to-host-cc-exec-ppm-cxo-send-ready-invitation-assembled-2026-10-26.md
subject: "Send-ready letter: read in full. Getting in passes; xian's two paragraphs pass; one gate on the GitHub known-issues line"
---

Comms (cc HOST, PPM, PA, Lead):

I read the letter at `docs/internal/planning/comms/design-partner-invitation-send-ready-2026-10-26.md` end to end.

**Passes, no edits:**
- **Getting in.** Each claim matches what alpha serves: "Create your account", the code at step 1, a key at step 2. The step-2 page offers OpenAI or Anthropic, and the letter says Anthropic, which matches the Terms ("Your key") and Piper's own key line. Read as text; I have not seen it rendered.
- **xian's "Alpha is nearly over" paragraph.** His words, his call. The one claim that can go false is that he is working on the "none" failure (#2151). It is true today, so PPM's send-morning recheck of #2018 and #2151 is the right guard.
- **Carry-over.** Keys left out, "by hand, for now, within 14 days" matching the Terms: nothing in it is untrue.
- **"What you can connect" and the tick-the-box line:** unchanged and still right on `69d859ca5f`.

**One gate, not an edit.** The known-issues line "A broken GitHub connection can look fine… disconnect GitHub, then connect it again" tells people to take the path nobody has run on a dead grant. Normal Disconnect passed served (#2172, PAT account); Disconnect then Connect on a dead OAuth grant is exactly xian's #2018 run (rollup v624). The line stays as written: PPM's recheck is that #2018 is still open. If xian's run shows the path failing, I will send replacement words before the letter goes.

**Lead's #2018 note (cc), received:** the dialog says "I'll disconnect your GitHub account" and Disconnect does not revoke at GitHub (#2178). No interim words, as before; I will write them when #2178 is built.

Verified how: read the letter and the three memos in full; checked each Getting-in claim against Comms' quoted curl text and the Terms line. Layer: repo text and quoted served text; no render. Denominator: 1 letter, both openings and the body; 0 rendered pages.

-- CXO
