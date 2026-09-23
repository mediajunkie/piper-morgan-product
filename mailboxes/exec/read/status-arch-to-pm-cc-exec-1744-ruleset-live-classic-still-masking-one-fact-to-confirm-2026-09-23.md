---
to: xian (ceo)
cc: exec
from: arch
date: 2026-09-23
subject: "#1744 — I see the ruleset you created. Correct order, nothing broken, one fact I can't verify without your word or a riskier test."
---

# Noticed the ruleset exists — checked it before saying anything

Found this by routine re-check, not by you telling me — worth knowing your own change didn't need
me to confirm it landed; I just happened to look.

**You created**: ruleset `"main - bot delivery (#1744)"`, target `refs/heads/main`, enforcement
**active**. Rules: `deletion` + `non_fast_forward` (the force-push/deletion protections classic had
— correctly re-expressed, not dropped). Bypass actor: one `RepositoryRole`, `actor_id: 5`.

**You did the safe half first, correctly**: classic branch protection is **still fully active**
alongside the new ruleset (`enforce_admins: false`, same required check). That's exactly the order I
recommended — create the ruleset, don't delete classic yet. Nothing is broken; every push today
(including mine, this fire) has succeeded, but **that's provably classic's doing, not the new
ruleset's** — classic's `enforce_admins: false` would let admin pushes through regardless of whether
the ruleset's bypass actor is configured correctly. So today's clean pushes are not yet evidence the
ruleset itself works.

## The one thing I can't verify from here

**Is `RepositoryRole` id `5` actually "Repository admin"?** GitHub doesn't publish this mapping in
any doc I could find (I checked before declining to guess at it originally) — I only know it's
*some* role, not which one. If it's admin, we're done and safe to delete classic whenever you like.
If you picked something else in the dropdown (Maintain, Write), deleting classic would leave all 12
agent pushes hitting the required check for real, since agents push as your admin account and that's
the only thing currently exempting them.

**I'm not going to guess at this** — it's exactly the kind of fact CLAUDE.md says to look up or ask
about, never assume. Two ways to close it, your call:

1. **Tell me which role you picked in the UI dropdown.** Fastest, and you already know the answer.
2. **I test it directly** — a scratch commit pushed with classic protection's admin-bypass
   deliberately not relied on. This means briefly working around `enforce_admins` in a way I'd want
   your explicit go-ahead for first, since it's a live change to `main`'s protection during the
   test window, not something to do silently.

**My default, absent your answer**: leave classic in place until this is confirmed one way or the
other. It costs nothing to wait — classic is doing real work right now and nothing needs the
ruleset alone to function yet.

**Verified how**: `gh api repos/.../rulesets` and `.../rulesets/{id}` read directly this fire;
classic protection re-checked via `gh api repos/.../branches/main/protection` in the same fire, not
assumed unchanged since last week. **Layer: live GitHub API. Denominator: 1 of 1 rulesets on the
repo read in full; both protection mechanisms checked, not just the new one.**

— Arch, 2026-09-23
