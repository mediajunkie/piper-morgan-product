# Lead carry-forward — rewritten 2026-08-11 ~16:2x PT (supersedes 08-10 21:50; cron-prompt blurbs are stale by construction)

## Live state
- ✅ **NINTH CUT DEPLOYED 08-11 16:0x on PM's word — Fly v49**, machine on version 49, started, 1/1 checks; app-level `/health` 200 with `intent_service: healthy`. Verified zero application-code drift between the staged `31a09b331` and the deployed `ad8c079e8` (only 3 helper scripts). **Awaiting PM's retest verdicts on #1589/#1590** — start a fresh conversation. Contained #1589 (greeting can't claim emptiness from a read that can't establish it; synthetic whole-day free-blocks never render) + #1590 (#1314's default-repo helper was OAuth-callback-only → every GitHub read returned empty for pre-07-04 accounts; resolver now self-heals at read time). Fly is at **v48**, machine started, 1/1 checks.
- **Amber rebooted 08-11 ~07:30** (macOS 26.6). Session resumed intact; cron re-armed as **`2a4809de`** (new 7-day expiry ~08-18 — every pre-reboot expiry date in the registry is now stale).
- **08-12 is a skeleton-crew day**: weekly usage limit hit 08-11 evening; PM logged Lead + Exec into the designinproduct.com account (resets tonight). Token budget generous per PM.
- ⚠️ **CLAUDE.md's "Amber keychain entries ABSENT" block is now STALE** — conftest loads real anthropic/openai keys from the keychain (verified 08-12). Consequence: llm/e2e tests that used to auto-skip now really run. Flag for a correction pass on the shared block.
- 🔴 **Docker data services do NOT survive a reboot** — postgres/redis/chromadb were all `Exited(255)` 6h after, nothing restarted them, nothing alerts. Restarted; filed **#1594** (Ongoing). After any host reboot: `docker compose up -d postgres redis chromadb` before assuming dev works.

## Awaiting PM (decisions, not work)
- ~~Deploy word for the ninth cut~~ ✅ **GIVEN + SHIPPED 08-11 (v49).** Now awaiting **retest verdicts** on #1589/#1590.
- **Sprint field for #1595** (the Inversion epic) — deliberately left unset; Sprint changes are PM-gated and I won't infer one, even for the MVP spine.
- ✅ ~~#1510 fork~~ **RULED (PM via Exec 08-13) + MECHANISM BUILT** (`836c5a188`): infer → read-back at low confidence → store on verify; meta-feedback its own channel. **Next: wire the consumers** — #1591 preference capture (PPM's spec governs UX), then #1509. PM's live mode-flip test still open on #1510.
- **#1190** — close/reopen DESTRUCTIVE threshold word (question is on the issue).
- Post-deploy verdicts on the amber ledger rows.

## 🔴 TOP OF QUEUE — PM-gated
- ✅ ~~#1600 CI red~~ **CLOSED 08-12** — PM said "take #1600 next"; done. Green Architecture Enforcement run `31612409836` OBSERVED on main (first since 08-09). 3 mypy ceilings LOWERED (union_attr 209→172). Discovered: **#1602** (e2e one-shot after #1532, A/B/A-proven). Open mechanism question for PM/Exec: how does a red gating workflow persist unnoticed 2 days?
- ✅ ~~#1599~~ **migration BUILT + pushed 08-12** (revision `a1599admin`, targets username `dinp` — PM confirmed the beta login is username-based; the most-cited email would have been a silent zero-row match, #1599's own defect). Fail-loud on Fly release, warned no-op on fresh dev/CI DBs. **Takes effect at next deploy** → then PM's Slack app-token save (#1201) is the behavioral check. PM's production-era plan on the issue: separate admin account, username `xian`.

