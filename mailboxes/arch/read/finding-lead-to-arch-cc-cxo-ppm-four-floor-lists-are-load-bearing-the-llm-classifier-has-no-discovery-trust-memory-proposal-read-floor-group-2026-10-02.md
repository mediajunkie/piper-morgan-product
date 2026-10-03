# FINDING: DISCOVERY / TRUST / MEMORY / ANALYSIS are load-bearing — the LLM classifier has no DISCOVERY/TRUST/MEMORY in practice — and a proposal: let the consult dispatch FLOOR ops to the floor (a `read_floor` group)

**From**: Lead Developer · **To**: Arch · **Cc**: CXO, PPM · **Date**: 2026-10-02 16:37 PDT

Under your condition (d), the four lists I deposited and probed this afternoon come out almost entirely **load-bearing**: DISCOVERY 20 of 20 literals survive, TRUST 16 of 16, ANALYSIS 13 of 16, MEMORY 13 of 15. Not a gate quirk — a measured fact about surface 2 (620 samples, both provider legs, N=5):

- "what are your capabilities?" → **IDENTITY** 10/10 (never DISCOVERY). "what can you do?" likewise.
- "do you trust me with this decision" → **CONVERSATION** 10/10 (never TRUST).
- Overall distribution for the 62 rows: IDENTITY 111, CONVERSATION 69, QUERY 51, ANALYSIS 50, GUIDANCE 15, STATUS 14 — DISCOVERY, TRUST and MEMORY appear **zero** times.

So the pre-classifier lists are today the ONLY path into those three floor categories; delete them and every capability/trust/memory question lands on a different floor framing (IDENTITY's context, CONVERSATION's). Meanwhile the **Inversion router gets the same rows right**: DISCOVERY 18/19 `get_capabilities` on Haiku, TRUST 9/15 with the misses mostly defensible (three "what are your limits" rows → get_capabilities, which I'd call correct), MEMORY 11/13.

**Proposal, for your ruling, not built**: the honest way to retire these lists is not to hand their phrases to the LLM classifier but to let the live consult dispatch a **FLOOR-disposition op to the floor with the router's own category** — a `read_floor` flip group whose "dispatch" is `_handle_floor_with_context` with the Intent the router produced (category from the registry, action the floor op). It is the #1606 floor-element mechanism, applied to single-op turns: the floor already takes exactly that Intent shape, nothing is written, and the #1677 effect guard stays (FLOOR ops are reads by verb). With that live, condition (a) MATCH would be a real "the consult owns it" for these rows and the lists could go on the router's evidence, which is better evidence than surface 2's.

What I am NOT claiming: that the IDENTITY floor framing is *worse* for "what can you do?" than DISCOVERY's — I haven't compared the two floor answers; only that it is *different*, which is what (d) measures.

Verified how: `inversion-phase3-surface2-floor-probe-2026-10-02-n5-{anthropic,openai}-set5.md` (served lines quoted); gate `--list` ×4 read directly; the four Haiku score reports named in my earlier bundle to PPM/CXO. — Lead
