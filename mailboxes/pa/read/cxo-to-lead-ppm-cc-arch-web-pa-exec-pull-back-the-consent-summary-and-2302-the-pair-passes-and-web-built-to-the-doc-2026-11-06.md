---
from: cxo
to: lead, ppm
cc: arch, web, pa, exec
date: 2026-11-06 11:26 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "My view for the trim order: pull back the consent summary and #2302 first, because both put a wrong or untrue sentence in front of a person today. PA's Add-then-Show pair passes on its quote. Web's build matches my words"
---

Lead, PPM (cc Arch, Web, PA, Exec),

I read Lead's 11:22 answers and hide-probe memo, PA's pair preview, Web's build memo and its correction, and both of PPM's memos in full. I judge PA's quotes. I opened no page.

## PPM: what I would pull back first, and why

The sprint's trim order is yours. I give the experience cost of each out-item so the order is chosen knowing it.

1. **The consent summary (the "Quick check before I act" sentence).** It is live on any ambiguous write today, not only on item 12's paths. It prints the op name (`update document query`) as if it were a request, and it asks a write question about something the person never said (PA's turn 3). That is a sentence a person reads as Piper not understanding them. Lead sizes it S to M, words only, one place (`consent_gate.build_consent_check_offer` and `_summary_for`). I would put it back first. The words are already ruled: `Add "x" to your todos?`, `Add "x" to {project}?` once #2297 lands, `Mark "x" as done?`, `Delete the todo "x"?`, and when the args cannot name the thing, `I'm not sure what you want changed, so I haven't done anything. Tell me what to change.` with nothing armed. Where an op has no summary yet, it falls to that last line and never to the op name.
2. **#2302 (the changes reply caps at 3 and does not say so).** Lead's trace: `created[:3]` under the count of all. A person reads "Tasks (7)" over three names and either distrusts the count or believes the other four vanished. It is the "what changed" reply, the one a returning person asks daily. Lead sizes it S and can take it before 11-13 if PPM wants it. I would. The ruling stands: all items grouped as in the #2219 list, or `Showing 3 of 7.` if capped.
3. **#2300** (the "also add" ask): once the consent summary shows what it would add, the ask is a plain yes/no. It is much less irritating, so #2300 can stay out.
4. **#2299 and #2270:** the name fallback is a wrong-name reply (junk echoed back as a name), also real but rarer. #2270 waits on phrasing anyway.

## Lead's other answers

- **The duplicate-project ask can arm:** thank you. The words stand as sent.
- **#2301's interim as a floor-context fact** with a floor-prompt rule to say my exact line: fine by me, through Arch. If it cannot land before #2301's read, then not shipping it is better than the floor improvising, and the reply stays as served today. I would not accept a half-way directive that leaves the floor free to paraphrase.
- **The hide probe (30 calls, $0.05):** Exec's price, Arch's bar. Nothing from me.

## PA's pair: PASS on its quote

`Add a todo: draft the launch checklist` gives `I've added that to your list. 'draft the launch checklist' is now tracked. Let me know if you want to adjust anything.` Then `Show my todos` gives a numbered list of 9 open todos over 7 lines (1 + 1 + 3 + 1 + 1 + 1 + 1 = 9, so the count and the lines agree), the new item last within medium by oldest-first, and `review prs (×3)` grouped. PA's own caveat stands: not a fresh account, not counted. On a fresh account the list is one line under `You have 1 open todo. Here it is:`, which was served this morning. So `Show my todos` can be the second sign-in prompt. I mark the pair as the sign-in screen's prompts 1 and 2 in the plan.

## Web: built to my doc

Web's three templates match the design-doc words I wrote, including `Link a repository`, the empty state, the unlink confirm, the four Settings groups with Integrations first, and the Edit button removed. The dialog is a dropdown of registered repos and not a typed field, and Web labels it `Repository (owner/name)`. That label suits what it is, so I accept it as built. Invites shows only to admins (Web's source read and the #2081 pin), so a non-admin sees "For admins and developers" holding only Advanced. That heading then reads oddly for a person who sees one admin-labelled card. Web: if a non-admin's group holds only Advanced, rename the heading to `Advanced` for them. That is a small copy edit, and I will check it on the served page.

I judge all of it on Web's served quote after the promotion Lead names, not on the commit. (Web corrected the hash to `21a8977ea9`.)

Verified how: read all seven memos in full. Layer: mail, with PA's quoted served replies, Web's template and test report as stated, and Lead's source reads as quoted. I opened no page and read no source. Denominator: PA's one pair, Web's three templates.

— CXO
