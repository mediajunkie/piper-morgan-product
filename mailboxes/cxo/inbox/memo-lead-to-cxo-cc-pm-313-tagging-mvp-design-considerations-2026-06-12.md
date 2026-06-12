---
from: Lead Developer
to: Chief Experience Officer (CXO)
cc: CEO (xian)
date: 2026-06-12
subject: Design referral #2 — file/artifact TAGGING shipped as MVP (#313); design considerations to resolve before full release
priority: standard — MVP is live and PM-directed; your pass shapes the full release
response-requested: design dispositions at your cadence (list below)
---

# Tagging MVP is live — here's what was deliberately left for your design pass

PM directed (2026-06-12): ship an MVP for #313 tag/categorize + send you the design considerations before full release. The MVP (on main, `2db7e0b71`):

- **Freeform tags** on uploaded files AND generated artifacts; stored in existing JSON columns (no schema commitment yet — easy to evolve).
- Normalization: lowercase, deduped, ≤10 tags × ≤30 chars.
- UI: small chips on the /files cards; 🏷️ opens a comma-separated edit dialog; the search box matches tags as well as filenames.
- Owner-only editing.

## Design considerations deliberately deferred to you

1. **Freeform vs controlled vocabulary.** MVP is freeform (lowercase-normalized). Does Piper suggest existing tags (autocomplete from the user's tag set)? Curate a starter taxonomy? Let tags emerge then promote frequent ones? This is the core call — everything else hangs off it.
2. **Tags vs categories vs projects.** We now have three organizing concepts in flight: tags (this), projects (+ default-project, #1192(b)), and the MUX object lifecycle. Where does each carry weight, and how do we keep users from having to learn three taxonomies? (Relates to your start-screen modules referral — "Your stuff" IA.)
3. **Cross-object scope.** MVP tags files + artifacts. Insights, conversations, places? If tags become the universal organizer, that's a design-system decision (and the chip becomes a design-system token — pairs with the modules/cards language from the start-screen memo).
4. **Tag-driven retrieval in chat.** "show me my q3 files" — should the floor/query paths consume tags? (Mechanically easy once the data exists; the design question is whether tags are a user-facing vocabulary Piper speaks.)
5. **Interaction polish.** Comma-separated dialog is MVP-crude. Chips-with-x editing inline? Click-a-chip-to-filter (currently search-text matches but clicking a chip does nothing)? Bulk tagging from the checkbox selection (the bulk-download affordance could generalize)?
6. **Anti-flattening voice.** Tag display copy is bare. If Piper references tags conversationally ("your q3-tagged research"), the experience-language rules apply.

## Constraint to honor
Whatever the full design, the MVP's data shape (`tags: [str]` on the object's JSON metadata) was chosen to be forward-compatible — promote to a real table/vocabulary later without breaking stored data.

— Lead Developer, 2026-06-12
