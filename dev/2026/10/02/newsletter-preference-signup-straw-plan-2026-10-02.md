# Newsletter preference-based signup — straw model plan

**Status**: DRAFT for PM review and discussion. Not scoped, not approved, not started. Written at
PM's explicit request (2026-10-02) as a starting point to react to, not a final design.

**Author**: Web. **Context**: Step 2 of the two-step newsletter plan agreed 2026-10-02 — Step 1
(honest LinkedIn/Medium links replacing the stale "576+" CTA) is shipped and live
(`website@4b6cf04`). This is Step 2: let a visitor choose what they actually want — blog updates,
Weekly Ship, and/or the beta waitlist — from one signup surface.

---

## 1. Forensic search — what already existed

PM asked whether this had been planned before. Searched both repos' mail, session logs, and
content-strategy archives rather than assume. Three findings, none of them a built plan:

1. **2026-08-15, PM raised the idea in passing** (`dev/2026/08/15/...-web-code-log.md`): "native
   Buttondown newsletter publishing from the site, possibly with subscriber choice (blog vs. Ship,
   narrative vs. insights)." Explicitly **"not tonight"** — filed to carry-forward, never designed,
   never built. This is the direct ancestor of today's conversation.
2. **2026-06-25, a cross-project routing (Janus/DinP)** asked who owns the PM site's "preference
   center" (`mailboxes/web/sent/memo-web-to-exec-cc-pm-newsletter-items-response-2026-06-25.md`).
   Web's answer at the time: **there is no on-site preference center — Buttondown owns subscriber
   management entirely**, and that was treated as a closed fact, not a gap to fill. (Finding 4
   below means that answer was incomplete, not wrong — Buttondown's own hosted surface can *be* the
   preference center; nobody had looked into whether it supported this shape yet.)
3. **An older, pre-current-site content-strategy doc** (`devel/content-strategy/content_integration_recommendation.md`,
   predates the Next.js rebuild, likely from whenever "576+" was still an accurate number)
   proposed a **different-shaped idea**: one single signup, then *"post-signup segmentation for
   advanced engagement tiers."** That's segmentation after the fact, not a choice at signup time —
   not what PM described this week, and never built either. Noted for completeness, not treated as
   a precedent to build on.

**Bottom line**: nothing to resume or extend. This is new design work, starting from PM's 08-15
idea and today's conversation, not a rediscovery of abandoned scaffolding.

## 2. What already exists in code today (real, working, in production)

`NewsletterSignup.tsx` already POSTs a `source` prop to Buttondown's embed-subscribe endpoint as a
**tag** (`formData.append('tag', source)`), per a comment dated 2026-06-15. Two live forms already
use this: `/blog` used `source="blog-post"` (now retired as part of Step 1), `/try/beta` still uses
`source="beta-waitlist"`. **So Buttondown is already receiving per-signup tags today** — the
plumbing for "tag a subscriber based on what they signed up for" is not new; it's one list with
two different tags already in it.

## 3. The key technical fact — checked, not assumed

The 2026-08-15 carry-forward note (and the 2026-09-20 audit) both flagged, unverified: *"Buttondown
may not support that granularity without multiple newsletters."* **Checked directly against
Buttondown's own documentation rather than carrying that assumption forward**:

- Buttondown supports **sending an email to only subscribers with a specific tag** — when composing
  a send, choosing "Custom → Tag" targets just that tag. ([Segmenting your audience](https://docs.buttondown.com/segmenting-your-audience),
  [Tagging your subscribers](https://docs.buttondown.com/tags))
- **A subscriber can hold any number of tags simultaneously.**
- Buttondown has a **hosted subscriber-facing "Portal"** where tags marked "subscriber editable"
  render as checkboxes a subscriber can change themselves, with no code on our side.
  ([Send emails to certain tags!](https://buttondown.com/blog/tagged-emails), [Subscribers can tag
  themselves](https://buttondown.com/blog/2024-02-19))

**This means the old blocking assumption was wrong.** One Buttondown account, one list, three tags
(`pref-blog`, `pref-ship`, `pref-beta`) is sufficient — "multiple newsletters" is not required. The
06-25 answer ("no on-site preference center, Buttondown owns that surface") turns out to be closer
to the actual solution than the problem: **Buttondown's own Portal can be the preference center**,
hosted, no custom backend.

## 4. Straw-model shape

**Signup time**: one form, three checkboxes (not radio — someone can want all three), each mapped
to a tag on submit. Replaces (or sits alongside — open question, see §6) the current single-purpose
forms.

**Ongoing preference changes**: point subscribers at Buttondown's hosted Portal (a link, likely in
every email footer) rather than building a custom on-site preference page. Requires enabling
"subscriber editable" on the three tags in Buttondown's dashboard — a PM-side config step, not code.

**Sending**: whoever sends a Weekly Ship issue targets tag `pref-ship` in Buttondown's own compose
UI; a blog-digest send (if that becomes a thing) targets `pref-blog`; beta-access emails target
`pref-beta`. No new send infrastructure — this is exactly how Buttondown's compose flow already
works, just pointed at a tag instead of "everyone."

**Existing subscribers**: the handful already tagged `blog-post` or `beta-waitlist` need an explicit
migration decision (map old tags to new ones, or leave as legacy tags alongside the new three) —
not a blocker, just needs a choice before shipping.

## 5. Relationship to Step 1 (today's stopgap)

Step 1 deliberately sends blog visitors *away* to LinkedIn/Medium, because the site's own list had
nothing real behind it. Once Step 2 ships, the site's own signup becomes worth pointing people to
again — Step 1's CTA would likely get replaced or supplemented at that point, not left as-is
forever. Not urgent; noting the dependency so it doesn't get forgotten.

## 6. Open questions for PM — this is where review matters most

1. **Does the three-tag model match what you actually want**, or did you have a different shape in
   mind (e.g., should "beta waitlist" stay fully separate from the other two, given it's a
   different kind of promise — "we'll email you directly" — not a newsletter digest)?
2. **One combined signup form, or keep `/try/beta`'s dedicated page and add the other two
   elsewhere?** A single combined form is simpler to build but may undersell the beta waitlist's
   distinct, personal framing.
3. **Is Buttondown's Portal an acceptable long-term preference-management surface**, or do you want
   something on-site eventually (more work, no clear need identified yet)?
4. **What happens to the Step 1 LinkedIn/Medium CTA once this ships** — replaced, demoted to a
   secondary mention, or kept alongside indefinitely as a third option for people who prefer those
   platforms?
5. **Existing-subscriber tag migration** — map old tags forward, or let them lapse?

## 7. What this plan deliberately does NOT cover

No effort estimate, no UI mockup, no decision on exact tag names or copy — all downstream of
PM's answers above. This is the shape of the problem and the one technical fact that changes the
feasibility picture, not an implementation spec.
