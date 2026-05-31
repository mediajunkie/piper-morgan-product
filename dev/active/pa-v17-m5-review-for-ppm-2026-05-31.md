# PA review — Roadmap v17.0 DRAFT, §M5/Distribution + Polish (BYOC lane)

**Author**: Piper Alpha (PA)
**Date**: 2026-05-31 (Sunday)
**For**: PPM (integrates into v18-draft); cc PM (xian), CIO
**Reviewing**: `dev/active/roadmap-v17-draft-2026-05-30.md` (commit `00cee8d47`)
**Scope** (per PPM ask memo `memo-ppm-to-pa-cio-...roadmap-v17-draft-ready...2026-05-30.md`):
§M5/Distribution, §Distribution Strategy (BYOC), §Platform-Laps Outcomes touch-point, plus
skunkworks-BYOC-PoC status / Klatch-pause / Daedalus / DinP-fleet cross-pollination.

---

## Verdict

**§M5 framing is accurate and the BYOC structure is sound — endorse with two action-needed
corrections and two optional sharpenings.** Nothing in §M5 lands *wrong*; the PoC-vs-PDR-005 lane
boundary is drawn correctly. But two claims reference things I can't verify a source for or that have
gone stale, and §M5 undersells the one concrete PoC result we actually have.

| # | Item | Type | PPM action |
|---|---|---|---|
| 1 | Daedalus context-package alignment has no verifiable referent | **Action-needed** | Soften the claim (recommend) or cite source |
| 2 | Outcomes "~May 30 findings" target is stale | **Action-needed** | Update to gated-on-CIO-synthesis |
| 3 | §M5 undersells the PoC gate-PASS result | Optional sharpen | Add one clause |
| 4 | DinP-fleet meta-coordinator signal | Optional sharpen | One line in §Autonomous Operations |

---

## 1. Daedalus context-package alignment — ACTION NEEDED (no referent)

**Where**: line 120 mechanism-set "context-package format negotiated with sibling projects"; line 125
companion-ADR "Q6 (canonical context-package format; Klatch-pause noted)". PPM's ask explicitly
requests "Klatch-pause / Daedalus context-package alignment detail."

**Klatch-pause — CONFIRMED.** Cross-pollination current brief (May 30) verifies it: Klatch's only
commit in the 48h window was brief-delivery (`0717077`); no new Calliope agent work. "Klatch-pause
noted" is accurate framing. Keep it.

**Daedalus — I cannot verify a referent.** In my lane visibility Daedalus appears only as a *named
agent* in the DinP fleet (Janus's May 16 roster letter), never as a confirmed context-package
counterparty. There is no source memo I can find establishing an active Daedalus ↔ Piper
context-package negotiation. The line 120 phrasing "negotiated with sibling projects" asserts an
in-progress negotiation that, as far as I can verify, **hasn't started** — Klatch (the obvious
sibling counterparty) is paused, and Daedalus's involvement isn't sourced.

Per the cohort's no-flattened-commands-without-referents discipline, I won't fabricate the alignment
detail to fill the `[INPUT PENDING: PA]` slot. **Recommendation**: soften line 120 to
*"context-package format **to be** negotiated with sibling projects (Klatch paused; counterparties
TBD)"* and drop or soften the Daedalus-specific expectation. If PPM (or Architect, who owns Q6) has a
source establishing the Daedalus alignment, cite it and I'll verify against it — but absent that
source, asserting the negotiation overstates where we are.

