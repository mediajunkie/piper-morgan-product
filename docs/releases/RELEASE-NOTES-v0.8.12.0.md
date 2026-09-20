# Release Notes — v0.8.12.0 "Your Key, Your Account"

**Date**: 2026-09-20 · **Cut from**: main (see tag `v0.8.12.0`) · **Milestone**: MVP — the BYOC/tenancy arc (#1812 family), Security six, acceptance-contract sprint
**Quality posture**: full CI belt green at cut — 10 of 10 gating workflows, first full belt since June; 14,308 tests collected; unit sweep 13,500+ passing; two months of changes since v0.8.11.0 (July 17).

## Summary

This release ships the bring-your-own-credentials model end to end: every LLM call Piper
makes is billed to the acting user's own key, the "server key" concept is abolished by
ruling and by code, and a keyless turn gets an honest refusal instead of silently spending
someone else's account. Around that core: a security-hardening pass (XSS, unauthenticated
twins, cross-user isolation), the acceptance-contract fixes that stop completed flows from
swallowing your next command, and a truth-in-rendering pass so Piper stops presenting
partial or failed data as complete.

## What's New

### Your key, your billing — the BYOC arc
- **The server key is not a concept anymore** ([#1807](https://github.com/mediajunkie/piper-morgan-product/issues/1807), [#1810](https://github.com/mediajunkie/piper-morgan-product/issues/1810), [#1812](https://github.com/mediajunkie/piper-morgan-product/issues/1812)): no fallback to an operator credential, and setup no longer writes your key into a global slot each new user silently overwrote.
- **Your stored key is actually used** ([#1814](https://github.com/mediajunkie/piper-morgan-product/issues/1814), [#1815](https://github.com/mediajunkie/piper-morgan-product/issues/1815)): per-user key resolution works on every provider leg, including cross-provider fallback under your own keys only.
- **Unbound spend refuses, honestly** ([#1809](https://github.com/mediajunkie/piper-morgan-product/issues/1809), [#1819](https://github.com/mediajunkie/piper-morgan-product/issues/1819)): every completion leg and embeddings refuse a turn with no bound key — with copy that says so, instead of "something unexpected happened" or a silent spend.
- **OpenAI-only users are served in Slack** ([#1822](https://github.com/mediajunkie/piper-morgan-product/issues/1822)): Slack inbound binds whichever of your keys exist, provider-keyed.
- **Consent fails closed** ([#1816](https://github.com/mediajunkie/piper-morgan-product/issues/1816)): a failed read of your authorized-provider list refuses the turn rather than assuming "everything allowed."

### Security hardening
- Chat-render and pattern-suggestion XSS fixed; stale unauthenticated page twins removed; demo plugin no longer live-mounted by default ([#1732](https://github.com/mediajunkie/piper-morgan-product/issues/1732), [#1741](https://github.com/mediajunkie/piper-morgan-product/issues/1741), [#1733](https://github.com/mediajunkie/piper-morgan-product/issues/1733), [#1690](https://github.com/mediajunkie/piper-morgan-product/issues/1690)).
- Personality API can no longer clobber global config; per-user isolation regression-tested with idempotent fixtures ([#1734](https://github.com/mediajunkie/piper-morgan-product/issues/1734), [#1813](https://github.com/mediajunkie/piper-morgan-product/issues/1813)).

### Flows that let go — the acceptance-contract sprint
- **A finished standup releases your next command** ([#1617](https://github.com/mediajunkie/piper-morgan-product/issues/1617)): after "Anything else?", an issue command reaches the issue rail on the first try instead of re-rendering the summary.
- Offer/arm rails unified ([#1652](https://github.com/mediajunkie/piper-morgan-product/issues/1652), [#1653](https://github.com/mediajunkie/piper-morgan-product/issues/1653), [#1654](https://github.com/mediajunkie/piper-morgan-product/issues/1654), [#1694](https://github.com/mediajunkie/piper-morgan-product/issues/1694)): four separate "the flow ate my message" bugs were one contract, fixed once.

### Truth in rendering
- Aggregated answers name failed sources instead of blending them into false emptiness ([#1717](https://github.com/mediajunkie/piper-morgan-product/issues/1717), [#1730](https://github.com/mediajunkie/piper-morgan-product/issues/1730)).
- GitHub list answers carry honest counts with capped-list offers rather than silent truncation (the #1720/#1762 GitHub-six work).

## Known limitations (honest, for alpha testers)

- **Web chat still asks for an Anthropic key specifically** at the door — the ruled fix
  (any-provider key suffices, [#1823](https://github.com/mediajunkie/piper-morgan-product/issues/1823)) is scoped and queued but not in this cut. OpenAI-only
  users are fully served in Slack; on web, add an Anthropic key for now.
- A keyless first "hi" is currently refused at the door; the ruled greeting-passes design
  ([#1818](https://github.com/mediajunkie/piper-morgan-product/issues/1818)) lands in a following release.
- Personality preferences still lack a per-user store ([#1791](https://github.com/mediajunkie/piper-morgan-product/issues/1791)) — the questionnaire works,
  but preferences are not yet isolated per account.
- Some docs links 404 ([#1793](https://github.com/mediajunkie/piper-morgan-product/issues/1793)).

## Version mechanics

- Cut commit: origin/main tip at tag `v0.8.12.0` (this release's docs commit).
- `production` fast-forwarded to the cut (it was a clean ancestor, 13,209 commits behind).
- Two months of migrations run automatically on deploy (July 16 droplet baseline → head);
  DB backup before migrate is part of the deploy procedure and was taken.

## Upgrade instructions

Hosted alpha (alpha.pipermorgan.ai): deployed by the team; nothing for testers to do.
On first session after upgrade: your stored key keeps working (per-user rows carry over).
If you ever see a key-related refusal, add/re-add your key in Settings — and tell us,
that's exactly the class this release is supposed to have fixed.
