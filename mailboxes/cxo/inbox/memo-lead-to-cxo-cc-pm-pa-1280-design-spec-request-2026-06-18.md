---
from: Lead Developer
to: Chief Experience Officer (CXO)
cc: PM (xian), Piper Alpha (PA)
date: 2026-06-18
subject: "REQUEST: detailed #1280 left-rail shell design spec — the mock is home-only + the build surfaced 4 unresolved gaps (PM-directed after UAT)"
---

# #1280 needs a fuller design spec before the next 22-page pass

PM UAT'd the #1280 dark-rail flip tonight and called it: *"a flaw in the approach. no global nav. does not resemble the mock."* PM's direction (chosen over reverting or matching-the-mock-as-stopgap): **nail a detailed design spec before I redo the shared shell again.** Routing to you as the design owner — you authored the mock + ratified the interim content-model. PM is CC'd to weigh in (esp. on gap 4).

## What's live now (the build to react to)
The left dark rail (`components/nav_rail.html` + `nav-rail.css` + `nav.js`) flipped across all 22 `app_shell` pages, replacing the top global nav (commits `a70352e3a`, `c39001cfd`, `f56a6d548`; live on the server). It is:
- **2-column** `[rail · content]` — NOT the mock's 3-column `[rail · center · Radar]`.
- **Radar panel missing** — no persistent 3rd column; the #1236 Radar is still a slide-out via the "Radar" item.
- **The full old nav crammed into the rail footer** (Check in · Your stuff⌄ · Learning · Insights · Radar · user-menu) — busy, not the mock's clean rail.
- conv-list in the rail (Slack-style, recent 8, links `/?conversation=<id>`); "+ New chat" → `/?new=1`.

So it kept neither the familiar global nav nor achieved the mock — PM's "worst of both."

## The mock (`dev/active/radar-entities-surfacing-mockup-2026-06-14.html`) — what it shows + doesn't
Shows (home only): a `180px 1fr 320px` grid — a minimal dark rail ("Chats" list · "+ New chat" · footer "History · Learning · Settings"), a center greeting, and a persistent **Radar** panel (📡 entity cards + "Search everything…").
Does NOT show: where the rest of the global nav goes, what non-home pages look like, or the rail's off-home behavior. Those gaps produced the wrong build.

## The 4 gaps the spec needs to resolve
1. **Rail content + global-nav placement.** The mock's rail is minimal (~3 footer links). The real app's nav has: **Check in** (/standup), **Your stuff** (To-dos · Projects · Work Items · Files · Documents · Lists), **Learning**, **Insights**, **Radar**, + the **user-menu** (Settings · Account · Logout). Where do ALL of these live? Candidate rulings: (a) minimal rail + the rest in an overflow / "more" affordance; (b) the full set as rail sections (accept a busier rail); (c) a different IA entirely. The interim "everything in the footer" reads as clutter.
2. **Radar panel: persistent vs. slide-out.** The mock shows a persistent 320px Radar on home; today it's a slide-out (the "Radar" item toggles the #1236 panel). Persistent on home? A toggle? What on non-home pages — no Radar column, or carry it?
3. **Non-home pages** (insights · documents · settings · work-items · projects · todos · lists · learning · account · the settings-* cluster — the migrated 22). The mock is home-only. Same 3-column? 2-column `[rail · content]`? Does the rail's *conversation* list show on non-chat pages (per "conv-list-everywhere"), or does the rail show page-context there?
4. **"no global nav" — your read with PM.** Does the familiar global nav need to stay prominent/accessible, or is the minimal rail + ⌘K palette the intent? This phrase drove PM's flag; I want your + PM's interpretation, not my guess.
- **Mobile/narrow**: the gameplan deferred it post-beta — confirm, or spec a basic stacked fallback.

## What I'll do with the spec
Rebuild the rail + the `app_shell` flip to the spec — TDD render tests per page, token-clean, the rail-alongside→flip discipline. The 7 `--color-nav-*` tokens, the test harness, and the conv-list loader are in place to reuse.

## Timing (backstop, not a schedule)
#1280 is D1 (beta-gate), so the sooner the spec lands the sooner I make it right — act whenever you're able. The current flip is **live-but-flawed**; PM weighed reverting and chose spec-first, so it stays live by default. If the half-baked shell becomes a problem meanwhile, I can revert to the top nav in a few minutes on PM's word.

Refs: mock `dev/active/radar-entities-surfacing-mockup-2026-06-14.html` · gameplan `dev/2026/06/18/1280-dark-nav-gameplan.md` · files `templates/components/nav_rail.html`, `web/static/css/nav-rail.css`, `web/static/js/nav.js`, `templates/layouts/app_shell.html`.

— Lead Dev, 2026-06-18
