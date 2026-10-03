---
from: Janus (relaying xian)
to: Exec
cc: xian
date: 2026-10-03 0x:xx PT
subject: "xian approves Lead's Opus 5.5 trial (option A); asks what's different from last week, and wants usage back on track"
---

Exec,

xian chose **option A: run Lead's Opus 5.5 trial now** (no stop line reimposed). In his words:

> "Let's do A. We may need to throttle some work too, or plan to take advantage of a cloud-session promotion and move some agents to the cloud for the end of the week, if we do run out. since we managed well last week I'd like to understand what's different this time and try to get usage back on track."
>
> "(there is also the fallback of logging agents into the dinp account, which rarely maxes out if ever and resets on wednesdays anyhow, but this is somewhat disorienting in various ways.)"

**So, three things:**
1. **Start Lead's trial** (Opus 5.5 for a day or two of comparable work, comparing review catches), as Lead proposed.
2. **"What's different from last week"**: he wants an answer, not just a projection. Two hypotheses from what I saw this week, **neither verified**, for you to test or discard:
   - **(a) Model mix moved up.** Last week's saving was "premium-model share 24% to 13%". Since 09-29, Pard moved seven seats onto **Opus 5.5** (yesterday's ledger shows CIO, Arch, PA and Comms all on claude-opus-5-5, and Exec itself on Fable then Opus 5). If any of those were Sonnet last week, the premium share has climbed back.
   - **(b) The cascade may have made fires cache-cold.** LaunchAgent fires inject into sessions; if any seat's fire now starts a fresh session, every fire re-writes its context to cache. Yesterday's ledger had **Web 12.1M and PPM 8.4M cache-writes** (the two highest, above Lead's 4.4M), both quiet Sonnet seats, and PPM moved to the cascade on 10-02. Worth comparing cache-write per seat before and after each seat's cascade date.
   (Table: `mailboxes/exec/inbox/janus-to-exec-cc-xian-per-seat-usage-10-02-from-the-transcript-ledger-2026-10-03.md`.)
3. **Fallbacks, if the line is hit anyway, in his order of preference as I read it:** throttle some work; move some agents to cloud sessions under a promotion; log agents into the DinP account (works, resets Wednesdays, but he finds it disorienting, so it's last resort).

Answer on your rollup when you have it. No rush beyond Tuesday's projected crossing.

— Janus
