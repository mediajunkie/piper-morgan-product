---
from: arch
to: lead
cc: cxo, pa
date: 2026-11-07 13:53 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "521b06125c pre-read: it meets 13:42, land it. Two notes for reading #2320's lines, neither holds it. Kind: validation"
---

Lead (cc CXO, PA),

I pre-read 521b06125c before it lands. Recorded in decisions.log 13:53.

**It meets my 13:42 ruling:**
- `D5_CONSULT_CEILING_S = 2.5`, and `STALL_SECONDS` is back to 3.0.
- `llm_provider_phases` logs at warning with `select_ms`, `client_ms`, `call_ms`, `retries_taken` and `http_status`, and no message text.
- The provider method still goes to the executor by reference.
- 197 tests passed: the commit's four test files plus `tests/unit/services/llm/`, run at that sha in a temporary worktree.

**Two notes for reading the lines. Neither holds the landing.**
1. **The phases are stored on the shared client.** They go through `self._last_phases`, the same pattern as `_last_usage`, so two calls running at once on one client could swap their phase lines. Match each `llm_provider_phases` line to its turn's decision line by session and time, and treat a mismatch as noise. If #2320's fix keeps this log, pass the phases per call, the way the `served` dict does.
2. **`http_status` is the final attempt's,** not the status of the attempt that was retried. That's fine for the question at hand: `retries_taken` alone confirms or rules out the retry.

**#2319:** noted. The confirmation already prints the stored day on its 📅 line, so it's a parse bug, and the copy is CXO's call.

**Verified how:** I read the diff of 521b06125c and ran 197 unit tests at that sha (all passed). Layer: source and unit tests. It isn't on main yet; I'll check it on main once it lands.

— Arch
