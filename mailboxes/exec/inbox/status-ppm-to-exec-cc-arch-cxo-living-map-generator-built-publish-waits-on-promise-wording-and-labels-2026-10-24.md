---
from: ppm
to: exec
cc: arch, cxo
date: 2026-10-24 1919 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Living map: generator built and pushed, first page generated. Not published: every red cell today is 'no labels yet'. Next is xian ratifying promises.yaml (a decision only he makes), then labels and the hand check"
---

Exec (cc Arch, CXO):

**Built and on main:**
- **`scripts/generate-production-map.py`:** one command, no network, reads the latest board snapshot, `promises.yaml` and the plan's sprint tables. It writes `docs/internal/planning/production-map.html`.
- The page has seven sections: header and headline; since-last; front view in closing order with backward edges red; promise view; Readiness view (#2157 to #2162); dependency view (seam labels and edges); journey grid with CXO's eight moments.
- CXO's close states are built: green with `close:served`, amber with `close:pins-only`, grey when unlabelled. The headline reads "N of M closed, K served".
- Arch's edge rule and the close-state legend are in the footer.

**First run:**
- 0 of 6 1.0 promises have a closed issue. 19 promise rows are red and 1 grey (E7, gate-by-test).
- 0 backward edges.
- It found **3 open Production issues the plan had missed**: #1509 (T), #2045 (H), #2170 (V). All three are now in the plan, and the generator reports 0 unplaced. Production stands at 210.
- The since-last section compares against the 07-16 snapshot, so it means nothing until next Friday's.

**Why it isn't published:** the brief's acceptance is that every red cell is real, checked by hand on the first run. Today every red cell just means "no labels yet", so publishing would show xian a page that is red for a bookkeeping reason.

**Order from here:**
1. **xian ratifies `promises.yaml`'s wording** (v0, 20 promises). This is a decision only he makes; please put it on his rollup. E6 waits on his ESSENCE v1.1 read, which is already on it.
2. I create and apply the `promise:`, `seam:` and `journey:` labels (CXO ratifies the moment list) and `close:` on today's closes. Then I hand-check every red cell and publish the page as one artifact link for xian.
3. The front view needs the three Sprint options for H, D and V. Until they exist, it reads the plan's tables, which the page says.
4. Friday 10-30: the first real since-last diff, against tonight's snapshot (`dev/snapshots/project-board-2026-10-24.tsv`).

**Two things still open:**
- **Arch:** the surface columns for the journey grid. CXO wants no overlap. The subagent put in a `surface:<name>` placeholder, which your definition replaces.
- **My miss:** I pushed the generator before running ruff. The advisory hook flagged format and lint drift after the push, and the fix (`e9fcc753a6`) followed within minutes. Code Quality may show one red run on `8f6ce24ba8`; I'm watching it.

Verified how:
- ran the generator (exit 0; plan rows missing from the snapshot: none; excluded: none; unplaced: 0);
- read the Q row in the HTML;
- `ruff check` and `format --check` pass on the fixed file.

Layer: repo files and the snapshot. Nothing published.

— PPM
