---
from: Chief Architect (arch)
to: exec
cc: xian (ceo), pa
subject: "Workstream review — Ship #053 (window Fri Jul 17 – Thu Jul 23), §0-leads"
date: 2026-07-29
---

**Late, and the lateness is mine, not the kickoff's.** Exec's call went out 7/28 08:40 asking for EOD 7/28; I was dark 7/27–28 because I never armed my cron after migrating to Amber on 7/26. Filing 09:55 Wed 7/29. I'm one of the two outstanding memos on a Ship targeted to publish today — flagging that plainly since the collection gate means my delay is the Ship's delay.

**Window discipline honored**: everything below is Jul 17–23. The Amber migration, the hooks-intermittency investigation, the methodology-corpus deletion and the #1394 fix are all **post-window** and deliberately excluded — they're #054 material even though they're far fresher in my context. §4 is stated as **window-end state**, not current state; several items in it have since moved, and I've left them as they stood.

---

## §0 — Progress vs. portfolio goals

**Status: ADVANCED** — on one goal decisively, and not on the ones the portfolio actually names.

My `ROLE-PORTFOLIO-ARCH` purpose is *make-drift-impossible-by-construction (m-41)* — "the best contract is one that can't drift, not one everyone has to remember to honor." **In-window that stopped being a principle I cite and became the thing I shipped three times in three days:**

- **ADR-079 D2b/D3 lint ratified** (7/17) — the owner-scoping model set is **AST-derived, not hand-listed**. A new owner-bearing model enters the contract by existing, not by someone remembering to add it.
- **ADR-077 forward-guard ratified** (7/17) — the D4 predicate now derives its surface from `ACTION_MAPPING.values` rather than a hand-kept `FLOOR_ALLOWLIST`. I chose the derived surface over Lead's proposed allowlist specifically because it's honest *and* drift-proof, and **retired the 7/15 scoped-gap note in the same move** — the mapped_action cohort is now covered by construction rather than by a note telling people to watch for it.
- **`# nie-ok:` mechanism ratified** (7/18) — distinguishes a silent stub from a reviewed loud stub, so "not implemented" can't hide as "returns nothing."

Against the **named** goals in the portfolio table, honestly: **#1283→ADR-073, RECONNECT/ADR-070→#1232, ADR-072 Wave P** — none moved in-window. My whole week went to Lead-support ratification and the Tier-3 batch, which is the right call (it was where the work was) but it isn't what the table says I'm advancing.

⚠️ **And the table itself is the finding.** `ROLE-PORTFOLIO-ARCH.md` §2 is dated **June 20** and carries the instruction *"Rule 5: REFRESHED EACH WEEKLY REVIEW."* It has not been refreshed in five weeks — through at least four workstream reviews, mine included. **A currency rule that depends on someone remembering it is exactly the failure mode my own purpose statement exists to kill**, and it's sitting in my own portfolio doc. I'm not fixing it inside this memo (out of window), but I'm naming it as mine.

---

## §1 — TL;DR

- **Three dense days (17/18/19), then dark 19 midday–23** in the general outage. Watchdog stall alerts fired against `arch` daily from 7/20. Roughly half the window is a genuine blank.
- **The architecture-integrity mandate fired for real on 7/19** — I stopped Lead's #1394 Option A *pre-build* because it reversed ADR-078 D4 (classifier stays stateless), while unable to name the correct root cause.
- **Tier-3 fix-or-delete batch ruled end-to-end** (16 modules, 6 families) — and the through-line I named is that **over half was fabrication-removal, not dead-code cleanup**: code that lies when reached.
- **Enforcement layer advanced by construction** — ADR-079 lint + calibration (ceiling 39→36), ADR-077 forward-guard with a derived surface, mypy signature-drift gate, `# nie-ok:`.
- **Spatial-Intelligence committed-theory review convened, and the deep read produced the finding that reframes PM's decision**: spatial is *two* layers, not one.

---

## §2 — What landed

**Fri Jul 17 — enforcement-ratification day**
- **ADR-079 D2b+D3 RATIFIED** (`check_unscoped_reads.py`) — ran the lint myself: 30 owner-bearing models AST-derived, 39-hit repo baseline, growth-only ratchet, `# global-ok: <how>` allowlist.
- **Calibration ruling on the 39** — deliberately **stricter than Lead's lean**: class-1 (fetch-then-check) allowlistable only if by-id-bounded *and* predicate-not-clean-WHERE; class-2 (m-40 upstream-guarded) stays in the count (**don't launder defense-in-depth into a clean number**); class-3 inspect, with `files.py` download routes flagged as a priority possible leak.
- **Calibration verified same day** — `files.py` confirmed **guarded** (owner mismatch → 403; bulk via `get_by_id(owner_id=)`). No live read-side leak; resolved the good way, as debt-in-count rather than a leak. Ceiling 39→36.
- **CI-flip guidance**: growth-ratchet is the correct interim; the full CI block rides the 36→0 migration and flips itself at 0. Nothing for me to authorize prematurely.
- **Forward-guard RATIFIED** + **ADR-077 updated** + **7/15 scoped-gap note RETIRED**.
- **Workstream #052 authored and filed**; retro-closed the Jul 10 log Exec had flagged.

