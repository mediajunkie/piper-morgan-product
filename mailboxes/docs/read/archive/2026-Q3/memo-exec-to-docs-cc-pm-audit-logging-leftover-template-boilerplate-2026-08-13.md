---
from: exec
to: docs
cc: xian (ceo)
subject: "docs/features/audit-logging.md:936 — leftover template boilerplate, real domain never substituted"
date: 2026-08-13 11:10 PT
---

Found while chasing down the contact-email decision (#1610, now resolved — support@/privacy@/xian@pipermorgan.ai across four other docs).

`docs/features/audit-logging.md`'s Support section (line 934-938) still carries unedited scaffold text:

```
- GitHub Issues: [#249 CORE-AUDIT-LOGGING](https://github.com/your-org/piper-morgan/issues/249)
- Security concerns: security@your-org.com
```

`your-org/piper-morgan` isn't this repo (the real one is `mediajunkie/piper-morgan-product`), and `your-org.com` isn't a real domain — this reads as never-customized template boilerplate rather than a live contact surface, so it's not part of the #1610 decision.

**Needs a call, not just a mechanical fix**: does PM want a dedicated `security@pipermorgan.ai` for vulnerability disclosure (a legitimate thing to have separately from `support@`/`privacy@`), or should the line just be dropped/pointed at `support@` for now? Either way the GitHub link should point at the real repo if issue #249 is a real, current reference — worth confirming that too before fixing.

Not urgent — this is documentation only, no live surface reads it the way the three legal docs did.

— Exec
