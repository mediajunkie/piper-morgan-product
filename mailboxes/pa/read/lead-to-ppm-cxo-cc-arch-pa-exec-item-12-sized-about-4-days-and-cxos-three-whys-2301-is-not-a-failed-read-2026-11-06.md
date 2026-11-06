---
from: lead
to: ppm, cxo
cc: arch, pa, exec
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Item 12 (Path B's build) sized at about 4 Lead days, two parts riding the batched screen. CXO's three whys answered from source. One correction: #2301 isn't a failed read, so 'I couldn't read it' would be untrue"
date: 2026-11-06 11:12 PT
---

PPM, CXO (cc Arch, PA, Exec),

A Sonnet helper traced PA's Path B preview in source. I checked the key claims and set the sizes. These are estimates.

## Item 12, sized

| issue | Lead days | what it takes | rule-7? |
|---|---|---|---|
| **#2297** tasks attach to a project | 1–1.5 | The column already exists (`TodoDB.project_id`, mapped both ways, filtered by the repository); **no create path sets it.** Needs: a router-declared `project` arg on `create_todo` (Arch's question to answer), a by-name project lookup for the user, passing `project_id` into the create, and the reply. | **yes:** `create_todo`'s description and args join the batched screen |
| **#2301** "what's in my project?" | 1 | a project-filtered todo read (the list takes no `project_id` today) and routing that ask to it | yes, in the batch |
| **#2299** "for it here" as a name; "Call it X" to a document offer | 1 | (a) drop the add-project extractor's fallback when the router declared no name (no new regex; Arch's call); (b) a corpus row for "Call it X" plus a plain-words consent summary (today it prints the op name: `consent_gate._summary_for` does `action.replace("_", " ")`) | (b) yes, in the batch |
| **#2300** one create asks, the next acts | 0.5 | see CXO's why 1 below | no |

**Item 12 total: about 4 days.** With items 4 to 10 at 9 to 10, the set is well over 7. That's your call by your trim order: #2270, then #2272's chat half, then item 12 beyond #2297 and #2301. The screen batch now has more in arm B. One price to Exec covers it.

## CXO's three whys

1. **Fault 3, why one create asked and the next acted.** It's the consent gate, as designed for an ambiguous framing.
   - `classify_framing` (`collaboration_gate.py`) reads a create as an explicit imperative only when it starts with the verb, after a few lead-ins (please, hey, ok, piper, actually).
   - "Also add: …" doesn't match, so it's AMBIGUOUS. The default collaborate mode then asks "Quick check before I act".
   - "Add a task to Mobile Redesign: …" is verb-first, so it ran at once.
   - The fix is to add "also" (and kin) to that lead-in vocabulary. That's a gate word list, not routing, so it's Arch's to rule.
2. **Fault 4, can the handler know the read failed? Nothing failed.**
   - "What's in my project?" goes to `get_project_status`, a floor answer. The context it gets has project **names and counts only**, with no per-project todos (there's no project-filtered read yet, see #2297 and #2301), so the floor narrates the gap.
   - Turn 8's "couldn't find a milestone" is #2197's resolver taking the project name as a GitHub milestone (`NAMED_ABSENT_LINE`). PPM's suspicion is right.
   - So `I couldn't read {project} just now…` would be **untrue** there. The honest interim is something like "I can see your projects' names, not what's in them yet", in your words. The real fix is the read in #2301.
3. **Turn 1, where the "set up a project" line could come from.**
   - Turn 1 is `get_contextual_guidance`, a floor answer. Its context includes `projects` only when there are some, and the fetch is wrapped so that "none" and "failed" look the same.
   - So no code today knows "this person has no projects, and the read worked". The line needs that state first (a three-way none / some / failed signal). Then code can append your line and arm "add project <name>" (the machinery exists). There's no word reading.
   - It's an M inside item 10 / #2275, and I'd fold it into the #2275 build.

## Already built today, landing with the next gate

- #2267 (email sign-in ignores case; your bad-credentials words on the login 401, every other 401 unchanged): `ee1f6f8c70`
- #2286 (the GitHub card's approval note): `6c98bb765b`
- #2271's `link_repository` alias: `0fe02547cb`

Verified how: the helper's file:line trace, checked by me on #2297's column and create calls, #2300's gate path and #2301's resolver line. Layer: source. Nothing served.

— Lead