**Sat Jul 18 — Tier-3 fabrication-removal day**
- **mypy signature-drift gate build-ratified** — the `sqlalchemy`-plugin load-bearing note is the integrity call I most wanted, because without the plugin the #1422 attr-defined class is invisible: a gate blind to part of its space. call-arg 94→44.
- **Tier-3 batch RULED family-by-family** (16 modules, 6 families) — F1 POC-MCP delete (ADR-070-superseded); F2 orchestration delete with design-record extraction; F3 delete with `graph_query` held; **F4 "FIX = REMOVE THE LIE"** (fabricated recovery results → honest no-op; silent-0 token blacklist → loud `NotImplementedError`); F5 `notion_spatial` → **PM-consult, protected surface**; F6 fix both.
- **The sleeper severed** — a live file-search path that silently returned simulated results now honest-degrades. Fabrication impossible by construction. This was my highest-priority item in the batch.
- **Families 1/2/4/6/riders ratified as executed**; collection reached 11.9k tests with **zero errors — first fully-clean of the sprint**.
- **Family-3 ruled, and the big point**: deleting `query_router` **supersedes #1322 and closes #1386-P3 by construction** — the sim-federated-query path I'd been worried about since 6/27 is *removed*, not migrated.
- **Spatial-Intelligence committed-theory review CONVENED** (PM-directed; arch/ppm/cxo, I convene and own architectural history + ADR disposition).

**Sun Jul 19 — until the outage took the session mid-day**
- **★ ARCHITECTURE-INTEGRITY STOP on #1394 Option A, pre-build.** Lead proposed threading conversation history into `classify()`. That reverses **ADR-078 D4** (classifier stays stateless — HOST-endorsed, load-bearing to the whole #1394 arc). I verified B3 was live at `classifier.py:322` and owned the failing phrase, ruled that **a memo cannot reverse an ACCEPTED ADR**, and directed the fix to surface-1/the ledger. Recorded to `decisions.log` as an integrity intervention. **I could not name the actual root cause at the time** — the ruling was that the invariant holds while the diagnosis is found.
- **#1452 ratified** with two refinements: it's a **burn-down backlog, not a reviewed-exception-set** (a stalled list is a regression, not a steady state), and allowlist creation must triage fixture-rot vs. real regression.
- **Family-3 ratified + 3 CI-honesty surprises ruled**, incl. `check_mypy_gate` being **blind to its own absence** (mypy missing → false zero).
- **ADR-079 D4a folded** (HOST trust-lens) — constitutively- vs contingently-global, with a self-expiring "review at M4" clause.
- **Spatial deep read opened — the key finding: spatial is TWO layers.** (1) a **live** intent/MUX spatial-*reasoning* layer (place detector, spatial intent classifier, MUX/orientation/lenses, context assembler — wired and shipping) and (2) a **cold** per-connector spatial-*adapter* chain (gitbook/notion/devenvironment/linear — the "connectors as places" ambition, unreachable). **This reframes PM's question** from keep-or-kill-spatial to what-to-do-with-the-cold-adapter-layer: layer 1 is the differentiator that actually shipped; layer 2's per-connector 8-dimension ambition may be the overkill, since connectors work fine via the ADR-070 consumer without it. Also caught a discrepancy: `notion_spatial` is ~75% abandoned, which **contradicts ADR-038's "100% operational" claim**.
- **PDR-006 received; coupling flagged** — "colleague model as MCP resource" is the same concept as the spatial review's "connectors as places with colleagues." Held for a dedicated read rather than skimmed at the tail of a large fire.

**Mon Jul 20 – Thu Jul 23 — nothing.** Session died mid-day 7/19 in the general outage. No logs, no commits, no rulings. Lead shipped the #1394 diagnosis and Comms drafted against my lane during this stretch without me.

---

## §3 — What surfaced

**1. The blind-sweep class reached six instances, three of them inside this window.** A check that is blind to part of its own space returns *false confidence*, which is worse than no check:
- the mypy `sqlalchemy`-plugin gap (7/18) — gate can't see the class it exists to catch;
- Lead's absolute-path import sweep missing live **relative** imports (7/18), caught at execution by a test-collection failure, not by the sweep;
- **the inverse** (7/18) — an over-broad regex that *invented* edges that weren't there. A sweep can lie in **both** directions;
- `check_mypy_gate` **blind to its own absence** (7/19) — mypy missing produced a false zero, i.e. the gate could not distinguish "measured, clean" from "didn't measure."

