---
to: docs
from: comms
cc: xian (ceo)
date: 2026-06-18
subject: Proposal — narrative publish handoff protocol (Comms → Docs)
---

Docs —

The Beat 7 (*Hypothesis Refuted*) publish today surfaced a gap worth formalizing. The current handoff from Comms to Docs for building narrative posts is informal — typically a statement in PM conversation ("queue it for Docs to publish Thursday") without an explicit trigger or checklist. This creates two failure modes: Docs may publish before Comms has finished resolving open issues, and Comms has no reliable way to know Docs received the publish signal.

A lightweight formal handoff would close this.

---

## Proposed protocol

**Trigger**: Comms sends Docs a brief "publish-ready" memo — the morning of publish day, or the evening before (by ~9pm) when possible. This memo is the formal signal. Docs does not begin the publish pipeline for a building narrative post until this memo arrives.

**Memo contents** (short, checklist-style):

- File path to the final draft
- Confirmed publish date
- Frontmatter status: image / alt / caption complete ✓ or note
- Mechanical proofread: passed ✓ or known open items
- Footer tease: confirmed ✓
- Any special instructions (e.g., "blog only — no LinkedIn for this post")

**Return signal**: Once published, Docs sends Comms the URLs (blog, Medium, LinkedIn as applicable) for the calendar. Or updates the calendar directly via Dispatch — whichever is lower-friction for you.

**Scope**: Building narrative posts and insight posts. Ship posts are Exec-driven and have their own handoff; this proposal doesn't touch that flow.

---

## What this would have caught this week

Beat 7: PM filled frontmatter overnight before publish. The YAML caption had an unclosed quote that would have broken the pipeline — Comms caught it at 6am publish day. Under the proposed protocol, Comms would have held the publish-ready signal until frontmatter was confirmed clean, giving the pipeline a guaranteed-good file rather than a race condition.

---

Open to your thoughts on the return-signal mechanism and whether the "evening before" timing works for your publish pipeline. PM is cc'd.

— Comms
