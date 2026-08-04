---
name: template-audit
description: Run a mechanical template audit on a finished blog draft before sending the publish-ready signal to Docs. Use after PM's voice pass is complete. Produces a pass/fail report with specific flags. Blocks the publish-ready signal on any FAIL.
scope: comms
version: 1.5
created: 2026-06-19
updated: 2026-08-04
---

# template-audit

Mechanical pre-publish checklist for Comms. Runs against the **final draft** (after PM's voice pass). Every check must pass before sending the publish-ready memo to Docs.

**Critical**: run this AFTER PM's voice pass — not before, not during. PM's edits can introduce new jargon, change section headings, or rewrite paragraphs that break previously-clean checks. The miss that prompted this skill (Jun 19): "cohort" found 4× in *This One's Taken* after PM's voice pass; Comms' pre-pass grep had returned 0.

## When to Use

- After PM confirms their voice/edit pass is complete on a draft
- Before sending the publish-ready memo to Docs inbox
- Any time PM asks "is this ready to go to Docs?"

NOT for: draft-time discipline (that's in `draft-blog-post`) or Docs' final proof (that's Step 5 of the run-of-show). This is Step 3 only.

## Pre-Flight (before reading the draft)

1. Open `docs/internal/planning/comms/blog-post-template.md` — the structural reference
2. Open `docs/internal/planning/comms/xian-voice-tone-guide.md` — the voice reference
3. Pull the next scheduled post from `editorial-calendar.csv` — needed for footer tease verification

```bash
# Get the file's pubDate, then find the next post after it
grep -i "$(basename <draft> .md)" docs/internal/planning/comms/editorial-calendar.csv
# Find the next pubDate entry after this post's pubDate
```

## ⚠️ FIRST: check the theme. Four checks are calibrated for narratives and are WRONG on Weekly Ships.

**Look up `theme` on the calendar row before running anything.** Measured 2026-08-04 against the **6 most recent published Ships** — posts that shipped clean and are live on the site:

| check | Ships that would FAIL | why it's wrong for a Ship |
|---|---|---|
| **#1** caption non-empty | **6 of 6** | Ships carry no caption by convention (#044/#050 use the literal `N/A`) |
| **#6** footer tease present | **6 of 6** | Ships sit outside the tease chain entirely — see check #6 |
| **#12** word count ≤1,600 | **4 of 6** | Ship norm is **~1,630 words** (measured #049–#053: 1279 / 1384 / 1906 / 1827 / 1764). The 800–1,300 target is a *narrative and insight* range |
| **#14** no `#NNN` in prose | **6 of 6** | `#053`, `#054` are **Ship numbers**, not issue numbers, and they are conventional in Ship prose + the previous/next links |

**So a full audit against a Ship produces roughly four false FAILs every single time.** On `theme=ship`, mark these **N/A — by convention**, never FAIL. Every other check applies to Ships unchanged.

⚠️ **Why this is worth a table rather than four footnotes**: a mandatory gate that cries wolf on four of fourteen checks trains its own operator to discard failures by eye — and the discarding habit does not stay confined to the four that deserve it. That is the same dynamic CLAUDE.md documents for the sign-off checklist, where a step that reported thousands of unpushed commits every session got quietly substituted away by the people following it most carefully. **A check that is wrong in a knowable, repeating way is a check people learn to skim.**

## The Checklist

Run each check in order. Mark ✓ PASS or ✗ FAIL with a specific note on failures. **On a Ship, apply the calibration table above first.**

### 1. YAML frontmatter — all three fields present and non-empty

⚠️ **This check used `import yaml` until 2026-07-29 and was silently unrunnable on Amber for every role, in every location** — no `pyyaml`, and **no venv anywhere on the host** including the shared checkout (found by Comms on Ship #053, independently verified one level deeper by Docs). It emitted a `ModuleNotFoundError` traceback into a column of twelve passes, which is exactly what a pass looks like to a skimming reader. **It is the frontmatter check — the class that produced the caption `''` bug — so the hole sat in the one check whose absence had already cost us a real defect.** m-44 inside the audit tool itself.

**The version below has no third-party dependency and cannot lose one.** It only needs three keys, so it parses the block directly. It also prints an explicit verdict token per key rather than relying on the reader to interpret silence.

```bash
python3 - "<draft>" <<'PY'
import re, sys
path = sys.argv[1]
text = open(path, encoding='utf-8').read()
m = re.match(r'^---\n(.*?)\n---\n', text, re.DOTALL)
if not m:
    print('FAIL: no frontmatter block'); sys.exit(0)
body = m.group(1)
fields = {}
for line in body.split('\n'):
    if re.match(r'^\s', line) or ':' not in line:
        continue                                   # skip continuations / non-kv lines
    k, _, v = line.partition(':')
    fields[k.strip()] = v.strip()
for k in ('image', 'alt', 'caption'):
    if k not in fields:
        print(f'FAIL: {k} key MISSING')
    elif not fields[k] or fields[k] in ("''", '""'):
        print(f'FAIL: {k} present but EMPTY')
    else:
        print(f'OK: {k} = {fields[k][:60]}')
PY
```

⚠️ **`caption` is legitimately empty on Weekly Ships** — verified across #047–#052, and #044/#050 use the literal `N/A`. So a `FAIL: caption present but EMPTY` on a `theme=ship` draft is **expected and not a blocker**; treat it as N/A-by-convention and say so in the report. On narratives and insights it is a real FAIL.

**If this check ever cannot run** — a `Traceback`, a missing interpreter, anything other than three verdict lines — **report it as `⚠ CANNOT RUN`, not as PASS, and verify the frontmatter by reading it.** A check that did not execute has measured nothing, and its silence is indistinguishable from a clean result (methodology-44). The same rule applies to check #13 below.

⚠️ **`\[PM\b` was added 2026-08-03 and it is the load-bearing half.** The prior pattern missed the two bracket forms actually in use — **`[PM: …]`** and **`[PM VOICE-PASS: …]`** — which are the conventions these drafts really carry, present in **5 drafts** at the time of the fix. Measured: the old pattern scored **0** against a draft with a live open bracket, so **this check — the one that BLOCKS the publish-ready signal on placeholders — was passing drafts with unresolved PM questions in them.** It was caught only because an ad-hoc grep during a pre-pass used a different pattern than the skill's own and disagreed with it. Verified: `\[PM\b` catches every real instance across the drafts directory with **zero false positives** — every match is a genuine editorial bracket. Note the skill's own check #13 already referenced `[PM: ...]` brackets, so the form was documented here while this check could not see it.

**Caption format check**: if caption starts with `'"`, it's a spoken-line format. Verify any apostrophe inside is doubled: `'"It''s fine."'` not `'"It's fine."'` (the latter breaks YAML). ⚠️ **The `''` doubling is correct ONLY inside single-quoted YAML.** Copying that form into markdown **body** text renders the doubled apostrophe literally — a real instance shipped in the Ship #053 draft as `*"OK, let''s see"*`. If a caption also appears in the body, it takes ordinary prose punctuation.

### 2. Title is H1

```bash
grep -n "^# " <draft> | head -3
```

First `#` heading should be the post title on the first non-frontmatter line. FAIL if missing or if it's `##`.

### 3. Dateline — italicized, correct format, no stray draft dates

```bash
grep -n "^\*" <draft> | head -5
```

Look for `*Month DD–DD, YYYY*` (or `*Month DD, YYYY*` for single-day). FAIL if:
- No dateline
- Format wrong (e.g., `*March 2026*` without day range)
- A second date line appears above the dateline (stale draft date)

### 4. Section headings — `#` for top-level, `##` for subsections only

```bash
grep -n "^##\+" <draft>
```

Top-level sections must be `#`. `##` is allowed only for genuine subsections within a section. `###` and deeper: FAIL (not used in published prose).

### 5. No placeholder brackets

```bash
grep -nE "\[PM\b|\[CHRISTIAN|PLACEHOLDER|CONSIDER\]|ADD PERSONAL|FACT-CHECK|SOURCE NEEDED|TBD\]|\[alt text" <draft>
```

Any match = FAIL. All brackets must be filled or removed before publish.

### 6. Footer tease — present and matches editorial calendar

```bash
grep -n "Next on Building Piper Morgan" <draft>
```

Must be present **on narratives and insights**. The title in the tease must match the **next scheduled post** from the calendar (checked in pre-flight step 3) — not assumed, not the next narrative beat if an insight comes first.

⚠️ **Weekly Ships sit OUTSIDE the tease chain — two rules, both measured 2026-08-03, and getting this wrong causes ACTIVE DAMAGE rather than a miss:**

- **A Ship carries no footer tease at all.** `theme=ship` → check #6 is **N/A, not FAIL**. Measured: **6 of the 6 most recent Ships (#048–#053) have none.**
- **Narratives and insights tease past a Ship to the next non-Ship post.** Measured: **7 of 8** recent cases where a Ship fell next in the calendar. So when the calendar's literal next row is a Ship, the correct tease target is the row *after* it.

**Why this warning exists**: the sentence above used to end at "next scheduled post," full stop. Read literally against the calendar it would have had me "correct" *The List That Lies* (Aug 4) to tease Ship #054 (Aug 5) — **breaking a chain that was already right**, the day before it published. Unlike check #5's blindness, a wrongly-*directive* check doesn't just miss things; it manufactures the defect it claims to prevent. **A gate that is confidently wrong is worse than a gate that is silent.**

**Determine the target this way, not from the raw next row:**

```bash
python3 -c "
import csv
rows=sorted([r for r in csv.DictReader(open('docs/internal/planning/comms/editorial-calendar.csv')) if r['pubDate']],key=lambda r:r['pubDate'])
me='<this post title>'
i=next(n for n,r in enumerate(rows) if r['title']==me)
nxt=next((r for r in rows[i+1:] if r['theme']!='ship'), None)
print('tease target:', nxt['title'] if nxt else 'NONE — last in queue')"
```

### 7. Reader question — present

```bash
grep -n "^\*.*?\*$" <draft> | tail -5
```

The closing `*[question]?*` paragraph must be present after the `---` footer separator.

### 8. Zero semicolons in prose

```bash
grep -c ";" <draft>
```

Result must be 0. Any semicolon = FAIL (banned in published prose; split into two sentences).

### 9. No "load-bearing" in prose

```bash
grep -in "load-bearing" <draft>
```

Any match = FAIL (internal docbase term; public prose uses "critical" or rephrase).

### 10. No "cohort" in prose

```bash
grep -in "cohort" <draft>
```

Any match = FAIL. Public prose uses "team" (default) or "agent team" (agents-specific context). "Cohort" is fine in session logs, mail, and internal docs — not in published posts.

### 11. AI-writing-tics / cliché constructions

```bash
grep -inE "(isn't|wasn't) [a-z][^.]{0,60}\. (It'?s|It was|They were)|wasn't [a-z][^.]{0,60}, it was|-fold\b" <draft>
```

This one needs judgment, not just the grep above — read the prose for the *rhetorical device*, not only the literal string. Known members of this family (grows over time; add here when a new one gets caught):

- **The negation-reveal cliché**: "It isn't X. It's Y." / "X wasn't Y, it was Z." A dramatic-sounding contrastive construction that reads as an AI tic once it appears more than once in a piece. It can hide in other surface phrasings too — "X was never the answer. Y was" is the same shape wearing different words. **Fix**: usually just state the affirmative directly and drop the negated setup — "It's Y" / "It was Z" / "Y was" — per PM's stated technique. Caught 2026-07-09 (PM: "rife... we need to tighten up the review you do") — found in 4 of 4 drafts checked that day, none caught by the pre-existing checklist. The grep above is a starting point, not a substitute for reading: its first version only matched `It's`/`Its` as the follow-up clause and missed 3 real instances phrased as "It was" in the very next draft checked — read every `wasn't`/`isn't` in context, don't just trust a clean grep result. Don't over-apply: a plain factual negative ("the volume held scratch data that rebuilt cleanly") is NOT this pattern — only the tight deny-then-reveal construction is.
- **"-fold" as a crutch suffix** (e.g., "twofold," "manifold significance") — rephrase plainly.
- **"load-bearing"** — see #9.
- **"cohort"** — see #10.

Any confirmed instance of the reveal-cliché or "-fold" = FAIL.

### 12. Word count — within range

```bash
wc -w <draft>
```

Target: ~800–1,300 words for narratives and insights (markdown word count includes some frontmatter noise — subtract ~10). FAIL if significantly over (>1,600) — flag for PM review, don't auto-block.

### 13. Acronym sweep

```bash
python3 scripts/check-acronyms.py <draft>
```

Any `⛔ FALSE-UNPACK` line = FAIL. Warnings are advisory — surface to PM if unexpected. (Skip if script not present; note the skip.) NO-GLOSS warnings matching text ONLY inside a `[PM: ...]` editorial bracket or a `[PLACEHOLDER ...]` footer note are false positives — check where the match actually falls before flagging.

### 14. Issue/commit references in narrative prose

```bash
grep -n "#[0-9]\{3,\}\|[a-f0-9]\{7,40\}" <draft>
```

Issue numbers (#824, #888) and commit hashes in narrative prose = FAIL unless they're inside a technical-detail section or coordinate reference (e.g., a metrics table). Replace with role-functional descriptions in running prose.

## Output Format

Report results as a compact table, then a verdict:

```
TEMPLATE AUDIT — <slug> — <date>

Check                        Result
─────────────────────────────────────
1. YAML frontmatter          ✓ PASS        ← use ⚠ CANNOT RUN if it didn't execute; never PASS
2. Title H1                  ✓ PASS
3. Dateline                  ✓ PASS
4. Section headings          ✓ PASS
5. No placeholders           ✗ FAIL — [CONSIDER] at line 49 still present
6. Footer tease              ✓ PASS — teases "Branch-or-Anchor" (Jun 23) ✓
7. Reader question           ✓ PASS
8. Zero semicolons           ✓ PASS (0)
9. No "load-bearing"         ✓ PASS
10. No "cohort"              ✗ FAIL — 4 instances (lines 13, 33, 49×2, 51)
11. AI-writing-tics          ✗ FAIL — negation-reveal cliché at lines 17, 29
12. Word count               ✓ PASS (1,104 words)
13. Acronym sweep            ✓ PASS
14. Issue refs in prose      ✓ PASS

VERDICT: FAIL (3 issues)
ACTION: Fix items 5, 10, 11 before sending publish-ready signal.
```

## On Failure

Fix each FAIL before sending the publish-ready memo. If a fix requires PM's voice (e.g., a placeholder that only PM can fill), flag it to PM and hold the signal — do not work around it.

On PASS: send the publish-ready memo to Docs inbox per the handoff protocol (Jun 18).

## Cross-references

- `docs/internal/planning/comms/blog-post-template.md` — the structural standard
- `docs/internal/planning/comms/xian-voice-tone-guide.md` — the voice standard
- `docs/internal/planning/comms/content-publishing-run-of-show.md` — step 3 of 7
- `docs/internal/planning/comms/editorial-calendar.csv` — footer tease source of truth
- `docs/internal/development/methodology-core/methodology-44-CLEAR-IS-NOT-A-MEASUREMENT.md` — why a check that cannot run must never report as PASS

---

*v1.2 — 2026-07-29. **Check #1 rewritten to have no third-party dependency**, after it was found silently unrunnable on Amber for every role in every location (no `pyyaml`, and no venv anywhere on the host including the shared checkout). It had been emitting a `ModuleNotFoundError` traceback into a column of twelve passes — the frontmatter check, i.e. the one class that had already produced a real shipped defect (the caption `''` bug). Found by Comms while auditing Weekly Ship #053; independently verified one level deeper by Docs, who established the venv is absent host-wide rather than worktree-local. The replacement parses the block directly (three keys don't need a YAML engine) and was behaviorally tested across four shapes before shipping: filled, empty-quoted `''`, YAML-escaped `''` apostrophe inside a caption, and no-frontmatter — all correct, no traceback. Also added: the explicit `⚠ CANNOT RUN` verdict token (a non-executing check must never occupy the PASS column, per m-44), the Ship-caption N/A-by-convention note, and the warning that `''` doubling is correct in YAML but renders literally in markdown body text.*

*v1.3 — 2026-08-03. **Check #5 widened to `\[PM\b`.** The placeholder gate could not see `[PM: …]` or `[PM VOICE-PASS: …]`, the two bracket forms these drafts actually use — so the check that blocks a publish-ready signal on unresolved PM questions was scoring 0 on drafts that had them. Found during a pre-pass when an ad-hoc grep disagreed with the skill's own pattern. Zero false positives across the drafts directory. Frontmatter version and footer bumped together, which is the defect v1.2 shipped with.*

*v1.4 — 2026-08-03. **Check #6 corrected: Weekly Ships sit outside the footer-tease chain.** The check said the tease must match "the next scheduled post" with no exception for Ships. Measured against actual practice: **6 of 6 recent Ships carry no tease**, and **7 of 8** narratives/insights whose next calendar row was a Ship teased *past* it to the following non-Ship post. Read literally, the old wording would have had me "fix" *The List That Lies* to tease Ship #054 — **corrupting a correct chain the day before it published.** Distinct from the v1.3 defect and worse in kind: check #5 was *blind* (it missed things), check #6 was *wrongly directive* (it would have manufactured the defect it claims to prevent). Added a calendar-derived query for the tease target so the rule isn't re-derived by eye. Second gate defect found in this skill in one day — both surfaced by running the gate against real queue state rather than reading it.*

*v1.5 — 2026-08-04. **Added the Ship-calibration table at the top of the checklist.** Four checks — #1 caption, #6 tease, #12 word count, #14 `#NNN` refs — are calibrated for narratives and produce **false FAILs on Weekly Ships**: measured against the 6 most recent published Ships, they'd fail **6/6, 6/6, 4/6, 6/6** respectively, on posts that shipped clean and are live. Ship word norm measured at **~1,630** (#049–#053), against the narrative target of 800–1,300. Two of the four (#1, #6) already had scattered N/A notes; #12 and #14 had none. **Consolidated into one theme-keyed table rather than a fourth footnote**, because the real hazard isn't any single false FAIL — it's that a gate crying wolf on four of fourteen checks teaches its operator to discard failures by eye, and that habit doesn't stay confined to the four that earned it. Same dynamic CLAUDE.md records for the sign-off checklist. Found while pre-passing Ship #054.*
