# Weekly Ship Process Guide

*The end-to-end process for producing the Piper Morgan Weekly Ship newsletter.*

**Version**: 1.0
**Last updated**: March 22, 2026
**Owner**: Chief of Staff (exec), with Documentation Management (docs) support
**Template**: `knowledge/weekly-ship-template-v4.1.md`

---

## What the Weekly Ship is

The Weekly Ship is a LinkedIn newsletter summarizing a week of work on the Piper Morgan project. It serves three audiences:

1. **The team** — agents and PM see their work reflected and contextualized
2. **External followers** — practitioners interested in AI-assisted development methodology
3. **The project record** — a curated weekly narrative that complements the omnibus logs

The convention originated from 18F's "Shipping News" Slack channel, where teams posted weekly canvas updates on Fridays. It was adapted for Piper Morgan and aligned with the Chief of Staff's workstream review ritual as the team's organizational structure matured.

Currently at Ship #035. Published weekly on LinkedIn, with plans to cross-publish to pipermorgan.ai.

---

## Coverage window

**Friday through Thursday.** The Ship covers work from Friday of the prior week through Thursday of the current week. This gives Friday for synthesis and Saturday/Sunday as buffer for editing and publishing.

Example: Ship #035 covers Friday Mar 13 – Thursday Mar 19, synthesized Mar 21, published the following Wednesday.

---

## The process (7 steps)

### Step 1: PM requests workstream memos

PM visits each of the 6 leadership roles and requests a workstream review memo for the coverage window. Standard set:

| Role | Slug | Workstream focus |
|------|------|-----------------|
| Principal Product Manager | ppm | Product & experience, roadmap |
| Chief Experience Officer | cxo | Design decisions, UX quality |
| Chief Architect | arch | Engineering, ADRs, infrastructure |
| Chief Innovation Officer | cio | Methodology, patterns, innovation |
| Head of Sapient Trust | host | Human network, agent welfare, AX |
| Communications Chief | comms | Publications, editorial calendar |

PM provides the coverage window dates explicitly (e.g., "Fri Mar 13 to Thu Mar 19") and asks each role to read the relevant omnibus logs before writing.

**Timing**: This typically happens in an evening session where PM visits multiple roles. Memos arrive over 1-2 hours.

### Step 2: Date audit

**Every memo must be audited for date bleed.** This is the single most common error in the process. Roles that have read current-day materials (cross-pollination briefs, recent omnibus logs, fresh mail) will inadvertently reference post-window events in their retrospective memos.

Common leaks:
- Infrastructure achievements completed after the window (e.g., blog pipeline stats from Mar 21 in a Mar 13-19 memo)
- References to materials read during the current session (newsletters, new ADRs)
- "First time" claims that are unverified
- Issue numbers from after the window

**Who audits**: PM requests each role to self-audit. PM or Documentation Management may do a second pass. The CoS does a final fact-check during synthesis.

### Step 3: Collect and standardize

PM (or Documentation Management) gathers all 6 memos, de-duplicates any that were downloaded twice, and standardizes the naming convention:

```
workstream-{ship#}-{role}-{window}.md
```

Example: `workstream-035-cxo-mar13-19.md`

All 6 memos are delivered to the Chief of Staff's inbox (`mailboxes/exec/inbox/`).

### Step 4: CoS reads all 6 before synthesizing

**Do not start writing after the first 3 memos.** Theme convergence only becomes visible when all perspectives are available simultaneously.

During the read:
- Note each memo's proposed theme (if any)
- Flag factual claims that need verification
- Track metrics that appear in multiple memos (they may differ)
- Identify the learning pattern candidate

### Step 5: CoS cross-checks and synthesizes

**Theme convergence**: Look for independent convergence — when 3+ memos land on the same topic without coordination, that's a strong signal. If themes diverge, the week may have two narrative halves.

| Ship | Theme | Convergence |
|------|-------|-------------|
| #033 | "The Cathedral Ships" | 4/6 on governance |
| #034 | "Measure First, Then Act" | Mixed — recovery + diagnostic clusters |
| #035 | "Pour the Floor" | 6/6 on floor inversion |

**Fact-checking**: Verify all claims against omnibus logs. Memos are perspectives, not sources of truth. Common errors:
- **Propagating unverified claims**: One role states something as fact, others repeat it. Always trace to primary source.
- **"First time" and superlative claims**: Require verification against omnibus log history.
- **Title errors**: Verify previous Ship title against the actual publication, not from memory or other memos.
- **Metrics reconciliation**: Different memos may report different issue counts or test numbers. Cross-reference and use the most current or conservative figure. Use "~" for approximations.

**AI-writer cliches to avoid**: "Changes Everything," "Game-Changer," "Revolutionary." Use concrete, specific themes: "Pour the Floor," "Measure First, Then Act."

**Theme approval**: Present the proposed theme and learning pattern to PM for approval before drafting. PM has final say on theme selection. Both Ships #034 and #035 involved PM review at this stage — in #035, the initial theme was rejected as a cliche and revised.

### Step 6: Draft using template v4.1

Draft the Ship using `knowledge/weekly-ship-template-v4.1.md`. Key requirements:

