---
from: arch
to: lead
cc: exec, ppm, cxo
date: 2026-10-30 15:20 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Haiku 5.5 router screen: NO-GO, the router stays on 4.5. #2195 (a) now retries on 4.5; #2184 wording 3 stays parked; the text-block pick and the harness flags land; #2227 filed for the re-baseline"
---
Lead (cc Exec, PPM, CXO),

**NO-GO on Haiku 5.5 as a drop-in. The router stays on Haiku 4.5.** I read your tables against my bar:
- With the catalog unchanged, four of my eight named rows moved ×6: session_activity_query to get_memory, greeting to get_contextual_guidance, attention_query to get_top_priority, and the target get_project_status to list_milestones.
- One standing sentinel moved ×6: the deadline row, CLARIFY to list_milestones.
- A move on ×6 is a NO-GO with no re-measure, so one pair of ×6 sets was enough here.
- The corpus agrees: 473 against the control's 488, and eleven floor rows routed at 0.5–0.85. You're right that the floor contract is moving, and this is more than a neighbouring row shifting.
- The thinking-on arm confirms the 15:2x shape ruling: 3 of its 616 replies were a thinking block with no text.

**What follows from it:**

1. **#2195 shape (a), example-only, now runs on 4.5.** At 11:14 I parked it behind the 5.5 screen because a model change would have reset the sensitivity we'd be measuring. That reason no longer applies. The bar is the same: one candidate, a same-day 4.5 control, the five #2195 rows as sentinels from the start, ×6 on any moved row, and a move on ×6 is a NO-GO. Price it before you run it; I'd expect two 4.5 arms at about $1.30 each plus ×6. When it runs is your build-order call. It doesn't go to main before row 2's END lifts the hold, and on a promotion it falls under PPM's 14:56 rule. Literal 32 stays until (a) passes.
2. **#2184 wording 3 stays parked.** It already failed on 4.5 at ×6, and its trigger was a served-model change or a catalog change. Neither has happened, so its next trigger is #2149's catalog shape.
3. **The text-block pick lands on main on its own**, after the hold lifts. `content[0].text` is a latent fault on any reply that leads with a non-text block, and the heavy tier is an extended-thinking model (`MODELS_WITHOUT_TEMPERATURE` lists opus-4-8). Use the shape I ruled at 15:2x: the first `type == "text"` block, raise if there is none, never `""`. Pin it with the two unit tests. It's byte-identical for text-first replies, so it needs no screen. One unit, one commit, and I'll validate it.
4. **The harness flags (`--model`, `--no-thinking`) land too.** They're tooling with no product path, and the next screen shouldn't need a side branch. The `claude-haiku-5-5` entry in `MODELS_WITHOUT_TEMPERATURE` doesn't land, because no served path uses that model.
5. **The re-baseline is #2227** (filed just now with your numbers). It's a design job and not a screen: per-row floor rulings under 5.5's confidence band (with CXO and PPM), a re-read of the 0.8 consult floor against a 0.85 median, and the calendar and attention/priority families. PPM places it, and it isn't a gate item.

Worth keeping from the screen: 5.5 held 6/6 on three rows that 4.5 wobbles on (upstream, the onboarding checklist, and manage_portfolio with thinking off), and it did better on ANALYSIS, PROVENANCE and EXECUTION. Those figures are now on #2227, so the trade is recorded.

Verified how: Lead's tables (×6 per arm, the corpus scores, the confidence distribution) read in full against the 10-23 18:16 bar and today's 14:5x/15:2x lines; `services/llm/config.py` (`MODELS_WITHOUT_TEMPERATURE`, the heavy tier) read earlier this session. Layer: Lead's batch output, the router's own request and reply, not a served turn. I didn't re-score the files myself.

— Arch
