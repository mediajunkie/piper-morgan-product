---
to: xian (ceo)
cc: exec, lead
from: arch
date: 2026-09-23
subject: "#1744 — behaviorally confirmed, not just config-checked. My own push this fire went through the new ruleset with zero bypass notice. Closing."
in-reply-to: rule-arch-to-pm-cc-exec-pard-lead-1744-verified-clean-recommend-delete-classic-on-main-only-2026-09-23.md
---

Noticed classic protection is gone (`GET .../branches/main/protection` → 404, "Branch not
protected") — you must have acted on this afternoon's recommendation. Checked what that actually
proved rather than just confirm the config changed:

**My own commit this fire pushed to `main` with no "Bypassed rule violations" message** — the exact
notice every prior push this week has printed, because it was always classic's `enforce_admins:
false` doing the bypassing. This time there was nothing to bypass and nothing was blocked. **That's
the behavioral proof the ruleset's Admin bypass actually works**, not just a config field that reads
correctly — a real admin push went through the new mechanism alone, once classic was no longer there
to mask it either way.

**`main-old` confirmed untouched**: still exists, still carries its own separate `enforce_admins:
true` protection, unaffected by anything that happened to `main`. Nobody needs to worry about it as
a side effect of this closing.

**#1744 is done.** Ruleset live, Admin bypass behaviorally confirmed (not just configured), old
protection retired, `main-old` correctly left alone pending its own separate review of the 503
commits. Nothing further from me on this issue.

**Verified how**: `gh api .../branches/main/protection` → 404 (classic gone); `main-old`'s
protection re-checked directly, still `true`; the ruleset still active and unchanged. My own push
this fire is the behavioral evidence, not inferred from config alone. **Layer: live GitHub API +
one real push, this session.**

— Arch, 2026-09-23
