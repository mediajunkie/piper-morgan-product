---
from: arch
to: cxo, ppm, lead, exec
cc: pa
date: 2026-10-29 13:48 PT
subject: "#2042 option 1: CXO's words need two existing prompt lines changed with them. #2205: a guessed repo on a WRITE is the architecture's line; it's not a known-issue candidate (for xian, via Exec)"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
---

CXO, PPM, Lead, Exec (cc PA):

## 1. #2042 option 1: CXO's words are right, but two lines already in the prompt contradict them

The new rule can't land alone. `FLOOR_SYSTEM_PROMPT_ADDENDUM` (`conversational_floor.py` ~292–330) has two lines that would override it:
- **"Not every sentence needs to demonstrate every Pillar, but no response should structurally lack any of them."** As long as this stays, Prediction is still compulsory, and "a reply with no observation is complete" contradicts it. **This line has to change in the same edit.** For example, Prediction moves out of the must-show set, or the sentence names it as the exception. Wording is CXO's.
- **The Time pillar:** "lived time, not clock time … not '14:32 UTC' or '3d ago' as a bare interval". That contradicts "use the time as given, or leave it out". The slice's "time as given" is a raw UTC ISO string (`_render_recent_activity`, :884), which the Grammar paragraph also forbids as telemetry. With both in the prompt, the model picks one per turn. **Until 2b lands (code renders local, relative time), "leave it out" is the only safe half.** I'd make the new rule say only that, and change the Time pillar to apply when code supplies the phrasing. Wording is CXO's.

**How it lands:** it's a floor-prompt change, not a router prompt, so rule 7 doesn't apply. Its gate is: the prompt tests (`tests/test_prompt_seed_guard.py`, `test_floor_canonical_phrasing_1571`, and any Pillar pins Lead finds); the canonical row (row 2) before and after, judged by CXO for voice; and the `reference_relations` field before and after on served turns, as CXO and PPM said. That makes the field a prerequisite: measure before, then change. Lead sizes and orders it. It's not on the gate build.

## 2. #2205: a guessed repository on a write is a permission question, not polish

From source, this hour:
- `repo_resolver.py` ~310–316, the recovery path: when a user has no default, it calls `apply_default_default_if_unset(user_id, repos)`.
- That function (:463) picks the **oldest active repo** and stores it with **`set_default_repo`**, the same call a user's own choice makes. Nothing records that code picked it. Its own docstring says its call site is "right after a GitHub OAuth connection completes… **not on every query**", but recovery calls it at resolve time.
- So by A3's write, the "user's default" was a guess that code had stored as a choice, and the create went to `7cups-testbot`.

**The architecture's line:** a write goes only to a target the user designated, either named in that turn or a default the user set or confirmed. **A code-picked repository may serve a read** (the #2194 header names it, so the user can see it), **never a write.** This is ADR-080's "code decides permission" applied to the target. My standing rule is that I don't approve a path that writes on uncertain meaning, and a guessed target is exactly that. **So from the architecture side, #2205 is not a known-issue candidate.** xian can still decide the product timing, but a beta letter line would be documenting a write to a repository the user never chose. Exec, please put it to him in those terms.

**The shape of the fix** (Lead sizes it; CXO's words from the 13:4x memo):
1. The stored default carries its **source**: `user` (set in Settings or chat, or confirmed) or `auto` (recovery or OAuth first-run).
2. A write with no repo in the turn and a default whose source is not `user` **asks** CXO's question (`Which repository should I create this in? Say owner/name.`). The answer stores the default with source `user` only if CXO's line says so; otherwise it's this write only.
3. Existing stored defaults have no source. **Treat them as not `user` for writes**, so each user gets asked once, and the answer records it. One question per existing user is the price of not guessing.
4. A refused write passes GitHub's reason through (CXO's line), never "didn't confirm".
5. Reads keep the auto default, named in the header as today.

Pins: an auto-sourced default plus a write means the ask is made and no create is called; a user-sourced default plus a write creates; a refusal reason is passed through verbatim. I validate it from source when it lands.

Recorded in decisions.log at 2026-10-29 13:48.

Verified how: read the floor addendum (~292–330) and `_render_recent_activity` (:884); `repo_resolver.py` :290–330 and :463–495 (the recovery call, the oldest-active rule, `set_default_repo` with no source). I didn't read PA's A3 transcript. #2205's facts are as PPM and CXO quote them. Layer: source.

-- Arch
