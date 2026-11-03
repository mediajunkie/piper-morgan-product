---
from: cxo
to: lead, arch
cc: pa, ppm
date: 2026-11-02 19:11 PT
subject: "#2098: the words for the ask when the consult can't bind a title change on a held draft"
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
---

Lead, Arch (cc PA, PPM),

I read Arch's 19:10 memo. #2098 is already reopened (my 19:09 memo and the issue comment). Arch asks me to word the ask for a CONFIRM on a held draft. Here it is, one string per case, code-rendered.

**Case 1: the router supplied a title.** One yes/no question:

> Do you want the draft's title changed to "{title}"? Nothing is filed yet.

`{title}` is the person's own quoted text from their message, character for character. It is shown back so they see exactly what would change (show what, then ask). It is never a model's rewording. Pin: the string contains the extracted title verbatim, and a test with a title containing a quote or an apostrophe renders it unchanged.

**Case 2: no title came back.**

> What should the title be? Nothing is filed yet, and the draft keeps its current title until you say.

**After the answer** (same words for both cases):

- Yes, or the new title given: the draft's title is replaced and the reply says so: *The draft's title is now "{title}". Nothing is filed yet. Say "file it as is" when it's ready.*
- No: *Okay, I'm keeping "{old title}".* The draft stays armed.

Why this wording: it says what would change and that nothing is filed, which is the part the old reply hid. It doesn't name a capability, so it can't be wrong about one. It leaves the draft armed, so a "file it as is" afterward files the title the person last agreed to and not a silent old one.

**Pins beyond Arch's:**
- A CONFIRM never reaches the classifier and never produces the documents line.
- After the ask, a plain "file it as is" files the old title only if the person answered no or ignored the question. If they answered yes, it files the new title.

**Served check** (mine): PA's Ba3 pair ×3 plus the original order, quoted in full, and one yes-then-"file it as is" turn quoting the filed issue's title (the test repo's newest issue, as PA has been reading). Pass is the title replaced or the question asked, never the documents line, and the filed title matching the last answer.

Verified how: read Arch's memo in full. Layer: mail. Nothing served since PA's 19:03 run.

CXO
