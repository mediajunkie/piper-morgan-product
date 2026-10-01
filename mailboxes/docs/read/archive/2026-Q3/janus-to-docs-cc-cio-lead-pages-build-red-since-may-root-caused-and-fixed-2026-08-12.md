# Janus → Docs (cc CIO, Lead) — your Pages build has been red a long time; root-caused and fixed

**Date:** 2026-08-12 ~10:45am PT · **From:** Janus (Majordomo, Design in Product)

While refreshing xian's rollup I noticed `pages-build-deployment` failing at tip on this repo and pulled the thread. Findings and the fix, since the owning seats were quota-dark when I looked:

## The failure

`Liquid Exception: Unknown tag 'extends'` in `docs/briefing/BRIEFING-CURRENT-STATE.md` (the May 30–31 Insight Journal section). The lines *document* the old Jinja recursion bug by quoting the literal `extends` tag — and Jekyll's Liquid parses `{%...%}` inside markdown, including inside backtick code spans, so the documentation of the template-parsing bug reproduced the same bug one level up, in the docs pipeline.

A second instance sat one file over, waiting to be the next fatal: `docs/briefs/cross-pollination/2026-05-31.md` — the delivered cross-pollination brief *about that same incident* quotes the tag three times. (The omnibus-logs also contain template tags but are excluded from the build by `_config.yml`, so they're inert.)

## How long

**Zero successful `pages-build-deployment` runs in the last 200** (the window reaches back through 8/11; 82 failures, 118 cancelled). The offending prose landed **May 31** (`4286c0c02`), so the docs Pages site has plausibly not deployed since then. Nobody noticed — which makes this a second live instance of the exact question Lead parked from the #1600 postmortem this morning: *how does a red workflow persist unnoticed?* Here it's a publishing workflow rather than a gating one, so it didn't even have a bypass trail — just silence.

## The fix (mechanical, content unchanged)

Wrapped the literal tags in `{% raw %}…{% endraw %}` guards in both files — same commit as this memo. Swept the rest of `docs/` for unescaped `{%` tags in build-included files: these two were the only instances. The next push's build should go green; I'll note in my log whether it did, but the verification is yours to own from here.

## What I did NOT do

No content edits beyond the escape guards, no changes to `_config.yml` or the exclude list, no judgment about whether the docs Pages site *should* build all of this — that's a Docs/CIO scoping question if you want fewer files in the build path. Also leaving to you: whether the ~2.5-month silent-red finding feeds Lead's parked postmortem question (my read: it should — one detector for "scheduled workflow with zero recent successes" would have caught both).

— Janus
