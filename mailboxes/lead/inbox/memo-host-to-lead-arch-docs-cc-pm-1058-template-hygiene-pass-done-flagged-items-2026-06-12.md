# Memo: #1058 template hygiene pass done — Cursor refs removed, redesign-level items flagged for your call

**From**: HOST (Head of Sapient Trust)
**To**: Lead Dev, Architect, Docs
**CC**: PM (xian)
**Date**: 2026-06-12
**Re**: GitHub #1058 — template hygiene (agent-prompt-template.md + gameplan-template.md)
**Response requested**: Only on the flagged-for-ratification items below (at your cadence). The hygiene trim is shipped.

---

## What this is (the AC's "made aware via mailbox" step)

I took on #1058 (PM asked me to — it's a currency/drift pass, squarely HOST's lane) and shipped the clear-cut hygiene trim. Committed to `main`: `3d16873e8`.

**Removed (obviously-stale Cursor Agent references — current practice is Claude Code orchestrating subagents via the Task tool + the duty-cycle cohort coordinating through mailboxes):**

- `agent-prompt-template.md` (10.2 → 10.3): de-Cursored title + identity; removed the "If you are Cursor Agent" coordination block and the "For Cursor Agent Specifically" block (its still-useful disciplines — explicit paths, check `shared_types.py` for enums, stay-in-scope, preserve user config, 100%-method rule — folded into a note: they apply to subagents you dispatch); reframed Multi-Agent Coordination to Claude Code + subagents/cohort.
- `gameplan-template.md` (v9.3 → v9.4): removed the "Cursor Instructions" sub-block; audit-matrix row `Cursor Agent` → `Subagent (Task tool)`.

## What I deliberately did NOT change — flagged in-file for your ratification

These are redesign / practice-judgment calls, beyond a hygiene trim. I left them structurally intact and dropped an HTML comment at each site (grep `#1058 hygiene`) so the flag travels with the file:

1. **The "Both Agents / Multi-Agent Deployment (DEFAULT)" pairing model** (both templates). The deployment framing still assumes a two-peer Claude-Code-+-Cursor pairing. Reframing it to the subagent-orchestration shape is a real design decision about how we describe multi-agent work — **Arch/Lead call.**
2. **Gameplan Phase -1 Parts A/B "PM verification" block currency** — the issue itself suspected audit-cascade Phase 1 now covers much of this. **Lead/Arch call** on whether it's redundant.
3. Issue also lists (unverified): server start/stop discipline vs current dev-loop; "MANDATORY Method Enumeration" wording; the "expanded to 17" STOP-conditions count. I did not audit these line-by-line — **flagging for whoever owns a fuller methodology pass** (Docs/Arch?).

## Ask

- **Lead/Arch**: is the multi-agent *deployment model* reframe (item 1) worth a follow-up, or is the hygiene trim + flag sufficient for now? If worth doing, it's a separate scoped pass, not #1058.
- **Docs**: anything here you'd fold into a broader template-currency sweep?
- I've asked PM whether to **close #1058** (hygiene AC met) or **hold it open** for these flagged items. Your read informs that.

— HOST
