#!/usr/bin/env python3
"""Mechanical citation census for methodology-core/ and patterns/ corpora.

Input: git-grep dumps (path:lineno:content) produced beforehand.
Output: census_report.md (tables + stats) and audit.md (FP-risk samples).
"""

import os, re, sys, subprocess, collections, json

REPO = "/Users/xian/Development/piper-morgan-worktrees/arch"
S = os.path.dirname(os.path.abspath(__file__))

METH_DIR = "docs/internal/development/methodology-core"
PAT_DIR = "docs/internal/architecture/current/patterns"

# ---- corpus inventories ----
meth_files = sorted(os.listdir(os.path.join(REPO, METH_DIR)))
pat_files = sorted(f for f in os.listdir(os.path.join(REPO, PAT_DIR)) if f.endswith(".md"))
pat_files.append("proposals/pattern-family-index-proposal.md")

meth_num = {}  # int -> relpath
pat_num = {}  # int -> relpath
corpus = {}  # relpath -> corpus id ('m' or 'p')
for f in meth_files:
    rel = f"{METH_DIR}/{f}"
    corpus[rel] = "m"
    m = re.match(r"methodology-(\d{2})-", f)
    if m:
        meth_num[int(m.group(1))] = rel
for f in pat_files:
    rel = f"{PAT_DIR}/{f}"
    corpus[rel] = "p"
    m = re.match(r"pattern-(\d{3})-", os.path.basename(f))
    if m:
        pat_num[int(m.group(1))] = rel

# structural index files (do not count as citations of their own corpus)
STRUCTURAL = {
    "m": {f"{METH_DIR}/INDEX.md", f"{METH_DIR}/README.md"},
    "p": {f"{PAT_DIR}/README.md"},
}

# basename-matched docs: relpath -> regex
BASENAME_RX = {
    f"{METH_DIR}/chat-protocols.md": r"(?i)\bchat-protocols(\.md)?\b",
    f"{METH_DIR}/claude-code-workflow.md": r"(?i)\bclaude-code-workflow(\.md)?\b",
    f"{METH_DIR}/enhanced-autonomy-continuity-protocols.md": r"(?i)\benhanced-autonomy-continuity-protocols(\.md)?\b",
    f"{METH_DIR}/enhanced-autonomy-experiment.md": r"(?i)\benhanced-autonomy-experiment(\.md)?\b",
    f"{METH_DIR}/gameplan-template.md": r"(?i)\bgameplan-template(\.md)?\b",
    f"{METH_DIR}/HOW_TO_USE_MULTI_AGENT.md": r"(?i)\bHOW_TO_USE_MULTI_AGENT(\.md)?\b",
    f"{METH_DIR}/MULTI_AGENT_INTEGRATION_GUIDE.md": r"(?i)\bMULTI_AGENT_INTEGRATION_GUIDE(\.md)?\b",
    f"{METH_DIR}/MULTI_AGENT_QUICK_START.md": r"(?i)\bMULTI_AGENT_QUICK_START(\.md)?\b",
    f"{METH_DIR}/multi-agent-templates.md": r"(?i)\bmulti-agent-templates(\.md)?\b",
    f"{METH_DIR}/resource-map.md": r"(?i)\bresource-map(\.md)?\b",
    f"{METH_DIR}/working-method.md": r"(?i)\bworking-method(\.md)?\b",
    f"{METH_DIR}/METHODOLOGY-DISCOVERY-GUIDE.md": r"(?i)\bMETHODOLOGY-DISCOVERY-GUIDE(\.md)?\b",
    f"{METH_DIR}/INDEX.md": r"(?i)methodology-core/INDEX\.md",
    f"{METH_DIR}/README.md": r"(?i)methodology-core/README\.md",
    f"{PAT_DIR}/README.md": r"(?i)patterns/README\.md",
    f"{PAT_DIR}/grammar-application-patterns.md": r"(?i)\bgrammar-application-patterns(\.md)?\b",
    f"{PAT_DIR}/META-PATTERNS.md": r"(?i)\bMETA-PATTERNS(\.md)?\b",
    f"{PAT_DIR}/PATTERN-FAMILIES.md": r"(?i)\bPATTERN-FAMILIES(\.md)?\b",
    f"{PAT_DIR}/PROTO-PATTERNS.md": r"(?i)\bPROTO-PATTERNS(\.md)?\b",
    f"{PAT_DIR}/pattern-000-template.md": r"(?i)\bpattern-000(-template(\.md)?)?\b",
    f"{PAT_DIR}/proposals/pattern-family-index-proposal.md": r"(?i)\bpattern-family-index-proposal(\.md)?\b",
}
BASENAME_RX = {k: re.compile(v) for k, v in BASENAME_RX.items()}

