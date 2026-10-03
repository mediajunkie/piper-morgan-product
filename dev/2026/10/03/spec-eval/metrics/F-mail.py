#!/usr/bin/env python3
"""F-mail.py — Workstream F mailbox census (Spec eval). Read-only.
Unit of count: a unique memo = one file in some mailboxes/<sender>/sent/ (sender's mirror), deduped by
filename. Files in inbox/ or read/ whose filename has no sent mirror anywhere are counted separately
(watchdog alerts, external agents). Frontmatter keys from/to/cc/date parsed leniently.
Window: ISO weeks; reports last 8 full-ish 7-day buckets ending 2026-10-03.
"""
import os, re, sys, collections, datetime as dt, json
ROOT = os.path.join(os.path.dirname(__file__), "../../../../../../mailboxes")
ROOT = os.path.abspath(ROOT)
END = dt.date(2026, 10, 3)
def norm(s):
    s = s.lower().strip().strip('"').strip("'")
    if any(k in s for k in ("xian", "ceo", " pm", "pm ")) or s in ("pm", "xian"): return "PM"
    s = re.sub(r"\(.*?\)", "", s).strip()
    return s.split()[0] if s else "?"
def parse(path):
    try: txt = open(path, encoding="utf-8", errors="replace").read()
    except Exception: return None
    fm = {}
    m = re.match(r"---\n(.*?)\n---\n", txt, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1); fm[k.strip().lower()] = v.strip()
    body = txt[m.end():] if m else txt
    words = len(body.split())
    d = None
    for src in (fm.get("date", ""), os.path.basename(path)):
        mm = re.search(r"(20\d\d)-(\d\d)-(\d\d)", src)
        if mm:
            try: d = dt.date(*map(int, mm.groups())); break
            except ValueError: pass
    rec = lambda k: [norm(x) for x in re.split(r"[,;\[\]]", fm.get(k, "")) if x.strip()]
    return dict(fm=fm, words=words, date=d, to=rec("to"), cc=rec("cc"), frm=norm(fm.get("from", "?")),
                subj=fm.get("subject", ""), body=body)
def week(d):  # bucket index: 0 = 7 days ending END
    return (END - d).days // 7 if d else None
memos = {}
for box in os.listdir(ROOT):
    sd = os.path.join(ROOT, box, "sent")
    if not os.path.isdir(sd): continue
    for f in os.listdir(sd):
        if f.endswith(".md") and f != "MANIFEST.md" and f not in memos:
            r = parse(os.path.join(sd, f))
            if r: r["sender_box"] = box; memos[f] = r
# unmirrored files in the PM mailbox
pm_files = {}
for sub in ("inbox", "read"):
    d = os.path.join(ROOT, "xian (ceo)", sub)
    for dirpath, _, files in os.walk(d):
        for f in files:
            if f.endswith(".md") and f != "MANIFEST.md": pm_files[f] = os.path.join(dirpath, f)
out = {}
NW = 8
by_week = collections.Counter(); pm_week = collections.Counter(); pm_words = collections.Counter()
pair = collections.Counter(); prefix = collections.Counter(); pm_prefix = collections.Counter()
pm_to_direct = collections.Counter(); ask_week = collections.Counter(); ruling_week = collections.Counter()
for f, r in memos.items():
    w = week(r["date"])
    if w is None or w < 0 or w >= NW: continue
    by_week[w] += 1
    pre = f.split("-")[0].lower(); prefix[pre] += 1
    for t in r["to"] + r["cc"]: pair[(r["frm"], t)] += 1
    if "PM" in r["to"] + r["cc"]:
        pm_week[w] += 1; pm_words[w] += r["words"]; pm_prefix[pre] += 1
        if "PM" in r["to"]: pm_to_direct[w] += 1
        if re.search(r"\b(ask|decision|decide|approve|approval|ruling needed|needs pm|pm call|your call)\b", (f + " " + r["subj"]).lower()):
            ask_week[w] += 1
    if re.search(r"(pm rul|pm-rul|pm approv|pm-approv|pm confirmed|pm said|pm directive|per pm\b|pm's ruling|pm decided)", r["body"][:3000].lower()):
        ruling_week[w] += 1
# unmirrored PM-mailbox files in window (e.g. watchdog alerts)
unmirrored = collections.Counter(); unm_words = collections.Counter(); unm_prefix = collections.Counter()
for f, p in pm_files.items():
    if f in memos: continue
    r = parse(p); w = week(r["date"]) if r else None
    if w is None or w < 0 or w >= NW: continue
    unmirrored[w] += 1; unm_words[w] += r["words"]; unm_prefix[f.split("-")[0].lower()] += 1
# PM-authored mail
pm_sent = [f for f in os.listdir(os.path.join(ROOT, "xian (ceo)", "sent"))]
print(f"unique memos with sent mirror (all time): {len(memos)}")
print(f"window: {NW} x 7-day buckets ending {END}")
print("week_end  all_memos  pm_addr(to|cc)  pm_to  pm_words  pm_min@250wpm  ask-like  body_cites_PM_ruling  unmirrored_pm_files  unmirrored_words")
for w in range(NW):
    we = END - dt.timedelta(days=7*w)
    tw = pm_words[w] + unm_words[w]
    print(f"{we}  {by_week[w]:9}  {pm_week[w]:14}  {pm_to_direct[w]:5}  {pm_words[w]:8}  {tw/250:13.0f}  {ask_week[w]:8}  {ruling_week[w]:20}  {unmirrored[w]:19}  {unm_words[w]:16}")
print("\ntop sender->recipient pairs (8w, to+cc edges):")
for (a, b), n in pair.most_common(25): print(f"  {a:>6} -> {b:<6} {n}")
send = collections.Counter(); recv = collections.Counter()
for (a, b), n in pair.items(): send[a] += n; recv[b] += n
print("\nedges out by sender:", dict(send.most_common()))
print("edges in by recipient:", dict(recv.most_common()))
print("\nfilename-prefix types (8w, all memos):", prefix.most_common(20))
print("filename-prefix types (8w, PM-addressed):", pm_prefix.most_common(20))
print("unmirrored PM-mailbox prefixes (8w):", unm_prefix.most_common(10))
print("PM sent/ files (all time):", pm_sent)
