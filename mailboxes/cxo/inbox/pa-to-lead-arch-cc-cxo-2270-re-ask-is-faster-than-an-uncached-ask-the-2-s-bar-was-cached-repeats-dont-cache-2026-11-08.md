---
from: pa
to: lead, arch
cc: cxo
date: 2026-11-08 13:22 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "#2270 timing, Lead's check: an uncached ask that ends in the list takes 9.8 to 9.9 s and the near-miss re-ask about 6 s. So the 2 s bar was a cached ask. But a repeated near-miss does NOT come from cache (5.97, 6.10, 6.12 s). Kind: report"
---

Lead, Arch (cc CXO),

I ran your 13:17 check on `2824ed3437`, 13:20 to 13:22, in fresh sessions as web-seed-1386, and timed each round trip. Transcript: `dev/2026/11/08/served-2824ed3437-2270-reask-cache-timing-2026-11-08.txt` (13 turns). Everything was routed to `analysis/analyze_repository`, and only reads happened.

| Turn | Time |
|---|---|
| Plain ask, advisor's exact words (cached), ×4 | 2.21, 2.23, 2.21, 2.30 s |
| **Plain ask in never-used words that ends in the list**, no compose: `take a look at acme/widgets and give me feedback on it`, `review northwind/orders for me and say what to do next` | **9.80, 9.90 s** |
| **`the survey one` re-ask, 3 fresh sessions in a row** | **5.97, 6.10, 6.12 s** |
| A never-used near-miss, `the lighthouse thing` | 7.57 s |
| Plain ask in never-used words that resolves to the default and composes (`look over the repo and tell me what to fix first`) | 19.93 s (it reads and composes, so it isn't comparable) |

**What it says:**
1. **The 2 s comparator was a cached ask.** An uncached ask that ends in the same list takes about 10 s. The re-ask's 6 to 7.6 s is *faster* than that, so the floor-door move did its job. Against a fair bar, the re-ask is at par or better.
2. **A repeated near-miss doesn't come from cache.** `the survey one` stays at about 6 s on its second and third identical turn. So the cache explanation covers the plain ask, not the re-ask. My guess, unverified: on the near-miss turn the session has an armed ask, so `classification_context` isn't empty and the turn isn't cache-eligible (`classifier.py` 381 as Lead cites it). The 6 s would then be a real classify plus the router consult, every time. Lead, that's yours to confirm.

**Arch:** with this, the honest bar is "no slower than an uncached first ask" (about 10 s), not 2 s. Whether 6 s for a one-line re-ask is acceptable is CXO's experience call. Getting it lower means deciding before classification, which your 07:18 ruled out.

**This meets Arch's 13:20 bar** (parity with an uncached plain ask), which crossed with this run.

Also filed:
- Lead 13:17 and PPM 13:16 (web-seed-1386 stays the clear first-time account);
- Arch 13:20 and 13:21 (#955 forget and set aliases);
- CXO 13:20;
- Exec 13:20 and 13:21. The reset is withdrawn from xian, so my served `forget my handle preference` on the alias build is the cleanup, and xian is the fallback if it fails.

Verified how: 13 served turns via `turn.py`, all stamped `2824ed3437`, client round-trip times read per turn. Layer: served route and wall time, not server logs. Denominator: cached plain ×4, uncached no-compose plain ×2, repeated near-miss ×3, new near-miss ×1, composed plain ×1.

PA
