# Piper Morgan plugin: directory listing copy (DRAFT)

**Author**: PA, 2026-10-06. **Status**: draft for Comms' voice pass, then PM approval. Nothing submitted.
**For**: the Claude directory portal (name ≤100 chars, one-liner ≤200, description ≤2000, 1–5
categories) and the OpenAI plugin submission (icon, short and long description). Limits are from the
portal docs read 2026-10-05.

**Truth constraint (same rule as the consent page, #1911):** every claim below must match what v0.1.0
actually does. It is read-only, has three skills, and comes from one hosted connector. Re-check this copy
whenever the plugin's skills or the server's tools change.

## Name (≤100)

Piper Morgan

## One-liner (≤200), 145 chars (counted)

A product-management colleague who knows your priorities and open issues, and turns them into a daily
standup and a ranked to-do list. Read-only.

## Description (≤2000)

Piper Morgan is a product-management colleague. Connect Piper once and your assistant can see what Piper
knows about you: your organization, active projects and stated priorities, what Piper has confirmed
about how you like to work, and your open GitHub issues.

Three skills put that to use:

- **What Piper knows**: see your profile, priorities and open issues in one place, including what
  Piper *doesn't* know yet.
- **Morning standup**: a plan for today, short enough to read in thirty seconds, tied to your stated
  priorities and to specific open issues.
- **Prioritize my issues**: your open issues sorted into do first, next, and defer or drop, each with
  one line of reasoning, plus the biggest judgment call it made, so you can overrule it.

**Clear about what's missing.** Piper reports empty as empty. They don't invent progress they can't
see, and they label their own inferences. In our tests against sample data, each skill does this where
the same assistant without the plugin doesn't.

**Read-only.** The connector can't change anything in Piper or GitHub, and it can't see anyone else's
data. You approve access on a Piper sign-in page.

Piper Morgan is in invitation-only alpha. You need a Piper account at pipermorgan.ai.

*(≈1,150 chars. ⚠️ Add "Revoke anytime in Settings → Connected apps" only after the Revoke fix is live
on alpha and seen working.)*

## Categories (1–5), proposed

Productivity · Project management · Developer tools (for GitHub issues)

*(Exact category names come from the portal's picklist; map these at submission time.)*

## Still needed before submission (not copy)

- ~~Icon~~ RESOLVED 10-06 (PM): `pm-logo-color` → plugin repo `assets/icon.png` (2000px) + `icon.svg`.
- Support contact (PM; see `docs/legal/mcp-privacy-and-support-proposal-2026-10-05.md`).
- Privacy-policy MCP section live (same proposal).
- A reviewer test account (an alpha invite through the real invite flow).
- The Revoke fix live (`87e8bc9c49`) before any "revoke" sentence anywhere.

## Sources and changes (Comms, 2026-10-06, per PM)

- **Piper takes they/them** (PM 2026-10-06: they/them for Piper in product copy too, not "it"). The connector stays "it".
- **"short enough to read in thirty seconds"**: source is `piper-morgan-plugin/skills/morning-standup/SKILL.md`
  step 2 ("short enough to read in thirty seconds"). That's a **design target** in the skill, not a measured
  property, so the copy now says it as a target.
- **"In our tests against sample data… doesn't."** was "In our evals, each skill does this reliably…". Source is
  the plugin README ("all three skills score 1.00 with the plugin and 0.00 without") and
  `evals/results/` (gitignored, 6 runs 2026-10-06 13:49–13:54Z, mocked connector, 3 trials per arm). The
  saved runs are partial (1–2 cases each) and earlier ones include with-plugin scores of 0.5 and 0.67, so
  **"reliably" isn't shown yet**. PA: if one complete run reproduces the README's 1.00/0.00 across all
  cases, cite it here and "reliably" can come back.
- **"can't see anyone else's data"**: PM 2026-10-06. Data separation is a **release requirement**, not a
  copy hedge ("I will not release software that doesn't offer clear data separation"). So the claim stays,
  and the gate is release readiness (cross-caller isolation, #1458) before any listing goes live.
