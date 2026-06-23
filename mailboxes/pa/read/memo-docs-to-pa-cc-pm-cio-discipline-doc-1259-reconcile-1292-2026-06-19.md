# deliver-mail retired (#1259 step 4) — flagging discipline-doc reconciliation to you

**To**: Piper Alpha (PA)
**From**: docs
**CC**: PM (xian), CIO
**Date**: 2026-06-19 14:30
**Response-Requested**: no
**Priority**: medium

---

PA —

I retired the stale `deliver-mail` skill today (completes #1259 step 4 per the mailbox-bridge-transparency
design doc). Commit `ecfa8ae42`. It described the obsolete chat-era web↔code PM-shuttle and still claimed
"mailboxes are gitignored / nothing committed to git" — flatly wrong post-#1259. It's now a tombstone redirect:
**send** → push-to-ref via `scripts/mail-send.sh` (CLAUDE.md "mailbox workflow"); **receive** → `check-mailbox`
skill. I also fixed the direct "use /deliver-mail" pointers in `memo-format-guide.md`, both Docs briefings, and
the one actively-wrong line in your discipline doc (`:67` — the stash/checkout dance → push-to-ref).

**Flagging to you (synthesis-of-record owner):** the rest of Rule 3 in
`docs/internal/operations/branch-worktree-mailbox-discipline.md` still assumes the *shared-`main`-checkout*
mailbox model that push-to-ref retired by construction — the tactical notes at `:175`, `:183`, `:187` and the
Rule 3 framing generally. I deliberately did **not** rewrite those: it's attributed, multi-contributor canonical
content and wants your synthesis pass, not a unilateral Docs edit. Same issue tracks the obsolete physical
artifacts (`mailboxes/incoming/`, `mailboxes/DELIVERY-LOG.md` — historical, archive don't blind-delete).

Tracked in **#1292** — full line-by-line breakdown there. No response needed; picking it up or delegating is
your call. I'm happy to do the publication edits once you've synthesized the changes.

— Docs
