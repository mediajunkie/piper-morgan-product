---
name: cohort-attention-rollup
description: >
  Compile the cohort duty-cycle attention docs into a single, skimmable HTML
  rollup for the PM/CEO — what needs a decision, what's drift-worth-knowing,
  what's clean — with a live-state verification pass so the board reflects NOW,
  not a stale snapshot. Use when PM asks for the attention dashboard / rollup, on
  a duty-cycle fire that owns the rollup, or any time the cohort's open PM items
  need a single-glance summary. Originally a PA prototype; maintained by the
  Chief of Staff (Exec) as part of the org-attention oversight lane.
argument-hint: "[--date YYYY-MM-DD if compiling for a date other than today]"
---

# cohort-attention-rollup

A single-glance HTML board of everything across the agent cohort that touches the PM/CEO's attention,
sorted by whether it needs a **decision**, is **drift worth knowing**, or is **clean**. The value is two
things at once: (1) it collapses N scattered attention docs into one skimmable page, and (2) it does a
**live-state verification pass** so a decision the PM already made doesn't keep showing as "open" just
because some role's doc is stale.

> **Provenance / lane.** Built as a PA (product-assistant) prototype. Maintained by the **Chief of Staff
> (Exec)** as part of org-attention oversight — cohort-wide bottleneck synthesis is Exec's lane (same
> family as the Weekly Ship synthesis), not the product-assistant lane. Adapt the shape to your working
> approach; the sections below are the prototype, not a straitjacket.

## When to use

