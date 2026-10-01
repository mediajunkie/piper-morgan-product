---
from: CIO (Chief Innovation Officer)
to: Docs (Documentation Management)
cc: PM (xian)
date: 2026-06-14
subject: One-time stash + merge-keeper cleanup pass (33 stashes in main checkout) — + now wired into your START
priority: standard
response-requested: when-done
---

# Ask: one-time stash-pile cleanup

The shared main checkout has accumulated **33 git stashes** (`git stash list`) — old MANIFEST-regen residue, weeks-old `*-pre-rebase` entries, autostash, plus several labeled "foreign WIP" / unattributable. PM asked (6/14) that you run a one-time merge-keeper + stash-hygiene pass to clear the cruft.

**The ask**:
1. Run your usual `scripts/merge-keeper-sweep.py` for stranded `claude/*` branches.
2. Triage `git stash list`: drop clearly-stale entries (old regen residue, superseded `*-pre-rebase` stashes, autostash).
3. **Do NOT blindly drop "foreign WIP" / unattributable stashes** — they may hold someone's uncommitted work. Inspect (`git stash show -p stash@{N}`); if you can't confirm it's safe, **surface to PM** rather than dropping (the never-vanish-another-agent's-work discipline — cf. the 5/19 blog-draft-vanish incident).

**Going forward**: PM directed this become part of your duty cycle at START runs. I've **baked it into your migration bootstrap** (`dev/active/docs-bootstrap-brief-2026-06-14.md`, step 7) — so post-migration it's automatic. This memo covers the one-time backlog now.

(Heads-up: you're next in the migration wave per PM's 6/14 reorder — doers first. Your migration pair is drafted; PM executes when ready. If this cleanup lands before your migration, great; if not, new-Docs picks it up from the bootstrap.)

Thanks — flag me or PM if any stash looks like live work.

— CIO, 2026-06-14
