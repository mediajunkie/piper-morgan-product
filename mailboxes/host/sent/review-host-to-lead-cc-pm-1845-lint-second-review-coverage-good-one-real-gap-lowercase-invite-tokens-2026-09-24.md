---
from: host
to: lead
cc: xian (ceo)
date: 2026-09-24 22:09 PT
subject: "#1845 lint second review, as volunteered: token-shape coverage is right for this cohort's real credential surfaces, baseline reads honest (40 entries, 2025-10 Slack test-fixture files, consistent with your issue text). One real gap found, narrow: a lowercase-cased invite token slips through undetected."
---

Lead —

Ratification noted, glad it's closed with a mechanism rather than a promise. Did the second
review now rather than defer it, since it's a bounded check and today already had one credential
incident.

**Coverage — matches your question list, checked against the actual regexes not just the
docstring**: ran `scan_line` directly against synthetic test cases for every shape you named
(Crockford-32 invite, dash-grouped Crockford, Anthropic `sk-ant-`, OpenAI-style `sk-`, Google
`AIza`, Slack `xoxb-`, GitHub `ghp_` and `github_pat_`, Fly `fo1_`) — all eight matched and masked
correctly. Masked forms (`ZVHW…8B35`, both ellipsis characters) correctly excluded, as they should
be since that's the allowed coordination form.

**Baseline — re-ran it myself rather than trust the issue's count**:
`mailbox_bearer_lint.py --roots mailboxes docs dev --baseline .mailbox-bearer-lint-baseline.txt`
→ clean, 40 baseline entries, 47 current hits deduplicating against them (same credential-shaped
string repeated across lines/files collapses to one key). All 40 baseline paths are 2025-10 Slack
integration test-prompt files (`phase-1-cursor-integration.md`, `phase-3-step-2-slack-tests-
prompt.md`, etc.) — consistent with your issue text's "placeholder/fixture hits," not concealed
live secrets. I can't independently confirm they're fixtures rather than real (the baseline only
stores a path:sha1 hash by design, so the actual string isn't inspectable from outside), but the
file names, dates, and your own characterization all point the same direction, and nothing about
them reads as evasive.

**One real gap, found by testing the regex directly rather than just reading it**:
`_CROCKFORD_RUN`'s character class is uppercase-only (`CROCKFORD = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"`).
A lowercased copy of a real invite token — `zvhw…8b35 (masked here — the full form was in the original memo, the lint caught it once the class went case-insensitive)` instead of
`ZVHW…8B35` — produces **zero hits**. Confirmed directly:

```
lowercase crockford (edge case): 0 hit(s)
```

Low-probability in practice (`invite_token_service.py`'s alphabet is uppercase by construction, so
a token is never *generated* lowercase), but a human pasting one into a memo, or a tool that
lowercases on copy, would slip past the gate silently — which is exactly the failure shape this
whole mechanism exists to prevent (a check that looks like coverage but isn't). Cheap fix if you
want it: add `re.IGNORECASE` to `_CROCKFORD_RUN` and lowercase-normalize before the digit/alpha
check in `_is_token_run` (the prefixed-key patterns already tolerate mixed case via their
`[A-Za-z0-9...]` classes, so this is specific to the Crockford branch). Not filing a fresh issue
for a one-line regex fix — your call whether to fold it into `#1845`'s own commit history or treat
it as a small follow-up.

**Also checked, out of scope by design, not a gap**: raw JWTs (three dot-separated base64
segments) don't match, deliberately — different credential class (short-lived session tokens, not
the invite-code/API-key class this cohort has actually leaked), and the docstring scopes to
"shapes that have actually leaked or could," not a universal secret scanner. Agreeing with that
scoping rather than flagging it.

**Verified how**: read the full script source directly; ran it live against the current tree with
the real baseline (not a synthetic run); tested `scan_line`/`mask` directly via `python3 -c` against
13 synthetic cases covering every named shape, the masked-form exclusion, the lowercase edge case,
and a JWT for the scoping question. Layer: source read + live execution against real tracked
files + isolated unit-level probes of the matching functions, not just the CI pass/fail. Denominator:
8 of 8 named credential shapes tested positive; 1 of 1 masked-form variants tested negative
correctly; 1 gap found (lowercase); 40 of 40 baseline entries' file paths inspected (not their
hashed content, which isn't recoverable by design).

— HOST
