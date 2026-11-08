---
from: arch
to: lead
cc: cxo, pa
date: 2026-11-08 07:20 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2270 default-lead echo (CXO 07:18): drop the body's first sentence only when it starts 'Looking at' and contains the exact repo full name; otherwise leave the body untouched. CXO's gap-B words fit my 07:18 rule as is."
---

Lead (cc CXO, PA) —

CXO wants the repo named once and asked for a code-held fix. The mechanism:

- **The floor block** tells the model the reply already opens with which repo was read. That's cheap, but a prompt line is not a constraint, so it isn't the fix by itself.
- **The code step.** After composing, and only on the default-lead path, drop the body's first sentence if both hold:
  - it starts with `Looking at`;
  - it contains the exact `owner/repo` the handler read.

  Both are exact matches against code-held strings, so this reads no meaning (ADR-080 governs reading the person's words; this checks our own output against our own token). If either check fails, the body stays as composed. Never reword or trim anything else.
- **Pins:**
  - PA's r8 body: the echo is dropped, and the repo is named once in the first two lines.
  - A body that opens with a finding is unchanged.
  - A named read (no lead) is never touched.

CXO: your words `I couldn't find "{their words}" among your repositories or projects.` fit my 07:18 gap-B rule as written. Our memos crossed; they agree.
