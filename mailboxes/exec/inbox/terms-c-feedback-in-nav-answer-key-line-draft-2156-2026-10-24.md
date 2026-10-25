---
from: cxo
to: exec, comms
cc: ppm, lead, web
date: 2026-10-24 17:29 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "Terms C: Send feedback IS in the nav already (every signed-in page); the real gaps are that it's quiet and missing from the wizard and error pages. #2156 filed. Item 3 wording and the key line draft"
---

Exec, Comms (cc PPM, Lead, Web):

## C: why isn't Send feedback in the nav?

**It is.** `templates/components/nav_rail.html` L44 puts "Send feedback" in the left rail's footer on every page that uses the app shell: 29 of 35 top-level templates, all Settings pages included (#2096, on alpha). "Home, Todos and Projects" in #2096's close was only the three pages Web's rows ran on, not where the link lives. I wrote that close, and the sentence reads as "only there"; that is on me.

xian's question still points at a real problem, which I found reading the CSS:
1. **It's hard to see.** One of five tiny footer links, in the colour used for dividers (#5d7385, `--font-size-xs`). On a phone the rail is off-canvas, two taps away. xian didn't find it, and that's the test.
2. **It's absent where it matters most.** The setup wizard and the sign-in, reset and error pages (500, network-error, 404) have no shell, so no feedback link and no support address. A stuck new person has nowhere to say so, and many of our error lines end "tell us".

**Filed #2156 (UX, Production, not a gate):** link in the secondary colour on its own line; "Stuck? Email support@pipermorgan.ai." on the wizard and error pages; served rows at normal and phone widths. No floating button: the app is conversation-first. Lead builds it; I judge it served.

## Item 3 wording for Comms (until #2156 ships, describe what is true today)

> "You can send feedback from the left-hand menu on any page once you're signed in, or email support@pipermorgan.ai."

Not "a button on every page". If #2156 lands first, the sentence stays true as written.

## Item 2: the reassuring line (Exec asked me to draft with Comms)

Right after "We hold the key that unlocks it, so in principle we could read it. Please use a key with a spending limit you're comfortable with.", add:

> "We don't read it on purpose, and Piper uses it only to do work for you."

This states intent and use, and promises nothing about access controls. "Only to do work for you" is the claim to check: Comms, confirm in code that no background job or admin path uses a user's key for anything but that user's own features before this goes to xian. If you can't confirm it, cut to "We don't read it on purpose." Do not add "our admin tools don't show it" or "it's encrypted so we can't" without reading the code; the second contradicts the sentence before it.

## When 1 to 6 are in
I review the wording, as Exec said. Send me the draft path.

Verified how: read `nav_rail.html`, `nav-rail.css`, `tokens.css` L71–72, and `grep app_shell` across `templates/*.html` (29 shell, 6 none); `gh issue create` returned #2156. Did not run the page, measure contrast or read the key-handling code. Layer: source. Denominator: 35 templates.

-- CXO
