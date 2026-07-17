---
subject: Ship #052 workstream review — Comms (window Fri Jul 10–Thu Jul 16)
---

# Comms — Ship #052 Workstream Review

**From**: Comms
**To**: Exec
**CC**: PM, PA
**Window**: Friday Jul 10 – Thursday Jul 16, 2026

---

## §0 — Progress vs. portfolio goals

Against `ROLE-PORTFOLIO-COMMS.md` §2 (last refreshed Jul 11): **advanced on all four tracked priorities**, plus closed a real self-inflicted incident at the root rather than just patching it.

- **Building narrative cadence** — **advanced**. Beat 13 ("The Migration Wave," Jul 14) and Beat 14 ("Into Production," Jul 16) both published this window, on schedule. Weekly Ship #051 also published Jul 15. No slot went empty.
- **Editorial mechanism upgrades** — **advanced**. `update-calendar` skill went v1.1→v1.2 mid-window after a real same-day corruption incident (see §3) — by-name field access is now mandatory, whole-file verification replaces single-row checks. This is exactly the "recurring one-off catch → permanent check" pattern this priority tracks.
- **Weekly Ship pipeline** — **advanced**. Ship #051 fact-checked against all 6 workstream memos plus underlying primary logs; caught 2 real "adjacent-story number contamination" errors (a recurring fact-check failure shape, now a standing memory) before publish, not after.
- **BYOC narrative** — **still blocked**. No direction memo this window either; now ~4 weeks stale (first surfaced 6/17). Flagging again since it's crossed a month.

## §1 TL;DR

- Beats 13 + 14 published on schedule; Weekly Ship #051 published with 2 real fact-check corrections caught pre-publish.
- I corrupted a shared calendar row via a coding-technique bug, caught by a peer session, fully root-caused, and turned into a permanent skill fix (`update-calendar` v1.2) same day — full account below, no softening.
- Investigating that incident's aftermath surfaced a second, unrelated finding: 38 real published posts had a stale calendar column value I'd previously (and wrongly) characterized as dead backlog — corrected fix verified, held pending PM go-ahead per a permission-classifier caution.
- A real cross-repo bug (calendar showing stale in the new admin editing UI) was traced, routed to Web, and closed same-day with a precise root-cause fix on their end.
- A 3-beat narrative-slate proposal for the Jul 8-15 window is ready and awaiting PM's steer — the front currently sits at Jul 7.

## §2 What landed

- **Beat 13, "The Migration Wave" (Jul 14)** — full fact-check against primary per-role logs found 3 real corrections (a misattributed holdup story, a duty-cycle/worktree-migration conflation, a two-unrelated-sevens conflation). PM voice-passed via a cross-machine edit that hit a real merge conflict + a large-file git crisis (two 100MB+ unrelated design files swept into a push) — walked PM through recovery via chat, fully resolved, no data lost. Discovered a systemic gap along the way: blog-post PNGs were never committable due to a blanket `.gitignore` rule — filed #1403 (still open).
- **Weekly Ship #051, "Impossible by Construction" (Jul 15)** — full fact-check against all 6 workstream memos plus underlying Lead Dev logs; found and corrected 2 real numeric errors (Beta Blockers end-of-window count, write-path release count) that were both classic "real number, wrong sentence" contamination. PM supplied the P.S. personally (I'd drafted one first and caught myself falling into the exact negation-reveal cliché I've spent weeks flagging in other drafts — corrected, now in standing memory).
- **Beat 14, "Into Production" (Jul 16)** — fact-checked Jul 14 (tag/checkpoint conflation, corrected 7-item Linux-portability list), voice-passed by PM via the new website admin editing UI, proofed same day. Two substantive editorial questions resolved carefully rather than guessed: Beatrice's name removed from the post (PM confirmed both privacy and — more importantly — accuracy: she never actually tested the plugin, despite a primary PA log stating otherwise, which I'd trusted in my original fact-check); a "plugin" vs. "extension" terminology question I verified directly against PA's own primary log rather than assume either way.

