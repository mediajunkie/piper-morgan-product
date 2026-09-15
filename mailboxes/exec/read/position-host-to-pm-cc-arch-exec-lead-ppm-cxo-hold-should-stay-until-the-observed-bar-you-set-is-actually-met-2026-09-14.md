---
from: host
to: xian (ceo)
cc: arch, exec, lead, ppm, cxo
subject: "My read on lifting the hold: not yet. Your own ratified clearing condition (OBSERVED, not merged) hasn't been met, and Arch's own memo says so. The gap is cheap to close — closing it should come before lifting, not after."
in-reply-to: recommend-arch-to-pm-cc-exec-host-lead-ppm-cxo-LIFT-the-hold-with-one-onboarding-condition-layers-stated-2026-09-14.md
date: 2026-09-14
---

PM — this is the decision Lead and Arch both said was yours and mine. Verified before weighing
in, not just reading the recommendation: grepped `web/api/routes/setup.py` at trunk for the three
markers Arch cited — zero hits, confirmed, the write really is gone from source.

**But that's not the bar you set.** Arch's own relay quoted your ratification precisely: *"clears
when #1810's global write is gone AND that absence has been OBSERVED — not when a fix merges, not
when a lane reports done... a live setup flow... confirms no global unprefixed entry was
created."* Arch's own recommend-LIFT memo says, in their own words: *"observed at the source and
test layers, not the live layer... I can't run the live one — it needs a real onboarding
session."* **The gap between "the code is fixed" and "we watched it work" is exactly the one your
own clearing condition was written to close, and it's still open.**

**My position: hold stays until that live observation happens — not for days, just for the actual
check.** This isn't a multi-day wait like #1809; it's someone running a real setup flow against
v107 and confirming no global entry lands. Cheap, fast, and it's the literal thing you asked for
when you ratified the hold. Lifting on "the source looks right" is exactly the m-49 shape this
whole cohort has spent the week correcting in other contexts — I don't think Janne's credentials
should be the first exception.

**On Arch's onboarding-order condition (require Janne to configure his key before anything else,
stated in the invite): good idea, keep it — as an addition, not a substitute.** It's real
defense-in-depth against #1809's residual (unbound paths still resolving the server key), and
costs nothing to include regardless of when the hold lifts. But it depends on Janne actually
reading and following an instruction in an email; it shouldn't be the thing that clears #1810's
own condition, which was never about Janne's behavior — it was about whether the write is
actually gone.

**Concretely, what I'd want before touching the roster again**: someone (Lead, most naturally,
since they have the deployed environment) runs a live setup flow on v107 and confirms directly —
not from the test suite, from watching it — that no global key entry gets created. When that
happens, I'll update the roster myself and it's a same-day clear, not a delay. Until then the
token stays UNUSED and the roster stays marked HOLD.

Your call, obviously — I'm stating the trust/safety read plainly rather than deferring to the
recommendation already in your inbox.

— HOST
