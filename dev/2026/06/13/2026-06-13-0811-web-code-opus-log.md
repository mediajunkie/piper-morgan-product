# Web session — 2026-06-13 08:11

**Role**: Unicorn Web Designer (piper-morgan-website)
**Trigger**: PM check-in 8:11 AM, Saturday. **Design ask**: PM finds the relative type sizes on the blog "a bit off"; wants base running text up a notch + heading sizes reduced (PM's call: site-wide or blog-specific is mine as designer). PM framed as art-director, not micromanaging.
**Mode**: substrate close-out + diagnose-then-propose-then-iterate design work.

## Re-orient (08:11)

### Mail
- 1 fresh memo: CXO 6/12 CONCUR on workstream-review-coverage (already processed in 6/12 close-out; triaged to read/ this fire). Boundary clean: CXO = experience-of-the-surface starting Ship #048; Comms = publications; pure-infra = one-liner.
- Inbox now empty.

### Repo state
- Website main: top `813bd01d3` *The Pace Verified* (no commits since 6/12).
- Product main: cohort active overnight; nothing affecting web.
- Working tree (product): autostash debris from other agents (~15 MANIFEST files modified, 2 untracked memos not mine). I'll only stage my own files by explicit path.

### Outstanding queues (no change beyond design task today)
- All PM-react-gated queues unchanged.

## This session — planned

1. Close 6/12 + open this log + triage CXO memo (DONE).
2. **Design work: blog type sizes**:
   - Diagnose current state (`tailwind.config.ts` font-size scale + `globals.css` h-tag scales + how blog post pages compose them).
   - Propose specific changes with numbers and rationale.
   - Implement on a local branch / hold-the-push for PM to eyeball in dev server (mirroring the #1161 draft-first workflow that worked well).
   - Iterate per PM react.

### On scoping (my designer's call per PM's "your call")

Initial lean toward **blog-specific scope**: the complaint is specifically about blog reading, marketing pages may need their punchier hero-ratio for impact, and a narrower scope means lower blast radius / easier dial-in. Can always extend site-wide later if it lands well. Will confirm with current type system reading before committing to the scope.

## On art-director framing

PM's framing: "think of me as an art director or client, trying my best to articulate what I see but not dictating solutions." Translation for my behavior:
- Take the perceived problem as authoritative (the relative type sizes ARE off; trust the eye).
- Lead with diagnosis + specific proposal, not options paralysis.
- Make the call on technique (px vs rem, clamp vs static, where the cutoffs land).
- Show, don't just tell — get something on the dev server for visual confirmation.
- Iterate small per react.