## §3 What surfaced

**I corrupted a shared calendar row, twice, same day — full account.** Editing `editorial-calendar.csv` on Jul 14, I used positional indexing (`row[-2]`) to target the `notes` field, but the 18-column schema has `altText` at that position, not `notes`. My edit's content landed silently in the wrong column; a second edit compounded it. A peer general-purpose Code session caught it (a later, unrelated edit's field-count check made the drift externally visible), repaired the structure, and wrote a precise incident memo rather than silently patch it. I owned it fully: ran a whole-file integrity scan (confirmed nothing else was silently wrong), repaired the row's actual content, and fixed the root cause in `update-calendar` (v1.1→v1.2): by-name field access is now mandatory, positional/`Edit`-tool row surgery is banned, and verification is whole-file rather than single-row. Saved as a durable memory.

**That fix then surfaced a second, related finding the next day.** The new semantic-anchor check flagged 38 rows with non-canonical values in the `canonicalSite` column — I'd already characterized these as "dead backlog" in a hastily-filed issue (#1406) the day before, without checking the actual data. Investigating properly this time: all 38 are genuinely `status=published` posts with real `blogURL` values — a schema-drift artifact, not dead content. The correct fix (`canonicalSite=distributed` on all 38) is verified and ready, but I stopped short of writing a 38-row bulk mutation to shared data one day after the first incident — the permission system flagged the same-day repeat pattern, and I agreed with that caution rather than push past it. Still awaiting PM's go-ahead as of this memo.

**A real cross-repo bug, found and closed the same day.** PM's new website admin editing UI showed stale calendar data (a published post as unpublished, a Ship missing entirely). My own CSV was confirmed current; I traced the likely mechanism (a documented two-repo publish pipeline) and routed a precise question to Web rather than guess into a repo I don't have checked out. Web found the actual root cause — a build-time copy script that silently failed on every real Vercel deploy since Jul 12 — and shipped a fix same-day, verified live.

**A recurring failure shape got a second confirming instance this window: primary logs can misattribute a named person, not just a number.** My Jul 14 fact-check had trusted a PA log line naming Beatrice as a specific tester; PM's direct correction Jul 16 revealed that line was simply wrong, not ambiguous. New standing memory saved — named-person claims in source logs need the same scrutiny as numeric claims, since a log records what was believed at the time, not independent truth.

## §4 What's still open

- **PM decision pending**: 38-row `canonicalSite` calendar fix (verified, ready to write).
- **PM steer pending**: 3-beat narrative-slate proposal for Jul 8-15 ("The Write-Path Chase," "Alpha Launches," "The Architect's Own Trap") — researched, independently verified against primary logs, presented as candidates, not drafted.
- **#1403** (blog-image gitignore gap) — still open; individual posts have worked around it with `git add -f`, but the durable fix (narrow the rule, or document the workaround in the publish checklist) hasn't landed.
- **#1406** — now stale-titled given the finding above; the actual 38-row fix is the resolution, pending the PM decision noted above.
- **BYOC marketplace narrative** — still no direction, now ~4 weeks stale.

## §5 Cross-role threads

- The calendar-corruption incident and its fix touch anyone who edits `editorial-calendar.csv` programmatically — the `update-calendar` skill v1.2 upgrade is a general lesson (by-name field access, whole-file verification) that could apply to any CSV/TSV a role maintains, not just this one file.
- The Web calendar-sync fix closes a real gap between the product repo (source of truth) and the website repo (what's actually displayed) — worth Web/Docs awareness if other tooling assumes those two stay in sync automatically.

## §6 For PM/exec consideration

Two decisions sit with PM directly, both flagged above and not resolved as of this memo: the 38-row canonicalSite fix, and the narrative-slate steer. Neither is urgent-urgent, but both are fully staged and ready to move the moment PM has a minute.

— Comms
