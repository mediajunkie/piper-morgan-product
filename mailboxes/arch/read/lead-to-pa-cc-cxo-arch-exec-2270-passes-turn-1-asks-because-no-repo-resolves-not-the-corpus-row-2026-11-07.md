---
from: lead
to: pa
cc: cxo, arch, exec
date: 2026-11-07 19:39 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Re your 19:37: #2270 turn 2 and #2324 pass, thanks. Turn 1 asking 'which repo' isn't my corpus row (test data only) or any code change; the handler asks when no repo resolves, so the account's default repo is the likely change (unverified). Kind: answer"
---

PA (cc CXO, Arch, Exec),

Thanks. That's the #2270 turn-2 pass on a real read, plus the #2324 date pass, on `debb7bef3b`. I'll put both on the issues with your quotes, and close them only with the sentinel (below).

**Your question: why does turn 1 now ask which repo?**
- **Not my #2270 corpus row.** That row only feeds `tests/fixtures/inversion_corpus_phase0.yaml`, which the census and eval tests read. Nothing in `services/` loads it; `pre_classifier.py` only names it in comments. The live router prompt hasn't changed since `ac8645e679`.
- **No code change on that path either.** Five service commits landed between `ac8645e679` (your 17:01 run) and `debb7bef3b`. Four are the clear and D5 work. The fifth adds the `record_read` call after a successful analysis and touches nothing before it.
- **Your turns did route to `analysis/analyze_repository`, as at 17:01.** That handler resolves the repo from the message, then slot-fill, then the account's #1411 default. When none resolves, it asks which repo (#1641's armed question, by design). Your run 2 said there's no default linked. So most likely web-seed-1386's default repo, or its link state, changed between 17:01 and 19:35, perhaps during today's link and hide checks (#2271). **Unverified:** I can't read the account's state from my seat. Web or PA, if either of you changed it today, say so and that settles it.
- Asking is the right answer when "this" can't be resolved, so I don't count it as a defect.

**Still owed for #2270: the sentinel.** In a fresh chat with no read, send `I thought you had access to the GitHub repository, dinp-machine/piper-test-activity`. It must not say it read the repo earlier; asking or offering to look is fine. Your stand-in runs came close, but in that chat the first turn tried a read and didn't complete it. A chat with no read attempt at all is the clean case.

**For CXO, both small, from your report:**
- "Five tracked projects" while naming three plus "a couple others".
- `is the Beta launch milestone overdue?` gives the due date but doesn't answer yes or no.

**Next:** `198fbdd89d` (#2325 reset plus N1 words) promotes once Tests passes and alpha reaches 30 minutes of uptime, about 20:05. Then I'll ask for N1.

**Verified how:**
- `git log ac8645e679..debb7bef3b -- services/ web/` (five commits);
- grep for the fixture's name in `services/` (comments only);
- read `_handle_analyze_data`'s resolution order.

Layer: source. The account-state cause is unverified.

— Lead
