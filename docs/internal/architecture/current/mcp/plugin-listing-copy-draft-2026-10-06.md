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

## One-liner (≤200), 146 chars (counted)

A product-management colleague that knows your priorities and open issues, and turns them into a daily
standup and a ranked to-do list. Read-only.

## Description (≤2000)

Piper Morgan is a product-management colleague. Connect it once and your assistant can see what Piper
knows about you: your organization, active projects and stated priorities, what Piper has confirmed
about how you like to work, and your open GitHub issues.

Three skills put that to use:

- **What Piper knows**: see your profile, priorities and open issues in one place, including what
  Piper *doesn't* know yet.
- **Morning standup**: a thirty-second plan for today, tied to your stated priorities and to specific
  open issues.
- **Prioritize my issues**: your open issues sorted into do first, next, and defer or drop, each with
  one line of reasoning, plus the biggest judgment call made so you can overrule it.

**Honest by design.** Piper reports empty as empty. It never invents progress it can't see and labels
its own inferences. In our evals, each skill does this reliably where the same assistant without the
plugin does not.

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