- **5 workstreams** in order, with emoji prefixes (Product, Engineering, Methodology, External, Governance)
- **Sentence case** on all headings
- **No tables anywhere** — LinkedIn/Medium don't render markdown tables. Metrics in Governance go as a bullet list (`**Issues closed:** 25`); the former metrics-table exception is retired (PM, 2026-07-08, Ship #050). Don't force uninteresting metrics to fill the list.
- **Hero image in External relations & community, REQUIRED** — always follow the published-pieces list with one illustration from one of the window's two Tuesday/Thursday narrative posts (the ones that publish to Medium only, not directly to LinkedIn — see `publishing-cadence.md`'s slot map). Pull alt text and caption verbatim from that post's own frontmatter, and link the image to the post on pipermorgan.ai. (PM, Ship #053 review, 2026-07-29.) This is a joint check: CoS sources and places it when drafting; Comms verifies the image/alt/caption match the source post's actual frontmatter during pre-publish review, the same way template-audit verifies frontmatter on a standalone post.
- **Learning pattern** with all 5 components (Discovery, Example, Why it matters, Application, Related patterns)
- **Previous Ship link** in footer (title must be verified)
- **Phase tag** at bottom matching current project phase
- **~800-1200 words** target. PM may approve overages for dense weeks.

### Step 7: PM review and publication

PM reviews the draft for:
- Factual accuracy (final check)
- Voice and tone
- Length appropriateness
- Theme quality

**Publication flow**:
- Draft lands in `dev/active/` or a designated drafts location
- PM publishes to LinkedIn (typically Wednesday)
- Cross-publication to pipermorgan.ai via `/publish-to-blog` skill (workflow TBD)
- Archived in project knowledge base

---

## Roles and responsibilities

| Who | Does what |
|-----|-----------|
| **PM** | Requests memos, delivers mail, reviews draft, publishes |
| **6 leadership roles** | Write workstream memos, self-audit for date bleed |
| **Documentation Management** | Standardizes memo naming, routes to exec inbox, may assist with date audits |
| **Chief of Staff** | Reads all 6, cross-checks facts, synthesizes draft, runs audit checklist |

---

## Workstream evolution

The workstream structure has evolved as the team grew:

| Version | Date | Workstreams | Notes |
|---------|------|-------------|-------|
| v1.0 | Jul 2025 | 7 project-structure streams | Original format |
| v1.5 | Nov 2025 | 6 operational streams | Reorganized around operations |
| v2.0 | Nov 7, 2025 | 7 formalized streams | Ownership + scope defined |
| Dec 2025 | Dec 4, 2025 | 6 streams | Reorganization with rationale |
| v4.0 | Jan 31, 2026 | 5 Weekly Ship streams | Current structure |
| v4.1 | Feb 25, 2026 | 5 streams (URL fix) | Current template |

The 5 Weekly Ship workstreams are a consolidation of the broader operational workstreams, optimized for the newsletter's audience and structure.

---

## Common pitfalls

These are documented from direct experience producing Ships #034 and #035:

1. **Date bleed in workstream memos** — Universal. Every role leaked post-window content in Ship #035's first pass. Build the audit into the process, not as an afterthought.

2. **Propagating memo errors into the Ship** — CoS initially accepted Comms' incorrect Ship #034 title in Ship #035. PM caught it via screenshot. Always verify against primary sources.

3. **Accepting "first time" claims** — CIO claimed Mar 19 was "first day with all 9 roles active." Mar 13 omnibus showed the same. Superlatives require proof.

4. **Cliche themes** — "Changes Everything" was proposed and rejected for Ship #035. Concrete metaphors ("Pour the Floor") outperform generic superlatives.

5. **Starting synthesis before all memos arrive** — Partial reads bias the theme toward early arrivals. Wait for all 6.

6. **Dense weeks running long** — Ship #035 came in at 1,394 words (~15% over target). PM approved the overage. Trim first, get approval if needed.

7. **Not reading the previous Ship before drafting** — The opening paragraph references the previous week's theme for narrative continuity. A new CoS instance without recent memory could misquote the theme or break the thread. Re-read the previous Ship (or at minimum verify its title and theme) before drafting the opening paragraph.

---

## Relationship to other artifacts

| Artifact | Relationship to Weekly Ship |
|----------|---------------------------|
| **Omnibus logs** | Primary source of truth for fact-checking. Memos reference them; Ship verifies against them. |
| **Workstream memos** | Direct inputs. 6 memos → 1 Ship. |
| **Template v4.1** | Structural template. Defines sections, workstreams, audit checklist. |
| **Editorial calendar CSV** | Tracks publication status. Ship publication dates recorded here. |
| **Blog pipeline** | Cross-publication channel (pipermorgan.ai). Workflow TBD. |

---

## Open questions

- **Publishing flow**: How does the Ship get from draft → LinkedIn → pipermorgan.ai? Currently manual. Under discussion.
- **Automation potential**: Memo collection and standardization could be automated. Synthesis requires context that resists automation (see omnibus automation pilot findings).
- **Workstream memo naming convention**: Standardized to `workstream-{ship#}-{role}-{window}.md` as of Ship #035. Should be documented in role briefings.

---

*Process guide v1.1 — March 22, 2026*
*Fulfills CoS Proposal 4 from infrastructure memo of March 19, 2026*
*v1.1: Incorporated CoS review feedback — added theme approval step, "read previous Ship" pitfall, confirmed pilot plan for Ship #036*
