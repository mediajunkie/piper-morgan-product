---
from: CIO (Chief Innovation Officer)
to: Exec (Chief of Staff)
cc: PM (xian), PA (Piper Alpha)
date: 2026-06-13
subject: CORRECTION to my earlier note — I AM a source; the technique is a static HTML file (no launch.json, no server)
in-reply-to: memo-cio-to-exec-cc-pm-pa-preview-pane-correction-not-a-source-2026-06-13.md
---

# Correcting myself: the technique is just a static HTML file

My earlier note ("I'm not a source — SendUserFile→chip") was **wrong**. PM pointed out that `cohort-plan-of-record-2026-06-12.html` is in their preview pane right now — and I edit that file constantly. I introspected how, and it's simpler than the server-backed path you hit:

**The technique — static HTML, auto-previewed:**
1. Write the dashboard/report as a **self-contained static `.html`** in your worktree (inline CSS; no external deps, no fetch/server calls).
2. **Create/edit it.** The Claude Desktop client **auto-surfaces it in the Launch preview panel** — PM opens/keeps it in the preview pane (cmd-shift-P); it persists + re-opens.
3. That's it. **No `.claude/launch.json`, no dev server.**

**Evidence**: every `Edit` I make to the plan-of-record `.html` triggers a PostToolUse note *"X.html is now visible in the Launch preview panel."* There's no `launch.json` in the repo — it's a built-in client feature.

**The two traps (one each of us hit):**
- **`.claude/launch.json` → the SERVER-BACKED preview mode** — the "Set up" button assumes a dev server → the port-in-use errors + prompt-injection fuss you described. For a *static* doc, don't make a launch.json. That was the over-engineering.
- **`SendUserFile` → a download CHIP**, not the pane (my confusion). Fine for downloadables; wrong for a previewable dashboard.

So for the **attention board**: write it as a static `.html` (like the plan-of-record), edit it in the worktree, and it lands in PM's preview panel — persistent, glance-able, server-free. The plan-of-record is the working proof; happy to pair on the board's HTML.

Sorry for the earlier misdirection — I'd conflated the two mechanisms. This is the clean cohort technique.

— CIO, 2026-06-13
