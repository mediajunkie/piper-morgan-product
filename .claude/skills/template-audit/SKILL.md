---
name: template-audit
description: Run a mechanical template audit on a finished blog draft before sending the publish-ready signal to Docs. Use after PM's voice pass is complete. Produces a pass/fail report with specific flags. Blocks the publish-ready signal on any FAIL.
scope: comms
version: 1.1
created: 2026-06-19
updated: 2026-07-09
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

## The Checklist

Run each check in order. Mark ✓ PASS or ✗ FAIL with a specific note on failures.

### 1. YAML frontmatter — all three fields present and non-empty

```bash
python3 -c "
import re, yaml
with open('<draft>') as f:
    text = f.read()
m = re.match(r'^---\n(.*?)\n---\n', text, re.DOTALL)
if not m:
    print('FAIL: no frontmatter')
else:
    parsed = yaml.safe_load(m.group(1))
    for k in ['image', 'alt', 'caption']:
        v = parsed.get(k)
        if not v:
            print(f'FAIL: {k} is empty or missing')
        else:
            print(f'OK: {k} = {repr(v)[:60]}')
"
```

**Caption format check**: if caption starts with `'"`, it's a spoken-line format. Verify any apostrophe inside is doubled: `'"It''s fine."'` not `'"It's fine."'` (the latter breaks YAML).

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
grep -n "\[CHRISTIAN\|PLACEHOLDER\|CONSIDER\]\|ADD PERSONAL\|FACT-CHECK\|SOURCE NEEDED\|TBD\]\|\[alt text" <draft>
```

Any match = FAIL. All brackets must be filled or removed before publish.

### 6. Footer tease — present and matches editorial calendar

```bash
grep -n "Next on Building Piper Morgan" <draft>
```

Must be present. The title in the tease must match the **next scheduled post** from the calendar (checked in pre-flight step 3) — not assumed, not the next narrative beat if an insight comes first.

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
1. YAML frontmatter          ✓ PASS
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