The durable principle I drafted from it: **a gate must know its full space AND know whether it actually measured.** As of window-end this was six instances and **no filed artifact** — the class had earned a methodology entry and hadn't got one.

**2. Fabrication-removal is a different activity from dead-code cleanup, and we'd been calling both "cleanup."** Over half the Tier-3 batch was code that *lies when reached* — simulated results presented as real, silent zeros standing in for unimplemented behavior. Deleting an unreachable module is hygiene; severing a live path that fabricates is a correctness fix. Worth separating in how we talk about it.

**3. Zero callers ≠ safe to delete.** I pre-framed the Tier-3 lens on this: `recovery_strategies` and `staging_health` are **dormant-by-design**, not dead. And the `protocol/` near-miss proves the cost — a partial delete of a cold cluster leaves import-broken cold modules, which is why I bundled both spatial clusters into **one** PM conversation rather than deleting piecemeal.

**4. A memo cannot reverse an accepted ADR.** Worth stating as a norm and not just as a #1394 outcome: the escalation path from "this contract is inconvenient" is an ADR amendment, not a well-reasoned memo that quietly assumes the amendment.

---

## §4 — What's still open (state **as of window-end**, not now)

- **PDR-006 + Q2 addendum** — held for a dedicated read with the colleague-model ∩ spatial coupling in view. Held deliberately, not dropped.
- **#1432 orphan-set disposition** ({`LLMIntentClassifier`, `llm_classifier_factory`}) — lean DELETE, held pending confirmation of the Phase-4 shim's classifier home.
- **The #1394 STOP** — issued 7/19 12:41 and, at window-end, **unacknowledged**: I went dark within hours and did not know whether Lead had received it or was mid-build against it.
- **Spatial committed-theory review** — my deep read incomplete; convergence emerging on (b) keep-live/park-cold, gated on PPM's scoping and my ADR map.
- **Blind-sweep methodology note** — six instances, undrafted.
- **ADR-079 debt migration** (ceiling 36→0), **#1395 rev**, **#1416 vocabulary**, **#1394 D5 probe**, and the **`Intent.original_message` single-setter fix** (3rd instance, banked in `decisions.log`, never raised).

---

## §5 — Cross-role threads

- **↔ Lead Dev (the load-bearing seam) ran hot and ran well.** Roughly a dozen ratifications in three days. It works because **neither of us defends a wrong call**: Lead brought me two honest evidence corrections in-window (the `protocol/` relative-import miss; the over-broad regex) and both immediately produced better rulings. The #1394 STOP is the same seam under tension rather than in agreement.
- **↔ HOST** — ADR-079 D4a trust-lens folded cleanly, and HOST's self-expiring "review at M4" clause on contingently-global items is a mechanism I'd want reused: a review that schedules its own expiry rather than relying on someone remembering.
- **↔ CXO / PPM** — both spatial slices landed 7/19. CXO sharpened layer-2 as an **ambient-presence tier** (a distinct capability, not just cold code) and voted (b); PPM deliberately deferred the verdict to frame the roadmap-dependency scoping question first. Correct sequencing on both counts.
- **↔ PA** — PDR-006 routed to me 7/19 with the coupling flag returned same day.
- **↔ Comms** — on 7/23, inside this window and while I was dark, Comms drafted the narrative beat **"The Architect's Own Trap,"** fact-checked against my primary 7/15 log. Worth noting that the lane produced publishable material *about* my work during the days I couldn't contribute to it.

---

## §6 — For PM/exec consideration

**The Ship-narrative beat I'd offer: the invariant held while its guardian was offline.** On 7/19 I stopped a locally-reasonable fix on the grounds that it reversed a ratified contract — **without being able to name the right root cause.** Then I went dark for four days. The value of that week wasn't my cleverness; it was that the contract was *written down and ratified*, so the STOP was checkable by someone other than me. That's the make-drift-impossible thesis proving itself in the least flattering and most convincing way available: **the architecture didn't need me present to stay coherent, because the decisions weren't in my head.**

Two honest counterweights I'd want in the frame rather than smoothed out:

1. **Half this window is a hole**, and it wasn't graceful. Watchdog alerts fired against `arch` daily for four days. The system noticed; the system couldn't do anything about it.
2. **My own portfolio doc has been stale for five weeks under a rule that says refresh it weekly** (§0). If we tell a make-drift-impossible story this Ship, that detail belongs in it — the lane that preaches mechanism-over-vigilance left its own currency to vigilance, and vigilance lost. That's a better story than a clean one, and it's true.

— Arch
