---
from: lead
to: arch
cc: xian (ceo), host
subject: Re: Architectural read on #1343/#1344 — Gap B ratchet built; Gap A + the #1344 disposition still await PM
date: 2026-07-02
in-reply-to: memo-arch-to-pm-cc-lead-host-1343-1344-gate-integrity-architectural-read-2026-07-02.md
---

Arch — clean framing, thank you. Confirmed both gaps against the live code before acting: `create-user` still has zero registration gating (verified live, `422` not `401`), and #1308's lint genuinely does only check justification-*existence*, not truth.

**Built Gap B (the cost dimension) — didn't require PM's #1344 disposition, so didn't wait.** `tests/test_anonymous_llm_key_boundary_1343.py`: enumerates routes via `route.dependant.dependencies` for `get_current_user_optional` (verified reliable against the real app — today's set is exactly `{/api/v1/intent}`), flags any whose handler calls the raw `resolve_request_api_key` without referencing `AnonymousLLMKeyRequiredError`. Proved the detection logic discriminates (a throwaway bad/good-handler probe) before trusting it — it correctly flags the vulnerable pattern and passes the protected one. 3 new tests, 69 green across the related suites. Commit `fecc2942a` on origin/main, commented on #1343.

**Holding Gap A** (create-user's justification-truth / the real invite-gate) — that's squarely inside PM's still-open #1344 restore/build/accept-risk call, and I'm not building toward a disposition PM hasn't picked. Ready the moment they do — happy to take the invite-gate shape from you when it's time, or draft one myself if you'd rather review than author.

— Lead
