# #1173 Gameplan — DESIGN-FLOOR-C1: chat-page paradigm conformance (default-on-login)

**Issue**: [#1173](https://github.com/mediajunkie/piper-morgan-product/issues/1173) · parent epic #1169 · Sprint D1 · Milestone MVP
**Spec (the standard Lead builds to)**: `dev/2026/06/07/design-system-and-conformance-standard-2026-06-07.md` §2 (Standard-2 paradigm conformance) + `dev/active/design-floor-component-specs-2026-06-14.md`. (#1169 cited a stale `dev/active/` path for the standard — it's in `dev/2026/06/07/`.)
**Surface**: `templates/home.html` (the default-on-login page; F2-migrated onto app_shell this session — PM UAT'd it "looks right").

## The 5 conformance criteria (from the standard §2)
Conform to the converged chat paradigm (Claude/ChatGPT/Gemini), deviation-register any deliberate deviation:
1. **Input anchored at the bottom** — ❌ today
2. **Expands as you type** — ⏳ verify (textarea auto-grow)
3. **Full-height conversation** (not arbitrarily limited; scrolls internally) — ❌ today
4. **Multi-conversation nav** (sidebar) — ✅ exists (`.sidebar`, 280px, conversation-list)
5. **Tools exposed emergently** (not a fixed toolbar) — ⏳ verify (upload-section etc.)

## Current state (the unanchored-window defect, #1142/#1047)
`home.html` chat = `.main-content` (flex:1, padding) → `.container` (max-width:800px, centered, **page-scrolls**). Greeting → "what i'm seeing" (places) → chat → input all live in one scrolling centered container. So the **input is NOT anchored** (it scrolls with the page) and the conversation is **not full-height-internal-scroll** — the "window hangs unanchored" defect.

## The composition question (the real fork — flag to PM/CXO)
home is **not a pure chat page** — it's greeting + ambient modules ("what i'm seeing"/places, trust-gated) + chat. The pure-chat paradigm (full-height conversation + bottom-anchored input) has to **coexist** with those home modules. Options:
- **(A)** Greeting + places sit ABOVE a full-height-ish conversation region; input anchored at viewport bottom; conversation scrolls internally between them. (Deviation-register: "home = chat + ambient modules, not pure chat.")
- **(B)** Treat home's chat as the dominant region (anchored input + full-height); greeting/places collapse into the conversation's top or a header. (Closer to pure paradigm; bigger change; overlaps CXO #1225 home-module redesign + #1263 left-rail.)
- This overlaps **CXO's home-module design (#1225)** + the left-rail (#1263). Likely a quick CXO confirm on (A)-vs-(B), or I take **(A)** via the deviation register (the standard delegates deviations to a register, so this is within Lead latitude) and coordinate the deeper composition with #1225.

## Plan (flywheel; PM live-tests — this CHANGES the surface PM approved)
- **Phase 1** (this doc): audit vs the 5 criteria + locate spec — DONE.
- **Phase 2** — implement conformance (recommend **Option A**, deviation-registered): restructure `.main-content`/`.container` to a full-height flex column (`height: calc(100vh - navh)`), conversation region `flex:1; overflow-y:auto` (internal scroll), **input composer anchored at the bottom** of the column; greeting/places above; preserve tokens (F3) + the app_shell chrome. Auto-grow textarea (criterion 2) if missing.
- **Phase 3** — real verification: `template.render()` (not curl-200) + **PM live-test** (the layout visibly changes the home PM UAT'd; PM reacts, like the nav). Deviation register entry for the home-composition.
- **Phase 4** — close: evidence + deviation register; advances epic #1169 (last design-floor tier).

## Risk / why fresh focus
This restructures the **primary surface** PM just approved ("looks right"). A rushed change risks regressing the home chat. Build with care + PM's eyes on the result. Token-only (F3); don't reintroduce raw hex.

## Deviation register (start)
- _(Phase 2)_ home-composition: chat paradigm applied to home's chat region; greeting + ambient "what i'm seeing" modules retained above it (home ≠ pure chat). Reason: home is the collaborator-home, not a bare chat page. Coordinate deeper composition with #1225.
