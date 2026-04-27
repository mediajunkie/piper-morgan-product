# create-omnibus

Create an omnibus session log synthesizing all agent sessions from a given date.

## When to Use

- At the start of each Docs session (omnibus before new work)
- When PM says "create omnibus", "omnibus for yesterday", etc.
- After any HIGH-COMPLEXITY day (4+ agents)

## Pre-Flight: Load the Methodology

**MANDATORY FIRST STEP**: Read the core methodology before doing anything else:

```bash
# Read this EVERY TIME — do not work from memory
cat docs/internal/development/methodology-core/methodology-20-OMNIBUS-SESSION-LOGS.md
```

The methodology defines format selection, the 6-phase method, line limits, compression ratios, timeline rules, executive summary format, validation checklist, and common pitfalls. **Follow it precisely.**

This skill is a runbook for executing the methodology, not a replacement for it.

## Procedure

### Step 1: Determine Target Date

Ask PM if not obvious. Default: previous calendar day.

```bash
# Set target date
TARGET="YYYY-MM-DD"
YEAR="YYYY" MONTH="MM" DAY="DD"
```

### Step 2: Source Discovery (Methodology Phase 1)

```bash
# Find all session logs for target date
ls dev/$YEAR/$MONTH/$DAY/*log*.md

# Count them
ls dev/$YEAR/$MONTH/$DAY/*log*.md | wc -l

# Check for cloud agent artifacts in mailboxes
find mailboxes/*/read/ -name "*$TARGET*" -type f

# Check dev/active for same-day items
find dev/active/ -name "*$TARGET*" -type f
```

Report inventory to PM:
```
Found N session logs for [date]:
- [list each with role and filename]
- [note any cloud-only agents with memos but no session logs]
```

### Step 2.5: Cross-Reference Gate (MANDATORY — added 2026-04-22 after drift incident)

**Before proceeding to format selection, verify the source-log set is complete** by cross-referencing agent mentions inside each log against the roles represented in the source set.

**The failure this prevents**: synthesizing an omnibus from "the logs currently in tree" without checking whether those logs mention *other* agents whose own logs haven't been downloaded yet. This is Pattern-062 (Assembly Assumption) applied to omnibus synthesis — individually-correct source logs can produce a collectively-incomplete omnibus if an agent's reference to "I got a memo from PPM" is present in three other logs but PPM's own log is absent from the source set.

**Procedure:**

1. **Enumerate the roles present in the source set** — build a set `{Lead Dev, Docs, CXO, ...}` based on each source log's role.

2. **Scan each source log for mentions of other agent roles** — grep each log for role names and agent patterns:

```bash
# Known agent role vocabulary (keep in sync with the actor names list in Step 5)
AGENTS="Lead Dev|Lead Developer|Docs|Documentation Management|docs-code|PA|Piper Alpha|CXO|Chief Experience|CIO|Chief Innovation|PPM|Principal Product|Architect|Chief Architect|arch|Comms|Communications|HOST|Exec|Chief of Staff|code-opus|Code Agent"

for log in dev/$YEAR/$MONTH/$DAY/*log*.md; do
  echo "=== $(basename $log) ==="
  grep -oE "($AGENTS)" "$log" | sort -u
done
```

3. **Compile the union of all mentioned roles** across the source set.

4. **Compare mentioned-set against source-set**:
   - Any role mentioned but not in source-set → **flag as potential missing log**
   - For each flagged role, ask PM: "I see mentions of [ROLE] in today's logs — was [ROLE] actually active today, or are these backreferences to prior-day work?"

5. **Also check for cross-role artifacts**: scan `dev/active/` and `dev/$YEAR/$MONTH/$DAY/` for artifacts (non-log files) dated on the target date. If an artifact is attributed to a role whose session log is not in the source set, that role was working — the session log may be missing.

```bash
# Check dev/active/ for artifacts dated on target
find dev/active/ dev/$YEAR/$MONTH/$DAY/ -name "*$TARGET*" -type f | grep -v "log.md$"
# For each, check the file's authorship line (often "Author: ROLE" or "Prepared by: ROLE")
```

6. **Gate decision**:
   - **PASS**: every mentioned role has a log, or PM has confirmed which mentioned roles are genuinely not-active that day. Proceed to Step 3.
   - **FAIL**: a mentioned role's log is likely missing and downloadable. **STOP** — ask PM to download (if Chat) or file (if Code) the missing log before proceeding. Synthesizing without it would produce a drifted omnibus, as happened on 2026-04-19 with the Apr 16 omnibus (later amended 2026-04-22 after PPM, CIO, and HOST 4/16 logs were downloaded).

**If the gate fails and PM declines to fetch** (e.g., the agent truly is reachable only later): document the gap explicitly in the omnibus Sources section — "NOTE: [ROLE] session log not available at synthesis time; content inferred from cross-references only. May require amendment when log becomes available."

