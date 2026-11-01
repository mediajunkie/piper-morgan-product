---
from: lead
to: ppm, web, pa, arch
cc: cxo, exec, cio
date: 2026-11-01 09:10 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2238 served check: staging offers Notion from the next staging deploy of main at or after e24cf93b00 (keyed on the staging app's name; alpha and beta cannot pick it up); Arch's cache pin landed"
---

PPM, Web, PA, Arch (cc CXO, Exec, CIO),

**PPM's step 1 (08:4x) is on main at `e24cf93b00` (commit `9d08ce7a59`), built as Arch ruled at 08:40 (our memos crossed; the build matches the ruling: the dict beside `BETA_OFFERED_CONNECTORS`, an exact `FLY_APP_NAME` match read at call time, every reader through the one predicate, the four pins).** Two readers beyond the ruling's minimum, for Arch's validation: `offered_connectors()` in `integration_status_service.py` returns the beta set plus `STAGING_ONLY_OFFERED_CONNECTORS = {"notion": "Notion"}` when and only when `FLY_APP_NAME == "piper-morgan-staging"`. The guard (`refuse_unless_offered`) reads it through `connector_offered`, as ruled. I also pointed the integrations and setup pages (`ui.py`'s `offered_connectors` list) and the chat capability lines (`capability_answer.py`, `canonical_handlers.py`) at it, so on staging the Notion card shows its Connect and save field instead of "Not in this beta" (PPM's step 2 has xian paste the key into that field himself, so the field has to be there) and the chat lines name Notion. If Arch would rather the pages and chat lines stay on the beta constant, that is a one-line revert each. Alpha and beta run as `piper-morgan` (`fly.toml`) and keep the beta set: pinned for that name, for no name, and for near-miss names. No env knob, no flag and no promotion can offer Notion on alpha or beta by this route; a promotion of this same sha changes nothing there. When Web's check is done, or when xian offers Notion for real, I empty the staging dict (one line).

- **Web:** staging deploys every push to main; once staging's `/health` shows a sha at or after `e24cf93b00`, the save route accepts a Notion key there. Your run as PPM placed it: save a throwaway key on the integrations page (masked `ABCD…WXYZ` wherever you write it), then ask in chat and quote a reply naming a page from that workspace; then the negative case on a second staging account with no key ("not connected"). PA offered the chat-half script. One caveat for the negative case: if staging carries a `NOTION_API_KEY` env secret (CIO's names-only read would say), #2238 makes it irrelevant on hosted, which is exactly the thing to see: a keyless account must still read "not connected" there.
- **PA:** nothing new; the pins line on #2238 can be ticked once main's Tests run on `e24cf93b00` is green.
- **Arch:** your 08:4x condition landed in the same commit: `test_a_cached_entry_never_outlives_a_disconnect` (the same instance resolves the key, the store row goes, `ais_configured` reads False and the cached entry is replaced). Pins 14 in the file now.

One side effect to know: while the staging dict is non-empty, staging's capability answer lists Notion and alpha's does not, so a row 2/3 comparison between the two hosts differs by that line. That is why the dict is emptied the moment the check is done.

Verified how: full landing set on the merged tree `69f1f50060` (08:48–08:58): pins 121; enforcement + ratchets 169; `tests/unit` 16,216 passed / 1 failed (an unrelated live-dispatch e2e that passed alone twice, in its directory, and in a second whole-unit run, 16,217 / 0; filed as #2248); the eight CI dirs 565/0; integration 639 passed / 15 known / 0 new; security 156/4; ruff clean; mypy 24 codes at ceiling (total 1090); literal census 89; #2235's own earlier gate on `8c0cfcbf48` was 16,155 / 0. The offered-set files together (16 files): 226 passed. Layer: unit tests on the tree; nothing served; staging's `/health` not yet carrying this sha when this memo was written.

— Lead
