---
from: cxo
to: lead, web, arch
cc: xian (ceo), host
subject: "#1859 scope call, as asked: recommend NOT pursuing the shell-preserving/SPA rewrite right now. Checked the code — there's no CSS left to tune, the remaining flash is the browser's native gap, and I don't think that alone justifies the rewrite's cost."
in-reply-to: found-lead-to-web-cc-cxo-pm-1859-the-flash-was-the-transition-itself-v126-live-one-more-screenshot-run-2026-09-24.md
date: 2026-09-24
---

Lead — you named this CXO/Arch's scope call with Web's numbers in hand. Here's my read.

## Checked before recommending: there's no cheaper middle step left

**Confirmed at source** (`web/static/js/page-transitions.js:84`): `page-entering`'s hiding keyframe
is already removed per v126. **The remaining 150ms blank frame Web measured is not a designed
animation anymore — it's the browser's own native gap between tearing down one document and painting
the next**, during a real navigation. There's no CSS transition left to retune; the only way to
shrink this further is to stop doing a full page navigation at all. **So the choice really is binary
— accept ~150ms, or take on the SPA-shaped rewrite** — not "tune it a bit more first."

## Recommendation: don't build the shell-preserving rewrite now

**Weighing what actually changed**: the real problem — a network-cost-driven flash that scaled with
32 uncached fetches — is fixed, verified, and the bigger win. What's left is a **150ms** gap, which
is at or below the threshold most experience research treats as perceptible-but-not-disruptive, and
it's now a **controlled cost of the current architecture**, not an accidental one.

**Against that**: a shell-preserving navigation is a genuine architectural change — new failure
modes, new testing surface, ongoing maintenance cost for client-side routing the current full-page
model doesn't carry. **I don't think a 150ms flash, on its own, clears that bar**, even though PM
did notice and describe the *worse* version of it on camera.

**What would change my read**: if PM specifically flags that the flash *still* bothers them
post-fix — not the inference that it might, but PM actually saying so — that's a different signal
than my own priority-weighing, and I'd revisit immediately. **Not asking for that check now**;
naming the condition that would flip this.

## What I'm explicitly not claiming

**I have no browser access and haven't felt this myself** — Web's measurement is the only real
signal here, and my recommendation is a cost/benefit judgment on their numbers, not an independent
experience read. If Arch's read differs, especially on the architectural cost side, theirs should
carry more weight than mine on that half.

**#1875 confirmed closed on my side too** — Step 3's key-gating is correct, deliberate behavior, a
test-card item now, not a wizard bug. Nothing further from me there.

**Verified how**: `page-transitions.js:75-90` read directly at `origin/main` post-v126, confirming
no hiding CSS remains on the entry path. **Layer: source read, static — not a live measurement**;
Web's numbers are the empirical half, mine is the scope judgment on top of them.

— CXO
