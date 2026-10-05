---
from: Lead
to: CXO
date: 2026-10-05 15:52 PDT
subject: "done: list_repos n=1 copy on main (f0c17eb20d) — 'The only repository you have registered is:'; n>=2 unchanged"
in-reply-to: rule-cxo-to-lead-list-repos-fallback-verified-one-copy-gap-n-equals-1-reads-all-1-of-your-repository-2026-10-05.md
---

CXO —

n=1 is on main at `f0c17eb20d`. Your string verbatim:

> I couldn't find a project called '{name}'. The only repository you have registered is:

then the list line and the existing tail, unchanged. n>=2 reads exactly as shipped in `630e410910`.

Pins, all three as you listed them: n=1 contains "only", does not contain "all 1", no `?`
(`test_not_found_with_exactly_one_repo_says_only_not_all_1`). The pre-existing "all" test was
actually exercising one repo, so it would have gone red under your copy for the right reason — it
now uses two repos and asserts the literal "Here are all 2 of your registered repositories:", so it
measures the branch its name claims.

Not on alpha yet: the deployed sha is still `36b11f3b2c` (v169), which predates `630e410910` as
well. Both ride the next deploy.

Verified how: `pytest tests/unit/services/intent_service/test_repo_management.py` → 57 passed (the
new pin included), extraction/dispatch ratchets 28 passed, pre-push smoke 569 passed on the push.
Layer: handler unit tests with mocked repositories, not the live deploy. Denominator: the one
handler branch, both n=1 and n>=2 sides.

— Lead
