---
from: Lead Developer
to: CXO, PM
date: 2026-04-04
subject: Re: UAT Findings — Finding 1 and 2 addressed, more to do
---

Received and acted on. Here's where we are:

**Finding 1 (Floor LLM not reaching user) — FIXED in commit c2bdb772 (#940)**:
- Root cause confirmed: conversation task type was hardcoded to Anthropic, which was returning 404. OpenAI was working but never tried.
- Fix: Removed all hardcoded provider-to-task assignments. LLMClient now uses the user's configured default provider at runtime, with automatic fallback to the other provider if available.

**Finding 2 (Canned template masks all failures) — FIXED in same commit**:
- Conversational floor now classifies errors into three types with distinct messages:
  - Auth/key failure → tells user to check API key in Settings
  - Transient failure → suggests retry
  - No provider configured → explains what's needed

**Finding 3 (Handler pre-flight checks) — Not yet addressed**. Will file.

**Finding 4 (Todo completion) — Not yet addressed**. Root cause identified (mocked service in tests, real service failing). Needs investigation of TodoManagementService persistence layer.

**Finding 5 (Input parsing rigidity) — Not yet addressed**. Fix is straightforward (regex update) but bundled with Finding 4 investigation.

Additionally: Setup UI no longer mandates OpenAI. Any single LLM provider (OpenAI or Anthropic) is sufficient to complete setup.

Ready for re-test once Findings 4 and 5 are fixed.
