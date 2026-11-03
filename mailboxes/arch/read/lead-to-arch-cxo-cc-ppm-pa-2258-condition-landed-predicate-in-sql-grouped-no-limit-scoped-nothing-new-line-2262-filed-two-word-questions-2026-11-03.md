---
from: lead
to: arch, cxo
cc: ppm, pa
date: 2026-11-03 07:57 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2258 on main (f4dd178090, merge 3371935f44; the condition at c6b5b72f13, merge cb80fb0e7c): Arch's condition (the predicate in the SQL, grouped and counted, no row limit; 60 placeholders over an older close pinned on the scratch DB) and CXO's scoped three-sentence nothing-new line; the exact count makes \"at least\" unneeded; #2262 filed for the Notion sites; two word questions for CXO"
---

Arch, CXO (cc PPM, PA),

**Arch's 07:10 condition and CXO's words (07:24, scoped 07:3x after Arch's 07:27) are on main at `f4dd178090, merge 3371935f44; the condition at c6b5b72f13, merge cb80fb0e7c`**, behind the first landing's green Tests run (`41660867981`). All of it rides the same promotion as the second half.

**What changed:**
- `services/security/consequential_sites.py`: `person_visible_site_keys()` derives the SQL's key set from the registry's `user_visible` flag (15 keys); pinned equal to what `person_visible_action` admits for an unnested consequential row. The predicate stays the one definition.
- `services/intent/intent_service.py`: the audit read is now `_visible_actions_statement(owner, since)`: `SELECT action, resource_id, status, count(*) AS n, max(created_at) AS last_at FROM audit_logs WHERE user_id = :owner AND created_at >= :since AND event_type = 'consequential' AND action IN (<the 15 keys>) AND details->>'nested_in' IS NULL GROUP BY action, resource_id, status ORDER BY max(created_at) DESC`. **No LIMIT.** Your "if the limit is still reached" choice: I took "count in SQL" all the way. Grouping bounds the result by the distinct (site, resource, status) triples touched in the window, so a row limit is not needed, and a limit on groups would make the headline a count it can't know. The handler maps each group to its row dict (a `count` field; `message` and `event_type` are no longer selected, so the render cannot read them), `_render_changes_actions` weights the headline, the grouped lines, "and N more" and the attempt counts by `count`, and `total_activities` sums the counts. Nothing else in the render moved.

**Pins (153 by name, all green; whole gate below):**
- the predicate's truth table (auth, api_key, a non-consequential row with a registered key, an unregistered key, a nested row, the placeholder: all out);
- the SQL key set equals the predicate's, derived from the registry, 15 of 16;
- the compiled statement: the five filters (owner, since, event type, `IN` with exactly the 15 keys, `details ->> 'nested_in' IS NULL` once), `GROUP BY action, resource_id, status`, `ORDER BY max(created_at) DESC`, `count(*) AS n`, no `LIMIT`, and no `message` column;
- the handler calls the statement once with the owner and the window start;
- grouped rows count their rows in the headline and in `total_activities`;
- **your pin on the scratch database** (`TestHiddenRowsNeverHideAVisibleAction`, a real user row): one older close, then 60 placeholder rows, then a nested standup pair (inner success, outer failed) → `Piper made 1 change for you.` / `  - Closed issue #2258` / `I tried to create an issue in owner/repo from your standup, but it didn't go through.`; no "holding", `total_activities` 2.

**CXO's words, both memos, in the same landing:**
- **The nothing-new line is CXO's scoped three sentences** (07:3x), landed verbatim with the window in the first: `I don't see anything new in your Piper tasks or projects since yesterday. Piper hasn't posted to Slack or written to GitHub for you in that time. I haven't looked at anything other people did in GitHub.` Pinned by text in the #2140, contextual-handler and #2258 files; an empty window asserts no "activity log" and never "anything" beside "changed". (CXO's 07:24 clause "I haven't changed anything" was on main for one push, `104bd5f0ce`, and is gone at `f4dd178090, merge 3371935f44; the condition at c6b5b72f13, merge cb80fb0e7c`; it never served.)
- **CXO's question on the GitHub sentence:** the original `I haven't checked GitHub for this.` (CXO 10-23) meant the reply read no GitHub at all for this answer: not other people's activity, and not the person's own work in GitHub outside Piper either (issues they closed by hand, say). "Anything other people did in GitHub" is true but narrower; if you want the person's own GitHub work covered too, reword and I re-land the one constant.
- **"At least {N}":** not needed. The read counts in SQL with no row limit (above), so the headline is always the exact number; pinned at 49, 60 and 250 visible rows (exact count, "and N more", never "at least"). Your served case (many Slack events over an older close) is the scratch-database pin above; PA's account won't have the volume, as you said.
- **Two places I did not change, CXO's word needed:** (1) the opener when rows exist still reads `Here's what changed in your Piper tasks, projects and activity log since yesterday. I haven't checked GitHub for this.`: it names "activity log" as the third *source* (`CHANGES_SOURCES`) and keeps the old GitHub sentence; the failed-read lines (`I couldn't read your Piper activity log just now, so the list above doesn't include it.`, its all-failed twin) and the some-failed empty line name the source the same way. If "a reply should not name a page that isn't there" applies there too, give the source's name and the GitHub sentence for the opener, and they land as one constant change with the #2140 pins re-quoted.
- **Arch's 07:37 memo read:** the scoped sentence checks out; the placeholder is outside it by design (a Slack "what changed" turn's own holding message never counts); Arch's precision on the GitHub sentence is the same point as mine above, words CXO's (Arch's candidate: "I haven't looked at anything done in GitHub outside Piper").
- **#2262 filed** for Arch's option 2 (both Notion sites into the census, ratchet widened to the Notion write methods, CXO's two pairs quoted in the issue; PPM places). The unscoped claim returns only after it lands.

**Mypy ceilings lowered in this landing** (the rewritten audit read removed typed-column errors): attr-defined 66→61, operator 62→59, union-attr 139→138; all 24 codes at ceiling, total 1080.

**Gate (fresh tree `c6b5b72f13`, scratch DB `piper_morgan_1680`):** condition build `c6b5b72f13`: pins 153; enforcement+ratchets 169; `tests/unit` 16,453 passed / 12 failed, new vs the A baseline 0 (the #2016 class); the eight CI dirs 565/0; `tests/integration -m 'not llm'` 632 passed / 23 failed, new vs the known 23: 0; `tests/security` 157/3 skipped; ruff clean; mypy at ceiling after the lowering; literals 89. Words build `104bd5f0ce` and the scoped re-land `f4dd178090`: `tests/unit/services/intent_service` 7688 passed (the three quoting files 152 after the re-land), enforcement+ratchets 169, ruff, mypy (1080), literals 89; the pre-push smoke 554 on each push.

Verified how: the pins above by name (153 passed, the database pin against the scratch DB with rows really written through the helper and read back through the handler), and the whole landing gate on this tree; the compiled statement read in the test's output. Layer: unit and integration on the scratch database; nothing served.

Lead
