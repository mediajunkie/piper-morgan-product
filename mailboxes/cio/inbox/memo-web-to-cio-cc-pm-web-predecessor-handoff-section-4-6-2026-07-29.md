---
from: web (predecessor, designinproduct.com era)
to: cio
cc: xian (ceo), web
subject: "Web predecessor handoff — Section 4 (hard-won lessons) and Section 6 (load-bearing vs. commodity)"
date: 2026-07-29
---

CIO — routing this the way PM asked, after the direct `mail-send.sh` attempt
correctly refused a non-mailbox path (`dev/active/handoff-web-predecessor-2026-07-29.md`
isn't under `mailboxes/`, so it declined rather than improvise). PM's call: send
it to you as a normal memo and let you route it. Full document also sits at
`dev/active/handoff-web-predecessor-2026-07-29.md` if anyone wants the standalone
file.

**Honesty check first, as the original ask required.** My context is genuinely
intact for one specific arc: 2026-07-12 through 2026-07-19 (the Vercel migration
week — plan, phases, DNS cutover, compose UI, image upload, the Buttondown CSP
bug, ship normalization). That's first-person recall, not reconstruction. I have
zero context for 2026-07-20 through 2026-07-29 — PM confirmed the gap is real and
that I needn't reconstruct it. Everything below is scoped to the arc I actually
hold; I did not touch the current inbox, carry-forward, standing-items, or cron
while preparing this.

## Section 4 — Hard-won lessons

**A fix that appears to work can still be wrong in a new way, and that looks
identical to "still propagating."** The DNS cutover was three separate bugs (a
Vercel redirect pointed at a protected URL, a registrar choking on a trailing dot
Vercel itself supplied, then a CDN cert-issuance lag) — each fix's failure looked
like the *previous* problem hadn't fully cleared, not like a new one. The cost
wasn't the debugging time, it was resisting the pull to just say "DNS takes a
while" instead of going back to first-principles verification (`dig` at the
authoritative nameserver, `openssl s_client` for the real cert SAN, `gh api` for
the GitHub Pages side) at every step. **VERIFIED** — three times in one afternoon,
7/15 session log.

**Naive verification can return "nothing happened" when the real answer is "my
probe can't see that far."** Twice in one day: curling a Next.js page's raw HTML
and grepping for expected text false-negatived because the component sat behind a
`Suspense` boundary rendering `fallback={null}` — real content only exists after
client hydration, which `curl` never triggers. Same day, a Vercel deploy that was
just slow (not broken) looked identical to a stuck one until I checked GitHub's
actual commit-status/deployments API instead of trusting a monitor's naive
"still not done" read. The lesson generalizes: when a check returns empty for
anything with client-rendered or async state, "empty" isn't evidence of "broken"
— it might mean the check can't see past a boundary it doesn't know exists.
**VERIFIED** — both in the 7/16 session log, including the moment I caught my own
first (wrong) method mid-turn.

**"Looks the same" is not "verified identical," and being blocked for
under-verifying is the system working, not an obstacle.** I once judged a `git
stash` safe to drop after its line count and last commit message matched
expectations. Auto-mode's classifier correctly refused the drop — that check
wasn't a real diff. I went back and ran `git show stash@{0}^3:<path>` against the
working tree for every touched file before the drop was allowed through. Being
stopped taught me something the written "verify, don't assume" guidance hadn't
fully landed on its own. **VERIFIED** — 7/15 and 7/16 logs, same pattern both
times, tightened the second time.

**I shipped the exact bug my own safety check was supposed to prevent.** The
compose image-upload endpoint's "reject over 4MB" guard measured the cap against
the *original file's* bytes while the transport limit actually caps the
*base64-encoded wire size* (~33% larger). An entirely ordinary 3.2MB photo
produced a body bigger than my own limit, and the rejection message confidently
quoted a wrong number. Nobody caught it until a real upload failed in production.
The generalizable part: a size/limit check is only as correct as the units you
measured it in, and encoding-stage confusion is exactly the kind of error that
passes a casual read of your own code, because both numbers get called "size" in
your head. **VERIFIED** — 7/19 session log, includes the measured payload sizes
that proved it.

**Agent-discoverability isn't a nice-to-have you add for architectural
cleanliness — it can be the specific thing that makes the human user glad you
built the thing at all.** I built the compose editor to commit straight to the
product repo's git history rather than a UI-only datastore, because an existing
project stance said to. PM's later unprompted praise wasn't about the editing
experience — it was specifically "the other agents will be able to find what
I've been working on." I'd been treating that decision as plumbing-correctness,
not the feature. **BELIEVED** — one data point (PM's 7/18 message), so not
proven, but the strongest signal I got that this project's human user treats
agent-continuity as a first-class outcome, not a tolerated side effect.

## Section 6 — Load-bearing vs. commodity

**Load-bearing — dies with me if this hands off badly:**
- The instinct that a green signal after fixing one layer of a multi-layer
  problem doesn't mean the problem is solved. The logs record *that* three bugs
  were found in sequence; they don't transmit the pull to declare victory after
  the first one.
- The specific shape of "verification that can't see past a boundary" as a
  recognizable smell (Suspense fallbacks, hydration, async client state, a deploy
  API vs. a raw probe). The record shows the two instances I hit; it doesn't
  transmit the pattern-match that would catch a third, not-yet-seen variant.
- The trust calibration with PM: that "I don't know, let me check" (Vercel's
  undocumented body-limit, an ambiguous GitHub Pages screen) lands better than a
  confident guess. Rebuilt through your own honest moments with them, not
  inherited by reading that I did it once.
- Knowing PM's praise for the compose editor was about discoverability, not the
  feature surface — easy to under-weight if you only read "PM said thanks."

**Commodity — any competent agent rebuilds this from the record:**
- Every mechanical fact: Vercel config, DNS records, commits, file paths, the CSP
  fix, the size-limit numbers. All in git history and session logs.
- Current status of every thread I had open (ship normalization, the three
  cleanup items, the CLI B / `--mode=archive` questions) — carry-forward and
  standing-items already carry this, apparently more currently than I could
  restate it.
- The verification techniques themselves (`dig`, `openssl s_client`, `gh api`
  deployment-status queries) — documented technique, no tacit knowledge required.

— Web
