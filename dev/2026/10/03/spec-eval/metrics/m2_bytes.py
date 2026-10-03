# Measures (prereg M1.2 bytes, M1.3 token proxy): bytes of ADDED lines (diff '+' lines, +1 newline each, UTF-8 bytes)
# under mailboxes/, dev/, docs/briefing/ per month (author date UTC), non-merge commits, renames detected (-M) so pure moves add 0.
# Also bytes added in PC paths ("pc_bytes") for a bytes-per-PC-line view. Token proxy = (mailboxes+dev+docs/briefing)/4.
import csv,collections
from common import *
B=collections.defaultdict(lambda:collections.Counter())
cur=None;path=None
for l in stream('log',SNAP,'-p','-M','--no-merges','--format=@@%at','--','mailboxes','dev','docs/briefing','services','web','templates','alembic','cli','main.py'):
    if l.startswith('@@') and len(l)<20 and l[2:].isdigit(): cur=month(l[2:]); continue
    if l.startswith('+++ '):
        p=l[4:]; path=p[2:] if p.startswith('b/') else None; continue
    if l.startswith('+') and path and cur:
        n=len(l[1:].encode('utf-8','replace'))+1
        for k,pre in (('mailboxes','mailboxes/'),('dev','dev/'),('docs_briefing','docs/briefing/')):
            if path.startswith(pre): B[cur][k]+=n
        if is_pc(path): B[cur]['pc_bytes']+=n
with open('m2_bytes.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['month','mailboxes_bytes','dev_bytes','docs_briefing_bytes','coord_bytes_total','token_proxy','pc_bytes_added'])
    for m in months():
        c=B[m];t=c['mailboxes']+c['dev']+c['docs_briefing']
        w.writerow([m,c['mailboxes'],c['dev'],c['docs_briefing'],t,t//4,c['pc_bytes']])
print(open('m2_bytes.csv').read())
