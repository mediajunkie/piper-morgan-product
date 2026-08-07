#!/usr/bin/env python3
"""Format-agnostic mailbox triage scan.

WHY THIS EXISTS: a `grep '^from:'` scan reads YAML frontmatter only, and ~19% of
cohort memos (65 of 337 measured in comms/read, 2026-08-07) use a header style
instead — `**From**: HOST · **To**: ...` under an H1. Those show BLANK in a
frontmatter scan. HOST (18) and CXO (9) are the heaviest header-style senders,
so the blind spot is concentrated in two of the most active correspondents.
Comms nearly skipped a HOST memo addressed directly to them because of it.
"""
import sys, os, re, glob

def parse(path):
    txt = open(path, encoding='utf-8', errors='replace').read()
    frm = sub = to = ''
    m = re.match(r'^---\n(.*?)\n---\n', txt, re.DOTALL)
    if m:                                             # YAML frontmatter
        fm = m.group(1)
        g = lambda k: (re.search(rf'^{k}:\s*"?(.*?)"?\s*$', fm, re.M) or [None, ''])[1]
        frm, to, sub = g('from'), g('to'), g('subject')
    if not frm:                                       # header style
        h = re.search(r'\*\*From\*\*:\s*([^·\n]+)', txt)
        t = re.search(r'\*\*To\*\*:\s*([^·\n]+)', txt)
        frm = h.group(1).strip() if h else ''
        to  = t.group(1).strip() if t else ''
    if not sub:                                       # fall back to the H1
        h1 = re.search(r'^#\s+(.*)$', txt, re.M)
        sub = h1.group(1).strip() if h1 else ''
    return frm, to, sub

d = sys.argv[1] if len(sys.argv) > 1 else 'mailboxes/comms/inbox'
files = [f for f in sorted(glob.glob(os.path.join(d, '*.md')))
         if os.path.basename(f) != 'MANIFEST.md']
blank = 0
for i, f in enumerate(files, 1):
    frm, to, sub = parse(f)
    if not frm and not sub:
        blank += 1
    flag = '⚠ ' if re.match(r'(URGENT|CORRECTION|RULING|FALSIFIED|WITHDRAWN)', os.path.basename(f)) else '  '
    print(f"{flag}[{i}] from:{frm[:14]:14} to:{to[:34]:34}")
    print(f"      {sub[:104]}")
print(f"\n  {len(files)} memos · unparsed: {blank}")
