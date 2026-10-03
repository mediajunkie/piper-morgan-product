# Measures (prereg M1.4): new files ADDED (diff-filter=A, renames off so moves out of inbox/ are not new) under
# "mailboxes/xian (ceo)/inbox/" per month, and per 7-day bucket for the 13 weeks ending at snapshot (2026-10-03 17:41Z).
# Caveat: a file added, moved to read/, and re-added counts once per add; non-md files (MANIFEST.md) are excluded by name.
import csv,collections,datetime
from common import *
mo=collections.Counter();wk=collections.Counter()
snap=1791049304 # 2026-10-03T17:41:44Z
cur=None
for l in stream('log',SNAP,'--no-renames','--diff-filter=A','--name-only','--format=@@%at','--','mailboxes/xian (ceo)/inbox/'):
    if l.startswith('@@'): cur=int(l[2:]); continue
    if not l or not l.endswith('.md') or l.endswith('MANIFEST.md'): continue
    mo[month(cur)]+=1
    b=(snap-cur)//(7*86400)
    if b<13: wk[b]+=1
with open('m3_memos_monthly.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['month','ceo_inbox_new_memos'])
    for m in months(): w.writerow([m,mo[m]])
with open('m3_memos_weekly.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['week_ending','ceo_inbox_new_memos'])
    for b in range(12,-1,-1):
        e=datetime.datetime.fromtimestamp(snap-b*7*86400,datetime.timezone.utc).strftime('%Y-%m-%d'); w.writerow([e,wk[b]])
print(open('m3_memos_monthly.csv').read());print(open('m3_memos_weekly.csv').read())
