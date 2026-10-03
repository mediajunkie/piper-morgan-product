#!/usr/bin/env python3
"""F-overlap.py — M1b.2 PM-facing output overlap (Spec eval, workstream F). Read-only; uses git show at snapshot.
Pre-registered rule: two outputs overlap if >50% of their topic headings recur in the other within the same week.
Operationalization (stated, not pre-registered):
  topic heading = a markdown/HTML heading (h2-h4 / ##-####) OR the leading bold phrase of a list item/card
                  (first **..** or <strong>..</strong> on a line), length 3..200 chars.
  salient terms  = issue refs (#NNN+) if any; else content words (>=4 chars, not stopwords).
  recurs (LENIENT) = any issue ref found in the other artifact's full text, or >=60% of content words found in it.
  recurs (STRICT)  = same test against the other artifact's TOPIC HEADINGS text only.
  Headings with <2 content words and no issue ref are dropped as structural ("Closed — no action").
Pair overlaps if share>0.5 in BOTH directions (symmetric) — also reports either-direction.
"""
import re, subprocess, itertools, html, collections
SNAP = "a191856164351cf59ba033d7dbc4a34f036c6122"
def sh(*a): return subprocess.run(a, capture_output=True, text=True, cwd="/home/user/piper-morgan-product").stdout
def show(path, before=None):
    rev = SNAP
    if before:
        rev = sh("git", "log", "-1", "--format=%H", f"--before={before}", SNAP, "--", path).strip() or None
        if not rev: return ""
    return sh("git", "show", f"{rev}:{path}")
tree = sh("git", "ls-tree", "-r", "--name-only", SNAP).splitlines()
def mails(prefix):
    seen, out = set(), []
    for p in tree:
        if p.startswith("mailboxes/") and p.split("/")[-1].startswith(prefix):
            f = p.split("/")[-1]
            if f not in seen: seen.add(f); out.append(show(p))
    return "\n".join(out), len(seen)
STOP = set("this that with from have been will your what when they them their there about into only just more most over than then also were which while would could should after before still each every week today yesterday none action clean closed open what's here it's isn't don't".split())
def topics(text):
    t = text
    out = []
    for m in re.finditer(r"<h[2-4][^>]*>(.*?)</h[2-4]>", t, re.S | re.I): out.append(m.group(1))
    for line in t.splitlines():
        m = re.match(r"\s*#{2,4}\s+(.*)", line)
        if m: out.append(m.group(1)); continue
        m = re.search(r"\*\*(.{3,200}?)\*\*", line) if re.match(r"\s*([-*]|\d+\.)?\s*\*\*", line) else None
        if m: out.append(m.group(1)); continue
        m = re.search(r"<(strong|b)>(.{3,200}?)</\1>", line, re.I)
        if m: out.append(m.group(2))
    res = []
    for h in out:
        h = html.unescape(re.sub(r"<[^>]+>", " ", h))
        iss = set(re.findall(r"#(\d{3,4})\b", h))
        words = {w for w in re.findall(r"[a-z][a-z0-9'-]{3,}", h.lower()) if w not in STOP}
        if iss or len(words) >= 2: res.append((h.strip()[:80], iss, words))
    return res
def recurs(topic, other_text, other_words):
    _, iss, words = topic
    if iss and any(re.search(r"#%s\b" % i, other_text) for i in iss): return True
    return bool(words) and len(words & other_words) / len(words) >= 0.6
def share(a, b, strict):
    ta = a["topics"]
    if not ta: return 0.0
    if strict:
        btxt = " ".join(x[0] + " " + " ".join("#" + i for i in x[1]) for x in b["topics"]); bw = set().union(*[x[2] for x in b["topics"]]) if b["topics"] else set()
    else:
        btxt = b["text"]; bw = set(re.findall(r"[a-z][a-z0-9'-]{3,}", b["text"].lower()))
    return sum(recurs(t, btxt, bw) for t in ta) / len(ta)
def omni(days): return "\n".join(show(f"docs/omnibus-logs/{d}-omnibus-log.md") for d in days)
weeks = {
 "A 09-20..09-26": dict(
   rollup=show("dev/active/exec-attention-rollup-current.html", "2026-09-27") or show("dev/active/exec-cohort-attention-rollup-2026-09-25.html"),
   ship_synthesis=show("dev/active/exec-ship062-synthesis-2026-09-25.html"),
   workstream_memos=mails("workstream-062-")[0],
   omnibus=omni([f"2026-09-{d}" for d in range(20, 27)]),
   current_state=show("docs/briefing/BRIEFING-CURRENT-STATE.md", "2026-09-27")),
 "B 09-27..10-03": dict(
   rollup=show("dev/active/exec-attention-rollup-current.html"),
   ship_synthesis=show("dev/active/exec-ship063-synthesis-2026-10-02.html"),
   workstream_memos=mails("workstream-063-")[0],
   omnibus=omni(["2026-09-27", "2026-09-28", "2026-09-29", "2026-09-30", "2026-10-01", "2026-10-02"]),
   current_state=show("docs/briefing/BRIEFING-CURRENT-STATE.md")),
}
print("workstream memo counts: 062=%d 063=%d" % (mails("workstream-062-")[1], mails("workstream-063-")[1]))
for wk, arts in weeks.items():
    A = {k: dict(text=v, topics=topics(v)) for k, v in arts.items()}
    print(f"\n== week {wk}")
    for k, a in A.items(): print(f"  {k:18} words={len(a['text'].split()):6}  topic_headings={len(a['topics'])}")
    nsym = {"lenient": 0, "strict": 0}; neither = {"lenient": 0, "strict": 0}
    for x, y in itertools.combinations(A, 2):
        row = []
        for mode in ("lenient", "strict"):
            s1, s2 = share(A[x], A[y], mode == "strict"), share(A[y], A[x], mode == "strict")
            sym = s1 > .5 and s2 > .5; eit = s1 > .5 or s2 > .5
            nsym[mode] += sym; neither[mode] += eit
            row.append(f"{mode}: {s1:.2f}/{s2:.2f} {'OVERLAP' if sym else ('one-way' if eit else '-')}")
        print(f"  {x:>16} vs {y:<16} " + " | ".join(row))
    print(f"  pairs overlapping (both directions >50%): lenient={nsym['lenient']} strict={nsym['strict']} of 10; either-direction: lenient={neither['lenient']} strict={neither['strict']}")
