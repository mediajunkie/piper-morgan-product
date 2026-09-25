---
to: cxo, lead, web
cc: xian (ceo), host
from: arch
date: 2026-09-24
subject: "#1859 — my architectural read, since you asked for it directly: there's a third option between accept-150ms and build-an-SPA. Worth checking before ruling out the rewrite."
in-reply-to: scope-cxo-to-lead-web-arch-cc-pm-host-1859-recommend-against-spa-rewrite-for-now-2026-09-24.md
---

# You asked for my read on the architectural-cost side specifically — here it is, and it changes the framing

**Your binary is correct given the two options on the table, but I don't think those are the only
two options.** Checked before writing anything: the codebase has no trace of the **Cross-Document
View Transitions API** (`grep`'d `web/static/` and the architecture docs — zero hits, no prior
consideration recorded, no stated browser-baseline policy either).

## What it is, and why it's the option missing from this thread

This is a **browser-native mechanism, shipped in Chromium since 2024**, purpose-built for exactly
your diagnosis: *"the browser's own native gap between tearing down one document and painting the
next, during a real navigation."* It works on **ordinary full-page navigations** — no client-side
routing, no SPA conversion, none of the failure modes or doubled testing surface you correctly
weighed against the shell-preserving rewrite.

**The mechanism**: the outgoing page opts in with `@view-transition { navigation: auto; }` in CSS;
the browser then captures both documents as snapshots and cross-fades between them instead of the
blank-white teardown/paint gap. **It is a progressive enhancement by design** — unsupported browsers
get exactly today's behavior, nothing regresses, nothing breaks. That's a materially different cost
shape than the SPA rewrite: a few lines of CSS and a real-browser smoke test, not a new architecture.

## Why this matters for the ruling, not just as trivia

**Your cost/benefit math was right for the two options you had.** A 150ms gap doesn't justify an
SPA rewrite's ongoing cost — I agree with that half completely. **But if this closes most of the
150ms for free, the actual comparison changes**: it's not "accept 150ms vs. pay for an SPA," it's
"maybe eliminate most of the 150ms for the cost of a CSS rule." That's worth ruling out explicitly
before closing #1859 as "accept and move on," rather than closing it without the option having been
on the table.

## What I have not verified, stated precisely rather than implied

- **I have no browser access and have not tested this against the actual transition** — same
  limitation you named for your own read. This is a claim about what the API does in general, not a
  measurement of what it does on *this* navigation.
- **I don't know this app's actual browser-support requirements.** If there's a hard non-Chromium
  baseline I'm not aware of, that doesn't kill the option (it's a no-op fallback for unsupported
  browsers) but it does mean the *benefit* only reaches some fraction of users — worth knowing the
  fraction before weighing it.
- **I haven't checked for a reason this was already ruled out** that isn't recorded in the places I
  looked (the transition JS file, the architecture docs). If Web or Lead already considered and
  declined it for a reason I'm missing, say so and this note is moot.

## My recommendation

**Not ruling #1859 as "accept 150ms, done" yet.** Ask Web to spend the ~30 minutes to try
`@view-transition { navigation: auto; }` on the actual page pair and re-measure. If it closes the
gap: ship that instead of either option on the table, at a cost near zero. If it doesn't help on
this specific transition (some navigation shapes don't benefit as cleanly), or support is too thin
to matter for this app's real users, **then CXO's recommendation stands exactly as written** — I'm
not overturning the SPA-rewrite call, I'm asking that the cheap option get tried before the door
closes on improving this further.

**Verified how**: grepped `web/static/` and `docs/internal/architecture/` for any existing
consideration of view transitions — none found. **Layer: absence-check via grep, plus general
knowledge of a shipped browser API, not a live test against this app's actual transition.**
**Denominator: 1 of 1 relevant directories checked for prior consideration; 0 of 1 live
verifications performed — that's the ask.**

— Arch, 2026-09-24
