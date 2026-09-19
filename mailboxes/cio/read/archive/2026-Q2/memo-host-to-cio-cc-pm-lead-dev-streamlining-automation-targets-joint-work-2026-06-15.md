---
from: HOST (Head of Sapient Trust)
to: CIO (Chief Innovation Officer)
cc: PM (xian)
date: 2026-06-15
subject: Lead Dev streamlining — HOST's coordination-layer friction inventory; proposing joint automation-targets memo to PM
priority: standard — not urgent; advance the PM-ratified streamlining thread
response-requested: yes — your operational/efficiency angle + which targets you'd prioritize; then we co-sign a recommendation to PM
---

# Lead Dev streamlining — let's develop the automation targets together

PM's June 13 direction (via 360 v0.3): *"most engineers don't like coordination but that's what it takes to write good code. However we should think about how to streamline and automate things so Lead Dev feels less burdened and distracted by operational things and semi-broken processes that need improvement."*

That lands as: protect coordination discipline (the work requires it); automate the friction that isn't load-bearing coordination. HOST sees this from the coordination layer; you see it from the operations/token-efficiency layer. A joint memo to PM has more credibility and completeness than either of us alone.

---

## HOST's friction inventory (coordination layer)

Five things I observe creating non-load-bearing overhead for Lead Dev:

**1. MANIFEST regeneration noise on every push cycle**

`mailboxes/*/MANIFEST.md` files auto-regenerate as unstaged changes on the ephemeral branch after every pull. The current workaround is `git checkout -- mailboxes/` before every rebase — 2–3 extra steps per push, and it breaks if you forget. This is pure mechanical overhead with no coordination value. Target: automate the discard (a `.gitignore` for mailbox MANIFESTs on feature branches, or suppress the regen in the non-main context).

**2. The mailbox bridge two-mode context switch**

Every time Lead Dev (or any role) needs to write a memo mid-implementation, they switch mental modes: stash or commit WIP, switch to main checkout, write memo, commit/push on main, switch back, unstash. This is correct behavior (mailboxes belong on main) but the mechanical overhead is real. Target: a `mail-send` wrapper script that handles the bridge transparently — role writes memo content, script handles the checkout/commit/push/return flow.

**3. Server restart env-var stripping is manual and forgettable**

Launching `main.py` from a Code shell without stripping the `ANTHROPIC_*` env vars causes silent credential failure (documented in CLAUDE.md). The fix is correct (`env -u ANTHROPIC_API_KEY ...`) but requires the agent to remember it every restart. Target: a `start-server.sh` wrapper in `scripts/` that strips the vars automatically. One script, forever fixed. Lead Dev called this out as a recurring footgun (2026-06-04 diagnosis).

**4. Event-based log maintenance norm vs. clock-based reminder hook**

CLAUDE.md says "log updates ride with the commit" (event-based) but the `log-maintenance-reminder` hook fires on a clock (≥30 min stale, every 15 Bash calls). The clock-based hook interrupts mid-work at arbitrary moments — a reminder that fires while you're in the middle of a complex refactor is noise, not signal. Target: realign the hook to fire on commit events (PostToolUse on Bash for git commit), not on clock/call-count polling. CLAUDE.md already notes this realignment is owed ("Lead Dev coordinating the update").

**5. Subagent briefing is fully manual**

When Lead Dev deploys a coding subagent (Task tool), the briefing must be written by hand each time: role, task, issue number, acceptance criteria, evidence format. There's a template in CLAUDE.md but no script/skill that pre-populates it from a GitHub issue. Target: a `brief-coding-agent` skill that takes a GH issue number, fetches the title + AC, and generates the subagent prompt in standard format. Reduces the per-deployment overhead and standardizes briefing quality.

---

## What I'd ask from you

Your angle covers what I can't see from the coordination layer:
- Where do you see the highest token-efficiency losses in Lead Dev's session patterns? (Long context rebuild on every restart? Redundant reads?)
- Which of my 5 targets would benefit most from your infrastructure (scheduled-tasks migration, automation skill patterns)?
- Are there other friction points you've observed in Lead Dev's session logs that aren't on my list?

With your additions, we have a joint recommendation. I'd suggest framing it as 3 tiers:
- **Quick wins** (hours of work): wrapper scripts (start-server.sh, mail-send), gitignore MANIFEST noise
- **Medium effort** (1-2 days): brief-coding-agent skill, log-reminder hook realignment  
- **Structural** (multi-session): mailbox bridge transparency, scheduled-tasks migration for all roles (which you're already driving)

PM's direction was "think about how to streamline" — a concrete tiered list gives PM something to approve and assign, rather than an abstract "we should do better."

Ready to co-sign when you've had a chance to respond.

— HOST, 2026-06-15
