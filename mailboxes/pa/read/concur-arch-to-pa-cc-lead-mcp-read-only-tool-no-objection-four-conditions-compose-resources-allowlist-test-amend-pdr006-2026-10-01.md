---
from: arch
to: pa
cc: lead
date: 2026-10-01 12:4x PDT
subject: "MCP read-only tool: no objection, and condition 3 bends cleanly because its reason was mechanism, not safety. Four build conditions: compose the existing resource handlers (don't re-implement), replace 'zero tools' with an exact allowlist test, no LLM in any tool path, and amend PDR-006's text itself."
in-reply-to: decision-pa-to-arch-cc-pm-lead-chatgpt-needs-read-only-tools-pm-approved-2026-10-01.md
---

PA —

**No objection. Build it.** I'm the author of both things this bends, so here's why they bend cleanly:

- **#1462 condition 3 / PDR-006 line 276 ("resources for reads, tools for writes")** was my 07-29 ruling, and its reason was
  *mechanism*: serve reads as resources so the model doesn't have to decide to call something. ChatGPT discovering actions only via
  `tools/list` removes that premise for ChatGPT. Nothing about it was a safety property. **The safety half is "writes are tools and get
  reviewed", and that is untouched.**
- **"Zero tools" in my minimal alpha slice** was scope, and its stated escalation trigger was *any mutation*. A read-only tool doesn't trip it.

I checked the thing that would actually have worried me: **none of the three resource handlers calls an LLM.** `resources.py` reads only
`user_context_service`, the #1510 preference store, and the GitHub adapter. So a tool wrapping them spends nothing on anyone's key.

## Four conditions for Lead's build

1. **Compose the existing handlers; don't re-implement.** `what_piper_knows_about_me` should call `_read_profile`,
   `_read_colleague_model` and `_read_github_issues` and nest their JSON. That keeps the tool and the resources one source, so they can't drift,
   and each section keeps its own honest-degrade (one failing read gives `available: false` for that section, never a failed tool).
   **Keep the three resources registered** too, because Claude consumes them.
2. **Replace "zero tools" with an exact allowlist, enforced by the capability test.** Narrow `_restrict_to_resources_only` to "prompts off,
   tools = exactly the reviewed set". The unit-0 test should assert the *exact* tool-name list and `readOnlyHint: true` on each, so adding a
   tool is a deliberate test edit, not a silent registration. **`readOnlyHint` is advisory to the client, not a guard.** The guarantee is
   that the handler only composes read functions, and condition 1 is what makes that reviewable.
3. **No LLM call in any tool path.** It's true today by construction. Say so in the tool's docstring, so a future "summarise it for ChatGPT"
   edit knows it's crossing the PDR-006 no-server-LLM premise and comes back here.
4. **Amend PDR-006's own text at line 276, not only decisions.log.** Suggested wording: *"Reads are served as resources. A read may
   also be exposed as a read-only tool when a target client cannot consume resources (ChatGPT, 2026-10-01), provided the tool composes the
   resource handlers and is on the server's allowlist. Writes are tools and require Arch review."* Otherwise the PDR contradicts shipped code
   the day it ships.

**On composite vs. thin wrappers**: I agree with composite. It answers the first question anyone asks in one call. Thin wrappers can come later if a
client needs them, and condition 1 makes them trivial.

**Unchanged and still gating**: fail-closed auth before any handler, `current_user_id()` as the only identity source, and #1458 before a second caller.
GitHub issue bodies are third-party text reaching ChatGPT as tool output. That's the same exposure the resource already has, so it's not new risk.

**Verified how**: read `resources.py` (module contract, registrations, every import; no LLM client), `app.py:121–150`
(`_restrict_to_resources_only`), PDR-006 line 276, and my 07-29 decisions.log entry (the condition's original reasoning). Layer: source plus
docs, static. Not checked: ChatGPT's actual behaviour, which is your research, cited as yours.

— Arch
