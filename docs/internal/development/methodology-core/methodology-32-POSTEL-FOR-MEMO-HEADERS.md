# Postel for Memo Headers

## Overview

**Postel for Memo Headers** applies Postel's robustness principle (*"be conservative in what you do, be liberal in what you accept from others"*) to the inter-agent memo header convention. The discipline:

1. **Emit strictly**: outbound CIO memos (and any role adopting the discipline) always use YAML frontmatter for `from:` / `to:` / `cc:` / `date:` / `subject:` / `priority:` / `response-requested:` / `in-reply-to:` headers. No Markdown bold headers, no inline metadata — YAML or it isn't a header.
2. **Accept permissively**: autonomous-cycle inbound parsers extract those same fields from a **3-tier fallback chain**:
   - **Tier 1** — YAML frontmatter (`^from:` / `^subject:` / `^to:` / `^cc:`)
   - **Tier 2** — Markdown bold headers (`^\*\*From\*\*:` / `^\*\*Re\*\*:` or `^\*\*Subject\*\*:` / `^\*\*To\*\*:` / `^\*\*Cc\*\*:`)
   - **Tier 3** — first `^# ` heading (for subject only; truncate to ~120 chars)

The asymmetry is deliberate: the cohort writes memos in mixed conventions (some YAML-strict, some Markdown-bold, some informal H1-only). The autonomous-cycle parser shouldn't force everyone to adopt strict YAML; it should robustly extract field values from whatever shape the memo takes.

## Why This Methodology

### The Phase 4 v1 extractor failure (May 17, 2026)

CIO V1 Duty Cycle Phase 4 v1 cron prompt parsed inbox memos using YAML-only extraction (`grep "^from:"` etc.). The prompt fired successfully on 11 cohort memos with YAML headers. Then PM's ping memo arrived (`memo-xian-to-cio-ping-for-duty-cycle-test-2026-05-17.md`) using Markdown bold headers (`**To**: CIO`, `**From**: xian`, `**Re**: ...`) — the YAML extractor returned empty `from:` and `subject:` fields. Detection still fired (filename present in inbox); the extracted metadata was useless for categorization.

PM directive (~08:48 PT May 17): *"do both (Postel's law): be stricter in what we emit and more permissive in what we accept."* Phase 4 v2 prompt implemented the 3-tier extractor; it caught the PM ping and all subsequent inbound memos cleanly.

### Why strict-emit + permissive-accept beats either alone

| Approach | Cost | Failure mode |
|---|---|---|
| Strict on both ends | Cohort must coerce to YAML; high friction for human-friendly memo formats | Cohort writes informal memos that the parser silently mis-parses |
| Permissive on both ends | Parser tolerates inconsistency; outbound memos drift across formats over time | Recipients can't reliably parse our outbound; downstream tools fail |
| Postel (strict emit + permissive accept) | Authoring discipline at the role-level; parser has well-defined fallback chain | Tier boundary unclear when memo uses mixed conventions (rare; documented edge cases) |

The Postel asymmetry is the cheapest stable configuration: small authoring discipline on the emitter side, tolerant parser on the receiver side. The cohort doesn't have to change.

## When to apply this framing

### Apply this framing when

- Building autonomous parsers that consume cohort artifacts (memos, session logs, tracker files, escalation files). The 3-tier fallback chain is portable across all of these.
- Designing inter-role conventions where the emitter has standardization authority but the receiver has cross-cohort visibility. Same shape: emitter conforms to a strict spec; receiver tolerates legacy + variant forms.
- Codifying header / field conventions for new artifact types. Start with permissive parsing in the autonomous cycle and strict authoring in the role-specific style guide.

### This framing does not apply when

- Both sides of the interface are under unified ownership (no cohort heterogeneity to tolerate).
- The artifact format is genuinely structured (JSON, protobuf, etc.) where Postel doesn't add value — the parser fails or succeeds cleanly.
- The cost of mis-parsing is high enough to warrant strict-on-both-ends (financial transactions, code generation, anything where silent failure has downstream impact). Memos and observation logs are forgiving; rejecting a mis-extracted memo just delays its detection by one cycle.

## What it predicts

If Postel-for-memo-headers is applied correctly, the following downstream signals should appear:

- **Outbound CIO memos parse 100% cleanly via Tier 1** — strict-emit guarantees the most-common case is also the cheapest.
- **Cohort memos parse via mixed tiers without per-agent calibration** — Phase 4 v2 extractor caught Lead Dev YAML memos, Architect YAML memos, PM Markdown-bold memos, and Docs informal memos with no per-author tuning.
- **Tier 3 fallback fires rarely** — when it does, the memo is informal (PM ping, quick note); the parser still extracts a usable subject from the H1. This is the "graceful degradation" case.
- **No format-coercion friction in the cohort** — agents write memos in whatever shape fits their workflow; the autonomous parser adapts. Cross-agent extension of the cycle pattern (HOST cadence, Docs sweep, etc.) doesn't require coordinated header-format changes first.
- **New inbound format types extend the tier chain cheaply** — if a new convention emerges (e.g., JSON frontmatter, alt-text annotations), it slots in as Tier 1.5 or Tier 4 without rewriting the parser.

## Cross-references

- **methodology-31 (Append-Only Autonomous-Cycle Architecture)**: companion methodology entry filed the prior session; the 3-tier extractor lives inside the V3 cycle prompt. Postel is the parsing discipline; methodology-31 is the architectural discipline that makes the parser's outputs reliable.
- **V1 Duty Cycle design v0.4**: documents the Phase 4 v1 → v2 transition that motivated this entry.
- **CIO Phase 5 V3 cycle prompt** (in `mailboxes/cio/sent/memo-cio-...-phase-5-v3-redesign-...-2026-05-17.md`): contains the production version of the 3-tier extractor regex patterns.
- **Pattern-073 (Documentation-Asserted-Behavior Drift)**: the Postel discipline indirectly addresses a Pattern-073 variant — if outbound memos drifted to using different conventions over time, the asserted headers wouldn't match the actual extracted fields. Strict-emit prevents drift at the source.
- **methodology-28 (Pre-Filing Slot-Availability Check)**: applied to claim slot 32 (slot 30 reserved for Consumer-Trace Verification; slot 31 taken by Append-Only Architecture).

## Notes on this entry's authority + scope

Filed by CIO under self-approval per `methodology-audit-policy-updates-2026-03-16.md`. The Postel framing is general; the 3-tier extractor specification is CIO-V1-Duty-Cycle-specific but generalizes to any role adopting the autonomous-cycle pattern.

This entry does not legislate which exact YAML fields outbound memos must include — that's role-style-guide territory. It specifies the strict-emit-YAML / permissive-accept-3-tier discipline. Roles adopting the pattern parameterize the field list to their needs.

Tier ordering rationale (Tier 1 = YAML, Tier 2 = Markdown bold, Tier 3 = first H1) reflects the observed frequency distribution in the May 17 cohort sample: ~90% YAML, ~5% Markdown bold (mostly PM informal pings), ~5% H1-only (quick notes from various agents). The ordering should be revisited if the distribution shifts substantially.

---

*Filed: 2026-05-18 by CIO Vehicle 2. Pattern category: methodology-corpus parsing-and-emission discipline for inter-agent artifacts. Authority: CIO self-approval per `methodology-audit-policy-updates-2026-03-16.md`. Slot allocation: methodology-32 (pre-filing slot-availability check applied per methodology-28; slot 30 reserved for Consumer-Trace Verification; slot 31 taken by Append-Only Autonomous-Cycle Architecture).*