# ---- token regexes ----
METH_TOK = re.compile(r"(?i)methodolog[a-z]*[-_ /]0*(\d{1,2})\b(?!\s*(?:[%→]|->))")
M_TOK = re.compile(r"(?i)\bm-0*(\d{1,2})\b")
PAT_TOK = re.compile(r"(?i)\bpatterns?[-_ ]0*(\d{1,3})\b(?!\s*(?:[%→]|->))")
P_TOK = re.compile(r"(?i)\bp-0*(\d{1,3})\b")
CONT = re.compile(r"\s*(?:,|/|·|&|\+|–|—|-|\band\b|\bthrough\b)\s*(0*\d{1,3})\b")

DATE_RX = re.compile(r"(20\d{2})[-/](\d{2})[-/](\d{2})")

# citations[target_relpath] = dict(citer -> set of match-form strings)
citations = collections.defaultdict(lambda: collections.defaultdict(set))
audit = collections.defaultdict(list)  # risk-class -> sample lines


def parse_dump(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            raw = raw.rstrip("\n")
            parts = raw.split(":", 2)
            if len(parts) < 3:
                continue
            citer, lineno, content = parts[0], parts[1], parts[2]
            yield citer, lineno, content, raw


def add(target, citer, form, raw, risk=None):
    if target is None or citer == target:
        return
    citations[target][citer].add(form)
    if risk:
        audit[risk].append(raw[:300])


def numbers_with_continuation(rx, content, valid):
    """yield (num, form, endpos) for rx matches plus enumeration continuations."""
    out = []
    for m in rx.finditer(content):
        n = int(m.group(1))
        if n in valid:
            out.append((n, m.group(0), m.end()))
        # continuation scan regardless (list may start with an out-of-range? no)
        pos = m.end()
        while True:
            c = CONT.match(content, pos)
            if not c:
                break
            cn = int(c.group(1))
            if cn in valid and len(c.group(1)) >= 2 and len(c.group(1)) <= 3:
                out.append((cn, m.group(0) + "…" + c.group(0).strip(), c.end()))
            pos = c.end()
    return out


# ---- pass 1: methodology dump ----
for citer, lineno, content, raw in parse_dump(f"{S}/dump_meth.txt"):
    for n, form, _ in numbers_with_continuation(METH_TOK, content, meth_num.keys()):
        add(meth_num[n], citer, form, raw)

# ---- pass 2: m-NN dump ----
for citer, lineno, content, raw in parse_dump(f"{S}/dump_m.txt"):
    for m in M_TOK.finditer(content):
        n = int(m.group(1))
        if n in meth_num:
            digits = m.group(0).split("-")[1]
            risk = "m-single-digit" if len(digits) == 1 else None
            if risk:
                audit[risk].append(f"{citer}:{lineno}: {content[:240]}")
                continue  # excluded from counts; audited separately
            add(meth_num[n], citer, m.group(0), raw)

# ---- pass 3: pattern dump ----
for citer, lineno, content, raw in parse_dump(f"{S}/dump_pat.txt"):
    for m in PAT_TOK.finditer(content):
        n = int(m.group(1))
        if n not in pat_num:
            continue
        tok = m.group(0)
        # classify FP risk: unpadded, space/underscore-separated forms
        digits = re.search(r"(\d+)$", tok).group(1)
        sep = tok[len(tok) - len(digits) - 1]
        if len(digits) == 3:
            add(pat_num[n], citer, tok, raw)
        else:
            # unpadded: 'pattern-45' plausible, 'pattern 2' likely prose FP
            audit["pattern-unpadded"].append(f"{citer}:{lineno}: {content[:240]}")
            continue  # excluded from counts; audited separately
        # continuation numbers (padded lists like 'Patterns 045, 046, 047')
        pos = m.end()
        while True:
            c = CONT.match(content, pos)
            if not c:
                break
            cn = int(c.group(1))
            if cn in pat_num and len(c.group(1)) >= 3:
                add(pat_num[cn], citer, tok + "…" + c.group(0).strip(), raw)
            pos = c.end()
    # basename docs that live in this dump
    for rel, rx in BASENAME_RX.items():
        if rx.search(content):
            add(rel, citer, os.path.basename(rel), raw)

# ---- pass 4: p-NNN dump ----
for citer, lineno, content, raw in parse_dump(f"{S}/dump_p.txt"):
    for m in P_TOK.finditer(content):
        n = int(m.group(1))
        digits = m.group(0).split("-")[1]
        if n in pat_num and len(digits) == 3:
            add(pat_num[n], citer, m.group(0), raw)
        elif n in pat_num:
            audit["p-short"].append(f"{citer}:{lineno}: {content[:240]}")

# ---- pass 5: basename dump ----
for citer, lineno, content, raw in parse_dump(f"{S}/dump_base.txt"):
    for rel, rx in BASENAME_RX.items():
        if rx.search(content):
            add(rel, citer, os.path.basename(rel), raw)

# ---- manual adds (audited-genuine citations the mechanical regexes exclude) ----
MANUAL = [
    (
        f"{PAT_DIR}/pattern-029-multi-agent-coordination.md",
        f"{METH_DIR}/methodology-37-COVERAGE-AUDIT-GATE-FOR-REFACTOR-DELTAS.md",
        "Pattern-29 (unpadded, audited genuine)",
    ),
    (
        f"{PAT_DIR}/pattern-067-issue-body-reality-mismatch.md",
        "docs/public/comms/drafts/published/hypothesis-refuted.md",
        "Pattern 67 (unpadded, audited genuine)",
    ),
]
for target, citer, form in MANUAL:
    add(target, citer, form, form)


# ---- classification ----
def bucket(citer):
    if citer == "CLAUDE.md":
        return "CLAUDE.md"
    if citer.startswith(".claude/skills/"):
        return "skills"
    if citer.startswith(".claude/"):
        return ".claude-other"
    if "archive" in citer.lower():
        return "ARCHIVE"
    if citer.startswith(METH_DIR):
        return "corpus:methodology-core"
    if citer.startswith(PAT_DIR):
        return "corpus:patterns"
    if citer.startswith("docs/briefing"):
        return "docs/briefing"
    if citer.startswith("docs/agent-protocols"):
        return "docs/agent-protocols"
    if citer.startswith("docs/internal"):
        return "docs/internal"
    if citer.startswith("docs/"):
        return "docs/other"
    if citer.startswith("dev/"):
        return "dev"
    if citer.startswith("mailboxes/"):
        return "mailboxes"
    if citer.startswith("scripts/"):
        return "scripts"
    if citer.startswith(("services/", "tests/", "web/", "config/", "main.py")):
        return "code"
    if citer.startswith("knowledge/"):
        return "knowledge"
    return "other"


# ---- recency ----
git_date_cache = {}


def file_date(citer):
    m = DATE_RX.search(citer)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    if citer not in git_date_cache:
        try:
            out = subprocess.run(
                ["git", "-C", REPO, "log", "-1", "--format=%as", "--", citer],
                capture_output=True,
                text=True,
                timeout=60,
            ).stdout.strip()
            git_date_cache[citer] = out or "?"
        except Exception:
            git_date_cache[citer] = "?"
    return git_date_cache[citer]


# ---- header extraction ----
def header_info(rel):
    title = status = updated = ""
    try:
        with open(os.path.join(REPO, rel), encoding="utf-8", errors="replace") as fh:
            lines = [next(fh, "") for _ in range(40)]
    except FileNotFoundError:
        return "", "", ""
    for ln in lines:
        ln = ln.strip()
        if not title and ln.startswith("# "):
            title = ln[2:].strip()
        if not status:
            m = re.match(r"(?i)[*>\- ]*\**status\**\s*[:*]\s*(.+)", ln)
            if m:
                status = m.group(1).strip(" *")
        if not updated:
            m = re.match(
                r"(?i)[*>\- ]*\**(last[- ]?updated|updated|created|date)\**\s*[:*]\s*(.+)", ln
            )
            if m:
                updated = f"{m.group(1)}: {m.group(2).strip(' *')}"
    return title, status, updated


# ---- build report rows ----
def rows_for(corpus_id, file_list, dirprefix):
    rows = []
    for f in file_list:
        rel = f"{dirprefix}/{f}"
        cmap = citations.get(rel, {})
        real, index_only = {}, []
        for citer, forms in cmap.items():
            if citer in STRUCTURAL[corpus_id]:
                index_only.append(citer)
            else:
                real[citer] = forms
        # deduped view: drop auto-generated mailbox MANIFESTs; collapse mailbox
        # cc/sent/read copies of the same memo (same basename) to one
        nonmani = {
            c for c in real if not (c.startswith("mailboxes/") and c.endswith("MANIFEST.md"))
        }
        mb_bases = {os.path.basename(c) for c in nonmani if c.startswith("mailboxes/")}
        nonmb = [c for c in nonmani if not c.startswith("mailboxes/")]
        dedup = len(nonmb) + len(mb_bases)
        buckets = collections.Counter(bucket(c) for c in real)
        dates = sorted((file_date(c) for c in nonmani), reverse=True)
        recent = next((d for d in dates if d != "?"), "-")
        num = ""
        m = re.match(r"methodology-(\d{2})", f)
        if m:
            num = f"m-{m.group(1)}"
        m = re.match(r"pattern-(\d{3})", os.path.basename(f))
        if m:
            num = f"P-{m.group(1)}"
        title, status, updated = header_info(rel)
        rows.append(
            dict(
                file=f,
                num=num,
                count=len(real),
                dedup=dedup,
                buckets=buckets,
                recent=recent,
                index_only=bool(index_only) and not real,
                status=status,
                title=title,
                updated=updated,
                citers=sorted(real),
            )
        )
    rows.sort(key=lambda r: (r["dedup"], r["file"]))
    return rows


meth_rows = rows_for("m", meth_files, METH_DIR)
pat_rows = rows_for("p", pat_files, PAT_DIR)


def fmt_table(rows):
    out = [
        "| file | # | deduped | raw | citing dirs | most recent | status (own header) |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        b = ", ".join(f"{k}:{v}" for k, v in sorted(r["buckets"].items(), key=lambda kv: -kv[1]))
        flag = " (index-only)" if r["index_only"] else ""
        st = (r["status"] or "-")[:60]
        out.append(
            f"| {r['file']} | {r['num'] or '-'} | {r['dedup']}{flag} | {r['count']} | {b or '-'} | {r['recent']} | {st} |"
        )
    return "\n".join(out)


with open(f"{S}/census_report.md", "w") as fh:
    fh.write("## Corpus 1: methodology-core\n\n" + fmt_table(meth_rows) + "\n\n")
    fh.write("## Corpus 2: patterns\n\n" + fmt_table(pat_rows) + "\n\n")
    for name, rows in (("methodology", meth_rows), ("patterns", pat_rows)):
        zero = [r["file"] for r in rows if r["count"] == 0]
        idx = [r["file"] for r in rows if r["index_only"]]
        own = [
            r["file"]
            for r in rows
            if r["count"] > 0 and all(k.startswith("corpus:") for k in r["buckets"])
        ]
        strong = [
            r["file"] for r in rows if "CLAUDE.md" in r["buckets"] or "skills" in r["buckets"]
        ]
        fh.write(f"### Stats {name}\nzero-cited ({len(zero)}): {', '.join(zero)}\n\n")
        fh.write(f"index-only ({len(idx)}): {', '.join(idx)}\n\n")
        fh.write(f"own-corpus-only ({len(own)}): {', '.join(own)}\n\n")
        fh.write(f"cited from CLAUDE.md/skills ({len(strong)}): {', '.join(strong)}\n\n")
    fh.write("### Low-citation detail (deduped <= 6): actual citers\n")
    for rows in (meth_rows, pat_rows):
        for r in rows:
            if r["dedup"] <= 6:
                fh.write(f"- {r['file']} ({r['dedup']}): {', '.join(r['citers'])}\n")
    # detailed citers for docs cited from CLAUDE.md/skills
    fh.write("### CLAUDE.md / skills citers detail\n")
    for rows in (meth_rows, pat_rows):
        for r in rows:
            hits = [c for c in r["citers"] if bucket(c) in ("CLAUDE.md", "skills")]
            if hits:
                fh.write(f"- {r['file']}: {', '.join(hits)}\n")
    # full citer lists (compact JSON) for reproducibility
with open(f"{S}/citers_full.json", "w") as fh:
    json.dump({t: sorted(c) for t, c in citations.items()}, fh, indent=0)
with open(f"{S}/audit.md", "w") as fh:
    for k, v in audit.items():
        fh.write(f"## {k} ({len(v)})\n")
        seen = set()
        for line in v:
            if line not in seen:
                fh.write(line + "\n")
                seen.add(line)
        fh.write("\n")
# titles/updated for report composition
with open(f"{S}/headers.json", "w") as fh:
    json.dump(
        {
            r["file"]: dict(
                title=r["title"],
                status=r["status"],
                updated=r["updated"],
                recent=r["recent"],
                count=r["count"],
                buckets=dict(r["buckets"]),
            )
            for r in meth_rows + pat_rows
        },
        fh,
        indent=0,
    )
print("done. meth rows:", len(meth_rows), "pat rows:", len(pat_rows))
print("audit classes:", {k: len(v) for k, v in audit.items()})
