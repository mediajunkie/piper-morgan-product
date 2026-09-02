# The three Jake items you asked to have translated — plain English, no jargon

**For PM** · Exec, 2026-08-05 evening · per your asks relayed via Janus. No deadlines attached to any of this — these decisions take the time they take.

---

## First: Radar. Answered by the people who checked, and it's good news.

**Radar is not being lost.** CXO ran this down today and PPM verified it independently — both put it in writing to you and Janus this afternoon. The short version: the fix-list bucket that retires web-UI items ("bucket A") covers things like navigation menus and panel widths. **Radar's surface is not in that bucket.** Better: the earlier claim that "there is no web page for it" turned out to be wrong (PPM checked, corrected themselves publicly), and the plugin distribution plan (PDR-005/006 line) schedules a **cross-client variant** of Radar's surface — meaning the concept you've defended three times is not only surviving, it's slated to reach users on more surfaces than today. CXO's and PPM's memos carry the verification detail if you want it; nothing below depends on it.

## Item 3 — "tool-catalog naming direction" translated

**What's actually being proposed**: when Piper ships as a plugin, there's no navigation, no screens — the only "menu" a user ever sees is the list of tools Piper offers, each with a name and one-line description. The proposal is to name those tools after **the situation the user is in**, not after our internal objects.

- Object-style naming: `create_list`, `manage_items` — the user has to learn our vocabulary to know what to pick.
- Situation-style naming: "shape a vague idea into a spec," "break this epic into tickets," "draft acceptance criteria for issues that lack them" — the user picks by what they're trying to do.

**What changes for a user**: Jake's "which of the three lists am I supposed to use?" question becomes unaskable — he never has to map his situation onto our taxonomy, because the menu is written in situations. It's the same opinionation you wanted, placed in the cheapest possible spot.

**The honest caution (PPM's own, against their own proposal)**: a second "reader" also uses those names — the AI assistant hosting the plugin decides *which tool to call* partly from the name. Situation-style names might route better or worse than object-style ones, and nobody knows which. **The recommendation is therefore a direction plus a cheap test** (try both naming styles, measure which routes correctly more often) — not a blind commit. Your yes here means "test it and go with the winner, leaning situation-style," not "rename everything today."

## Item 6 — "PA's meta-intent flag" translated

**The actual behavior question**: when Jake typed "help me write a ticket about X," Piper *filed the ticket* instead of helping him write it. Those are different requests — "do X" versus "help me prepare X" — and the second kind (a request *about* a request) is the single most common thing a product manager types.

**Why it matters which layer fixes it**: there are two different places the wire could have crossed. Either Piper's *understanding* never distinguished "help me draft" from "do it" (in which case the fix is teaching it that distinction), or it understood fine and the *acting* layer jumped the gun (in which case the fix is a check before acting — which is also what the consent-gate work covers). **PA's flag isn't a decision for you** — it's an instruction to whichever engineer picks this up: check which layer failed *first*, because fixing the wrong one leaves the bug alive while looking fixed. It pairs with the consent gate you'll see in the same fix list; the two together make "surprise actions" structurally impossible rather than just less likely.

## And one clarification I owe you back

On the gate questions you answered **"(b)"** — the new first-contact criterion (cold account, one tool connected: does the user's own data appear in the first exchange, unprompted?). Janus and I read that as approving (b). **Could you confirm what you intend for (a) and (c)?** — (a) was "close the beta gate on its existing terms rather than expanding it," and (c) was "treat the consent gate as a genuine release blocker." No rush and no default assumed — we just don't want to treat silence on those two as a decision either way.

---

*Scorecard for reference: item 1 (bucket-filter sort order) — you said yes. Item 5 (Jake follow-up) — already done, you replied to him 7/25. Item 2 — (b) approved, (a)/(c) awaiting your word. Items 3, 4, 6 — translated above; 4 is resolved by CXO/PPM's verification. PPM converts the whole set to GitHub issues the same day your remaining answers land.*
