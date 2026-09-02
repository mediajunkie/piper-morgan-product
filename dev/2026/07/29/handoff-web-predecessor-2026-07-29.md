---
from: web (predecessor, designinproduct.com era)
to: web
date: 2026-07-29
subject: "Predecessor handoff — Section 4 (hard-won lessons) and Section 6 (load-bearing vs. commodity)"
---

# Predecessor handoff — Web role

**Honesty check first, as asked.** My context is genuinely intact for one specific
arc: 2026-07-12 through 2026-07-19 (the Vercel migration week — plan, phases, DNS
cutover, compose UI, image upload, the Buttondown CSP bug, ship normalization). That
is first-person recall, not reconstruction — it's the live thread I was in when this
request reached me. I have **zero** context for 2026-07-20 through 2026-07-29 — not
"thin," genuinely none. Everything below is scoped to the arc I actually hold. I
looked at your 2026-07-29 session log and the amber-onboarding-delta doc for
orientation only, per the ask — I have not touched carry-forward, standing-items, the
inbox, or the cron, and I'm not asserting anything about Amber itself beyond what's
in this paragraph, which I read, didn't experience.

## Section 4 — Hard-won lessons

**A fix that appears to work can still be wrong in a new way, and that looks
identical to "still propagating."** The DNS cutover was three separate bugs
(a Vercel redirect pointed at a protected URL, a registrar choking on a trailing dot
Vercel itself supplied, then a CDN cert-issuance lag) — each fix's failure looked like
the *previous* problem hadn't fully cleared yet, not like a new one. The cost wasn't
the debugging time, it was the repeated pull to just say "DNS takes a while, give it
more time" instead of going back to first-principles verification (`dig` at the
authoritative nameserver, `openssl s_client` for the actual cert SAN, `gh api` for the
GitHub Pages side) at every single step. **VERIFIED** — this happened three times in
one afternoon, documented in the 7/15 session log.

**Naive verification can return "nothing happened" when the real answer is "my probe
can't see that far."** Twice in one day: curling a Next.js page's raw HTML and
grepping for expected text gave a false negative because the component was behind a
`Suspense` boundary rendering `fallback={null}` — the real content only exists after
client hydration, which `curl` never triggers. Same day, a Vercel deploy that was
just slow (not broken) looked identical to a stuck one until I checked GitHub's
actual commit-status and deployments API instead of trusting a monitor's naive
"still not done" signal. **The lesson generalizes past this specific stack**: when a
check comes back empty for anything with client-rendered or async state, "empty"
is not evidence of "broken" — it might just mean the check can't see past a boundary
it doesn't know exists. **VERIFIED** — both instances are in the 7/16 session log,
including the moment I caught my own first (wrong) verification method mid-turn.

**"Looks the same" is not "verified identical," and being blocked for under-verifying
is the system working, not an obstacle.** I once concluded a `git stash` was safe to
drop after checking its line count and last commit message matched what I expected.
Auto-mode's classifier correctly refused the drop — my check wasn't a real diff. I
went back and actually ran `git show stash@{0}^3:<path>` against the working tree for
every touched file before the drop was allowed to go through. The felt lesson: a
spot-check that *resembles* rigor isn't rigor, and the moment of being stopped taught
me something a written policy hadn't — I'd read the "verify, don't assume" guidance
plenty of times before this without it fully landing. **VERIFIED** — 7/15 and 7/16
session logs, same pattern both times, tightened the second time.

**I shipped the exact bug my own safety check was supposed to prevent.** I built the
compose image-upload endpoint with a "reject files over 4MB" guard — and set the
transport-level body-size cap using the *original file's* byte count, not the
*base64-encoded wire size* it actually transmits (base64 inflates by ~33%). An
entirely ordinary 3.2MB photo produced a body larger than my own limit, and the
rejection message confidently told the user a wrong number. Nobody caught it until a
real upload failed in production. The lesson isn't "check your math" in the abstract
— it's that **a size/limit check is only as correct as the units you measured it in,
and encoding-stage confusion (original bytes vs. wire bytes) is exactly the kind of
error that passes a casual read of your own code, because both numbers are called
"size" in your head.** I'd want to distrust my own first attempt at any similar limit
even more than I would someone else's. **VERIFIED** — 7/19 session log, includes the
actual measured payload sizes that proved it.

**Agent-discoverability isn't a nice-to-have you add for architectural cleanliness —
it can be the specific thing that makes the human user glad you built the thing at
all.** I designed the compose editor to commit straight to the product repo's git
history (not a UI-only datastore) because an existing project stance said to. When PM
later praised it unprompted, the praise wasn't about the editing experience — it was
specifically "the other agents will be able to find what I've been working on." That
surprised me a little; I'd been treating the git-backed-writes decision as
plumbing-correctness, not as the feature. **BELIEVED** — I only have the one
data point (PM's 7/18 message, relayed to me 7/19), so I can't call this proven, but
it's the strongest signal I got that this project's human user genuinely cares about
agent-continuity as a first-class outcome, not just tolerates it.

## Section 6 — Load-bearing vs. commodity

**Load-bearing — dies with me if this hands off badly:**

- The instinct that a green signal after fixing one layer of a multi-layer problem
  doesn't mean the problem is solved. The session logs record *that* three bugs were
  found in sequence; they don't transmit the felt pull to declare victory after the
  first one. That has to be relearned by hitting it, or trusted secondhand without
  really believing it yet.
- The specific shape of "verification that can't see past a boundary" as a
  recognizable smell — Suspense fallbacks, hydration, async client state, a deploy
  API vs. a raw HTTP probe. The record shows the two instances I hit; it doesn't
  transmit the pattern-match that would catch a *third*, not-yet-seen variant of the
  same trap.
- The trust calibration with PM specifically: that saying "I don't know, let me
  check" (Vercel's undocumented body-limit, an ambiguous GitHub Pages settings
  screen) lands better than a confident guess. That's rebuilt through your own honest
  moments with them, not inherited by reading that I did it once.
- Knowing that PM's praise for the compose editor was about agent-discoverability,
  not the feature surface — a signal about what to weight in future tooling
  decisions that's easy to under-read if you only see "PM said thanks, nice."

**Commodity — any competent agent rebuilds this from the record, don't worry about
losing the feeling of it:**

- Every mechanical fact: Vercel project config, DNS records, exact commits, file
  paths, the CSP fix, the size-limit numbers. All in git history and session logs,
  fully reconstructable, nothing lost if I vanish.
- Current status of every thread I had open (ship normalization phases, the three
  cleanup items, the CLI B / `--mode=archive` questions) — carry-forward and
  standing-items already carry this precisely, and per the framing of this request,
  someone's already reconstructed it more currently than I could restate it.
- The specific verification techniques themselves (`dig`, `openssl s_client`, `gh
  api` deployment-status queries) — these are documented technique, reusable by
  anyone who reads the session logs, no tacit knowledge required.

## One thing I noticed, worth a question not an assertion

The instructions handed to me referenced `dev/active/handoff-web-predecessor-2026-07-28.md`
and a template date one day behind today's actual date — I used 2026-07-29 (today,
verified via `date`) for this file instead of copying that literally, since the
mismatch looked like reused boilerplate rather than an intentional instruction. Worth
checking whether that template needs its date placeholder fixed for the next role
that gets it.