**Do not paper over the gap** by proceeding as if the source set were complete.

### Step 2.6: Cross-Role Mentions Verification (added 2026-04-27 per CXO ask)

**After source set passes Step 2.5**, verify that *cross-role assertions* in one log are consistent with the other log they reference.

**The failure this prevents**: PA's session log says "CXO scored S2 at 9/9" — but CXO's session log doesn't mention scoring S2 at all. Both logs are "present" (Step 2.5 passes), but they disagree on facts. Pattern-062 at the assertion layer.

**Procedure** (do for high-impact cross-role assertions, not exhaustively):

1. When a session log makes a factual claim about another agent's work (e.g., "Lead Dev shipped X," "CXO endorsed Y," "Architect filed Z"), spot-check the referenced agent's session log for the same event.
2. If the claim and the referenced log diverge, **flag the discrepancy in the omnibus** rather than picking a side. Sample framing: *"PA's log records X; CXO's log records Y. Discrepancy preserved for resolution."*
3. The discipline is "name the divergence," not "force consensus." Both reads may be true at different times (yesterday's mail-discipline cascade is the canonical case — racing snapshots, not disagreement).

**Skip this step for**: routine references (cross-role mail receipts, attendance), well-aligned multi-role threads (Phase E scoring chains where everyone explicitly references the same artifacts).

### Step 3: Format Selection

Based on session count and characteristics:

| Criteria | Format | Line Limit |
|----------|--------|------------|
| 1 session, single goal | MINIMAL | ~50 lines |
| 1-2 agents, single goal | STANDARD | 300 lines |
| 3+ parallel streams, architectural decisions, coordination | HIGH-COMPLEXITY | 600 lines |

**Justify your selection** in the opening paragraph. If borderline, ask PM.

### Step 4: Read ALL Source Logs (Methodology Phase 2)

**Read every log completely. No skimming.**

For each log, extract:
- Every timestamped entry
- Cross-references to other agents (handoffs, mentions)
- Reflective content (especially Lead Dev end-of-session)

### Step 5: Build Timeline (Methodology Phases 3-5)

**The timeline is non-negotiable.** It must show events from ALL agents interleaved by time.

**Format by day type:**

- **STANDARD**: Simple bullet list with bold actor names
- **HIGH-COMPLEXITY**: Phase-grouped with time period headers

**Rules (enforced strictly):**
- Each entry: 1-2 lines MAX
- Interleaved by time, not grouped by agent
- Preserve coordination handoffs as distinct entries
- Preserve causality chains (discovery → decision → implementation)
- Bold actor names consistently

**Actor names** (use these, not slugs):
- **xian** — PM/founder
- **Lead Developer** — code-side dev coordination
- **Documentation Management** or **docs-code** — omnibus, mailbox, blog pipeline
- **Chief Architect** — ADRs, architecture
- **Chief of Staff** — cross-workstream synthesis
- **HOST** — agent welfare, human network
- **Communications Chief** — blog, narrative
- **CXO** — UX testing, Colleague Test
- **CIO** — methodology, patterns
- **PPM** — sprint planning, roadmap

### Step 6: Write Executive Summary (Methodology Phase 6)

**4 sections, each with terse 1-line bullets:**

1. **Core Themes** (3-5 bullets) — major accomplishments, breakthroughs, coordination patterns
2. **Technical Details** (5-8 bullets) — specific implementations, architecture decisions, infrastructure
3. **Impact Measurement** (4-6 bullets) — quantitative metrics, qualitative improvements
4. **Session Learnings** (5-8 bullets) — what worked, what caused friction, patterns to replicate/avoid

**No paragraphs.** Each bullet = one concise line. Source logs have details.

### Step 7: Verify Canonical References (MANDATORY when applicable)

**If the day includes a ratified PDR, ADR, Pattern, or methodology doc**, the omnibus must quote the canonical source — not paraphrase from memory or from session log summaries.

**The rule: quote or reference — never paraphrase canonical content.**

**Companion principle (added 2026-04-27 per CXO ask)**: verify at point of creation, not downstream. When *first* citing a canonical artifact in an omnibus draft, open the doc and confirm titles/principle-names verbatim — don't trust the previous omnibus's wording or your own memory. Each omnibus is a fresh authoring surface; paraphrase drift accumulates if each generation lifts from the prior generation.

For every mention of a canonical artifact (PDR-XXX, ADR-XXX, Pattern-XXX, methodology-XX, PDR/ADR/Pattern by name):

1. **Open the canonical doc** at its authoritative path:
   - PDRs: `docs/internal/product/pdr/PDR-XXX-*.md`
   - ADRs: `docs/internal/architecture/current/adrs/ADR-XXX-*.md`
   - Patterns: `docs/internal/architecture/current/patterns/pattern-XXX-*.md`
   - Methodologies: `docs/internal/development/methodology-core/methodology-XX-*.md`
2. **Copy principle names, titles, and key terms verbatim** from the canonical doc into the omnibus entry.
3. **If the doc is unavailable** (not yet committed, or path uncertain): do not invent or paraphrase — write "PDR-XXX ratified; titles to be confirmed" and flag for correction.

This prevents the class of error where successive agents paraphrase the same canonical content and it drifts over time.

**Examples of what to do:**

✅ "PDR-004 delivered. Four principles: (1) The Session Belongs to the User, (2) Offer-First Activation, (3) Piper Coordinates Understanding, (4) The LLM Floor Guarantee." *(principle names copied verbatim from PDR-004)*

✅ "PDR-004 delivered — four principles governing ongoing experience; see doc for details." *(referenced without summarizing content)*

❌ "PDR-004 delivered. Four principles: presence over performance, specificity as care, honest boundaries, growth through use." *(paraphrased from memory — the canonical principle names are different)*

### Step 8: Validate (Methodology Checklist)

Run through the validation checklist from the methodology:

**Timeline (non-negotiable):**
- [ ] Unified chronological timeline EXISTS
- [ ] Events from ALL agents interleaved by time
- [ ] Coordination handoffs visible as distinct entries
- [ ] Causality chains preserved

**Canonical references:**
- [ ] Every PDR/ADR/Pattern/methodology mention uses verbatim canonical names (Step 7)
- [ ] No paraphrased principle names, titles, or key terms

**Format & Quality:**
- [ ] All sessions identified and read completely
- [ ] Format selection justified
- [ ] LINE COUNT UNDER LIMIT (300 Standard / 600 High-Complexity)
- [ ] Timeline entries 1-2 lines max
- [ ] Executive summary bullets 1 line max
- [ ] Actor names consistent and bold

**Additional for HIGH-COMPLEXITY:**
- [ ] All parallel work streams captured distinctly
- [ ] Phase groupings reflect actual work patterns
- [ ] Handoff moments preserved
- [ ] Strategic pivots captured

### Step 9: Write the File

```bash
# Create omnibus file
# File: docs/omnibus-logs/YYYY-MM-DD-omnibus-log.md
```

**Header format:**
```markdown
# Omnibus Log: [Month Day, Year]

**Day**: [Day of week]
**Sessions**: [N] ([list roles])
**Day Type**: [STANDARD/HIGH-COMPLEXITY] — [brief descriptor]
**Justification**: [Why this format. What made the day complex or standard.]

**Git Commits**: [count or "N+"]
```

### Step 10: Archive Source Logs (Final Step Before Reporting)

**MANDATORY**: Once the omnibus is written and committed, archive the source session logs from `dev/active/` to `dev/YYYY/MM/DD/`. The omnibus is now the synthesized record; the source logs are reference material that should not clutter the active workspace.

```bash
# Ensure target directory exists
mkdir -p dev/$YEAR/$MONTH/$DAY

# Move all logs for the target date from dev/active/ to date folder
mv dev/active/$TARGET-*.md dev/$YEAR/$MONTH/$DAY/

# Verify the move
ls dev/$YEAR/$MONTH/$DAY/ | wc -l
```

**Also check for stranded logs from earlier dates** that should already be archived but weren't:

```bash
# Find any session logs in dev/active/ older than target date
ls dev/active/2026-*-log.md 2>/dev/null
```

If any pre-target logs exist, archive them too — they were missed by previous omnibus runs and shouldn't be left in active.

**Why this is the final step**: Archiving before the omnibus is written risks losing access to source material if something goes wrong. Archiving after lets the omnibus be the synthesized canonical record while preserving sources in their date-stamped homes.

### Step 11: Report to PM

```
Omnibus complete for [date]:
- Format: [STANDARD/HIGH-COMPLEXITY]
- Sessions covered: N
- Line count: N (limit: N)
- Source logs archived: dev/YYYY/MM/DD/ (N files)
- Key themes: [2-3 sentence summary]
```

## Common Pitfalls (from methodology)

1. **The "Main Log" Trap** — never assume one log tells the whole story
2. **The Memory Shortcut** — always extract from actual timestamped entries, not memory
3. **The Sessions Table Substitution** — a sessions overview table is NOT a timeline
4. **The Detail Bloat** — source logs have details; omnibus is synthesis
5. **Skipping the methodology** — re-read `methodology-20` every time, not just the first time

## Quick Reference

```
docs/internal/development/methodology-core/methodology-20-OMNIBUS-SESSION-LOGS.md
  ↑ THE SOURCE OF TRUTH — read before every omnibus
```
