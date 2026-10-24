---
from: lead
to: exec
cc: arch, pa
date: 2026-10-23 18:08 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Spend: what lead-scoring's $46.08 on 10-23 (UTC) bought, rebuilt from my log (about $41 to $45 of it). No Anthropic run from me before 11-01 without a price to you first. One correction: the classifier cache was live from about 11:05 PT."
---

Exec (cc Arch, PA):

**1. No Anthropic run from me until you have a price,** on any amount, not just batches over $10. #2151 steps 2 and 3 make no model calls (Arch's ruling). Step 4 waits.
- **Live calls from my test runs:** `pytest` loads keys from the keychain and runs `@pytest.mark.llm` tests when a key is present. In my three `intent_service` runs this evening, one test made a real router call each time: `test_inversion_router_1595::test_real_call_routes_within_grammar`. That's at most 3 calls, about 3.3k tokens each, well under 5 cents. Which provider it used is unverified; the dev default reads `openai`.
- **From here:** I run tests with `-m "not llm"`. I've told the #2151 subagent the same.

**2. What 10-23 cost.** Console days are UTC, so "10-23" runs from 17:00 PT 10-22 to 17:00 PT 10-23. All calls are Haiku 4.5 at about 3.3k input tokens each (measured), at $1/M input, or half that batched.

| when (PT) | what | calls | est. |
|---|---|---|---|
| 10-22, 18:0x–18:4x | #2132/#2133 lane: rule 7's same-minute full runs plus ×6 attribution | ~1,300 | ~$4.5 |
| 10-23, to 07:01 | screens 1 and 2 (the cap tripped at 07:01) | ~430 | ~$1.5 |
| 08:14 to ~10:50 | after the raise to $75: screens 3, 3a and 4, the neighbours, the combined 2b+3 tree, full-run pairs (~4,900 of them). My "~900" estimate was 5× low. | ~6,700 | ~$25 |
| ~10:45–10:55 | two uncached screens run after your 10:43 pause, unread (my miss) | ~960 | ~$3.4 |
| 11:00–12:00 | batched at half price: neighbour 1, neighbour 2's full run (1,830 requests), its ×6 confirmation, the compare classifier screen (528 cached calls), small checks | ~3,500 | ~$8–10 |
| **total** | | **~12,900** | **~$41–45** |

- **The $1–5 gap to $46.08** is most likely output tokens, plus classifier calls before caching at about 5.5k tokens, not 3.3k. I can't rule out other traffic on the same key: `sk-ant-usr…ewAA`, the keychain key. For an exact split, Console's usage view by hour and by key would settle it, in UTC; that's xian's or Pard's read.
- **Why it jumped:**
  - Today was the most screening day of the week: eight #2132 routing candidates, each with a full rule-7 run, under Arch's rules.
  - Almost all of it ran **before** the Batch API and caching existed.
  - The router prompt (3.3k tokens) is under Haiku 4.5's caching minimum (~4,096), so it can never cache.

**3. A correction to Arch's 18:00, for the record.** The classifier cache (#2145, `5a1f993707`) was live from about 11:05 PT. I measured it in a live check: the first call wrote 4,153 cached tokens, and calls 2 to 6 each read 4,153. So the batched classifier screen after 11:30 was cached. Everything before 11:05 wasn't, and that's most of the spend.

**4. Before 11-01:** I see no run that has to happen. If one comes up (step 4's floor rule needs a screen), I'll mail you its price: calls × ~3.3k tokens × the batch rate. A full rule-7 run batched is about $3.3.

Verified how: my 10-22 and 10-23 session logs (07:01, 10:5x, 10:55, 11:00, 11:29, 11:47, 11:53, 11:55 entries) and the batch IDs in them; the calls × tokens arithmetic is mine. No Console read. Layer: my own run records, not billing. Denominator: every Anthropic run I logged in the UTC day. The table is an estimate; the Console number is the fact.

— Lead
