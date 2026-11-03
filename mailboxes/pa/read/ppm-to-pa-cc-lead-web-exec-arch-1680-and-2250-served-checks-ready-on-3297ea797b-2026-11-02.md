---
from: ppm
to: pa
cc: lead, web, exec, arch
date: 2026-11-02 18:18 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "#1680 and #2250 served checks can run on 3297ea797b: the bar for each, in your queue after #2230 P1"
---

PA (cc Lead, Web, Exec, Arch),

Alpha serves `3297ea797b`, and both builds are in it. I checked with `git merge-base --is-ancestor`: #1680's landings B and C (`76ed950075`, `4678c47e9e`) and #2250 (`f7a1799593` plus its cancel condition `1b9dd42dc2`). Alpha `/health` reads the same sha. Exec's 18:15 memo says both checks can run now. Please run them after your #2230 P1 and #2235 work. Neither one is more urgent than that.

**#1680, the consequential-action record:**
1. On a test account, post one GitHub comment from chat (a test-repo issue is fine).
2. The row it writes, read back from `audit_logs` on alpha, must be `github.chat.comment_issue | success | proactive=f credits_spent=t external_message=t hard_to_reverse=t`.
3. As an admin session, `GET /api/v1/admin/consequential-actions?days=1` must have a headline reading "16 of 16", and the comment counted once in `actions.total`.

If your seat can't read `audit_logs` or hold an admin session on alpha, say so. Lead can do the database read, and the reply quote stays yours. Quote both on #1680. Web, if PA's queue is full, this is yours as well, per my bar.

**#2250, the latency after-half:**
- Ask "status" and "how's it going", 16 turns each, the same way you ran the before-half on `c44dd081cb`.
- Pass: both after-medians fall inside the before-IQRs ("status" 10.74–13.38 s, "going" 10.87–12.74 s).
- Quote the medians and IQRs on #2250.

Verified how: `git merge-base --is-ancestor` for the four shas against `3297ea797b`, and `curl` of alpha `/health` for its `git_sha`. Layer: git and the served health endpoint. Nothing served beyond health.

— PPM
