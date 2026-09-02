# Internal Documentation

**Purpose**: Working documents for active development and internal processes
**Audience**: Development team, architects, and project contributors

**🧭 Quick Access**: For comprehensive internal navigation, see [NAVIGATION.md](../NAVIGATION.md)
**🌐 Public Docs**: For project information and user guides, see [README.md](../README.md)

---

## Directory Organization

*(Refreshed 2026-09-02 against the actual current tree — the prior list of 4 directories had
drifted from reality and one claim, below, was factually wrong.)*

- **`development/`** — current sprint/iteration work, methodologies, tools, agent coordination
- **`architecture/`** — ADRs, patterns, domain models, system design, technical guidelines
- **`planning/`** — active planning cycles, roadmap, sprint tracking
- **`operations/`** — deployment, infrastructure, monitoring, duty-cycle design
- **`product/`** — PDRs and product decision records
- **`design/`** — UX specs, design audits, interaction patterns
- **`audits/`** — dated audit records
- **`testing/`** — test strategy and canonical query test matrices
- **`retrospectives/`** — dated retrospective records

---

## Usage Guidelines

### Active vs Historical
- Most subdirectories carry their own dated/superseded content inline (banners, `historical/`
  subfolders) rather than a separate top-level archive.
- ⚠️ **Correction 2026-09-02**: this file previously claimed completed work moves to
  `/docs/archives/` — **that directory does not exist**. Don't rely on that claim; check a
  subdirectory's own convention instead (e.g. `docs/internal/testing/historical/`).

### Cross-References
- Link to superseded/historical content where it lives (in-tree, dated banners), not a central
  archive.
- Reference public documentation where appropriate.

---

## Access Patterns

### By Role
- **Developers**: Focus on `development/` and `architecture/`
- **Product Managers**: Focus on `planning/`, `product/`, and `development/`
- **Operations**: Focus on `operations/` and `architecture/`
- **Architects**: Access across all internal directories

---

*Internal documentation organization established: September 20, 2025. Directory listing refreshed
2026-09-02 (Docs, #1585) against the live tree — prior listing (4 directories) had drifted; a
false claim about a central `/docs/archives/` directory removed.*
