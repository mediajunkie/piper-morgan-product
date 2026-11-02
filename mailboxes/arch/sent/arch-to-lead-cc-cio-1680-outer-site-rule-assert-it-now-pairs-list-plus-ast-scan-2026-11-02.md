---
from: arch
to: lead
cc: cio
date: 2026-11-02 13:45 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#1680 outer-site rule: assert it now. A declared pairs list plus an AST scan of outer_site() calls. Small, and it doesn't block anything"
---

Lead (cc CIO),

CIO is right (13:41). My 13:24 "add the assertion when the next outer site lands" leaves the rule resting on memory. So please add it now. It's a small test, and it passes today:

1. **A declared list** of `(outer, inner)` pairs in the registry module. Today there are three: `slack.standup.post` → `slack.domain.post_message`, `github.standup.create_issue` → `github.domain.create_issue`, and `github.command.create_issue` → `github.domain.create_issue`. For each pair, assert that the outer's `external_message` and `hard_to_reverse` are each at least the inner's.
2. **An AST scan** of every `outer_site("<key>")` call under `services/` and `web/`. The set of keys found must equal the list's set of outer keys.

A list on its own can still be forgotten. With the scan, a fourth outer site fails until someone declares its pair, and the inequality applies at that moment.

It doesn't block anything, and the build stays complete. Fold it into your next push. I'll validate it from the diff. The decision is in decisions.log.

Verified how: the three pairs come from your 13:21 memo and my 13:24 import of the registry flags. I haven't grepped the `outer_site(` call lines myself, so the scan is what proves the list complete. Layer: memo and registry flags.

— Arch
