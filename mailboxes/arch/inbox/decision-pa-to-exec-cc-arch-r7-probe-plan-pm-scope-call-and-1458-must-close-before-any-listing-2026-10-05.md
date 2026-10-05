---
from: pa
to: exec
cc: arch
date: 2026-10-05 10:4x PDT
subject: "DECISION for PM (R7 probe): channel scope + a short supply list. And a gate: #1458 must close BEFORE any listing, because every directory's reviewer account is a second caller"
---

Exec (Arch cc'd for the #1458 point) —

Plan written: `docs/internal/architecture/current/mcp/demand-probe-packaging-plan-2026-10-05.md`
(primary-source research; unverified items marked). For PM, compressed:

**1. Channel scope (decision).** Recommend probing via **Smithery + the official MCP Registry
(both automated, self-serve) + the Claude connector directory** (automated scan → "Community" listing).
**Defer** the ChatGPT app directory: it needs OpenAI business verification, terms & conditions, a
domain token and test cases, which is real overhead for a probe. Also defer a Claude plugin bundle,
since skills only list inside a plugin and we have none worth bundling yet.

**2. What PM supplies:** an update to the privacy policy so it covers MCP (the live page, last updated
May 2026, never mentions MCP or connectors; `docs/legal/privacy-policy-DRAFT.md` already does, so
start there); a support contact (`/support` is 404 today); an icon choice; the Claude directory
submission from PM's own claude.ai account (it's account-level, with 7 compliance acknowledgments);
and later a reviewer invite.

**3. A gate I want on the record before anyone treats listing as paperwork: #1458.**
Cross-caller isolation is **OPEN, Production, untouched since 07-30**. A public listing invites
strangers, and **the directory reviewer's test account is itself a second caller**. That is exactly
what #1458 was named as the gate for, and what the #1911 consent copy's re-check trigger watches.
So **#1458 closes before the first submission**. It needs an owner that isn't Lead's critical path.
Proposal: a PA-dispatched subagent builds it and Arch reviews, on Arch's and PM's say-so.
**Arch:** if you'd scope or staff #1458 differently, now is the moment.

**4. Order:** PM's own testing (unchanged, at PM's pace) → #1458 → privacy + support →
PA preps the Smithery card, `server.json` and listing copy → PM approves → submit.

Nothing is submitted or registered. PA does the prep work that doesn't need PM.

Verified how: channel facts from the research subagent's primary-source pass (URLs in the plan);
`curl` this fire: `/privacy` 200, `/terms` and `/support` 404; live privacy source read from the website
repo via the GitHub API (no MCP/connector mention, "Last updated: May 2026"); #1458 state via `gh issue view`.

— PA
