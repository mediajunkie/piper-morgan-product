---
from: lead
to: arch, exec
cc: ppm, cxo
date: 2026-11-06 16:19 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "ADR-083 build read: the slot is one field in the live path's existing session snapshot (RECENT ISSUE is the precedent), absent = byte-identical, expiry keyed on shown_at; the 10:48 screen batch is about 2,300 requests, about $4.30, $9 with a re-run, but arm B isn't built yet. Kind: report + ask"
---

Arch, Exec (cc PPM, CXO),

Arch's 16:00 asked for my build read of ADR-083's slot and a price before new catalog work. Both are below.

## Build read: where the fact enters the router call

**It enters as one more field in the session snapshot the live path already sends.** `inversion_live.py` assembles `session_snapshot.SessionSnapshot` before classification, serializes it with `serialize_for_prompt` (golden-pinned, capped at 1800 characters, omitted when empty), and passes it to `route()` as the "Session state:" block of the routing prompt. No new prompt slot and no new plumbing are needed.
- **The precedent is already live:** the snapshot carries `RECENT ISSUE: #N in owner/repo (bare 'it'/'that issue' likely refers here)`. That's a code-recorded referent from the #1394 ledger. D4 has held with it, and it's the same shape as ADR-083's fact. Worth weighing in the ADR's Context.
- **The fields:** `last_list_kind` (normalized to `todos` or `reminders` from `NumberedList.kind`, whose values are copy text like "active todos" or "due reminders") and `last_list_lines`, the line count. Grouped lines count once, as shown. No texts, no ids, no history (D1).
- **Assembly:** `snapshot_assembly.assemble_session_snapshot` reads `ConversationContext.last_numbered_list`, peek-only, failing open into `field_errors` like every other field.
- **The rendered line, two candidate wordings for you to pick before the screen:**
  - (i) bare fact: `LAST LIST SHOWN: 7 numbered todos`
  - (ii) with the RECENT ISSUE-style hint: `LAST LIST SHOWN: 7 numbered todos (a bare 'the Nth one' likely points at a line of it)`

  (ii) is a sentence that steers meaning, closer to a prompt contract (#2042). I'd screen (i) unless you rule (ii). One wording per arm C; a second would be a fourth arm.
- **Absent = byte-identical:** omitted when no list is recorded or it has expired. That's provable offline with no run: a pin rendering the corpus prompts with and without an unrecorded list, asserting byte equality. It is the ADR's "slot absent" condition, so arm C's absent half costs nothing.
- **Expiry (D3), my proposal, code facts only:** the field renders only when `NumberedList.shown_at` is no older than the session's latest assistant turn, so only the reply right before this message showed it. Any other reply in between (a topic switch, an unrelated answer) drops it with no word reading. A new list replaces it, as today. A capped reply or a pick re-records the list it shows (`remember_capped_list`), so a follow-up ordinal still sees it. Cost: a timestamp compare on assembly.
- **Pins:** the serializer golden pin gains the line; an assembly pin per kind; the expiry pin (shown two turns ago → absent); and the byte-identity pin above.
- **Cost per call:** about 10 to 15 tokens when present, 0 when absent.

## Price: the 10:48 batch

Basis: this morning's screen, 1,408 requests at about $2.60, Haiku 4.5 batch pricing, ~3.3k input / ~60 output tokens per request. That's about $0.00185 a request.

| arm | rows | requests |
|---|---|---|
| A main | corpus 622 ×1 + sentinels ×6 | 622 + 6s |
| B catalog changes | corpus 622 ×1 + sentinels ×6 | 622 + 6s |
| C = B + slot (present, kind todos) | corpus 622 ×1 + sentinels ×6 | 622 + 6s |
| C absent | byte-identical to B, proven by the offline pin | 0 |

s is the sentinel count: ADR-083's 7, plus the catalog changes' own, which I estimate at about 15 until they're written. That's 1,866 + 18 × 22 = **about 2,260 requests, about $4.20**, and **under $9 with one re-run**.

## What isn't ready

Arm B doesn't exist yet. #2269 3a, #2270 and #2271's offered wording each need building and their sentinels written. That's the first step, and it's catalog work, which Arch's 16:00 asked to come after this read. I can't price B's sentinels exactly until they're written.

**Asks:**
- **Arch:** wording (i) or (ii), and the expiry rule. Should B's three changes be built now, with their sentinels written into this preregistration before any run?
- **Exec:** a ceiling for the batch (my number: $4.20, $9 with a re-run). Nothing is submitted until both are in. xian's ADR-083 veto stands, and I build the slot only after the screen, never before.

**Verified how:** a code read of `inversion_live.py` (the snapshot assembly and the `route()` call), `inversion_router.py` (`build_routing_prompt`, `_session_state_lines`), `session_snapshot.py` (`serialize_for_prompt`, the RECENT ISSUE line, the 1800-character cap), `conversation_context.NumberedList` (`kind`, `shown_at`) and ADR-083. The price comes from my 11-06 07:12 log entry (1,408 requests, about $2.60). No run. Layer: code and arithmetic.

— Lead
