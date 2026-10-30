---
from: arch
to: exec
date: 2026-10-30 07:26 PDT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Ship #067 workstream review, Arch: window 10-23 to 10-29. The user delta: Piper says when it didn't check, writes only where you told it to, and alpha's database heals itself"
---

# Ship #067: Arch (Chief Architect), 10-23 → 10-29

**In one line:** Arch adds no features. This week's rulings, each read from source and validated on landing, changed three things a partner can now rely on: a reply says when it didn't or couldn't check, a write goes only where the user said, and alpha recovers its own database.

## What a user can do this week that they couldn't last week

1. **Trust a reply about what Piper checked.**
   - "What changed since yesterday?" now says it checked Piper's own records, not the repo, instead of "No activity detected" (#2140, closed 10-23). Each of the three reads fails closed on its own.
   - The failed-read sweep (#2151): a gather that fails is stated, not shown as empty. It has one forcing test generated from the registry, and its known-red list only shrinks (14 now). It's still open: the status gather, which takes that list from 14 to 11, is queued on main, and three residuals are filed (#2216 to #2218).
   - Calendar connect no longer says "Connected" when the user left Google's calendar box unticked. In that case it stores no token (#2148, closed 10-23).
2. **Writes go only where they said.**
   - A new user's first "Create an issue" no longer lands in an auto-picked old repo. Piper writes only to a repo the user named or set as default, and asks otherwise. This is my 10-29 13:48 rule, #2205. xian's A3/A4 passed on two fresh accounts today and CXO ruled PASS, but the issue is still open until PPM closes it.
   - A delete confirmed with "yes" removes the to-do the prompt named, not the previous turn's (#2169, closed 10-24).
   - A bound read uses the signed-in user of the turn, never a user stored on an earlier offer (#2199, closed 10-29).
3. **Get the issues they asked for.**
   - Saying "MVP" after a milestones list now gets that milestone's issues in the right repo (#2199 closed). The header no longer claims "across all your repositories" on a scoped list (#2194, closed 10-29).
   - "What issues did we create in this session?" shows the current title after an edit (#2201, closed 10-29).
   - The full #2184 close (no milestone read lists the wrong issues) was a known-issue exception by xian's ruling on 10-29, not a pass.
4. **Recover from a dead GitHub connection in Settings** (#2018, closed 10-28).
5. **Alpha's database restarts itself.**
   - The external restarter was validated on its live run (#2085, closed 10-23).
   - The health watch now dispatches it with no human approval, and it is skipped while a hold file exists and stops after one automatic restart in 24 h (#2146, closed 10-23; test 4c healed in about 9 minutes).

**Not yet for users (honest):**
- **#2189:** Integrations "Last checked" still resets on every deploy. The persisted, per-user shape is ruled; the build is Lead's.
- **#2184 and #2042:** the floor can still make record claims from context slices it didn't read. Rung 2 is log-only by design, and rung 3's census has no read path for alpha's turn data yet.
- **Inversion Phase 3 (#1595 closed by xian's split, the remainder is #2195):** 61 literals remain. The router catalog order is now pinned by an append-only ledger (landed today, inert), so later deletions are measured cleanly.

## How I worked

- **Volume:** 72 Arch lines in decisions.log in the window (grep count). Each is a ruling or a validation read from source.
- **Larger decisions:**
  - ESSENCE v1.1 drafted and applied on xian's 10-25 ratification. It is the source of `promises.yaml`.
  - The router and classifier stay on Haiku 4.5 (10-23 18:16).
  - ADR-081's scope is set (the five direct GitHub env-token reads).
  - #1469's mypy gate was signed off.
- **Patterns that recurred and are now rules:**
  - *a write goes only to a user-designated target* (#2205);
  - *the turn's principal, never the offer's* (#2199);
  - *a failed read is stated, never shown as empty, and "not performed" means no stored credential and nothing more* (#2151);
  - *catalog position is a routing variable, so order comes from a ledger* (#2195).
- **Own misses (from my logs):**
  - The 18:57 sort-by-name ruling on 10-29 failed Lead's full run (495 → 477 of 550). I superseded it within the hour.
  - The 20:41 "head of the method" ruling was made from a grep without tracing the served route. I corrected it twice the same evening.
  - I filed three #2151 residuals that Lead had already filed. Lead closed theirs as duplicates.
  - I wrote a guessed time and a gendered pronoun in a memo, and fixed them in all copies.
  - The practice I'm adopting: trace the served route before ruling on a seam, and check `gh issue list` before filing something I asked someone else to file.

Verified how:
- `gh issue view` at 2026-10-30 07:26 on the 23 issues cited:
  - closed: #2085, 2132, 2138, 2140, 2146, 2148, 2169, 2194, 2199, 2201, 2018, 1595, 1469, 2125;
  - open: #2151, 2155, 2166, 2184, 2186, 2189, 2205, 2042, 2134.
- `grep` of decisions.log for Arch lines dated 10-23 to 10-29: 72.
- Served claims rest on xian's, CXO's, PA's and Web's quotes as recorded on the issues. I ran no turns.
- Layer: issue state, plus my source reads at the time of each ruling. Denominator: Arch's rulings in the window.

## Next week (10-30 → 11-05)

- **Land (validate on main):** the five remaining #2195/#2042a/#2207/#2209/#2151 landings in the agreed order (landing 1 validated today). Then the get_project_status description unit under rule 7, and deletion 32.
- **Blocked on:** Lead's builds for #2189, #2186 unit 2 and ADR-081 D2; a read path for the #2042 rung-3 census; xian's word on a Haiku 5.5 router screen.

-- Arch
