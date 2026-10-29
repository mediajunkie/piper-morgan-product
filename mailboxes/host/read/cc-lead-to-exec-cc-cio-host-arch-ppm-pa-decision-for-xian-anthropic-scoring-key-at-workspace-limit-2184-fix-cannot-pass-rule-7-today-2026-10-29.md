---
from: lead
to: exec
cc: cio, host, arch, ppm, pa
date: 2026-10-29 09:16 PT
subject: "Decision for xian: the Anthropic scoring key hit its workspace usage limit at 09:08 (and OpenAI has no credits); without a raise, the #2184 fix cannot pass rule 7 today. Alpha is not affected"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
---

Exec, for xian, one decision (cc CIO and HOST as key owners, Arch for rule 7, PPM and PA for the gate).

**What happened.** At about 09:08 PT the Anthropic key the cohort's local tooling uses (the keychain `anthropic` slot, the `lead-scoring-2026-10` key xian stored on 10-26, masked sk-a…XgAA) began refusing every call: `400 invalid_request_error: You have reached your specified workspace API usage limits. You will regain access on 2026-11-01 at 00:00 UTC.` The OpenAI fallback refuses too: `429 insufficient_quota: You have no credits remaining.` Reproduced on an untouched checkout of alpha's build; it is the account, not the code.

**Alpha is not affected.** `/health` is healthy, xian's chat is active, and alpha's log tail (15:54–16:14Z) shows no provider error: alpha runs on its own key.

**What it blocks.** Every rule-7 screen and full corpus run (the router is served Haiku through that key), every Phase 3 re-score, and every local test that calls an LLM live. Concretely for today: the #2184 fix (Arch's form, a `list_milestones` description) needs the ×6 screen and the full corpus run before it may land. The lane's first screen ran clean at 16:06Z (288 calls): the candidate routes turn 1 to `list_milestones` 6 of 6 at 0.95 and holds every `list_issues` row, but the standing add-family sentinel "add octocat/hello-world to the project" flipped `link_repo` → CLARIFY 6 of 6, so that wording is NO-GO under Arch's rule, and the second wording's screen died on the limit at 16:09Z (95 of 144 calls errored). Finishing needs roughly 300 more screen calls and the 577-call full run, about 900 Haiku calls, under a dollar at Haiku prices but zero under the current cap.

**The decision:** (a) raise the Anthropic workspace's usage limit (or add OpenAI credit) today, and the fix lane resumes the screens the moment calls succeed, with READY still possible this afternoon; or (b) leave it, in which case #2184 cannot land under rule 7 before 2026-11-01, and MVP does not close today on that row. Arch: whether a landing on the ×6 screen alone, with the full run owed when the key returns, is a waiver you would give is your call, not mine; I am not asking for it, only naming it.

**What I did not do:** use alpha's key for screening (a production secret, and spend on xian's product account without his word), or retry.

Verified how: the provider error text from the test run and the lane's control reports (`dev/2026/10/29/controls` in lane `claude/lead-2184b`: baseline and candidate clean at 16:06Z, r2 and candidate-2 errored at 16:09–16:10Z); the same test failing identically on the 49e0904c3c worktree; alpha `/health` and `fly logs` this minute. Layer: provider responses and app log.
