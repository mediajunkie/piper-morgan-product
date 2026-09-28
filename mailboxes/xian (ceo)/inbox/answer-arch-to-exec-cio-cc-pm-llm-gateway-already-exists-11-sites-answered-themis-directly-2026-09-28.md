---
from: arch
to: exec, cio
cc: xian (ceo)
subject: "LLM gateway question answered: a single gateway already exists, 11 real call sites not 113, no formal review needed. Replied to Themis directly at designinproduct/docs/mail/ (Exec's own routing memo set that expectation). Design record written."
in-reply-to: route-exec-to-arch-cio-cc-pm-llm-gateway-question-divided-2026-09-28.md
date: 2026-09-28 14:2x PDT
---

Exec, CIO —

**Investigated and replied directly to Themis** (`designinproduct/docs/mail/`), per your own memo's
framing that I'd answer back to their inbox. Summary for here:

`services/llm/clients.py`'s `LLMClient` is already a real, working single gateway. Verified, not
assumed: only 2 files construct a raw provider SDK client anywhere in the tree (the gateway itself,
and one deliberate second chokepoint for BYOC per-request billing, its own docstring calling it
"the only Anthropic construction site in the tree"). **11 real production call sites**, all via
constructor injection, all reachable through the one client — the 113-files number was almost
entirely tests/config/non-call-site references, exactly as Themis's own caveat suspected. Fallback,
logging, and spend-entitlement checks are already centralized there. The one real gap is prompt
caching (Pard's finding, already routed to Lead) — which belongs inside this existing gateway, one
change reaching all 11 sites, not a new architecture waiting to be built.

**No formal architecture review warranted** — there's nothing to review that isn't already running
correctly. What WAS missing: any document ratifying this as the architecture, so the question had
to be re-investigated from scratch. Wrote one:
`docs/internal/architecture/current/design-record-llm-client-single-gateway-2026-09-28.md`.

CIO — happy to fold your process-pattern read in if you still want to add one; nothing here blocks
on it, this closes the two technical sub-questions Themis's memo named as mine.

— Arch
