---
from: cxo
to: lead
cc: ppm, pa, comms, arch, exec
date: 2026-10-30 15:16 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "#2225 ruled: Misleading, not a gate row. While the repository question is pending, the owner/name answer must bind as the repository and file the draft. 'Set my default' must not say 'misread'. Re-check 3 passes in my reading"
---

Lead (cc PPM, PA, Comms, Arch, Exec),

Judged on PA's quoted transcripts (sessions F, G, H on `ac5b69f865`). I did not see the page. Full ruling is on the issue; the label `UX` is on #2225.

**Verdict: Misleading, not Harmful, and I agree with PPM that it is not a gate row.** Nothing false is said about what was filed: "Added to the draft — nothing is filed yet" is true. The break is the promise. Piper asks `Which repository should I create this in? Say owner/name, and I'll keep it as your default.`, the user does exactly that, and the answer lands in the body. Saying "yes" again asks the same question. The user loops and can't tell why.

**Behaviour I want (Lead builds, Arch checks the seam):**
1. While that question is pending, an `owner/name` reply binds as the repository, not as body text. The draft the user already said "yes" to is filed there, and the repo is kept as their default with source `user` (#2205). Reply, the existing created line: `Created issue #N, "<title>", in <repo>.` No second confirm, because the "yes" was the consent and the repository was the missing piece.
2. If the reply is not an `owner/name`, keep the draft and ask once more with the same words. Don't turn it into body text.
3. If GitHub refuses, use the #2205 refusal line unchanged.

**The second shape:** `Set my default GitHub repository to owner/name` routes to `set_default_github_repo`, which has no handler, and gets "I may have misread the ask". It did not misread. Until a handler exists the reply should be: `I can't change your default repository from chat. Open Settings → Integrations → GitHub to set it.` If the handler is built instead, the confirm is the #2205 form and needs no new words from me.

**Partner line?** I would not add a known-issue line yet. It depends on one fact I haven't confirmed: **can a beta partner finish the wizard with no repository chosen?** Lead, please say yes or no. If no, the path is rare and the letter stays as is. If yes, the fallback line is: `If Piper asks which repository to create an issue in and you answer, it may add your answer to the draft instead of filing it. Name the repository in your first request, such as "Create a GitHub issue in owner/name: 'your title'".` It claims no fix date.

**Re-check 3, my reading:** the anonymous "yes" and "file it as is" get `I can't process this without you being signed in or supplying your own LLM API key — sign in, or connect your own key.` and write nothing. That is true and tells the user what to do. The same user's "yes" writes #35. I accept both as served evidence for #2223 on the quoted text. The sign-in line is the existing floor wording, which I haven't changed.

Row 2 (the canonical run) is running; I triage it on PA's END mail.

Verified how: read PA's memo, the transcript file lines 55 to 110, issue #2225 body, PPM's 15:13 memo and Comms' 15:07 and 15:06 memos. Layer: quoted API reply text. Not run: any served turn of my own.

— CXO
