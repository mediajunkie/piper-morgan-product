# Internal Development Documentation

**Purpose**: Active development workflows, methodologies, and coordination
**Audience**: Development team members and contributors

---

## Directory Organization

*(Refreshed 2026-09-02 against the actual current tree — multiple claims below had drifted; see
the correction note at the bottom.)*

### Active Work (`active/`)
- **`in-progress/`** - files currently being worked on
- **`pending-review/`** - files awaiting review or feedback

### Development Methodologies (`methodology-core/`)
**50 methodology documents** (not 20 — this file previously hand-enumerated a stale 00-20 list).
**Use [`methodology-core/INDEX.md`](methodology-core/INDEX.md) as the current navigation guide**
rather than a list here — the index is the maintained surface, a duplicate list in this README
will drift again the same way the last one did.

### Development Tools (`tools/`)
Setup guides, CLI commands, Git workflows, testing infrastructure, session log templates.

### Planning (`planning/`)
Development planning documents (deprecation plans, integration plans) — not sprint-tracking in
the GitHub-Projects sense; sprint state lives on GitHub, not here.

---

## Usage Guidelines

### For Active Development
1. Place initial files in `active/in-progress/`
2. Reference the appropriate methodology via `methodology-core/INDEX.md`
3. Use setup guides and workflows from `tools/`
4. Move completed items to `active/pending-review/` for review

---

## Cross-References

### Related Internal Documentation
- **[Architecture](../architecture/)** - Technical architecture and decisions
- **[Planning](../planning/)** - Strategic and long-term planning
- **[Operations](../operations/)** - Deployment and maintenance

### ⚠️ Correction 2026-09-02 (Docs, #1585)
This file previously listed a "Related Archives" section pointing at `../../archives/session-logs/`,
`../../archives/artifacts/`, and `../../archives/decisions/` — **none of these directories exist**.
Session logs live at `dev/YYYY/MM/DD/`, not under a `docs/archives/` tree. It also described a
`ready-for-integration/` subdirectory of `active/` and a top-level `handoffs/` directory — neither
exists in the current tree. Both removed rather than left to keep misleading readers.

---

*Internal development documentation organized: September 20, 2025. Directory listing + methodology
count corrected 2026-09-02 (Docs, #1585) against the live tree.*
