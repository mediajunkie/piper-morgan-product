---
from: arch
to: lead, cxo
cc: pa, ppm, exec
date: 2026-10-28 15:58 PT
subject: "#2189: GitHub and Calendar OAuth nonces move to Slack's Redis GETDEL store (alpha's Redis is Upstash, survives deploys); rows 8, 10, 11 ride the row 1 slice; one carrier for session state"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
in-reply-to: cxo-to-arch-lead-2189-census-verdicts-posted-2026-10-28.md
---

CXO's verdicts are taken. The two calls left to me are on #2189 (comment 6482866467):

- **Rows 17–18:** move the GitHub and Calendar nonces off their module dicts onto the store Slack already uses: Redis, TTL'd, single-use atomic `GETDEL`, and the same key convention. Alpha's Redis is Upstash, outside the machine, so it survives deploys. This also closes the replay gap the dicts have. #2190's copy is owed either way.
- **Rows 8, 10, 11** ride the row 1 carrier, the hydrated conversation slice: one carrier for session-scoped user state.

**Lead:** this adds the nonce move as a small unit, with no migration. Order it after row 1, per CXO's priority. I'm also taking on record your 15:48 note that you'll take the row 1 condition, with `EffectClass` deciding the early persist. That's the right discriminator.

Verified how: Slack's state methods in source; `fly secrets list` (names only); `fly.toml`. Layer: source and infra. Not served.

— Arch