- PM asks for "the attention dashboard," "the rollup," "what needs my attention."
- A duty-cycle fire that owns this artifact (Exec's cycle) reaches a compile point.
- Any time the cohort's open PM-facing items would benefit from a single-glance board.

> **Who runs this.** Currently Exec (handoff from PA, 2026-06-06). The "On your plate" section's *content* is role-specific (Exec uses it for org-level items; PA used it for product-assistant threads) but the *header pattern* — "whatever's on the compiler's own plate that PM should see" — generalizes across compilers. If the role shifts again, adapt freely.

## Delivery + cadence (PM-ratified 2026-06-13)

**Delivery — render it as an inline widget, not (just) a saved file.** The board mounts directly in the Code surface via the visualize `show_widget` MCP: call `mcp__visualize__read_me` with `["data_viz","interactive"]` first for the design system, then `mcp__visualize__show_widget`. This is the durable answer to "how do I surface an HTML view to PM in the Code surface" — *render it as a widget.* Do NOT rely on `SendUserFile` (delivers a download chip, not a view) or the Desktop dev-server preview pane (it is server-backed — a static doc needs a server behind it, and its "Set up" button injects dev-server prompts). **Reusable by ANY agent with the visualize MCP** — this is the cohort-general "mount a dashboard/report for PM" capability PM was after.

Widget discipline (from the read_me): CSS variables for every color (auto light/dark), sentence case, Tabler **outline** icons (no emoji), 0.5px borders + `--border-radius-lg` cards, font-weights 400/500 only, and **no titles/prose inside the widget** (orientation goes in the response text). Proven structure: three summary metric cards (needs-you / in-flight / clean) → "needs your decision" cards each with a `sendPrompt('discuss …')` button so PM can click to drill in → "in flight · for awareness" rows → "clean · no action" rows. Lead with a visually-hidden `<h2 class="sr-only">` summary.

**Cadence (PM 2026-06-13):**
- **At START** — each day's first PM-present engagement renders the current board.
- **On discuss** — any time PM and Exec are in conversation, refresh (re-render) the board *incrementally* from new memos / other information since the last render. If nothing board-relevant changed, **say so rather than re-render an identical board.**
- Keep the underlying board **data** current via the duty cycle so any render is fresh.

**Persistent-pane option — CONFIRMED (PA + CIO live investigation, 6/14).** PM also values a persistent Desktop preview-pane view (re-openable, glanceable). **The technique: write the board as a self-contained static `.html` in the worktree** — a full doc (DOCTYPE/html/head/body), inline CSS, no external deps, no fetch/server. Writing or editing it triggers Claude Desktop to **auto-surface it in PM's Launch preview panel** (a PostToolUse note confirms "X.html is now visible in the Launch preview panel"); PM opens with cmd-shift-P and it persists + re-opens. **Two traps to avoid:** do NOT create a `.claude/launch.json` (triggers server-backed preview mode → port-in-use errors + prompt injection), and do NOT use `SendUserFile` (delivers a download chip, not the pane). Evidence: `cohort-plan-of-record-2026-06-12.html` (CIO's). Worked example: `dev/active/exec-attention-board.html` (Exec's, 6/14).

So the board now has **two surfaces, pick by the moment:** (1) inline `show_widget` — transient, in-chat, themed + interactive (good for a one-shot "show me the board"); (2) static `.html` in the worktree — persistent, glanceable in the preview pane (good for a standing surface PM keeps open). Same content, two deliveries.

## Step 1 — Gather the source set

**The per-role `duty-cycle-escalations-{role}.md` docs are DEPRECATED (folded 2026-06-17, skill v1.13) — do NOT use them as a source; they're frozen/stale by definition now.** The canonical inputs post-fold:

1. **Per-role carry-forwards** — `dev/active/{role}-carry-forward.md` — the residual home for non-blocking PM-attention items (read + rewritten every substantive fire by each role, so they don't rot the way the old docs did). List: `ls dev/active/*-carry-forward.md`.
2. **GitHub** — live-verify every candidate (the half-reason the docs were foldable: re-derive truth rather than trust a doc).
3. **Blocker mail** — your exec inbox + cc'd blocker memos (the active-memo-the-gate path — blockers ride mail, not docs; see the Blocker bucket in Step 3).

Read the carry-forwards. Each is that role's self-reported view of what (if anything) needs PM
attention. **Treat them as perspectives, not ground truth** — they can be stale (a role may not have
refreshed since its last fire). That's exactly what Step 2 corrects.

Secondary inputs worth a glance for completeness: the session-start hook's staleness flags
(BRIEFING-CURRENT-STATE, cross-pollination brief, `dev/active/` bloat), recent ratifications the PM made
in-conversation, and any mailbox items explicitly addressed to PM that assign a decision.

## Step 2 — Live-state verification pass (the discipline that makes this trustworthy)

For every candidate "decision awaiting PM" item, **verify it's actually still open** before listing it:

- If it cites a GitHub issue/PR, check current state (`gh issue view <n> --json state,title` or the GitHub
  MCP). A "needs your call on #X" that's already closed is resolved, not open.
- If it cites a ratification/decision (a roadmap version, a PDR, an ADR), check whether the PM already
  ratified it (recent session logs, mailbox, or ask). A role's doc listing it "open" doesn't mean it is.
- Note the freshness of each source doc; if a doc is days stale, say so rather than presenting its
  contents as current.

This is what separates a useful board from a stale aggregation. The footer should state explicitly that
this was a live-state pass and what was verified.

> **No silent failures.** If you can't verify an item (no GitHub access, ambiguous referent), list it but
> mark it "unverified" — don't present an unverified item as confirmed-open, and don't silently drop it.

## Step 3 — Triage into buckets

Sort every item into one of these, by what it asks of the PM (priority order — **blockers first, always at the top**):

- **🛑 Blocker** — work that is STUCK until someone acts. **Renders at the TOP of the board, above everything else** (PM 2026-06-17: *"blockers should be at the top of my attention list"*). **Source**: blockers arrive via **active mail — a role memos the gating role, cc Exec** (the memo-the-gate discipline), NOT the per-role `duty-cycle-escalations-{role}.md` docs — those are scoped to *non-blocking* PM-input by construction (a 2026-06-17 finding: the rollup never carried blockers because the docs exclude them). So for this bucket, sweep your **exec inbox + cc'd blocker memos**, not just the attention docs. If none after the sweep, render "no blocked work" — but the section is always first.
- **🔴 Decision** — needs the PM's call (the work isn't necessarily stuck). (If none after verification, say so loudly — an empty decision queue is a feature, not an empty section.)
- **🟡 Drift / awareness** — worth knowing, no decision required (staleness flags, a role's cron not
  registered, an FYI).
- **⚪ Clean** — roles with no open PM item; one compact line each.
- **✅ Resolved since last board** — recently-closed decisions, struck through. Shows momentum and
  prevents "didn't I already decide that?" confusion.
- **📋 On your plate (non-cohort)** — *optional, adapt to your role.* In the PA prototype this surfaced
  the compiler's own threads with PM. Exec may repurpose this as org-level items, or drop it.

## Step 4 — Render the HTML

Write a self-contained HTML file (inline CSS, no external deps) using this template. Keep the severity
color-coding and the legend — they carry the at-a-glance meaning.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cohort Attention Rollup — {DATE}</title>
<style>
  :root { --bg:#fafafa; --card:#fff; --line:#e2e2e2; --ink:#1a1a1a; --mute:#6b6b6b;
          --red:#c0392b; --amber:#b7791f; --grey:#8a8a8a; --green:#2d7a3e; --link:#1a5fb4; }
  body { font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
         color:var(--ink); background:var(--bg); margin:0; padding:2rem 1.25rem; }
  .wrap { max-width:820px; margin:0 auto; }
  h1 { font-size:1.5rem; margin:0 0 .25rem; }
  .meta { color:var(--mute); font-size:.85rem; margin:0 0 1.25rem; }
  .legend { font-size:.8rem; color:var(--mute); margin:.5rem 0 1.5rem; }
  .legend span { margin-right:1rem; white-space:nowrap; }
  h2 { font-size:1.05rem; margin:1.75rem 0 .6rem; padding-bottom:.3rem; border-bottom:2px solid var(--line); }
  .item { background:var(--card); border:1px solid var(--line); border-left:4px solid var(--grey);
          border-radius:6px; padding:.7rem .9rem; margin:.55rem 0; }
  .item.drift { border-left-color:var(--amber); }
  .item.clear { border-left-color:var(--green); }
  .item .top { display:flex; align-items:baseline; gap:.5rem; flex-wrap:wrap; }
  .agent { font-weight:700; }
  .sev { font-size:.7rem; text-transform:uppercase; letter-spacing:.04em; padding:.1rem .4rem;
         border-radius:4px; background:#eee; color:#444; }
  .sev.drift { background:#fdf3e2; color:var(--amber); }
  .summary { margin:.35rem 0 .3rem; }
  .links a { color:var(--link); text-decoration:none; font-size:.82rem; margin-right:.9rem; }
  .links a:hover { text-decoration:underline; }
  .clean { color:var(--mute); font-size:.9rem; }
  .clean b { color:var(--ink); }
  .bigclear { font-size:1.05rem; color:var(--green); font-weight:600; }
  .resolved { font-size:.82rem; color:var(--mute); margin-top:.4rem; }
  .resolved s { color:#aaa; }
  footer { margin-top:2rem; padding-top:1rem; border-top:1px solid var(--line);
           color:var(--mute); font-size:.8rem; }
</style>
</head>
<body>
<div class="wrap">
  <h1>Cohort Attention Rollup</h1>
  <p class="meta">Compiled by {ROLE} · <b>{DATE TIME}</b> · live-state pass · source: {N} duty-cycle attention docs</p>
  <p class="legend">
    <span>🛑 <b>Blocker</b> — work stuck (TOP)</span>
    <span>🔴 <b>Decision</b> — needs your call</span>
    <span>🟡 <b>Drift/awareness</b> — worth knowing, no decision</span>
    <span>⚪ <b>Clean</b> — no open PM item</span>
  </p>

  <h2>🛑 Blockers — work that's stuck (always FIRST)</h2>
  <!-- one .item (red border-left) per blocker, sourced from exec-cc'd blocker memos (NOT the non-blocking attention docs); if none: <div class="item clear"><p class="bigclear">✅ No blocked work right now.</p></div> -->

  <h2>🔴 Decisions awaiting you</h2>
  <!-- one .item per decision; if none: <div class="item clear"><p class="bigclear">✅ Nothing currently needs your decision.</p></div> -->

  <h2>🟡 Drift / awareness — no decision, worth knowing</h2>
  <!-- one .item.drift per item: agent name + sev chip + summary + links to the source doc -->

  <h2>⚪ Clean — no open PM item</h2>
  <!-- one .item with a .clean block: one line per clean role + link to its doc -->

  <h2>✅ Resolved since the last board</h2>
  <!-- one .item with .resolved: struck-through decisions recently closed -->

  <footer>
    <b>Bottom line in one sentence.</b><br><br>
    Live-state pass — note what was verified (e.g. "checked #X against GitHub, confirmed PDR-005 ratification") so the board reflects now, not a stale snapshot.
  </footer>
</div>
</body>
</html>
```

## Step 5 — Write and deliver

- Write to `dev/active/{role}-cohort-attention-rollup-{DATE}.html` (e.g. `exec-cohort-attention-rollup-2026-06-10.html`).
- Commit it (per the repo's commit/sign-off discipline).
- Surface it to PM with an **absolute clickable path** so it opens in the Desktop file panel without a
  context shift. A one-line chat summary ("decision queue empty; 2 awareness items") plus the path is
  the right delivery — the page is the detail, the chat line is the headline.

## Notes for the maintaining role

- **Cadence**: this is a compile-on-demand / compile-on-fire artifact, not a continuous one. Daily during
  active cohort weeks; on request otherwise.
- **The live-state pass is the whole point.** A rollup that just concatenates the role docs without
  verifying inherits all their staleness. Budget the verification time.
- **Future automation** (noted in the prototype's footer): auto-stale-flagging + live-GitHub-verify
  (coordinated with CIO) would make the verification pass mechanical rather than manual.
- **Adapt freely.** The "On your plate (non-cohort)" section, the exact role list, and the cadence are
  starting points. Shape them to how org-attention oversight actually works in your cycle.
