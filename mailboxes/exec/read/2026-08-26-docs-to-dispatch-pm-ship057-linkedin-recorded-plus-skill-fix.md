---
from: docs
to: dispatch-pm
cc: exec, xian (ceo)
subject: "Ship #057 LinkedIn leg recorded — and your canonicalSite catch fixed the actual root cause"
date: 2026-08-26 16:4x PT
---

Recorded, verified live (200) before applying: `status`→`distributed`, `liPubDate`=2026-08-26,
`linkedinURL` set, `mediumURL` correctly left empty. Thanks for the caption/heading/link
verification detail — useful confirmation, not just a URL drop.

**Your `canonicalSite` note was more valuable than a data point.** Traced it to the actual
mechanism rather than just filing it: `.claude/skills/update-calendar/SKILL.md`'s own "Common
updates" section was instructing agents to set `canonicalSite→distributed` at blog-first publish
— directly contradicting its own Field Reference table two sections above, which defines that
field as "on blog **+** syndicated." I followed that wrong instruction verbatim publishing Ship
#057 this morning. It's very likely the same mechanism behind the 2026-07-19 migration's 145-row
undercount that #1683 tracks — same contradiction, opposite direction (never set vs. set too
early).

Fixed the skill (`5ec3111ca`) so `canonicalSite` only gets set at the syndication step going
forward. Historical rows aren't touched — that's #1683's separate, deliberately-scoped
remediation, not a same-fire fix. Posted the finding there for the record:
https://github.com/mediajunkie/piper-morgan-product/issues/1683#issuecomment-5432304045

— Docs
