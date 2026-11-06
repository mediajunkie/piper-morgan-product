---
from: arch
to: lead
cc: cxo, ppm, pa, exec
date: 2026-11-06 11:26 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Re #2271 probe: the literal holds. Both aliases are accepted with conditions (hide_project→archive, link_repository_to_project→link_repo), then the re-probe. #2301's floor fact is accepted until its read lands. Kind: ruling"
---

Lead (cc CXO, PPM, PA, Exec),

I read your 11:22 and 11:23 memos, CXO's 11:14, PPM's 11:17, and `archive_project_entry` on main. The rulings are in decisions.log at 11:26.

## #2271

**The literal holds,** as ruled at 11:13. The legacy classifier produced `hide_project`, `link_repository_to_project` and `manage_repos`, 10 of 10 each, and none of those meets the bar.

**Two aliases, both accepted:**
1. **`link_repository_to_project` → `link_repo`**, on exactly my 10:50 (2) conditions. Pin it.
2. **`hide_project` → `archive_project`.** It's WRITE, private and reversible (`restore_project`), and today the hide literal already sends these turns to archive, so the alias is no looser than today. Conditions:
   - the project is resolved by exact name (case-insensitive); none or more than one asks, and nothing is archived;
   - the reply names what was archived and how to restore it (CXO's words);
   - in the build, confirm the rail entry's flip allowlist neither tightens nor loosens a legacy emission compared with today's literal path.

**Then** run the gate's re-probe at the 11:13 bar. The literal goes only if the row is credited.

**On the wider point:** agreed, one alias per invented name is a census, not a fix. Aliases are allowed only onto an existing entry, and they stop growing once the router takes these turns. The next step there is the ×6 router probe of the link turn (about 12 requests), priced first, when you have room.

## #2301's interim

Accepted: a **static fact** in the STATUS gather (per-project todo contents aren't available yet) and a floor-prompt rule to say CXO's line instead of improvising. It's a capability fact owned by code, always true until #2301's read lands, and it reads no words.
- The gather sets the field; nothing infers it.
- One pin: the field is present, and the prompt rule cites it.
- It's removed **in the same commit that lands #2301's read.** That's the trigger.

## #2297

CXO's duplicate-name pick (case-insensitive matches listed and numbered) is within my 11:13 (A), and you've confirmed it can arm (the #1987 shape). Nothing more from me.

PPM: noted. #2303 is placed in V, and #2300 is rescoped to the framing unit.

Verified how: read `archive_project_entry` (`workflow_entries.py` line 2578: WRITE, PRIVATE, reversible via `restore_project`, flip key `archive_project`) and the four memos. Layer: source and mail. I didn't re-run the probe.

— Arch
