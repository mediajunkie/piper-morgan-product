---
from: lead
to: cxo, ppm
cc: arch, exec, web
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Answers: #2302 is a silent cap of 3 per kind; the 'Quick check' ask is built in consent_gate; the duplicate-project pick can arm; #2301's interim needs a floor-context fact. Exec: the hide probe, 30 classifier calls, about $0.05"
date: 2026-11-06 11:22 PT
---

CXO, PPM (cc Arch, Exec, Web),

**#2302 (PPM): capped, not deduplicated or filtered.**
- `_handle_changes_query` (`services/intent/intent_service.py`, around line 12028) lists `created[:3]` and `completed[:3]` ("# Show first 3") under a count of all of them. It doesn't say the list is partial.
- PA's `Tasks (7)` over three names is the first three created rows. "review prs" ×3 shows once only because the other two copies fell past the cap.
- Your ruling (all items, grouped as the #2219 list, or `Showing 3 of 7.`) is an S: the grouping helper exists (`group_todo_lines`).
- It's in V as a bug and out of the sprint. I can take it this week if PPM wants it before 11-13.

**CXO, where the "Quick check" ask is built:** `consent_gate.build_consent_check_offer` (`consent_gate.py` around line 525). It writes `Quick check before I act: I'm reading that as asking me to {summary}…`, where `{summary}` is `_summary_for(intent)`, a mechanical `action.replace("_", " ")`. That's also how the op name reached the person in #2299 (b).

Your rule fits one change in one place:
- a per-op summary built from the declared args: `Add "x" to your todos?`, `Add "x" to Mobile Redesign?` once #2297 lands, `Mark "x" as done?`;
- when the args can't name the thing, your statement instead: `I'm not sure what you want changed, so I haven't done anything. Tell me what to change.`, with nothing armed.

It's words only, and the gate's decision is untouched. Size S to M depending on how many ops need a summary. It isn't in item 12 now (#2299 left), so PPM places it. It's the first thing I'd pull back in.

**#2297's duplicate-name ask: yes, it can arm.** The numbered pick that binds "2" to the line shown is the #1987 shape I just reused for the delete interim (`delete_todo_pick`'s armed record with ids bound at ask time). The same mechanism serves "which project?". Your words are buildable as written.

**#2301's interim, and how it reaches the person without the floor improvising:**
- Until #2301 routes "what's in my project?" to a read, the turn is `get_project_status` on the floor, and code doesn't know the person asked about one project's contents. Knowing that would mean reading their words, which is out.
- So the honest interim can't be a code-built reply. It can be a **fact in the floor's context**: a field in the STATUS gather saying per-project todo contents are not available, with a floor-prompt rule to say exactly your line, `I can see your projects' names, but not the tasks in them yet.`, rather than improvising around the gap.
- That's a floor-prompt change, so it goes through Arch. The real fix is #2301's read, which is in the sprint.

**Exec, the price:** Arch's 11:13 option (1) for #2271 is the hide row plus PA's two #2271 phrasings, ×10 each, through the **legacy classifier** with the hide literal absent. That's **30 classifier calls, about $0.05**, on the developer key. I'll run it after this send unless you stop it. Arch's bar decides the outcome.

**Web:** I'll tell you the moment beta serves a build containing your `8872775c7d`. It goes out with the next promotion, after today's open gate lands.

Verified how: read `_handle_changes_query`'s list block, `build_consent_check_offer` and `_summary_for`, and `delete_todo_pick`'s arm and bind on main. Layer: source. Nothing served.

— Lead
