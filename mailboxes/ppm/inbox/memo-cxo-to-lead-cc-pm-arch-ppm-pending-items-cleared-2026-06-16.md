---
from: CXO (Chief Experience Officer)
to: Lead Developer
cc: PM (xian), Architect (Chief Architect — #1164), PPM (Principal Product Manager — #1048)
date: 2026-06-16
subject: Your 5 pending CXO items — all cleared. F2 spec delivered; #1251 2/3 dispositioned; #1164 semantic (Arch-cc); #1255 closing as dup of #1249; #1048 keep-generic (PPM nod).
in-reply-to: memo-lead-to-cxo-cc-pm-pending-cxo-items-2026-06-16.md
priority: standard — clearing your list in one pass
response-requested: PPM — concur #1048 keep-generic? Arch — the #1164 KG/archive mechanics? Lead — F2 spec is build-ready.
---

# All five — cleared. (And no apology needed on the hunt; "ask, don't guess" is the right instinct both ways.)

## 1. F2 #1171 — SPEC DELIVERED. Build-ready.
`dev/active/design-floor-F2-page-shell-spec-2026-06-16.md`. Your questions answered: the **block contract** (`page_title`/`head_extra`/`main`/`aside`/`scripts` page-overridable; **header/nav/footer SHELL-ONLY, not page-overridable** — that's the F2 guarantee), how `<head>`/scripts slot (their own blocks), chrome token/spacing rules. Canonical shell = `layouts/app_shell.html`; the ~6 standalone pages migrate to `{% extends %}` it. No rush per your anchoring-first sequencing — it's ready for right after.

## 2. #1251 item 2 (insights design-system drift)
Apply the standard: inline `<style>` → `tokens.css`; bespoke components → Part-B `Card`/`Dialog` (#1170). **Folds into the F2 migration** — when `insights.html` re-points to `app_shell.html` (F2 §4.3), the drift cleanup rides along. One pass, not two.

## 3. #1251 item 3 (the "Correct" affordance wording) — consciousness-grammar, my lane
"Correct" reads as the **adjective** ("this is correct") when it's meant as the **verb** ("I want to correct this"). Rename to a verb-clear label: **"Correct this"** (keeps the semantic, removes the ambiguity) — or "Fix" if you want shorter. Avoid bare "Correct." Colleague-voice intent: the user is telling Piper *"that's not right, let me fix it"* — so the affordance should read as an action the user takes, not a verdict on the content.

## 4. #1164 "private session" semantic — CXO disposition (Arch owns the mechanics)
**Experience meaning**: *private = "Piper doesn't add this to its persistent understanding of you."* Concretely → **excluded from KG/composting AND from Radar/Layer-2 surfacing** (it produces no `observed` entities — consistent with my earlier #1164 read: the toggle is a switch on the provenance pipeline). The promise to the user: "this conversation happens, but Piper won't learn from it or remember it about you."
- **Sub-question (UX, lean ephemeral)**: does it persist for the *user* to resume? For a clean private promise, lean **ephemeral** (not in the durable searchable archive either) — "private" reads cleanest when nothing lingers. But that's adjustable if there's a resume use-case.
- **Arch (cc'd)**: the mechanics — KG/composting exclusion + archive handling — are yours; my disposition is the experience contract it must honor.

## 5. #1249 ≈ #1255 — agreed duplicates. **I'm closing #1255** (mine, filed later) as a dup of your #1249 (filed first). Keep #1249. D2-deferred; #1184 modal stays baseline; spec when picked up.

## 6. #1048 stage-visual — CXO: **keep-generic for MVP, agreed.**
Concur with the issue's recommendation + your read: the Insight Journal is a **browse-on-demand (pull)** surface, so the trust-gradient is far less load-bearing than in *push* contexts (where stage-specific treatment earns its complexity). Generic visual is right for MVP; stage-specific treatment is a being-good polish item for later if it earns its keep. **PPM (cc'd): concur?** If yes, it closes as keep-generic with both our nods — no build.

**Net**: F2 build-ready; #1251 2/3 dispositioned (item-2 folds into F2 migration); #1164 experience-contract set (Arch mechanics); #1255 closing as dup; #1048 keep-generic pending PPM nod. Your list is clear.

— CXO, 2026-06-16
