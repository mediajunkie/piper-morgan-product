#!/usr/bin/env python3
"""
check-acronyms.py — glossary-backed acronym lint for drafts.

Defends against two failure modes in plain-language editing:
  (a) FALSE UNPACKING — an acronym spelled out incorrectly by guesswork
      (e.g. "PDR (product-design record)" when the glossary says
       "Product Decision Record"). The glossary is the single source of truth.
  (b) PLAIN-LANGUAGE OVERCORRECT / un-introduced jargon — a glossary acronym
      used without a first-use gloss (term should be defined once, then used).

Source of truth: the bullet lines in
  knowledge/piper-morgan-glossary-v1.1.md
of the form:  - **XXX**: Expansion words (optional note)
under two headers:
  "Artifact / process acronyms"  → LITERAL terms: one correct expansion;
                                    a wrong gloss is a hard ⛔ FALSE-UNPACK.
  "Role acronyms"                → ROLE terms: PM's voice allows *functional*
                                    descriptions ("the experience role (CXO)"),
                                    so a gloss mismatch is ⚠️ advisory only —
                                    flagged for a human eyeball, not auto-wrong.

Usage:
  python3 scripts/check-acronyms.py draft.md [more.md ...]
  python3 scripts/check-acronyms.py --glossary path/to/glossary.md draft.md
Exit 0 = no hard findings, 1 = at least one ⛔ FALSE-UNPACK (gate-able).
"""
import re
import sys
import os

GLOSSARY_DEFAULT = "knowledge/piper-morgan-glossary-v1.1.md"


def load_glossary(path):
    """Return {ACRONYM: (canonical_expansion, kind)} where kind in {literal, role}."""
    terms = {}
    kind = "literal"
    bullet = re.compile(r"^\s*-\s*\*\*([A-Za-z][A-Za-z0-9/&-]{1,12})\*\*:\s*(.+)$")
    with open(path) as f:
        for line in f:
            low = line.lower()
            if "role acronym" in low:
                kind = "role"
            elif "artifact" in low and "acronym" in low:
                kind = "literal"
            m = bullet.match(line)
            if not m:
                continue
            acro = m.group(1).strip()
            # canonical expansion = text before the first "(" or em-dash note
            exp = re.split(r"\(|—|\s-\s", m.group(2))[0].strip().rstrip(".")
            if len(acro) >= 2 and any(c.isupper() for c in acro):
                terms[acro] = (exp, kind)
    return terms


def words(s):
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).split()


def check(draft_path, terms):
    text = open(draft_path).read()
    findings = []
    for acro, (canon, kind) in terms.items():
        cw = words(canon)
        hard = (kind == "literal")
        # forward form:  ACRONYM (gloss)
        for m in re.finditer(rf"\b{re.escape(acro)}\b\s*\(([^)]{{2,80}})\)", text):
            gloss = m.group(1).strip()
            if gloss.startswith(acro):
                continue
            if words(gloss) != cw:
                kindtag = "FALSE-UNPACK" if hard else "ROLE-GLOSS?"
                findings.append((kindtag, hard,
                                 f'"{acro} ({gloss})" — glossary expansion is "{canon}"'))
        # reverse form:  expansion words (ACRONYM)
        for m in re.finditer(rf"([A-Za-z][\w\- ]{{3,80}}?)\s*\(\s*{re.escape(acro)}\s*\)", text):
            lead = words(m.group(1))[-len(cw):]
            if lead != cw:
                kindtag = "FALSE-UNPACK" if hard else "ROLE-GLOSS?"
                findings.append((kindtag, hard,
                                 f'"...{m.group(1).strip()} ({acro})" — glossary expansion is "{canon}"'))
        # un-introduced: acronym used with no gloss in either form, anywhere
        if re.search(rf"\b{re.escape(acro)}\b", text):
            glossed = re.search(rf"\b{re.escape(acro)}\b\s*\(", text) or \
                      re.search(rf"\(\s*{re.escape(acro)}\s*\)", text)
            if not glossed:
                findings.append(("NO-GLOSS", False,
                                 f'"{acro}" used without a first-use gloss '
                                 f'(introduce once as "{canon} ({acro})" then use "{acro}")'))
    return findings


def main():
    args = sys.argv[1:]
    glossary = GLOSSARY_DEFAULT
    if "--glossary" in args:
        i = args.index("--glossary")
        glossary = args[i + 1]
        del args[i:i + 2]
    if not args:
        print(__doc__)
        sys.exit(2)
    if not os.path.exists(glossary):
        print(f"glossary not found: {glossary}", file=sys.stderr)
        sys.exit(2)
    terms = load_glossary(glossary)
    hard_total = 0
    for draft in args:
        findings = check(draft, terms)
        if findings:
            print(f"\n{draft}:")
            for tag, hard, msg in findings:
                icon = "⛔" if hard else ("ℹ️ " if tag == "ROLE-GLOSS?" else "⚠️ ")
                print(f"  {icon} [{tag}] {msg}")
                if hard:
                    hard_total += 1
    if hard_total:
        print(f"\n{hard_total} hard finding(s) (⛔ FALSE-UNPACK) — must fix. "
              f"⚠️/ℹ️ are advisory (NO-GLOSS may be intentional; ROLE-GLOSS may be a "
              f"deliberate functional description).")
        sys.exit(1)
    print("✓ no hard acronym findings "
          f"({len(terms)} glossary terms checked; advisory items above if any)")
    sys.exit(0)


if __name__ == "__main__":
    main()
