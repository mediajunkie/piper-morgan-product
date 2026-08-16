---
from: docs
to: xian (ceo)
subject: "The 'sync-pm-local path is broken' report you got today was wrong on its central claim — verified, one real fix applied, one false one skipped"
date: 2026-08-16 13:4x PT
---

PM — a report landed in my inbox this morning from a general-purpose Claude Code agent (no
assigned role), claiming `sync-pm-local.sh` "cannot locate PM's checkout at all," that your real
checkout is at a space-containing path (`/Users/xian/Development/piper morgan/piper-morgan-
product`), and that CLAUDE.md's HARD RULE names a path that doesn't exist. It also claimed to
have fast-forwarded your checkout and cleared 7 dirty MANIFESTs on it.

**I checked before acting on it, and the central claim is false.** Worth you knowing directly,
both because the report is confident and detailed (reads like real diagnostic work), and because
it's the same shape of thing I published a post about yesterday — a fluent, specific, wrong
claim about system state.

**What I verified, directly, not by re-reading the report**:
- `git worktree list` (run fresh, right now) shows your checkout at
  `/Users/xian/Development/piper-morgan-product` — hyphenated, no space. The space-form path the
  report cites does not exist anywhere on disk; I checked.
- The script's actual candidate list already tries the hyphenated path *first*, and it's a valid
  git checkout with commits landing today.
- I ran the script myself (`--dry-run`) just now: it found the checkout fine and reported
  "nothing to clear."
- The commit hash the report cited (`04005bded`) does genuinely appear in your checkout's reflog
  two pulls back — so a real sync did happen at some point today, using the correct existing
  path. What's false isn't "a sync happened," it's the report's *explanation* of why one was
  supposedly needed (a broken path that in fact isn't broken).

**One thing in the report was real, and I fixed it**: CLAUDE.md's description of the script's
behavior was genuinely stale — it described v1's "abort the whole sync if anything's dirty"
behavior, when the script has actually run on v2's surgical 3-tier classifier since July 7. Fixed
that line; left the HARD RULE path alone since it's correct.

**Not touched, and not needing to be**: the report's recommendation to add a third candidate path
to the script, and to fix CLAUDE.md's HARD RULE path — both premised on the false claim.

No action needed from you. Flagging mainly so a false "your checkout's been 900 commits stale"
claim doesn't sit uncorrected, and so if this same report reached anyone else, you know it's
already been checked and doesn't hold up.

— Docs
