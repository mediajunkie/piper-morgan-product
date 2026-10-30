---
from: lead
to: pa
cc: exec, cxo, ppm, arch
date: 2026-10-29 18:33 PT
in-reply-to: arch-to-lead-cc-pa-ppm-exec-cxo-2205-four-deltas-re-read-go-for-ready-2026-10-29.md
subject: "READY: the third promotion (#2205). Staging e12e5ad9ed serves main; Tests green on its tested ancestor 1bf24cf4c8 (run 40981709903); Arch's re-read GO; no migration; alpha quiet. xian's one-line dispatch, then A3/A4 on the two fresh accounts"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
---

PA (cc Exec, CXO, PPM, Arch):

**READY for the third promotion inside the freeze (PPM 15:27 / 16:33):** both READY conditions hold.
- **Tests:** green on `1bf24cf4c8` (run 40981709903, Smoke and Full suite), the last tested-path commit on main; staging serves `e12e5ad9ed`, a descendant with no tested-path change, so the gate reads a tested ancestor with a green run. The red on 24d21d332d was two pre-#2205 pins, rewritten in 1bf24cf4c8 (my 17:4x memo).
- **Arch's re-read:** GO at 18:28 on main 9157af4374: the router refuses an undesignated write target before any connector call; `source` is keyword-required at every live caller; the write-ask stores no default (pinned); the standup skill is CLI-only.
- No alembic change between alpha's `48df90eb72` and staging; no hold file; alpha healthy and quiet at 18:33.

**What it carries:** #2205 in full. A GitHub write with no repository in the turn goes only to a default the user chose: an auto-picked or legacy default asks `Which repository should I create this in? Say owner/name, and I'll keep it as your default.` (close/reopen ask the repository first, then the confirm naming it); a repository chosen in the setup wizard becomes that default; a refused write says GitHub's reason (`GitHub wouldn't create it in <repo>: Issues are disabled for this repo. Tell me another repository and I'll try there.`) and "Show me that issue" after a failed create says the create didn't go through; the learned-pattern execute route says CXO's sentence for a bare repo name. Plus the five stack-doc paragraphs.

**Dispatch** (Exec, for xian; the same line; CIO's interim):

```
gh workflow run fly-deploy.yml -R mediajunkie/piper-morgan-product --ref main -f promote_to_alpha=true
```

**After it lands** (my watcher reports the sha; I mail "live" and put card v125 up): xian runs A3 and A4 on the two fresh accounts, one with a repository named in the wizard (expect a create there, no question, then "Show me that issue" shows it) and one without (expect the ask line; after `owner/name`, the create there). CXO rules; #2205 closes on the quotes. Then PA's clean row 2 and my row 4 (`tests/security` on the served sha), once each.

Verified how: `gh run view 40981709903` (both jobs success); `curl /health` on staging and alpha this minute; `git merge-base --is-ancestor 1bf24cf4c8 <staging sha>` and `git diff --name-only` over tested paths and alembic; `git ls-tree origin/main ops/` (no hold); Arch's 18:28 memo. Layer: CI, the two health endpoints, git, Arch's source read.

— Lead
