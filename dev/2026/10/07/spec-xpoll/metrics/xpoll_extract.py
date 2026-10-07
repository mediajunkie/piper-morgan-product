#!/usr/bin/env python3
"""xpoll_extract.py -- structured extraction of the cross-pollination brief corpus.

Run:  python3 -I xpoll_extract.py [--briefs-dir DIR] [--pm-repo DIR] [--out-dir DIR]
                                  [--skip-provenance] [--seed N]

Stdlib only. Re-runnable (outputs are overwritten; sampling is seeded).
Reads  : <briefs-dir>/*-brief.md, plus *-brief-rev*.md, plus sweep-log.md
Writes : briefs.jsonl insights.jsonl letters.jsonl corrections.jsonl
         xpoll_summary.md provenance_pilot.md  (default: directory of this script)

Principles: nothing is silently dropped. Anything that does not parse the
expected way is recorded in each record's `parse_notes` and collected in the
"Parse failures / edge cases" section of xpoll_summary.md. No quality judgement
is made anywhere in this file.
"""
import argparse
import collections
import datetime as dt
import glob
import json
import os
import random
import re
import statistics
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_BRIEFS = "/home/user/designinproduct/src/internal/briefs"
DEFAULT_PM = "/home/user/piper-morgan-product"

MONTHS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july", "august",
     "september", "october", "november", "december"], 1)}

# ----------------------------------------------------------------- front matter

