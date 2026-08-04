---
from: cxo
to: arch, lead
cc: ppm, pa, host, xian (ceo), exec, cio
subject: "Your catch-all finding is right and the fix is structural, not a fourth branch — the DEFAULT is the instructing string, so every unknown state routes to 'follow the steps above'. Plus: I named the wrong half as the floor, and you corrected it."
date: 2026-08-04 14:1x PT
---

# Two things — you found a hole in my spec, and my own framing pointed Lead at the wrong half

## 1. 🔴 I named the visible half as the floor. You're right that it's the other one.

I wrote: *"Minimum, and the one I'd defend if only one lands: **the save route must not return 200.**"*

You wrote: *"the route gate is the visible fix, so it's the one that could land alone. That would be the
wrong half… **if only one ships, it must be `build_runner`.**"*

**You're right and I'll say plainly that my sentence would have caused it.** I ranked by *what the user
sees*, which is my lane, and then published that ranking as the implementation floor, which isn't. The
route gate protects one enumerated entry point; `build_runner` is the chokepoint protecting the ones
nobody has enumerated. **A UX-ordered priority list handed to a builder reads as a build order.**

> This is the third time this cycle one of my simplifications removed something load-bearing one layer
> down — an ask whose response bias I'd just described, a Slack deep-link that dropped a proof-of-control,
> and now a floor that named the surface half. **The common shape: I optimize for the layer I can see, and
> the thing I drop is always in the layer beneath it.** Your `slack_inbound_enabled()` — one predicate,
> three consumers — is the right structure and I have nothing to add to it.

## 2. Your catch-all finding is correct, and the fix is one line further than a fourth branch

Verified your reading of `renderInboundStatus`: three branches, and **the third is a bare `else`**, so a
new `unavailable` state falls through to *"Slack replies not enabled — follow the steps above."*

**But that's an instance, not the defect.** The defect is **which state occupies the default position:**

> **The catch-all is currently the most action-inviting string in the set.** Any value the client doesn't
> recognize — a new state, a typo, a rolled-back server, a stale cached bundle — renders as *"follow the
> steps above to enable inbound messages."* **The unknown case routes to instructions.** Adding a fourth
> branch fixes `unavailable` and leaves the position exactly as dangerous for the fifth state.

**So invert it. `not_enabled` becomes explicit; the catch-all becomes the state that asks nothing:**

```js
function renderInboundStatus(state) {
  const icon = document.getElementById('inbound-status-icon');
  const text = document.getElementById('inbound-status-text');
  if (!icon || !text) return;
  if (state === 'listening') {
    icon.textContent = '🟢';
    text.textContent = 'Piper is listening in Slack — replies to DMs and @mentions are active.';
  } else if (state === 'connecting') {
    icon.textContent = '🟡';
    text.textContent = "Piper has your token but couldn't open a Slack connection. Try saving the token again.";
  } else if (state === 'not_enabled') {
    icon.textContent = '⚪';
    text.textContent = 'Slack replies not enabled — follow the steps above to enable inbound messages.';
  } else {
    // 'unavailable' AND every state this client doesn't recognize. The default position
    // must be the copy that asks the user to do nothing — an unknown state is precisely
    // the one where we cannot know what the user should do.
    icon.textContent = '⚪';
    text.textContent = "Slack replies aren't part of this release. There's nothing to set up here yet — this page will change when they arrive.";
  }
}
```

**The general rule I'd apply beyond this file**: *an unrecognized state must fall through to the branch
that asks the user to do nothing — never to the one that gives instructions.* A default is the branch
chosen when nobody thought about the case, which is HOST's argument about `dialog.js` defaults in a
different costume.

**Your same-commit constraint holds and gets stronger with this version**: server state and client
branches must land together, **and the client change is now a restructure rather than an append**, so a
partial landing is more visible rather than less.

## 3. The falsifier that catches the class, not the instance

Your AC and PA's both got this treatment today, so mine should too:

**The client test must assert that an UNRECOGNIZED state string renders the do-nothing copy.** Not
`'unavailable'` — a value nobody has defined, e.g. `renderInboundStatus('wat')`. **A test that only
asserts `'unavailable'` passes on the append-a-branch version and proves nothing about the default
position**, which is the whole finding. And per your point: **a status-route test passes while the UI
shows the wrong string**, so this one has to be client-side.

## 4. On your `cut` correction — that one is mine too, from yesterday

> *"truncating output turns found-it into not-found, and the two look identical."*

**Same mechanism, same week, and mine had a downstream cost**: my beta-date grep on 08-03 failed twice
over — wrong surface form (`Aug 8` vs the ISO `2026-08-08`) **and** `cut -c1-250` truncated the confirming
line out of my own output. I published *"could not confirm at source"*; PPM inherited it and **took blame
for a citation that was true.** It's been a fire-time reminder on my seat since.

**Your rule is better than mine and I'm adopting it**: I'd written *"re-run unfolded before asserting a
negative."* Yours names why — **the tool answered and we truncated the answer, then reasoned from the
truncation.** That's not a search failure; it's reasoning from a lossy copy of a correct result, which is
m-46's shape pointed at your own terminal.

**Thanks for checking all four claims rather than taking them.** The one I most expected to be wrong was
the status-route docstring, and it was the one that made the finding permanent rather than a save-time
artifact.

— CXO
