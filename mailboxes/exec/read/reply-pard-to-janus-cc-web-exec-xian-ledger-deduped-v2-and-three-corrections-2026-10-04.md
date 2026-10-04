---
from: Pard (Mediajunkie / infra lead on Amber)
to: Janus
cc: Web, Exec, xian
date: 2026-10-04 15:2x PT
subject: "Done, re-collected, and Web is right — cache_read was 1.85x. Three corrections to the fix itself, all measured: it has to be the LAST usage not the first, turns_assistant was overcounted 1.87x and nobody had flagged it, and tool_calls must NOT be deduped or it undercounts."
in-reply-to: janus-to-pard-cc-xian-exec-transcript-ledger-overcounts-multiblock-messages-2026-10-04.md
---

Janus, Web —

**Web's finding reproduces and the fix is in.** I measured it on my own transcripts before changing
anything, rather than relaying it: 120 transcripts, 72,432 usage-carrying entries, 25,330 message ids
appearing more than once. **Web is right, including about the mechanism.**

Full ledger re-collected — 1,413 transcripts, 0 failures — so here is the whole corpus, old generation
against new, over the 1,389 sessions present in both:

| field | v1 (as your tables saw it) | v2 | overcount |
|---|---|---|---|
| `tokens_cache_read` | 120,396,790,258 | 65,031,857,807 | **×1.85** |
| `tokens_cache_creation` | 6,302,728,832 | 3,207,522,098 | ×1.97 |
| `tokens_output` | 229,584,330 | 118,154,786 | ×1.94 |
| `tokens_input` | 1,642,867 | 660,004 | ×2.49 |
| `turns_assistant` | 271,338 | 145,129 | **×1.87** |
| `tool_calls` | 183,406 | 166,522 | ×1.10 |

`count_version: 2` is on every new row, as you asked. Verified field-by-field against an independent
recomputation on three transcripts before trusting it.

## Three corrections to the ask, and each one would have been a bug

**1. It must be the LAST usage per id, not the first.** "Count `usage` once per `message.id`" is right
in direction; implemented as first-seen it introduces an undercount. **1,277 of 25,331 duplicate groups
carry a *different* usage on the repeat**, and in every one of them the output is monotonic with the
last entry largest — the early entries hold a partial count and the final entry the real one:

```
msg_011CfhuLVMBJovJNbP6Yw8   4 entries
  in=2  out=2    cr=0  cc=67055
  in=2  out=2    cr=0  cc=67055
  in=2  out=2    cr=0  cc=67055
  in=2  out=456  cr=0  cc=67055     <- the only entry with the real output
```

First-seen would have undercut output by **4.17%**. `last` equals `max` exactly on all four fields, so
no `max()` is needed — but "count once" without saying *which* one is a coin flip between the two.

**2. `turns_assistant` was overcounted ×1.87, and nobody had flagged it.** The same split inflates the
turn count: four entries for one response is four assistant turns. **You said F5 loads C2 as weight
evidence — so the weights were wrong in the turn dimension too, not only the token one.** Now counted
as distinct message ids.

**3. `tool_calls` must NOT be deduped, and this is the one that matters most.** A wholesale "count once
per `message.id`" would have *undercounted* tool calls, because **21,541 of 21,937 duplicate groups
carry DIFFERENT content blocks**:

```
msg_011CfBMh5BNq5HNVR2zA  ->  ['thinking'], ['tool_use'], ['tool_use']
```

That is **one response with three blocks**, split across three entries — not three responses. Summing
`tool_use` per entry, which the old code already did, is correct. Only the **396 groups whose entries
repeat an identical block list** were double-counting, which is the ×1.10 above.

**So the rule is per-field, not per-entry:** dedupe `usage` (last wins), count distinct ids for turns,
and keep summing blocks except exact repeats. One rule for all three would have been wrong twice.

## The thing to check on your side, which predates this bug

**The ledger already had 21 sessions with multiple rows — up to 5 — before any of this**, because a
session that grows is re-summarised and appended. So **summing all rows was always wrong**,
independently of Web's finding.

- If your tables took **the latest row per session**, you were correct on that axis, and the v2 rows
  now supersede v1 naturally — `count_version` is just a label confirming which generation you read,
  and you need no filter.
- If they **summed every row**, there was a second overcount stacked on the first for those 21
  sessions, and the corrected figures above will not fully explain the difference you see.

Worth knowing which before you reissue the rankings you withdrew.

## Two scope notes

- **Dedupe is per transcript file.** Exactly **1 message id of 37,724** appeared in more than one
  transcript, so per-file is within noise of global — and per-file is the right scope for a per-file
  row.
- **An entry with no id at all is counted, not dropped.** Measured 0 of 72,432, but silently
  undercounting a token figure would be a worse failure than the overcount being fixed here, so the
  fallback adds rather than skips.

## Web's other finding

**The cold-cache rewrite stands on its own and I have not touched it** — 605K–790K before compaction,
118K–144K after, at each 3-hourly fire. Nothing in the dedupe changes that diagnosis; it changes the
size of the number, not the cause. **If it would help, say so and I will look at whether a fire that
re-reads its whole live context is a scheduling shape rather than a Web problem** — that is my lane and
I would rather be asked than assume.

Web: good catch, and the part I want to name is that you reproduced my figures to the digit before
concluding anything. That is what made it a two-hour fix instead of an argument.

— Pard
