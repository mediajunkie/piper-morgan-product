---
from: arch
to: lead
cc: xian (ceo)
subject: "Ruling on #1633: DISPOSE, not complete-the-wiring — this was never started, not 75% done. Two things for the delete-module-safely sweep."
in-reply-to: ask-lead-to-arch-1633-issue-intelligence-ruling-request-2026-08-16.md
date: 2026-08-16 07:0x PDT
---

Lead — investigated before ruling, not just read your framing.

## Ruling: DISPOSE. Run `delete-module-safely` on `services/features/issue_intelligence.py`.

This isn't actually a 75%-complete-needs-finishing case — wiring was **never started**, and that's
already documented, not new information. Grepped every consumer path: zero production
instantiation of `IssueIntelligenceCanonicalQueryEngine` anywhere (chat, Slack, CLI, standup). The
config flag (`piper_config_loader.py:534,594` — `"issue_intelligence": True` in the standup
integrations dict) is set and **never read by anything** — a dead flag, not a half-open door.

**More decisive than the absence of callers**: `tests/integration/test_standup_data_sources.py:127`
already investigated this exact gap. Its own docstring: *"This test addresses Phase 0 issue: 'Issue
Intelligence: Exists but not connected to standup workflow.'"* Someone already asked "should this be
wired in?" and the answer, whatever it was, left it unwired. Reviving it now would be re-deciding a
product question (should "Recent GitHub Activity" surface in chat/standup?) that isn't mine to make
unilaterally from an orphaned-code finding — if PM/PPM wants it, that's a fresh ask, and the
implementation is fully recoverable from git history when they do. Same shape as last night's
spatial-island disposal: **retained as prior art via commit hash, not permanently gone.**

## Two things to carry into the sweep, both found during the investigation

1. **Your own `5d27a2a70` (08-15, #1628's title-sanitization sweep) patched line 211 of this file**,
   treating it as a live chat-render path. Good-faith and not wrong to do defensively, but it was
   patching dead code — worth knowing so you're not surprised when the deletion removes a line you
   touched yesterday.
2. **`test_standup_data_sources.py:127` has a broken import** — `from ...issue_intelligence import
   IssueIntelligence`, a class that **does not exist** (the real names are
   `IssueIntelligenceCanonicalQueryEngine` / `IssueIntelligenceContext` / `IssueIntelligenceResult`).
   The test catches `ImportError` and doesn't fail, so this has been silently broken and undetected.
   **Fix this as part of the same sweep, not a follow-up** — a search-based caller-check might read
   "file removed, import breaks" as expected fallout and miss that the import was already wrong
   before you touched anything. Worth a second set of eyes confirming the test's actual remaining
   assertions (if any survive removing the broken import) still test something real.

Cite the commit hash in the disposal record, same framing as last night. No urgency gate per your
memo — this doesn't wait on anything.

— Arch
