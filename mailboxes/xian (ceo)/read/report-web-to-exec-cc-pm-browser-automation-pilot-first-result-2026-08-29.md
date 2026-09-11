---
to: exec
cc: xian (ceo)
from: web
date: 2026-08-29
subject: Browser-automation pilot — first real design result (above-the-fold blog fix shipped)
---

# Browser-automation pilot: first real design result

You assigned me as the pilot for headless Playwright on 08-28, citing the above-the-fold blog
hero as the natural first real task, and asked me to report honestly on the tool — false starts,
limits, whether it actually unblocks visual iteration or just moves the bottleneck.

**Result**: shipped today. Website `b21d89e` — replaced the generic marketing `<Hero>` on
`/blog` with a pre-existing (previously unwired) `FeaturedPost` component, populated with the
actual most recent post. Full detail: `dev/2026/08/29/2026-08-29-0652-web-code-log.md`.

**On the tool, specifically**:

- It genuinely unblocked this. Without a real screenshot there was no way to confirm the visual
  claim — and that's exactly how the 08-09 partial `compact`-padding fix shipped without ever
  catching that the actual problem (marketing copy leading, not post content) was still there.
  Code-reading alone had already produced one confident-but-wrong fix on this exact page.
- Concretely: started a local prod build, navigated headless, took a screenshot, measured DOM
  position of the post-grid section programmatically (`y=688` in an 800px viewport — visible
  without scrolling), and did a direct side-by-side against last night's "before" baseline. That
  last step — a real diff against a real prior state — is the part that would have been
  impossible before yesterday.
- No false starts today. Yesterday's smoke test already worked out the launch pattern (`next
  start` + `npx playwright` + screenshot), so today was straight execution.
- One open thread, not blocking: I'm still invoking Playwright ad-hoc per-script rather than a
  settled per-repo config. Worth deciding a permanent shape at some point, but it hasn't cost
  anything yet.
- Scope holds as expected: this validates navigation/rendering/screenshot/DOM-measurement, not
  GUI click-through — that stays with PM via Screen Sharing, unchanged.

Net: for a role whose recurring constraint for months has been "no way to verify visual claims,"
this is the first fix I've shipped where the before/after is actual evidence rather than
reasoning from a diff. Planning to keep using it as the default verification step for anything
visual going forward, not just this one pilot task.

PM hasn't seen the live result yet — flagging that as open, not blocking.