def parse_front_matter(text):
    """Minimal YAML subset: scalars, quoted scalars, '  - x' lists. Returns (dict, body, notes)."""
    notes = []
    if not text.startswith("---"):
        return {}, text, ["no front matter"]
    m = re.match(r"---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if not m:
        return {}, text, ["unterminated front matter"]
    fm, key = {}, None
    for line in m.group(1).split("\n"):
        if not line.strip():
            continue
        li = re.match(r"^\s+-\s+(.*)$", line)
        if li and key is not None:
            if not isinstance(fm.get(key), list):
                fm[key] = []
            fm[key].append(unquote(li.group(1)))
            continue
        nm = re.match(r"^\s+([A-Za-z_][\w-]*):\s*(.*)$", line)
        if nm and key is not None and isinstance(fm.get(key), (list, dict)) and not (isinstance(fm.get(key), list) and fm[key]):
            if not isinstance(fm[key], dict):
                fm[key] = {}
            fm[key][nm.group(1)] = unquote(nm.group(2))
            continue
        kv = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if kv:
            key = kv.group(1)
            val = kv.group(2).strip()
            fm[key] = unquote(val) if val else []
        else:
            notes.append("unparsed front-matter line: " + line[:60])
    return fm, text[m.end():], notes


def unquote(s):
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    return s

# ----------------------------------------------------------------- markdown structure

def split_sections(body):
    """Return list of (heading, [lines]) for '## ' headings, fence-aware. Preamble has heading None."""
    secs, cur, fence = [(None, [])], None, False
    for line in body.split("\n"):
        if re.match(r"^\s*(```|~~~)", line):
            fence = not fence
        if not fence and re.match(r"^## (?!#)", line):
            secs.append((line[3:].strip(), []))
        else:
            secs[-1][1].append(line)
    return secs


def split_h3(lines):
    """Split lines into (preamble_lines, [(heading, [lines])]) on '### ' headings, fence-aware."""
    pre, blocks, fence = [], [], False
    for line in lines:
        if re.match(r"^\s*(```|~~~)", line):
            fence = not fence
        if not fence and re.match(r"^### ", line):
            blocks.append((line[4:].strip(), []))
        elif blocks:
            blocks[-1][1].append(line)
        else:
            pre.append(line)
    return pre, blocks


def canon_section(h):
    h = h.lower()
    if h.startswith("key insights"):
        return "key_insights"
    if h.startswith("emerging pattern"):
        return "emerging_patterns"
    if h.startswith("background changes"):
        return "background_changes"
    if h.startswith("sources read"):
        return "sources_read"
    if h.startswith("letters to xian"):
        return "letters"
    if h.startswith("corrections"):
        return "corrections"
    if h.startswith("cultural vocabulary"):
        return "cultural_vocabulary"
    return "other"


def words(text):
    return len(re.findall(r"\S+", text))


def strip_rules(lines):
    return [l for l in lines if not re.match(r"^\s*(-{3,}|\*{3,}|_{3,})\s*$", l)]


NONE_RE = re.compile(r"^\W*(none|nothing|no (?:new |brief-worthy |entries|items|background|emerging|patterns)[^.]{0,120})\W*$", re.I)


def split_items(lines):
    """Item splitter for Emerging Patterns / Background / Corrections. Returns (items, method)."""
    lines = strip_rules(lines)
    pre, h3 = split_h3(lines)
    if h3:
        return [(h, "\n".join(b).strip()) for h, b in h3], "h3"
    text = "\n".join(lines).strip("\n")
    if not text.strip():
        return [], "empty"
    # top-level bullets
    items, cur, fence = [], None, False
    bullets = False
    for line in lines:
        if re.match(r"^\s*(```|~~~)", line):
            fence = not fence
        if not fence and re.match(r"^([-*]|\d+\.)\s+", line):
            bullets = True
            cur = [line]
            items.append(cur)
        elif cur is not None and (line.startswith(" ") or not line.strip()):
            cur.append(line)
        elif cur is not None:
            cur = None
    if bullets:
        return [(None, "\n".join(i).strip()) for i in items], "bullets"
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    bold = [p for p in paras if p.startswith("**")]
    if bold:
        return [(None, p) for p in bold], "bold_paragraphs"
    return [(None, p) for p in paras], "paragraphs"


def is_none_item(txt):
    t = re.sub(r"\s+", " ", txt).strip()
    return len(t.split()) <= 25 and bool(NONE_RE.match(t.strip("*_ ")))

# ----------------------------------------------------------------- evidence regexes

URL_RE = re.compile(r"https?://[^\s)>\]`\"']+")
SHA_RE = re.compile(r"(?<![\w/.\-#])([0-9a-f]{7,40})(?![\w\-/]|\.\w)")
ISSUE_HASH_RE = re.compile(r"(?<![\w&/])#(\d{1,6})\b")
ISSUE_NEAR_RE = re.compile(r"\b[Ii]ssues?\s+#?(\d{3,5})\b(?:\s*(?:,|and|&|/)\s*#?(\d{3,5})\b)*")
ISSUE_NEAR_LIST_RE = re.compile(r"\b[Ii]ssues?\s+((?:#?\d{3,5}(?:\s*(?:,|and|&|/)\s*)?)+)")
PATH_PREFIXES = ("services", "docs", ".claude", "dev", "scripts", "tests", "web", "config",
                 "knowledge", "mailboxes", "src", "development", "cli", "app", "lib", "internal",
                 "packages", "server", "client", "alembic", "templates", "prompts", "skills",
                 "metrics", "data", "public", "content", "piper-morgan-product", "mediajunkie",
                 "klatch", "one-job", "dispatch", "hooks", "agent", "agents", "core", "api",
                 "tools", "tooling", "ops", "research", "specs")
PATH_RE = re.compile(r"(?<![\w/:.\-])((?:%s)/[^\s`)\]\[,;'\"<>|]*[\w/*}])" %
                     "|".join(re.escape(p) for p in PATH_PREFIXES))
BT_PATH_RE = re.compile(r"`([\w.\-]+(?:/[\w.\-*{}]+)+\.\w{1,5})`")
ID_RES = {
    "adr": re.compile(r"\bADR-\d+\b"),
    "pdr": re.compile(r"\bPDR-\d+\b"),
    "m": re.compile(r"(?<![\w-])m-\d+\b"),
    "methodology": re.compile(r"\bmethodology-\d+\b", re.I),
    "pattern": re.compile(r"\bPattern-\d+\b"),
}


def uniq(seq):
    seen, out = set(), []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def extract_evidence(text):
    urls = uniq(u.rstrip(".,;:") for u in URL_RE.findall(text))
    nourl = URL_RE.sub(" ", text)
    shas = []
    for m in SHA_RE.finditer(nourl):
        s = m.group(1)
        # need >=1 digit AND >=1 letter, and not a pure date/number run
        if re.search(r"\d", s) and re.search(r"[a-f]", s):
            shas.append(s)
    issues = [int(x) for x in ISSUE_HASH_RE.findall(nourl)]
    bare = []
    for m in ISSUE_NEAR_LIST_RE.finditer(nourl):
        bare += [int(n) for n in re.findall(r"\d{3,5}", m.group(1))]
    paths = [p.rstrip(".:") for p in PATH_RE.findall(nourl)]
    paths += BT_PATH_RE.findall(nourl)
    paths = uniq(p for p in paths if "://" not in p)
    ids = {k: uniq(r.findall(nourl)) for k, r in ID_RES.items()}
    return {
        "shas": uniq(shas),
        "issues_hash": uniq(issues),
        "issues_bare_near_issue": uniq(i for i in bare if i not in issues),
        "paths": paths,
        "adr": ids["adr"], "pdr": ids["pdr"], "m_ids": ids["m"],
        "methodology": [x.lower() for x in ids["methodology"]], "patterns": ids["pattern"],
        "urls": urls,
    }

# ----------------------------------------------------------------- project normalisation

PROJ_PATTERNS = [
    ("piper-morgan", r"piper[ -]morgan|\bPM\b|piper-morgan-product"),
    ("klatch", r"klatch|\bCalliope\b|\bDaedalus\b|\bArgus\b|\bTheseus\b|\bIris\b|\bVergil\b"),
    ("one-job", r"one[ -]job|\bCoral\b"),
    ("dinp", r"design in product|\bDinP\b|designinproduct|\bJanus\b"),
    ("mediajunkie", r"mediajunkie|\bPard\b"),
    ("openlaws", r"openlaws"),
    ("atlas", r"\batlas\b"),
    ("globe", r"\bglobe\b"),
    ("cuneo", r"\bcuneo\b"),
    ("weather", r"\bweather\b"),
    ("nyt-crossword", r"crossword"),
]


def norm_projects(s):
    if not s:
        return []
    return [name for name, pat in PROJ_PATTERNS if re.search(pat, s, re.I)]


def norm_audience(s):
    """relevant_to -> list of project slugs plus 'any' if generic wording."""
    if not s:
        return []
    out = norm_projects(s)
    if re.search(r"\b(any|every|all|anyone|each)\b", s, re.I):
        out.append("any/generic")
    return out

# ----------------------------------------------------------------- sweep log

def parse_sweep_log(path):
    rows = collections.defaultdict(list)
    first = None
    if not os.path.exists(path):
        return rows, None, ["sweep-log.md not found"]
    notes = []
    for line in open(path, encoding="utf-8"):
        m = re.match(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*([^|]*)\|\s*([^|]*)\|\s*(.*?)\s*\|?\s*$", line)
        if m:
            d = m.group(1)
            rows[d].append({"time": m.group(2).strip(), "outcome": m.group(3).strip(), "notes": m.group(4).strip()})
            first = d if first is None or d < first else first
        elif line.startswith("|") and not re.match(r"^\|[-\s|]+\|?$", line) and not line.startswith("| Date"):
            notes.append("unparsed sweep-log row: " + line[:80].strip())
    return rows, first, notes

# ----------------------------------------------------------------- brief parsing

def month_day_to_date(month, day, year_hint):
    try:
        return dt.date(year_hint, MONTHS[month.lower()], int(day)).isoformat()
    except Exception:
        return None


def parse_brief(path, sweep, sweep_first):
    fn = os.path.basename(path)
    text = open(path, encoding="utf-8").read()
    fm, body, fm_notes = parse_front_matter(text)
    notes = list(fm_notes)
    date = fm.get("date")
    fn_date = re.match(r"(\d{4}-\d{2}-\d{2})", fn)
    fn_date = fn_date.group(1) if fn_date else None
    if not date:
        notes.append("no date in front matter; used filename")
        date = fn_date
    elif fn_date and date != fn_date:
        notes.append("front-matter date %s != filename date %s" % (date, fn_date))
    is_rev = bool(re.search(r"-brief-rev\d+\.md$", fn))
    if is_rev:
        notes.append("revision file (rev) -- same date as a primary brief")

    secs = split_sections(body)
    inventory = [h for h, _ in secs if h]
    canon = [canon_section(h) for h in inventory]
    secmap = collections.defaultdict(list)
    for h, ls in secs:
        if h:
            secmap[canon_section(h)].append((h, ls))

    rec = {
        "filename": fn,
        "date": date,
        "is_revision_file": is_rev,
        "status": fm.get("status"),
        "window": fm.get("window"),
        "sources_checked": fm.get("sources_checked") if isinstance(fm.get("sources_checked"), list) else [],
        "projects_covered": fm.get("sources_checked") if isinstance(fm.get("sources_checked"), list) else [],
        "secondary_provenance": ([k + " \u00b7 " + v for k, v in fm["secondary_provenance"].items()] if isinstance(fm.get("secondary_provenance"), dict)
                                 else fm.get("secondary_provenance") if isinstance(fm.get("secondary_provenance"), list) else []),
        "frontmatter_keys": sorted(fm.keys()),
        "title": fm.get("title"),
        "word_count": words(body),
        "word_count_total_incl_frontmatter": words(text),
        "section_inventory": inventory,
        "section_inventory_canonical": uniq(canon),
    }

    # ---- sweep join
    runs = sweep.get(date, []) if date else []
    if runs:
        rec["has_sweep_log_entry"] = True
    elif sweep_first and date and date < sweep_first:
        rec["has_sweep_log_entry"] = None   # unverified: predates sweep-log
        notes.append("has_sweep_log_entry unverified: brief predates sweep-log (first row %s)" % sweep_first)
    else:
        rec["has_sweep_log_entry"] = False if sweep_first else None
    rec["sweep_log_runs"] = [{"time": r["time"], "outcome": r["outcome"]} for r in runs]

    # ---- key insights
    insights = []
    ki_note = None
    for h, ls in secmap.get("key_insights", []):
        pre, blocks = split_h3(ls)
        pre_txt = "\n".join(strip_rules(pre)).strip()
        if not blocks and pre_txt:
            ki_note = pre_txt[:300]
        for idx, (bh, bl) in enumerate(blocks, 1):
            m = re.match(r"^(\d+)\.\s+(.*)$", bh)
            if m:
                ordinal, heading, numbered = int(m.group(1)), m.group(2).strip(), True
            else:
                ordinal, heading, numbered = idx, bh.strip(), False
            insights.append((ordinal, heading, numbered, idx, bl))
    ins_records = []
    for ordinal, heading, numbered, pos, bl in insights:
        ins_records.append(build_insight(date, fn, ordinal, heading, numbered, pos, bl, len(insights)))
    if insights and any(not n for _, _, n, _, _ in insights) and any(n for _, _, n, _, _ in insights):
        notes.append("mixed numbered/unnumbered insight headings")
    nums = [o for o, _, n, _, _ in insights if n]
    if nums and nums != list(range(1, len(nums) + 1)):
        notes.append("insight ordinals not 1..N consecutive: %s" % nums)
    if "key_insights" not in secmap:
        notes.append("no '## Key Insights' section")
    elif not insights:
        notes.append("Key Insights section present with zero '###' headings (note: %s)" % (ki_note or "none")[:120])
    if rec["status"] == "nominal" and insights:
        notes.append("status nominal but insights present")
    if rec["status"] == "substantive" and not insights:
        notes.append("status substantive but zero insights parsed")

    # ---- emerging / background
    def count_section(key):
        total, method, items_out = 0, None, []
        for h, ls in secmap.get(key, []):
            items, method = split_items(ls)
            real = [(a, b) for a, b in items if not is_none_item(b if a is None else (a + " " + b))]
            total += len(real)
            items_out += real
        return total, method, items_out

    rec["n_insights"] = len(ins_records)
    rec["n_insights_numbered"] = sum(1 for r in ins_records if r["heading_numbered"])
    rec["n_insights_unnumbered"] = sum(1 for r in ins_records if not r["heading_numbered"])
    ep, ep_m, _ = count_section("emerging_patterns")
    bg, bg_m, _ = count_section("background_changes")
    rec["n_emerging_patterns"], rec["emerging_patterns_item_method"] = ep, ep_m
    rec["n_background_items"], rec["background_item_method"] = bg, bg_m

    # ---- corrections
    corr_records = []
    for h, ls in secmap.get("corrections", []):
        items, method = split_items(ls)
        if method in ("bullets", "paragraphs") and len(items) > 1:
            notes.append("corrections section split by '%s' into %d items (heuristic)" % (method, len(items)))
        for n, (ih, itxt) in enumerate(items, 1):
            corr_records.append(build_correction(date, fn, h, n, ih, itxt, method, os.path.dirname(path)))
    rec["n_corrections"] = len(corr_records)

    # ---- letters
    letters = []
    for h, ls in secmap.get("letters", []):
        letters += parse_letters(date, fn, ls, notes)
    rec["n_letters"] = len(letters)
    rec["parse_notes"] = notes
    rec["_key_insights_note"] = ki_note
    return rec, ins_records, letters, corr_records


META_RE = re.compile(r"^\*\*(From|Relevant to|Why this matters now|Suggested action[^*]*)\s*:?\s*\*\*\s*:?\s*(.*)$", re.I)


def build_insight(date, fn, ordinal, heading, numbered, pos, bl, n_total):
    lines = strip_rules(bl)
    # metadata lines
    frm = rel = why = None
    sugg_lines, sugg_label = [], None
    cur = None
    body_lines = []
    fence = False
    for line in lines:
        if re.match(r"^\s*(```|~~~)", line):
            fence = not fence
        mm = None if fence else re.match(r"^\*\*(From|Relevant to|Why this matters now|Suggested action[^*]*?)\s*:?\*\*\s*:?\s*(.*)$", line.strip(), re.I)
        if not mm:
            # label inside the bold: **Suggested action:** text  (colon inside bold)
            mm = None if fence else re.match(r"^\*\*(From|Relevant to|Why this matters now|Suggested action[^*]*?):\*\*\s*(.*)$", line.strip(), re.I)
        if mm:
            label = mm.group(1).strip().lower()
            val = mm.group(2).strip()
            if label == "from":
                frm, cur = val, "from"
            elif label == "relevant to":
                rel, cur = val, "rel"
            elif label.startswith("why this matters"):
                why, cur = val, "why"
            else:
                sugg_label = mm.group(1).strip()
                sugg_lines = [val]
                cur = "sugg"
            body_lines.append(line)
            continue
        if cur == "sugg" and line.strip():
            sugg_lines.append(line.strip())
        elif cur == "sugg" and not line.strip():
            cur = None
        elif cur in ("from", "rel", "why") and line.strip():
            # continuation of a metadata line (no blank between)
            if cur == "from":
                frm += " " + line.strip()
            elif cur == "rel":
                rel += " " + line.strip()
            else:
                why += " " + line.strip()
        elif not line.strip():
            cur = None if cur not in ("sugg",) else cur
        body_lines.append(line)
    block_text = "\n".join(lines)
    body_text = "\n".join(body_lines)
    ev_all = extract_evidence(heading + "\n" + block_text)
    ev_body = extract_evidence(heading + "\n" + "\n".join(l for l in lines if not re.match(r"^\*\*From", l.strip(), re.I)))
    ev_from = extract_evidence(frm or "")
    from_src = "from_line" if frm else None
    from_projects = norm_projects(frm) if frm else []
    if not frm:
        from_projects = norm_projects(heading)
        from_src = "heading_keyword" if from_projects else "none"
    sugg_text = " ".join(sugg_lines).strip() if sugg_lines else None
    notes = []
    if not numbered:
        notes.append("heading not '### N.' form; ordinal is positional")
    if not frm:
        notes.append("no **From:** line")
    # the 'Suggested action' might be present as plain text without the bold marker
    if sugg_text is None and re.search(r"suggested action", block_text, re.I):
        notes.append("'suggested action' text present but not as **Suggested action** line")
    rec = {
        "id": "%s#%d" % (date, ordinal),
        "brief_date": date,
        "brief_file": fn,
        "ordinal": ordinal,
        "position": pos,
        "n_in_brief": n_total,
        "heading_numbered": numbered,
        "heading": heading,
        "from": frm,
        "from_source": from_src,
        "from_projects": from_projects,
        "relevant_to": rel,
        "relevant_to_projects": norm_audience(rel),
        "body_words": words(block_text),
        "body_words_excl_meta_lines": words("\n".join(l for l in lines if not META_RE.match(l.strip()))),
        "has_suggested_action": sugg_text is not None,
        "suggested_action_label": sugg_label,
        "suggested_action": sugg_text,
        "why_this_matters_now": why,
        "commit_shas": ev_all["shas"],
        "commit_shas_in_from_line": ev_from["shas"],
        "issue_refs": ["#%d" % i for i in ev_all["issues_hash"]],
        "issue_refs_bare_near_issue": ev_all["issues_bare_near_issue"],
        "repo_paths": ev_all["paths"],
        "repo_paths_in_from_line": ev_from["paths"],
        "repo_paths_excl_from_line": ev_body["paths"],
        "adr_ids": ev_all["adr"], "pdr_ids": ev_all["pdr"],
        "m_ids": ev_all["m_ids"], "methodology_ids": ev_all["methodology"],
        "pattern_ids": ev_all["patterns"],
        "urls": ev_all["urls"],
        "parse_notes": notes,
    }
    return rec


def build_correction(date, fn, sec_heading, n, ih, itxt, method, briefs_dir):
    lead = (ih or "") + " " + itxt[:400]
    year = int(date[:4]) if date else 2026
    target_date, kind = None, None
    m = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", lead)
    if m:
        target_date = m.group(1)
    else:
        m = re.search(r"\b(%s)\s+(\d{1,2})\b" % "|".join(k.capitalize() for k in MONTHS), lead)
        if m:
            target_date = month_day_to_date(m.group(1), m.group(2), year)
    if re.search(r"weekly digest|digest", lead, re.I):
        kind = "weekly_digest"
    elif re.search(r"\bbrief\b", lead, re.I):
        kind = "brief"
    mo = re.search(r"\b(?:item|insight)\s+(\d+)\b", lead, re.I)
    ordinal = int(mo.group(1)) if mo else None
    target_exists = None
    if target_date and kind == "brief":
        target_exists = os.path.exists(os.path.join(briefs_dir, target_date + "-brief.md"))
    return {
        "brief_date": date, "brief_file": fn, "section_heading": sec_heading, "ordinal_in_section": n,
        "item_split_method": method, "item_heading": ih,
        "text": itxt, "text_words": words(itxt),
        "corrects_date": target_date, "corrects_kind": kind, "corrects_ordinal": ordinal,
        "corrects_target_file_exists": target_exists,
        "corrects_date_is_stated": target_date is not None,
    }


LETTER_HDR = re.compile(r"^\*\*From\s+(.+?)\s*·\s*filed\s+([^·*]+?)(?:\s*·\s*(.*?))?\*\*\s*$")


def parse_letters(date, fn, ls, notes):
    out, cur = [], None
    lines = list(ls)
    for line in lines:
        m = LETTER_HDR.match(line.strip())
        if m:
            cur = {"hdr": m, "lines": []}
            out.append(cur)
        elif cur is not None:
            cur["lines"].append(line)
    recs = []
    if not out:
        txt = "\n".join(strip_rules(ls)).strip()
        if txt:
            notes.append("Letters section present but no '**From X · filed D**' header parsed")
            recs.append({"brief_date": date, "brief_file": fn, "letter_id": None, "from": None,
                         "filed": None, "status_text": None, "question": None, "answer_present": None,
                         "parse_notes": ["unparsed letters section: " + txt[:120]]})
        return recs
    for c in out:
        m = c["hdr"]
        frm, filed, extra = m.group(1).strip(), m.group(2).strip(), (m.group(3) or "").strip()
        body = c["lines"]
        q, ans, in_q, in_ans, rest = [], [], False, False, []
        for line in body:
            s = line.strip()
            if s.startswith("[Read the full") or s.startswith("*Canonical archive") or re.match(r"^-{3,}$", s):
                in_ans = False
                if s.startswith("[Read the full") or s.startswith("*Canonical"):
                    rest.append(s)
                continue
            if s.startswith(">") and not in_ans and not ans:
                q.append(s.lstrip("> ").strip())
                in_q = True
                continue
            if re.match(r"^\*\*xian:\*\*", s):
                in_ans = True
                after = re.sub(r"^\*\*xian:\*\*\s*", "", s)
                if after:
                    ans.append(after)
                continue
            if re.match(r"^xian'?s answer", s, re.I):
                in_ans = True
                ans.append(s)
                continue
            if in_ans and s:
                ans.append(s.lstrip("> ").strip())
        ans_txt = " ".join(ans).strip()
        placeholder = bool(ans_txt) and bool(re.search(r"reply expected|answer (is )?(incoming|in progress)|in progress|watch a coming brief", ans_txt, re.I)) and words(ans_txt) < 25
        if placeholder:
            ans_txt_raw, ans_txt = ans_txt, ""
        else:
            ans_txt_raw = ans_txt
        q_txt = " ".join(q).strip()
        low = (extra + " " + ans_txt).lower()
        hdr_status = ("answered" if "answered" in extra.lower() else
                      "awaiting" if "awaiting" in extra.lower() else
                      "incoming" if "incoming" in extra.lower() else
                      "in_progress" if "in progress" in extra.lower() else
                      "other:" + extra if extra else "none")
        ans_ans = re.search(r"answered\s+(.+)$", extra, re.I)
        pn = []
        if not q_txt:
            pn.append("no blockquote question parsed")
        recs.append({
            "brief_date": date, "brief_file": fn,
            "letter_id": "%s@%s" % (re.sub(r"\s+", " ", frm), filed),
            "from": frm, "from_project": (norm_projects(frm) or [None])[0],
            "filed": filed, "answered_date_raw": ans_ans.group(1).strip() if ans_ans else None,
            "header_status": hdr_status, "status_text": extra or None,
            "question": q_txt, "question_words": words(q_txt),
            "answer_text": ans_txt or None, "answer_words": words(ans_txt),
            "answer_present": bool(ans_txt),
            "answer_placeholder_only": placeholder,
            "answer_placeholder_text": ans_txt_raw if placeholder else None,
            "answer_present_and_header_answered": bool(ans_txt) and hdr_status == "answered",
            "full_exchange_link": next((r for r in rest if r.startswith("[Read the full")), None),
            "parse_notes": pn,
        })
    return recs

# ----------------------------------------------------------------- git helpers

def git(repo, *args):
    p = subprocess.run(["git", "-C", repo] + list(args), capture_output=True, text=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()

# ----------------------------------------------------------------- provenance pilot

def provenance(ins, repo, seed, out_path):
    L = []
    L.append("# Provenance pilot\n")
    L.append("Generated by `metrics/xpoll_extract.py` (seed %d). Layer: script over corpus + `git` queries against `%s`." % (seed, repo))
    rc, head, _ = git(repo, "rev-parse", "--verify", "-q", "origin/main")
    ref = "origin/main" if rc == 0 else "HEAD"
    rc2, sh, _ = git(repo, "rev-parse", "--is-shallow-repository")
    rc3, cnt, _ = git(repo, "rev-list", "--count", ref)
    rc4, first, _ = git(repo, "log", "--reverse", "--format=%cs", ref, "--max-parents=0")
    L.append("Repo ref used: `%s` (%s commits; shallow=%s; root commit date %s)\n" % (ref, cnt, sh, first.split("\n")[0] if first else "?"))

    # ---------- SHA check
    sha_ins = [r for r in ins if r["commit_shas"]]
    all_shas = uniq(s for r in sha_ins for s in r["commit_shas"])
    res = {}
    for s in all_shas:
        p = subprocess.run(["git", "-C", repo, "cat-file", "-e", s + "^{commit}"], capture_output=True, text=True)
        if p.returncode == 0:
            res[s] = "resolves"
        elif "ambiguous" in p.stderr.lower():
            res[s] = "ambiguous"
        else:
            res[s] = "not-found"

    def attrib(r):
        fp = set(r["from_projects"])
        if fp == {"piper-morgan"}:
            return "PM-attributed"
        if not fp:
            return "unattributed"
        if "piper-morgan" in fp:
            return "mixed (PM + other)"
        return "non-PM"

    L.append("## 1. Commit SHA resolution (`git cat-file -e <sha>^{commit}`)\n")
    L.append("Layer: git history of PM repo. Candidate SHAs are regex hits: 7-40 hex chars containing at least one digit and one a-f letter, "
             "excluding URLs. Regex hits can include non-SHA tokens; they would appear as not-found. SHAs from Klatch / One Job / other "
             "repos cannot be resolved here and will also read as not-found.\n")
    L.append("- Insights in corpus: %d; insights with >=1 candidate SHA: %d (%.1f%%)" % (len(ins), len(sha_ins), 100.0 * len(sha_ins) / max(1, len(ins))))
    L.append("- Distinct candidate SHAs: %d; resolves: %d, not-found: %d, ambiguous: %d\n" % (
        len(all_shas), sum(v == "resolves" for v in res.values()), sum(v == "not-found" for v in res.values()), sum(v == "ambiguous" for v in res.values())))
    L.append("Per-SHA occurrences by insight attribution (attribution = projects named in the insight's From line, or heading if no From line; "
             "this is a keyword heuristic, not ground truth):\n")
    L.append("| attribution | insights w/ SHA | SHA mentions | resolves | not-found | ambiguous | resolve rate |")
    L.append("|---|---|---|---|---|---|---|")
    by = collections.defaultdict(lambda: collections.Counter())
    nins = collections.Counter()
    for r in sha_ins:
        a = attrib(r)
        nins[a] += 1
        for s in r["commit_shas"]:
            by[a][res[s]] += 1
            by[a]["total"] += 1
    for a in ["PM-attributed", "mixed (PM + other)", "non-PM", "unattributed"]:
        c = by[a]
        t = c["total"]
        L.append("| %s | %d | %d | %d | %d | %d | %s |" % (a, nins[a], t, c["resolves"], c["not-found"], c["ambiguous"],
                                                      ("%.1f%%" % (100.0 * c["resolves"] / t)) if t else "n/a"))
    tot = collections.Counter()
    for a in by:
        tot.update(by[a])
    L.append("| **all** | %d | %d | %d | %d | %d | %.1f%% |\n" % (len(sha_ins), tot["total"], tot["resolves"], tot["not-found"], tot["ambiguous"],
                                                             100.0 * tot["resolves"] / max(1, tot["total"])))
    # insight-level for PM-attributed
    pm_ins = [r for r in sha_ins if attrib(r) == "PM-attributed"]
    allres = sum(1 for r in pm_ins if all(res[s] == "resolves" for s in r["commit_shas"]))
    anyres = sum(1 for r in pm_ins if any(res[s] == "resolves" for s in r["commit_shas"]))
    L.append("PM-attributed insights citing SHAs: %d. All cited SHAs resolve: %d; at least one resolves: %d; none resolve: %d." % (
        len(pm_ins), allres, anyres, len(pm_ins) - anyres))
    nf = [(r["id"], [s for s in r["commit_shas"] if res[s] != "resolves"]) for r in pm_ins if any(res[s] != "resolves" for s in r["commit_shas"])]
    L.append("\nPM-attributed insights with at least one non-resolving SHA (up to 40 listed; verify by hand -- may be non-PM SHAs cited in a PM-attributed insight, or regex false positives):\n")
    for i, ss in nf[:40]:
        L.append("- %s: %s" % (i, ", ".join("`%s`" % s for s in ss)))
    if len(nf) > 40:
        L.append("- ... %d more" % (len(nf) - 40))
    L.append("")

    # ---------- path check
    L.append("## 2. Repo-path existence at brief date\n")
    path_ins = [r for r in ins if r["repo_paths"]]
    L.append("Layer: git history of PM repo. Insights with >=1 candidate repo path: %d of %d (%.1f%%).\n" % (
        len(path_ins), len(ins), 100.0 * len(path_ins) / max(1, len(ins))))
    rng = random.Random(seed)

    def check_path(path, date):
        p = re.sub(r":\d+(?:-\d+)?$", "", re.sub(r"^piper-morgan-product/", "", path))
        if any(ch in p for ch in "*{}") or "..." in p or "…" in p:
            return "uncheckable (glob/ellipsis)", None, None
        until = date + " 23:59:59 +0000"
        rc, out, _ = git(repo, "log", "-1", "--format=%h", "--until=" + until, ref, "--", p)
        log_hit = bool(out)
        rc, commit, _ = git(repo, "rev-list", "-1", "--until=" + until, ref)
        exists = None
        if commit:
            p2 = subprocess.run(["git", "-C", repo, "cat-file", "-e", "%s:%s" % (commit, p.rstrip("/"))], capture_output=True, text=True)
            exists = p2.returncode == 0
        return ("hit" if log_hit else "miss"), log_hit, exists

    def run_sample(label, pool, k):
        sample = rng.sample(pool, min(k, len(pool)))
        L.append("### %s (n=%d sampled of %d eligible)\n" % (label, len(sample), len(pool)))
        L.append("`log_hit` = `git log -1 --until=<brief date> -- <path>` returns a commit (path was touched at or before the date; says nothing about later deletion). "
                 "`exists_at_date` = `git cat-file -e <last commit before date>:<path>` (path present in the tree at that time).\n")
        L.append("| insight | attribution | path | log_hit | exists_at_date |")
        L.append("|---|---|---|---|---|")
        n_paths = n_hit = n_ex = n_unch = 0
        ins_any_hit = ins_all_hit = 0
        for r in sorted(sample, key=lambda x: x["id"]):
            hits = []
            for pth in r["repo_paths"]:
                st, lh, ex = check_path(pth, r["brief_date"])
                if st.startswith("uncheckable"):
                    n_unch += 1
                else:
                    n_paths += 1
                    n_hit += 1 if lh else 0
                    n_ex += 1 if ex else 0
                    hits.append(lh)
                L.append("| %s | %s | `%s` | %s | %s |" % (r["id"], attrib(r), pth[:90], st if st.startswith("unch") else lh, ex))
            if hits:
                ins_any_hit += any(hits)
                ins_all_hit += all(hits)
        L.append("")
        L.append("Result: %d checkable paths (+%d uncheckable) across %d insights; log_hit %d (%.1f%%); exists_at_date %d (%.1f%%). "
                 "Insights with any hit: %d; with all checkable paths hit: %d.\n" % (
                     n_paths, n_unch, len(sample), n_hit, 100.0 * n_hit / max(1, n_paths), n_ex, 100.0 * n_ex / max(1, n_paths), ins_any_hit, ins_all_hit))
        return n_paths, n_hit, n_ex

    run_sample("Sample A: 20 random insights citing a repo path (all attributions)", path_ins, 20)
    pm_path = [r for r in path_ins if attrib(r) == "PM-attributed"]
    run_sample("Sample B: 20 random PM-attributed insights citing a repo path", pm_path, 20)
    L.append("## Caveats\n")
    L.append("- Only the PM repo is checked; paths and SHAs belonging to Klatch, One Job, DinP, Mediajunkie etc. cannot be verified here, so non-PM rows are expected to miss and are not evidence of fabrication.")
    L.append("- Attribution is a keyword heuristic on the From line; a PM-attributed insight can still cite another repo's path or SHA.")
    L.append("- `log_hit` is a weak existence test (touched before date). `exists_at_date` is the stronger test but paths are as written in prose (may be abbreviated, relative to a subdirectory, or point to untracked/gitignored files).")
    L.append("- Cited files such as omnibus logs may be written after the event the brief covers; for retrospective briefs a miss at the brief date can mean the file did not yet exist (exists_at_date=None means no PM commit existed before that date).\n- Trailing `:LINE` suffixes are stripped before checking.\n- Sampling is seeded (%d) so reruns reproduce, but only if the corpus is unchanged." % seed)
    open(out_path, "w", encoding="utf-8").write("\n".join(L) + "\n")
    return res

# ----------------------------------------------------------------- summary

def pct(a, b):
    return "%.1f%%" % (100.0 * a / b) if b else "n/a"


def table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return "\n".join(out)


def summary(briefs, ins, letters, corrs, out_path, sweep_first, sweep_notes, briefs_dir):
    L = []
    P = L.append
    P("# Cross-pollination corpus: extraction summary\n")
    P("Generated by `metrics/xpoll_extract.py`. Layer: script over corpus (`%s`). Static parse only; no quality judgement. "
      "Every percentage states its denominator." % briefs_dir)
    P("")
    nb = len(briefs)
    prim = [b for b in briefs if not b["is_revision_file"]]
    dates = sorted(b["date"] for b in briefs)
    P("## 1. Corpus\n")
    P("- Brief files parsed: **%d** (%d `*-brief.md` + %d revision file(s)); date range %s to %s." % (nb, len(prim), nb - len(prim), dates[0], dates[-1]))
    P("- Distinct brief dates: %d. Records: insights %d, letters occurrences %d (distinct letters %d), corrections %d." % (
        len(set(dates)), len(ins), len(letters), len(set(l["letter_id"] for l in letters if l["letter_id"])), len(corrs)))
    late = [d for d in set(dates) if d >= "2026-03-01"]
    span = (dt.date.fromisoformat(dates[-1]) - dt.date(2026, 3, 1)).days + 1
    P("- Coverage: before 2026-03 the corpus is sparse retrospective/weekly briefs (%d files); from 2026-03-01 to %s there are %d distinct brief dates over %d calendar days (%d missing dates: %s)." % (
        len([d for d in set(dates) if d < "2026-03-01"]), dates[-1], len(late), span, span - len(late),
        ", ".join(sorted(d.isoformat() for d in (dt.date(2026, 3, 1) + dt.timedelta(n) for n in range(span)) if d.isoformat() not in set(dates))) or "none"))
    P("")
    # by month and status
    P("## 2. Briefs by month and status (denominator: %d briefs)\n" % nb)
    bym = collections.defaultdict(collections.Counter)
    for b in briefs:
        bym[b["date"][:7]][b["status"] or "?"] += 1
    sts = sorted({b["status"] or "?" for b in briefs})
    rows = [[m] + [bym[m][s] for s in sts] + [sum(bym[m].values())] for m in sorted(bym)]
    rows.append(["**total**"] + [sum(bym[m][s] for m in bym) for s in sts] + [nb])
    P(table(["month"] + sts + ["all"], rows))
    P("")
    # insights per brief
    P("## 3. Insights per brief\n")
    P("The sweep spec says \"most windows produce 0-2; four would be an extremely unlikely maximum\". Actual histogram (denominator: %d briefs; counts = parsed `###` insight headings under `## Key Insights`, numbered or not):\n" % nb)
    hist = collections.Counter(b["n_insights"] for b in briefs)
    mx = max(hist)
    rows = [[k, hist.get(k, 0), pct(hist.get(k, 0), nb), "#" * hist.get(k, 0) if hist.get(k, 0) < 80 else "#" * 80] for k in range(0, mx + 1)]
    P(table(["insights", "briefs", "share", ""], rows))
    over4 = [b for b in briefs if b["n_insights"] > 4]
    over2 = [b for b in briefs if b["n_insights"] > 2]
    P("\n- Briefs exceeding 4 insights: **%d of %d (%s)**; exceeding 2: %d (%s). Max = %d. Mean %.2f, median %s." % (
        len(over4), nb, pct(len(over4), nb), len(over2), pct(len(over2), nb), mx,
        statistics.mean(b["n_insights"] for b in briefs), statistics.median(b["n_insights"] for b in briefs)))
    P("- Briefs with >4 insights, by month: " + ", ".join("%s: %d" % (m, c) for m, c in sorted(collections.Counter(b["date"][:7] for b in over4).items())) + ".")
    P("- Insights per brief by month (mean over briefs in month):\n")
    mm = collections.defaultdict(list)
    for b in briefs:
        mm[b["date"][:7]].append(b["n_insights"])
    P(table(["month", "briefs", "insights", "mean/brief", "max"], [[m, len(v), sum(v), "%.2f" % statistics.mean(v), max(v)] for m, v in sorted(mm.items())]))
    P("")
    # by source project and audience
    P("## 4. Insights by source project and by stated audience (denominator: %d insights)\n" % len(ins))
    P("Source project = keyword match on the `**From:**` line (fallback: heading). An insight may name several projects, so counts overlap. "
      "Aliases: Pard->mediajunkie, Coral->one-job, Janus->dinp, Calliope/Daedalus/Argus/Theseus/Iris/Vergil->klatch (heuristic).\n")
    c = collections.Counter()
    for r in ins:
        for p in r["from_projects"] or ["(none resolved)"]:
            c[p] += 1
    P(table(["source project", "insights", "share of %d" % len(ins)], [[k, v, pct(v, len(ins))] for k, v in c.most_common()]))
    fs = collections.Counter(r["from_source"] for r in ins)
    P("\n- `from` source: from_line %d, heading_keyword %d, none %d." % (fs["from_line"], fs["heading_keyword"], fs["none"]))
    sole = collections.Counter(tuple(sorted(r["from_projects"])) for r in ins)
    P("- Most common exact `from_projects` sets: " + "; ".join("%s: %d" % ("+".join(k) or "(none)", v) for k, v in sole.most_common(8)) + ".")
    P("")
    c2 = collections.Counter()
    rel_present = sum(1 for r in ins if r["relevant_to"])
    for r in ins:
        for p in r["relevant_to_projects"]:
            c2[p] += 1
    P("Stated audience (`**Relevant to:**`): present on %d of %d insights (%s). Overlapping counts:\n" % (rel_present, len(ins), pct(rel_present, len(ins))))
    P(table(["audience", "insights", "share of %d with line" % rel_present], [[k, v, pct(v, rel_present)] for k, v in c2.most_common()]))
    P("\n- Relevant-to present but no project/generic keyword resolved: %d." % sum(1 for r in ins if r["relevant_to"] and not r["relevant_to_projects"]))
    P("")
    # evidence
    n = len(ins)
    has_sha = sum(1 for r in ins if r["commit_shas"])
    has_path = sum(1 for r in ins if r["repo_paths"])
    has_path_body = sum(1 for r in ins if r["repo_paths_excl_from_line"])
    has_issue = sum(1 for r in ins if r["issue_refs"] or r["issue_refs_bare_near_issue"])
    has_id = sum(1 for r in ins if r["adr_ids"] or r["pdr_ids"] or r["m_ids"] or r["methodology_ids"])
    has_url = sum(1 for r in ins if r["urls"])
    has_any = sum(1 for r in ins if r["commit_shas"] or r["repo_paths"] or r["issue_refs"] or r["issue_refs_bare_near_issue"])
    has_sa = sum(1 for r in ins if r["has_suggested_action"])
    P("## 5. Cited evidence and suggested actions (denominator: %d insights)\n" % n)
    P(table(["evidence", "insights", "share"], [
        ["commit SHA (7-40 hex, digit+letter)", has_sha, pct(has_sha, n)],
        ["repo path (anywhere in block incl. From line)", has_path, pct(has_path, n)],
        ["repo path excluding the From line", has_path_body, pct(has_path_body, n)],
        ["issue ref (#N or 'issue NNNN')", has_issue, pct(has_issue, n)],
        ["ADR/PDR/m-N/methodology-N id", has_id, pct(has_id, n)],
        ["URL", has_url, pct(has_url, n)],
        ["any of SHA / path / issue", has_any, pct(has_any, n)],
        ["none of SHA / path / issue", n - has_any, pct(n - has_any, n)],
        ["`**Suggested action**` line", has_sa, pct(has_sa, n)],
    ]))
    P("\nBy era (insights with SHA / path / issue / suggested action; era = numbered vs unnumbered headings):\n")
    rows = []
    for lab, f in (("numbered `### N.`", lambda r: r["heading_numbered"]), ("unnumbered `### Title`", lambda r: not r["heading_numbered"])):
        sub = [r for r in ins if f(r)]
        k = len(sub)
        rows.append([lab, k, pct(sum(1 for r in sub if r["commit_shas"]), k), pct(sum(1 for r in sub if r["repo_paths"]), k),
                     pct(sum(1 for r in sub if r["issue_refs"] or r["issue_refs_bare_near_issue"]), k), pct(sum(1 for r in sub if r["has_suggested_action"]), k)])
    P(table(["heading form", "n", "SHA", "path", "issue", "suggested action"], rows))
    sal = collections.Counter(r["suggested_action_label"] for r in ins if r["has_suggested_action"])
    P("\nSuggested-action label variants: " + "; ".join("%s: %d" % (k, v) for k, v in sal.most_common(8)) + ".")
    P("\nCaveat: the SHA regex is a pattern match (a token like `1e65ef4` in prose counts); provenance_pilot.md tests which resolve in the PM repo. Evidence was extracted from the whole insight block including the `**From:**` line, which often holds a path to a session log; the 'excluding From line' row shows the difference.")
    P("")
    # letters
    P("## 6. Letters to xian\n")
    nl = len(letters)
    briefs_with_letters = len(set(l["brief_file"] for l in letters))
    P("- Briefs with a Letters section: %d of %d (%s). Letter occurrences: %d." % (
        sum(1 for b in briefs if "letters" in b["section_inventory_canonical"]), nb, pct(sum(1 for b in briefs if "letters" in b["section_inventory_canonical"]), nb), nl))
    byid = collections.defaultdict(list)
    for l in letters:
        byid[l["letter_id"]].append(l)
    P("- **Distinct letters: %d.** The same letter is re-featured across consecutive briefs (\"one letter featured at the end of each brief\"), so occurrences overcount." % len(byid))
    rows = []
    for lid, ls in sorted(byid.items(), key=lambda kv: min(x["brief_date"] for x in kv[1])):
        ans = any(x["answer_present"] for x in ls)
        rows.append([lid, len(ls), min(x["brief_date"] for x in ls), max(x["brief_date"] for x in ls),
                     "/".join(sorted(set(x["header_status"] for x in ls))), "yes" if ans else "no"])
    P("")
    P(table(["letter", "occurrences", "first brief", "last brief", "header status(es) seen", "answer text in any occurrence"], rows))
    ans_ids = sum(1 for lid, ls in byid.items() if any(x["answer_present"] for x in ls))
    P("\n- Answered share, distinct letters: **%d of %d (%s)**. Answered share, occurrences: %d of %d (%s)." % (
        ans_ids, len(byid), pct(ans_ids, len(byid)), sum(1 for l in letters if l["answer_present"]), nl, pct(sum(1 for l in letters if l["answer_present"]), nl)))
    P("- Letters by sender project: " + ", ".join("%s: %d" % (k, v) for k, v in collections.Counter((l["from_project"] or "?") for l in {x["letter_id"]: x for x in letters}.values()).most_common()) + " (distinct letters).")
    ph = [l for l in letters if l.get("answer_placeholder_only")]
    P("- Occurrences whose `**xian:**` block is only a placeholder ('reply expected...') and are counted as NOT answered: %d (%s)." % (len(ph), ", ".join(sorted(set(l["brief_file"] for l in ph)))))
    mismatch = [l for l in letters if l["answer_present"] and l["header_status"] in ("awaiting", "incoming", "in_progress")]
    if mismatch:
        P("- Header says pending but an answer block is present in %d occurrence(s): %s." % (len(mismatch), ", ".join(sorted(set(l["brief_file"] for l in mismatch)))[:300]))
    P("")
    # corrections
    P("## 7. Corrections\n")
    P("- Briefs with a Corrections section: %d of %d. Correction items parsed: **%d**." % (sum(1 for b in briefs if b["n_corrections"]), nb, len(corrs)))
    for c_ in corrs:
        P("  - %s item %d (%s split): corrects date=%s kind=%s item#=%s; target brief file exists in corpus: %s" % (
            c_["brief_file"], c_["ordinal_in_section"], c_["item_split_method"], c_["corrects_date"], c_["corrects_kind"], c_["corrects_ordinal"], c_["corrects_target_file_exists"]))
    P("- Section headings used: " + ", ".join(sorted(set(c_["section_heading"] for c_ in corrs))) + " (two heading variants: `## Corrections` and `## Corrections to the record`).")
    P("- Correction items stating a target date: %d of %d. Note: corrections also occur outside this section (e.g. in the Janus-style 'correction to 10-04 item 1' mention in sweep-log notes); this count covers only dedicated sections." % (
        sum(1 for c_ in corrs if c_["corrects_date_is_stated"]), len(corrs)))
    P("")
    # drift
    P("## 8. Section-format drift over time\n")
    P("Share of briefs per month containing each `## ` section (denominator = briefs in month; sections canonicalised by prefix):\n")
    canon_order = ["key_insights", "emerging_patterns", "background_changes", "sources_read", "letters", "corrections", "cultural_vocabulary", "other"]
    months = sorted(bym)
    rows = []
    for m in months:
        bs = [b for b in briefs if b["date"][:7] == m]
        rows.append([m, len(bs)] + [pct(sum(1 for b in bs if k in b["section_inventory_canonical"]), len(bs)) for k in canon_order])
    P(table(["month", "n"] + canon_order, rows))
    P("")
    # eras (data-driven)
    P("Era markers observed (first/last date each section/format appears; counts over %d briefs):\n" % nb)
    rows = []
    for k in canon_order:
        ds = sorted(b["date"] for b in briefs if k in b["section_inventory_canonical"])
        rows.append([k, len(ds), ds[0] if ds else "-", ds[-1] if ds else "-"])
    uds = sorted(r["brief_date"] for r in ins if not r["heading_numbered"])
    nds = sorted(r["brief_date"] for r in ins if r["heading_numbered"])
    rows.append(["insight headings `### N.` (insights)", len(nds), nds[0] if nds else "-", nds[-1] if nds else "-"])
    rows.append(["insight headings unnumbered (insights)", len(uds), uds[0] if uds else "-", uds[-1] if uds else "-"])
    P(table(["marker", "count", "first", "last"], rows))
    P("")
    src_sets = collections.defaultdict(list)
    for b in briefs:
        src_sets["+".join(sorted(b["sources_checked"])) or "(none)"].append(b["date"])
    P("Front-matter `sources_checked` sets (era by projects covered):\n")
    P(table(["sources_checked", "briefs", "first", "last"], [[k, len(v), min(v), max(v)] for k, v in sorted(src_sets.items(), key=lambda kv: min(kv[1]))]))
    P("")
    fk = collections.defaultdict(list)
    for b in briefs:
        for k in b["frontmatter_keys"]:
            fk[k].append(b["date"])
    P("Front-matter keys (count, first, last): " + "; ".join("%s: %d (%s .. %s)" % (k, len(v), min(v), max(v)) for k, v in sorted(fk.items())) + ".")
    ia = collections.defaultdict(list)
    for b in briefs:
        ia[b["date"][:7]].append(b)
    P("")
    P("Observed eras (from the tables above; descriptive, not authoritative -- the hub process docs were not consulted for this extraction):")
    P("- Retrospective thematic briefs: titles carry a theme and a month range (e.g. 'Genesis', 'The GREAT Refactor'); dates from %s; PM-only sources; see by-month table for sparsity." % dates[0])
    P("- Dated daily/PM-only briefs before Klatch existed (note in 2026-02-06: 'Klatch launched March 7, 2026'), many nominal.")
    P("- Dual-source (klatch + piper-morgan) dated briefs from March 2026; later additional sources (openlaws from 2026-04-11 rev2, one-job, etc.) per the sources_checked table.")
    P("- Numbered `### N.` insight headings through %s; unnumbered `### Title` insight headings from %s." % (nds[-1] if nds else "-", uds[0] if uds else "-"))
    P("- `## Letters to xian` from 2026-05-17; `## Corrections` only 2026-09-08/09/10-05.")
    P("- Per-project era (separate per-project briefs, e.g. 'Klatch -> Piper Morgan'): **not observed in `*-brief.md` front matter or titles in this corpus** -- all 234 files use the 'Cross-Pollination Brief' title with a unified `sources_checked` list. If a per-project era exists it is outside these files (unverified).")
    P("")
    # sweep join
    P("## 9. Sweep-log join\n")
    j = collections.Counter(str(b["has_sweep_log_entry"]) for b in briefs)
    P("sweep-log.md first row: %s. `has_sweep_log_entry`: True %d, False %d, null (predates log, unverified) %d, of %d briefs." % (
        sweep_first, j["True"], j["False"], j["None"], nb))
    missing = [b["date"] for b in briefs if b["has_sweep_log_entry"] is False]
    P("- Briefs dated on/after the first sweep-log row with no log row: %d%s" % (len(missing), (": " + ", ".join(missing[:30])) if missing else "."))
    mism = [(b["date"], b["status"], [r["outcome"] for r in b["sweep_log_runs"]]) for b in briefs if b["has_sweep_log_entry"]
            and b["status"] == "substantive" and not any(o.startswith("substantive") for o in [r["outcome"] for r in b["sweep_log_runs"]])]
    P("- Briefs whose status is `substantive` but no log row that day begins with 'substantive': %d" % len(mism) + ("." if not mism else " -- " + "; ".join("%s %s" % (d, o) for d, s, o in mism[:15])))
    mism2 = [(b["date"], b["status"], [r["outcome"] for r in b["sweep_log_runs"]]) for b in briefs if b["has_sweep_log_entry"]
             and b["status"] == "nominal" and any(o.startswith("substantive") for o in [r["outcome"] for r in b["sweep_log_runs"]])]
    P("- Briefs with status `nominal` but a log row beginning 'substantive': %d" % len(mism2) + ("." if not mism2 else " -- " + "; ".join("%s %s" % (d, o) for d, s, o in mism2[:15])))
    multi = collections.Counter(len(b["sweep_log_runs"]) for b in briefs)
    P("- Sweep runs per brief date: " + ", ".join("%d run(s): %d briefs" % (k, v) for k, v in sorted(multi.items())) + ".")
    nobrief = sorted(set(d for d in dates_in_sweep(briefs_dir) if d not in set(dates)))
    P("- Sweep-log dates with no brief file: %d%s" % (len(nobrief), (" (" + ", ".join(nobrief[:20]) + ")") if nobrief else "."))
    P("- Join key is date only; multiple runs on a date are all attached; log rows with 'started' outcome (no completion row) are included as runs.")
    for n_ in sweep_notes:
        P("- NOTE: " + n_)
    P("")
    # edge cases
    P("## 10. Parse failures and edge cases (nothing silently dropped)\n")
    ec = [(b["filename"], pn) for b in briefs for pn in b["parse_notes"]]
    ec += [(r["id"], pn) for r in ins for pn in r["parse_notes"] if "positional" not in pn]
    ec += [(l["brief_file"] + " letter", pn) for l in letters for pn in l["parse_notes"]]
    groups = collections.defaultdict(list)
    for who, pn in ec:
        key = re.sub(r"\d{4}-\d{2}-\d{2}", "DATE", pn)
        key = re.sub(r"\[[^\]]*\]", "[...]", key)
        key = re.sub(r"\(note: .*\)", "(note: ...)", key)
        key = re.sub(r"\d+ items", "N items", key)
        groups[key[:140]].append(who)
    for k, v in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        P("- **%s** -- %d occurrence(s): %s" % (k, len(v), ", ".join(v[:12]) + (" ..." if len(v) > 12 else "")))
    P("")
    unn = [r for r in ins if not r["heading_numbered"]]
    P("- Unnumbered insight headings: %d insights in %d briefs (%s .. %s); these are parsed as insights with positional ordinal (id `DATE#position`) and flagged `heading_numbered: false`. The task spec described `### N.` only; an extractor restricted to that form would miss these %d (%s of all %d)." % (
        len(unn), len(set(r["brief_date"] for r in unn)), unn[0]["brief_date"] if unn else "-", unn[-1]["brief_date"] if unn else "-", len(unn), pct(len(unn), len(ins)), len(ins)))
    nofrom = [r for r in ins if not r["from"]]
    P("- Insights with no `**From:**` line: %d of %d (%s)." % (len(nofrom), len(ins), pct(len(nofrom), len(ins))))
    P("- Nominal briefs (status: nominal): %d -- %s." % (sum(1 for b in briefs if b["status"] == "nominal"), ", ".join(b["filename"] for b in briefs if b["status"] == "nominal")))
    dup = collections.Counter(b["date"] for b in briefs)
    P("- Duplicate dates: " + (", ".join("%s (%s)" % (d, ", ".join(b["filename"] for b in briefs if b["date"] == d)) for d, c_ in dup.items() if c_ > 1) or "none") +
      ". The 2026-04-11 original is a stub superseded by rev2; both are in the output (rev file has `is_revision_file: true`); insight ids `2026-04-11#N` come only from rev2 because the stub has none.")
    iddup = [k for k, v in collections.Counter(r["id"] for r in ins).items() if v > 1]
    P("- Duplicate insight ids: %s." % (", ".join(iddup) if iddup else "none"))
    P("- Emerging-pattern and background item counts are heuristic (bullets / bold-lead paragraphs / paragraphs; method recorded per brief). Items that read as 'none' are excluded.")
    P("- Letters: the same letter appears in many briefs; `letter_id` = `sender@filed-date` is the dedupe key.")
    open(out_path, "w", encoding="utf-8").write("\n".join(L) + "\n")


_SWEEP_DATES = None


def dates_in_sweep(briefs_dir):
    global _SWEEP_DATES
    if _SWEEP_DATES is None:
        _SWEEP_DATES = set()
        p = os.path.join(briefs_dir, "sweep-log.md")
        if os.path.exists(p):
            for line in open(p, encoding="utf-8"):
                m = re.match(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|", line)
                if m:
                    _SWEEP_DATES.add(m.group(1))
    return _SWEEP_DATES

# ----------------------------------------------------------------- main

def write_jsonl(path, recs):
    with open(path, "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps({k: v for k, v in r.items() if not k.startswith("_")}, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--briefs-dir", default=DEFAULT_BRIEFS)
    ap.add_argument("--pm-repo", default=DEFAULT_PM)
    ap.add_argument("--out-dir", default=HERE)
    ap.add_argument("--skip-provenance", action="store_true")
    ap.add_argument("--seed", type=int, default=20261007)
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)
    sweep, sweep_first, sweep_notes = parse_sweep_log(os.path.join(a.briefs_dir, "sweep-log.md"))
    files = sorted(glob.glob(os.path.join(a.briefs_dir, "*-brief.md")) + glob.glob(os.path.join(a.briefs_dir, "*-brief-rev*.md")))
    briefs, ins, letters, corrs = [], [], [], []
    for p in files:
        b, i, l, c = parse_brief(p, sweep, sweep_first)
        briefs.append(b)
        ins += i
        letters += l
        corrs += c
    briefs.sort(key=lambda b: (b["date"], b["is_revision_file"]))
    ins.sort(key=lambda r: (r["brief_date"], r["ordinal"]))
    write_jsonl(os.path.join(a.out_dir, "briefs.jsonl"), briefs)
    write_jsonl(os.path.join(a.out_dir, "insights.jsonl"), ins)
    write_jsonl(os.path.join(a.out_dir, "letters.jsonl"), letters)
    write_jsonl(os.path.join(a.out_dir, "corrections.jsonl"), corrs)
    summary(briefs, ins, letters, corrs, os.path.join(a.out_dir, "xpoll_summary.md"), sweep_first, sweep_notes, a.briefs_dir)
    if not a.skip_provenance:
        provenance(ins, a.pm_repo, a.seed, os.path.join(a.out_dir, "provenance_pilot.md"))
    print("briefs=%d insights=%d letters=%d corrections=%d -> %s" % (len(briefs), len(ins), len(letters), len(corrs), a.out_dir))


if __name__ == "__main__":
    main()
