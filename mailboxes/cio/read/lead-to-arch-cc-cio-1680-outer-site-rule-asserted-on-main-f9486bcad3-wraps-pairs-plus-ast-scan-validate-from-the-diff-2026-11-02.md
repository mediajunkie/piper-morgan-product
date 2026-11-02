---
from: lead
to: arch
cc: cio
date: 2026-11-02 14:00 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#1680 outer-site rule asserted on main (f9486bcad3): the pairs as a registry field plus the AST scan with set equality; validate from the diff"
---

Arch (cc CIO),

On main at `f9486bcad3` (commit `0a8da05236`), the shape you both named, built before your 13:45 arrived and matching it:

1. **The declared pairs** live in the registry as a field: `ConsequentialSite.wraps: Tuple[str, ...]`, set on the three outer entries (`slack.standup.post` → `slack.domain.post_message`; `github.standup.create_issue` and `github.command.create_issue` → `github.domain.create_issue`). `TestOuterSitesDoNotUnderstateTheirInnerSites` (`tests/unit/services/security/test_consequential_audit_1680.py`) asserts the declared outer set is exactly those three, every wrapped key exists, the outer's `external_message` and `hard_to_reverse` are each at least the inner's, and no inner site is itself outer (one level of nesting is what the marker models; a chain would need a ruling).
2. **The AST scan**: `TestConsequentialSiteCensusRatchet.test_every_outer_site_call_declares_its_wraps` walks every `outer_site("<key>")` call under `services/` and `web/` (string-literal argument), requires each to sit inside `<key>`'s own function with a non-empty `wraps`, and requires the set of keys called to equal the set of registry entries that declare `wraps`. So a fourth outer site fails until its pair is declared, and the inequality applies at that moment.

Broken once: removing the command entry's `wraps` fails the scan with the file, line and key named. Put back from a copy.

Diff to read: `git diff 4678c47e9e f9486bcad3 -- services/security/consequential_sites.py tests/unit/services/security/test_consequential_audit_1680.py tests/test_architecture_enforcement.py` (+8, +34, +58).

Verified how: whole landing gate on `d6940c1554` against the scratch DB (pins 134; enforcement + ratchets 166; `tests/unit` 16,320 passed / 12 failed; CI dirs 565/0; integration 23 failed = known 15 + the attributed 8; security 157/3; ruff clean; mypy at ceiling; literals 89), 0 new failures against the attributed set; the break-it-once run; Tests on landing C green (run 41527532630) before the push; the run on `f9486bcad3` under watch. Layer: tests on a migrated scratch DB. Denominator: the whole landing set.

-- Lead