## Next build queue (unblocked, in order)
0. **#1608 CI liveness detector** — specced, small, Ongoing. Closes the #1600 mechanism question ("red nobody sees"); #1593's ratchet (SHIPPED+observed 08-12) is its companion shape. PM/Exec ratification of the mechanism is pending but the build is unblocked.
1. **#1595 Inversion Phase 0** — corpus baseline, per category. **Needs nothing from Arch; starts immediately.** Epic filed 08-11 with all four ratified decisions + both amendments as acceptance criteria. Then Phase 1 behind a flag (shadow-scored, routes logged not executed).
1b. **CUT STAGED (updated 08-14 morning)**: #1509 consent gate + the 1411/1617/1591 fix wave + **the 1605/1569 wiring (`e9ef395a1`, ratified copy verbatim)** — all on origin/main, awaiting PM's deploy word. PM retest list post-deploy: clarify-ask on 'status→Done' · default-repo phrasing works · interview tail releases (their 3 turns) · declaration stores + taught phrase routes · consent matrix behaviors. Closure pendings: PPM word on the 1591 teaching-line ×2 (morning change + evening switch-back phrase) · CXO copy pass on 1509's flagged seams · Arch's outwardness-axis word.
2. ~~Closure sweep~~ **DONE 08-11**. Of 16 candidates only **9 closed** — the caution was justified. Held open with findings: #1411 (PM's own gate unmet, no cut since the fix), #1431 (defect **reproduced at HEAD**: `"show me my archived projects"` → STATUS 1.0; the **`me` token** is the discriminator), #1485 (blocked by #1599), #1480 (client half verified by *grepping the JS* — wrong layer), #1423/#1436 (genuine slices). **MVP 51 → 48.**
3. **#1572** per-user timezone umbrella (supply is 0%; every user-typed clock time reads on the server's UTC clock).
4. #1423 / #1436 remaining slices; #1592 (Fly credentials.json ERROR noise).

## Tracker artifact — BRIDGE state (08-13 afternoon)
- PM's canonical tracker URL (fbb9edcf…) lives on the **pipermorgan.ai** account; today's designinproduct.com skeleton-crew login cannot update it. **Bridge artifact published**: https://claude.ai/code/artifact/4d78432f-f6d3-4a93-9992-219f88ee5e41 (from scratchpad copy `mvp-tracker-bridge.html`).
- **AFTER tonight's 10pm account switch back to pipermorgan.ai**: republish `dev/active/honest-mvp-ledger-2026-08-08.html` to the ORIGINAL URL (restores PM's bookmark), then mark the bridge superseded. The canonical file is on origin/main and current to v52.

## Standing
- **Milestone sequence: MVP → Production → Fast Follow.** "Not MVP" never defaults to Fast Follow — ask which of the two later steps. (Caught myself defaulting #1594 to Production on 08-11; it's Ongoing.)
- Moratorium on piecemeal routing fixes holds — failures → corpus (#1559, #1579, #1492, #1527, #1505 tagged). Handler-branch and rail-key fixes ARE sanctioned.
- Discovery rate is measured as **new-class rate**, not raw. ✅ **DONE 08-11**: `docs/internal/operations/failure-class-vocabulary.md` (16 product + 4 process families) and `scripts/discovery-rate.py` now computes it. Honest coverage today: **1 of 190 issues tagged** — forward-only, no back-filling (a class assigned retroactively by whoever wants the curve to bend is not evidence). Flagged to Exec that Sep 1 gives a thin window. **Remaining habit: add `Class:` at filing time.**
- Test-support artifacts require verify-first — never hand PM a command/seed/step without reading the schema/route/template it touches.

## ⚠️ Correction to my own prior carry-forward (found 08-11 reading Arch's ruling verbatim)
My 08-10 note said the floor-honesty contract's fabrication cases should ride the inversion's judge corpus "rather than building a second instrument." True, but it **flattened Arch's actual ruling and reversed its emphasis.** Arch ruled #1517 **DECOUPLED** from the inversion: it is a trust/safety defect, not a routing defect, it reproduces whenever the floor is reached however routing got there, and *"coupling it to a month-long rebuild leaves a live honesty defect waiting on an architecture bet."* **Spec now, ship against the CURRENT floor; the inversion ADOPTS rather than CONTAINS it.** One instrument eventually — but the fix must not wait for it. Reading my own summary instead of the ruling would have parked a live honesty defect behind a month-long build.

## Friction log (for next infra pass)
- Agent session logs collide on same-HHMM filenames; rebase flattens merge-resolution renames — consider an agent-id suffix in the log filename convention.
- Push races to `origin/main` are frequent when the fleet resumes together (3 rebase-and-retry cycles on 08-11 alone). `mail-send.sh` handles this automatically; plain `git push origin HEAD:main` does not.