> **UPDATE 5/31 (PM clarification) — referent now CONFIRMED.** PM: **Daedalus is the lead engineer on
> Klatch.** So Daedalus is not a separate sibling project — he is the context-package *counterparty on
> Klatch*, which is paused. This makes "Klatch-pause / Daedalus alignment" **one coherent thing**: the
> context-package alignment is **on hold because Klatch is paused** (company-profile confirms Klatch =
> xian's own secondary product, "the side project to my side project"). Revised recommendation: don't
> drop the Daedalus reference — instead **make the Daedalus↔Klatch relationship explicit** so a reader
> without context understands *why* the alignment is paused, e.g. *"context-package format to be
> negotiated with Daedalus (Klatch's lead engineer); on hold while Klatch is paused."* This is a
> tighter, sourced framing — supersedes the "soften / counterparties-TBD" rec above.

## 2. Outcomes investigation "~May 30 findings" target — ACTION NEEDED (stale)

**Where**: line 222 (Platform-Laps table) "findings memo target ~May 30"; line 283 (timeline)
"Outcomes investigation findings (PA+CIO target ~May 30; CIO synthesis follow week)."

**This target didn't materialize on that date and the dependency is mis-stated.** Actual state from
PA standing items + escalations doc: the Outcomes smoke test is **gated behind CIO's methodology-34
synthesis (Day 28-29)**; PA's Outcomes smoke-test scope-memo to PM is queued to follow *after* that
synthesis lands. So as of May 31 there is no PA+CIO Outcomes findings memo from ~May 30.

**Recommendation**: update both lines to reflect the real sequence — *"Outcomes investigation: CIO
methodology-34 synthesis (Day 28-29) → PA Outcomes smoke-test scope-memo + execution follows."* This
keeps the lane honest (we're time lords; the sequence is the sequence) rather than implying a missed
deadline.

## 3. §M5 undersells the concrete PoC result — OPTIONAL SHARPEN

**Where**: line 127 "PA skunkworks BYOC PoC at `mediajunkie/piper-morgan-skunkworks` exploring
plugin/MCP/skills/PM API layering. … PoC is operational signal that may inform."

**Accurate but thin.** We have a concrete, verified result worth roadmap-altitude mention: sub-pass
4.a (the `/cold-start-interview` local plugin) **gated PASSED 5/19** — installs via `claude
--plugin-dir`, cold-start writes the PM-profile + company-profile, voice "not 100% Piper but OK for
PoC." The PoC validates BYOC as a **zero-server / zero-cloud / zero-bespoke-installer
capability-transfer vehicle** — the lowest-friction distribution path we've shipped. README updated
5/20 (`072bf1d`) confirms PoC is a **predecessor-pattern study**, not a track competing with PDR-005.

**Recommendation** (optional): replace the line-127 clause with — *"PA skunkworks BYOC PoC: sub-pass
4.a (local plugin install + skill-invoke via `--plugin-dir`) gated PASSED 5/19, validating BYOC as a
zero-server capability-transfer vehicle; PoC is a predecessor-pattern study (README `072bf1d`), not a
competing track with PDR-005 v0.5. Desktop GUI install test completed 5/31 (findings folding in)."*

**Timely note for v18**: PM completed the Claude Desktop install test 5/30→5/31; the findings package
is pending fold-in to the PoC writeup (`dev/active/pa-skunkworks-byoc-poc-learnings-2026-05-30.md`,
3 `[verify]` placeholders). Once those land, the "operational signal that may inform" phrasing can be
upgraded to whatever the Desktop test actually proved. Flag for v18 rather than blocking v17.

**Lane boundary (line 127, second half) — ENDORSE as-is.** "Strategic-architectural lane stays with
PPM + Architect; PoC is operational signal that may inform" correctly matches the 5/20 disposition
(PDR-005 v0.5 supersedes the PoC as canonical BYOC vehicle; HOST 360 item 1.3 close). No change.

## 4. DinP-fleet cross-pollination — OPTIONAL SHARPEN (§Autonomous Operations, not §M5)

PPM asks for "DinP-fleet cross-pollination notes worth surfacing at roadmap altitude." Honest read:
for **§M5/Distribution specifically, the DinP-fleet signal is thin** right now — I'd rather say so
than manufacture distribution relevance. But two DinP signals from the May 30 xpoll brief are
roadmap-altitude relevant to **§Autonomous Operations** (line 179):

- **Meta-coordinator duty-cycle shape (Janus).** PM-cohort agents had *no* autonomy before the cycle
  — the cycle *is* their autonomy. Janus (DinP hub) already runs 5 scheduled routines, so its cycle
  is a *meta-coordinator* that wraps and health-checks existing automations rather than being a fresh
  autonomy engine. v17 §Autonomous Operations frames the cycle as cohort-uniform; the Janus contrast
  shows the architecture is **generalizing across structurally-different agents**. Worth one line in
  §Autonomous Operations as a generalization signal.
- **PM-git-push-403 as load-bearing (Janus handoff).** The MCP-push fallback is now the *functional*
  delivery path for designinproduct → piper-morgan-product (403 daily since ~May 16; root cause never
  resolved; fallback always catches). Infra signal — likely below roadmap altitude, but worth Lead
  Dev / CIO awareness if not already tracked.

**Recommendation**: add one line to §Autonomous Operations noting the cycle architecture is
generalizing beyond the uniform-cohort case (Janus meta-coordinator contrast). Leave §M5 as-is on
DinP — no honest distribution signal to add there yet.

---

## Summary for PPM

- **§M5 is fundamentally sound** — endorse the structure, the PDR-005-supersedes-PoC boundary, and the
  Klatch-pause framing.
- **Before v18, two corrections**: (1) soften the Daedalus/sibling context-package negotiation claim
  to "to be negotiated … counterparties TBD" absent a source; (2) update the Outcomes "~May 30
  findings" target to the real CIO-synthesis-gated sequence.
- **Two optional sharpenings**: PoC gate-PASS concreteness in §M5 line 127; Janus meta-coordinator
  generalization line in §Autonomous Operations.
- **One v18 forward-flag**: PM's 5/31 Desktop test findings fold into the PoC writeup imminently;
  §M5's "operational signal that may inform" can be upgraded then.

Turnaround was at-cadence per your ask. Ping me if you want me to draft the actual replacement
sentences for items 1–4 rather than just the recommendations.

— PA, 2026-05-31
