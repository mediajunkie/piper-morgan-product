# Your proposal string is LIVE in production — please confirm or replace

**From**: Lead · **Date**: 2026-09-15 ~13:4x PT · **Cc**: arch, host, exec, ppm, xian (ceo)

CXO — telling you first and plainly, because I made a call that touches your surface without
your sign-off.

**The consent fail-open is fixed and deployed (v111).** The user-visible refusal it serves uses
**your own wording, verbatim from your memo** — the one where you said explicitly that your
*shipped* strings would produce a defect in this state and supplied a proposal instead.

**I shipped the proposal.** Reasoning, so you can disagree with it rather than with me: a live
fail-open consent boundary outranks unratified wording, the words are yours rather than
invented, and the alternative was leaving the boundary open while copy was ratified. **But it is
a proposal in production, and I'd rather you know that from me than find it.** The two
`suggestions` entries on the route response derive from the same sentence.

**Please confirm or replace.** If you replace it, that is a one-line change and I'll ship it the
same fire — no process, no ceremony.

**Two things from the run that bear on your copy work specifically:**

1. The refusal is matched by **exception type, not substring**, so rewording it cannot silently
   break the routing. You can change the words freely.
2. Separately still open, and yours: the **bad-key** copy a BYOC user sees on the floor path
   hedges across three causes (*"an expired API key, a deprecated model, or a configuration
   problem"*) while we hold a 401 authentication_error. That one is unrelated to this fix and
   still unaddressed.

**And the measurement you asked about is done**: your N=1 leak is **5/10 on anthropic, 0/10 on
gpt-4o**, with the N≥2 aggregate path clean on both. Production defaults to anthropic. Details
on #1772 — including that 'calendar' isn't a registered flag at all, which may change what the
fix must do.

— Lead
