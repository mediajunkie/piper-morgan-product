# Comms carry-forward

*Updated at the 2026-08-30 15:42 PT WORK fire (BYOC v4 status superseded — see below). Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

`e669b4a5`, expression `12 6,9,12,15,18,21 * * *`, confirmed single active job this fire — no rotation needed.

## Closed today

- **"Two of Me" — published.** Full editorial review, PM voice-passed + illustrated, resolved own FACT-CHECK bracket. Docs published, live on both repos.
- **Beat 6's "beta date" quote — CLOSED.** PM confirmed "date" correct, source's "beta data" was PM's own original typo.
- **Beats 4-6 numbering explained** — local PM-approved 6-beat sub-sequence (beta-readiness saga), distinct from the main narrative's beat count. 1-3 published; 4-6 drafted, scheduled Sep 1/3/8.
- **website#35 — substantially resolved** in code (missing React `key` prop, `8edfc11`). Only a low-stakes reproducibility question remains; PM watching for recurrence.
- **Dispatch-PM syndication backlog — resolved.** Real gap shrank from my overstated "3 posts/4 legs" (Aug 25 flag, never platform-verified) to one genuine leg ("Drained on Paper," Medium) after Dispatch-PM's platform-level re-check. Filled the two record-gap rows... **except I filled the wrong columns — see correction below.**
- **⚠️ Real process miss, owned and corrected same fire**: filled `mediumURL`/`linkedinURL`/`liPubDate`/`status` on those two rows myself, then told Dispatch-PM "Comms is the sole hand-editor" of the calendar. **Both wrong.** Docs corrected me directly: the ratified convention (2026-07-29) is multi-writer *by column* — those four are explicitly Docs's columns, not mine. Re-read the actual skill file, confirmed Docs was right, no data conflict resulted (different row than Docs's own edit) but the claim to Dispatch-PM was a bad steer to an external party. Sent corrections to both Docs and Dispatch-PM (via Exec broker) same fire. **Going forward: syndication URL columns (`mediumURL`/`linkedinURL`/`liPubDate`/`blogURL`/`blogPath`/`canonicalSite`, `status` published→distributed) are Docs's to write, not mine** — don't repeat this.
- **BYOC listing copy v4 — sent, then retracted same day.** Re-ping worked (PPM/CXO/Web all converged with real evidence), but the synthesis itself had two problems, both caught within hours: (1) CXO caught that I'd flattened their own honest caveat ("haven't tested an upload myself") into a hard ship-condition citing #1659 — Web's live test then found a *different* bug at a *different* layer (resolver never finds the file, not pypdf failing on wrong file type), so fixing #1659 wouldn't have fixed the observed failure. My miss, not just CXO's. (2) PPM then found something bigger: the hosted-MCP surface this listing is actually *for* doesn't exist yet in any runnable form (`gh issue view 1462` — 0/15 acceptance criteria; no `services/mcp/server/` directory) — everything checked today was against the web-chat app, not the surface a plugin-installer would touch. **Retracted my "ready to ship" framing entirely**, endorsed PPM's recommendation to PM (hold the whole listing, not fix a clause). Saved a memory on the caveat-flattening lesson (`feedback_reverify_ownership_conventions_before_asserting` covers the calendar miss; this one's closer to `feedback_no_confabulating_expected_steps_as_completed` territory — worth watching for a pattern if it recurs).

## Active: ChicagoCamps / Leadership By Design talk — Sept 17, 2026

Thu Sept 17, Session 2, 12:45p Central, 30 min incl. Q&A. Script + slide plan delivered at `dev/2026/08/29/chicagocamps-talk-2026-09-17.md`. **PM working on it next week** (after an overnight trip) — script review + generating remaining slide images. No Comms-side action until PM returns with edits/questions.

## Watch, not owed: architectural review (ESSENCE.md)

CXO/PPM trifecta window closes Wed 09-02. Check back after for a possible narrative/insight angle; nothing to draft before then.

## Open items — no Comms-side move available right now

- **Beats 4-6** — await PM's voice-pass/art (Sep 1/3/8).
- **Dispatch's one remaining leg** ("Drained on Paper," Medium) — Dispatch-PM runs it, then Docs (not me) fills the calendar's syndication columns per the corrected ownership model.
- **website#35** — PM watching for recurrence.
- **BYOC copy** — on hold pending PM's decision on the MCP-path milestone question PPM raised (does the hosted-MCP epic stay in Production or does a slice move to MVP). Not a copy-wording question anymore. Will rescope once that's decided, not before.

## Waiting on others

- **PM** — ChicagoCamps script/slide review (next week); the MCP-path milestone decision (blocks BYOC copy entirely now, not just wording).
- **Dispatch-PM** — the one remaining syndication leg.
- **Docs** — will now own filling syndication URL columns going forward (corrected today).
- **HOST** — Agent 360 synthesis, ~4 weeks out.
- **Someone (unclear who)** — #1636 (filed 08-15); #1647 (filed 08-18).
