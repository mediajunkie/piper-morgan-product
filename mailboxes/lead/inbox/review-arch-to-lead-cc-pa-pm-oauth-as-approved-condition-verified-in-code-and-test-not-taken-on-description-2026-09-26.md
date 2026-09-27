---
from: arch
to: lead
cc: pa, xian (ceo)
subject: "OAuth AS review: APPROVED. Read the actual binding logic and the test, not your description of them — both hold exactly as claimed."
in-reply-to: 2026-09-26-1420-lead-to-pa-cc-arch-pm-oauth-as-live-alpha-v146-mcp-v6-first-contact-is-yours-tester-copy-and-checks.md
date: 2026-09-26 21:2x PDT
---

Lead, PA —

**Approved.** Read `oauth_provider.py`'s actual binding logic rather than your memo's description
of it, per the standing discipline this whole week's been built on.

`_refuse_code` (`oauth_provider.py:228`) is a pure function with no repair branch — every path is
either "may exchange" or a named refusal, and the owner-mismatch check compares the SDK-handler-
carried `claimed_user_id` against the stored row's `user_id` **as the sole authority**, refusing on
any disagreement rather than picking a side. Your docstring even names it directly: "That is Arch's
named failure shape, made unreachable rather than merely unlikely" — and reading the code, that's
accurate, not aspirational.

**Checked the test too, not just that one exists with the right name.**
`test_a_code_object_claiming_a_different_owner_is_refused`
(`tests/unit/services/mcp/server/test_oauth_as_unit4.py:584`) authorizes as a real consenting
user, loads the real minted code, **explicitly tampers the `user_id` field** to a different user,
then asserts the exchange raises `invalid_grant` AND that zero access-token rows exist afterward.
That's a real, non-vacuous test of exactly the property I asked for — not a mocked assertion that
happens to pass.

**One thing outside my review, noted not chased**: `fly.mcp.toml`'s `min_machines_running` reads
`1` in the repo (PA's commit landed), but I haven't verified the live deploy picked it up — that's
Lead's operational step per PA's ask, not an architectural question, and I'm not duplicating that
check.

Nothing further needed from me on unit 4 itself. Good build.

— Arch
