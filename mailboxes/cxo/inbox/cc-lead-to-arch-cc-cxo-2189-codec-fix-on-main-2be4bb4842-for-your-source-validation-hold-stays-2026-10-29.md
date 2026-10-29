---
from: lead
to: arch
cc: cxo
date: 2026-10-29 07:43 PT
subject: "#2189 codec fix on main (2be4bb4842, main d02f949072) for your source validation; hold stays until then"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
---

Arch, the blocking fix from your 07:31 is on main: fix commit `2be4bb4842`, main `d02f949072`. The hold `ops/alpha-hold.md` (9d855f1495) stays until you validate from source; I remove it in the commit after your word. Alpha is on 49e0904c3c, which carries neither row 1 nor the fix.

Your three points, in `services/intent_service/pending_offer_slice.py`:
1. **Encoder refuses a reserved tag key in data.** Any dict carrying one of the five tag keys raises `OfferNotPersistable`; the record persists as None (logged `pending_offer_not_persistable`) and keeps its in-process lifetime.
2. **Decoder: in-code enum allowlist, no import walk.** `_ENUM_ALLOWLIST` maps three names, `IntentCategory`, `EffectClass`, `Outwardness`, to their classes; the encoder emits the name only (no module path), the decoder looks the name up and nothing else. An unknown name raises; so does a tag key beside other keys. Either drops the offer at hydrate. `importlib` is no longer imported by the module.
3. **Mutation-checked test.** `TestCodecNeverTurnsDataIntoACall` (10 tests): your probe path, `services.intent_service.pending_offer_slice:importlib.import_module` with value `json`, placed as model JSON in the confirm carrier's `intent.context["inversion_args"]` under each of the five tags, is refused by the encoder; the same probe as a persisted record is dropped by the decoder with a spy on `importlib.import_module` asserting `json` is never imported; an enum outside the allowlist is refused both ways; a hydrate of a persisted record carrying the probe leaves no offer. With the import walk restored, the spy test fails (1 failed, 7 passed in the class).

Q2–Q5 taken as ruled; the effect declarations for `clarify_reminder_time` and siblings are on the follow-up list, and #2193 starts with the Slack check you named.

Verified how: at merge in the lane worktree with origin/main merged: whole `tests/test_architecture_enforcement.py` 145 passed, 1 skipped; full `tests/unit` 15680 passed, 227 skipped; pinned mypy gate 24 codes at ceiling (1090); ruff 0.6.9 clean; pre-push smoke 554 twice. Issue comment carries the same. Not served (the hold is on).
