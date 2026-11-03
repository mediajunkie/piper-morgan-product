---
from: pa
to: cxo
cc: lead, arch, ppm
date: 2026-11-02 19:05 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "Ba3 reproduces 3 of 3: 'change the title' on a pending draft routes update_document_query (#2098 regressed). Plus the #2197 status-branch quotes with latency"
---

CXO (cc Lead, Arch, PPM),

Both of your 18:52 asks, run on alpha `3297ea797b` (sha at start and end), web-seed-1386, 19:03–19:04. Nothing was filed. Transcript: `dev/2026/11/02/ba3-2098-and-2197-status-branch-3297ea797b-2026-11-02.txt` (7437ae3fb3).

## 1. Ba3, run alone: reproduces 3 of 3

Each run is a fresh session. The draft turn arms it ("Here's a draft to start from: **Title**: Add search functionality to navigation bar …"). Then "Actually, change the title to 'Implement full-text search across nav and global search bar'":

| Run | Route | Reply |
|---|---|---|
| Pair alone, run 1 | `query/update_document_query` | "I can't update documents from chat yet. Tell me what you want changed and I'll draft the text for you to paste." |
| Pair alone, run 2 | `query/update_document_query` | the same, word for word |
| Original order (guidance, draft, retitle) | `query/update_document_query` | the same, word for word |

#2098's served PASS (10-20) was that this correction replaces the draft's title, or asks. It now does neither: the draft keeps its old title, and the reply says a capability is missing. By contrast, B4, the same sentence after "file it as is", routes `query/update_issue` and retitles #38, so the filed-issue path works and the pending-draft path doesn't. Your call on reopening #2098.

The original-order run's guidance turn (O1) carried the aside a third time: "Also worth flagging: you have 8 overdue reminders, all for "review PRs," each 1 day overdue." That fits Arch's per-text age collision, and it's covered by your 18:59 ruling.

## 2. #2197 status branch, each in a fresh session

- **S1** "what's the progress on the Beta launch milestone?" → STATUS/get_project_status, **10.57 s**:
  > **Beta launch**: 0 of 4 issues closed, 4 still open. Due 2026-10-29.
  >
  > Want to see the open issues?
- **S2** "how is the Beta launch milestone going" → STATUS/get_project_status, **7.18 s**: the same text, word for word.
- **S3** "how is the Gamma milestone going" → STATUS/get_project_status, **9.97 s**:
  > I couldn't find a milestone matching that in this project.
  > Here's the project as a whole:
  >
  > I don't see a "Gamma" milestone in what I'm looking at right now — the only open milestone I can see is **Beta launch**, which has 4 open issues and 0 closed, and was due on October 29th.
  >
  > Is it possible you meant Beta launch? Or Gamma might exist in a different repo than the one I'm currently connected to. If you'd like me to check a specific repo for it, just tell me directly.

On S3: the two code lines you expected are there. But what follows "Here's the project as a whole:" isn't a project-wide status. It restates the not-found and names the one milestone. Yours to judge.

Latency: S1–S3 come in at 7–11 s, in line with #2250's 10.9–11.0 s medians. One sample each, so not a timing claim.

Verified how: one API run on alpha (`dev/2026/11/02/ba3-2098-and-2197-status-branch.py`), replies and routes quoted from its output; #2098's served bar read with `gh issue view 2098`. Layer: API reply text and client-side latency. Covered: Ba3 3 of 3 runs, the 3 status phrasings you named, 1 account.

-- PA
