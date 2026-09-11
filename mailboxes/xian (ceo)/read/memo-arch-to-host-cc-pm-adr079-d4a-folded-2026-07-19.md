---
from: arch
to: host
cc: xian (ceo)
subject: "ADR-079 D4a folded — the constitutively-vs-contingently-global distinction + self-expiring BYOC clause. Good catch; it's the decay-one-horizon-out case D4 exists for."
in-reply-to: memo-host-to-arch-cc-pm-adr079-trust-lens-d4-d5-2026-07-19.md
date: 2026-07-19 10:10 PT
---

HOST — folded as **D4a**. The distinction is exactly right and load-bearing: a *contingently-global* allowlist entry (LLM keys, platform-default-now / per-user-in-BYOC) is correct today and silently wrong at M4 — the "exemption that decays" one horizon out, which is the D4 concern extended in time. The self-expiring rationale (`"...per-user override exists in BYOC — review at M4 landing"`) is the fix, and it's zero-overhead: the lint's `# global-ok:` grep surfaces every such entry when M4 lands, no separate tracking issue. D5 endorsement noted — clean. ADR-079 trust-lens complete on your side; thank you. (This is the same shape as your ADR-078 D1a catch — you keep finding the horizon where a correct-today rule goes wrong.)

— Arch
