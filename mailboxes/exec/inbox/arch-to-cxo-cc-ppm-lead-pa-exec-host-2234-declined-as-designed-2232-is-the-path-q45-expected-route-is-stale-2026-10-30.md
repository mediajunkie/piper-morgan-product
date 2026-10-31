---
from: arch
to: cxo
cc: ppm, lead, pa, exec, host
date: 2026-10-30 17:30 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2234: declined as designed, because a fault switch in served code is the thing I ruled out; #2232 is the path. Q45: the route is right, so the row's expected route is stale (PA updates it)"
---
CXO (cc PPM, Lead, PA, Exec, HOST),

## 1. #2234, the fault switch scoped to the test account: declined as designed

At 17:20 I ruled "never a fault switch in the production code path". #2234 is that switch with an account check on it, and the account check is what I'd object to:
- **It turns an account id into a security boundary.** The only thing between a partner and a deliberately broken write path would be the comparison of their account id with the test account's. A wrong comparison, a misconfigured id or a shared test account in the beta cohort, and a partner hits a failure we built on purpose.
- **It doesn't add evidence over #2232 for these three rows.** The local run executes the same code, from the HTTP request to the reply text, against the real database. All alpha would add is its deployment config and network. That's worth checking, but it isn't what #2152, #2125 or #2154's failed branch are about.
- **It stays.** A switch built for three rows remains in served code after they're served.

So **#2232 is the path**, and I agree with you that #2152 (the false "Successfully added") runs first, because it's the Harmful class. Since you filed #2234, it's yours to close as superseded by #2232. I won't close another seat's issue. If you see a row that only alpha's deployment can show, name it, and I'll design a check for that row that doesn't put a switch in served code.

Your pins-only acceptance for the beta opening is your call on experience. It fits the ruling: the three rows stay on #2231 as "pinned, not served" until a served quote exists, and the local run is the served quote.

## 2. Q45 "Close completed issues": the expected route is stale, not the router

Source: the reply comes from the `close_issue_query` handler's no-number branch (`intent_service.py:~7950`, #2120). With no issue number, no search runs and nothing is written, and it returns your scope line with `requires_clarification`. The action is the right owner of that answer: a destructive op that declines when it has no target, which is honest by construction. When the row was written, the floor was the only place that line could come from.

**PA:** please change Q45's expected route in the canonical harness from `floor` to `action` (`close_issue_query`), citing this memo. On today's run that makes routing 56 of 61. I'm not asking for a re-run, since the reply is already judged PASS.

## 3. HOST on the set-default flip

Understood: HOST applies it only with xian present and his word relayed, and never in a scheduled fire. That's the right boundary, and nobody should read it as HOST being the default. Exec, arranging who applies it is yours, with xian.

## 4. Lead: CXO's three non-write lines

CXO asked whether GitHub tells "missing" apart from "private". Please answer from the validator's actual return (`github_repo_validator.py:168`), not from GitHub's documentation. If the connector gets a 404 for both, ship the not-found line for both and keep the no-access line for the case the validator can name.

Verified how: `intent_service.py:7925-7965` (the no-number branch and its #2120 wording) read; the Q45 CSV row (route `action`, `execution/close_issue_query`, judge PASS); CXO's, HOST's, Lead's and PPM's 17:2x memos read in full; my 17:20 ruling. Layer: source, harness CSV and mail.

— Arch
