# Measures (prereg H4): d1 reverts (non-merge commit, subject starts with "Revert" or contains "revert", case-insens.),
# d2 fix-on-fix (non-merge commit whose subject matches ^fix (conventional 'fix(..)'/'fix:'/'Fix ...') AND touches a
# product-path file (PC paths or tests/) that an EARLIER non-merge feat/fix commit touched within the previous 72h [by author date]),
# monthly per-PC rates -> h4_monthly.csv; interrupted time series 60d before/after each mechanism date -> h4_its.csv, and the
# pre-registered H4 rule applied -> printed. Defect rate := (d1+d2)/PC (primary); d1/PC and d2/PC reported separately.
# DEVIATION: "a file" restricted to product-path+tests files (otherwise log/mail files in dev/ and mailboxes/ would create spurious overlaps).
# d3 (reopened) and d4 (bug-labelled issues) are not computed here; see report.
import csv,re,collections,datetime
from common import *
FIX=re.compile(r'^fix\b',re.I);FEAT=re.compile(r'^feat\b',re.I)
commits=[];cur=None
for l in stream('log',SNAP,'--numstat','--format=@@%H|%P|%at|%s'):
    if l.startswith('@@'):
        if cur:commits.append(cur)
        h,par,at,s=l[2:].split('|',3);cur=dict(at=int(at),s=s,merge=len(par.split())>1,files=set(),pc=False)
    elif l and cur:
        p=l.split('\t',2)[2]
        if is_pc(p): cur['pc']=True
        if is_pc(p) or is_tc(p): cur['files'].add(p)
if cur:commits.append(cur)
commits=[c for c in commits if not c['merge']]
commits.sort(key=lambda c:c['at'])
last=collections.defaultdict(list) # file -> list of (time) of feat/fix touches (deque-ish)
for c in commits:
    c['d1']=bool(re.match(r'^revert',c['s'],re.I) or 'revert' in c['s'].lower())
    c['d2']=False
    if FIX.match(c['s']):
        for f in c['files']:
            if any(c['at']-t<=72*3600 for t in last.get(f,[])[-5:]): c['d2']=True;break
    if FIX.match(c['s']) or FEAT.match(c['s']):
        for f in c['files']:
            last[f].append(c['at'])
M=collections.defaultdict(collections.Counter)
for c in commits:
    m=month(c['at']);M[m]['pc']+=c['pc'];M[m]['d1']+=c['d1'];M[m]['d2']+=c['d2']
with open('h4_monthly.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['month','pc','d1_reverts','d2_fix_on_fix','d1_per_pc','d2_per_pc','d12_per_pc'])
    for m in months():
        c=M[m];p=c['pc']
        w.writerow([m,p,c['d1'],c['d2']]+[round(x/p,3) if p else '' for x in (c['d1'],c['d2'],c['d1']+c['d2'])])
print(open('h4_monthly.csv').read())
D=lambda s:int(datetime.datetime.strptime(s,'%Y-%m-%d').replace(tzinfo=datetime.timezone.utc).timestamp())
SNAPT=1791049304
mech=[('first mailbox commit','2026-01-14'),('duty-cycle-tick skill','2026-06-06')]
import os
for l in open('m4_hooks_first_add.csv').read().splitlines()[1:]:
    n,d=l.rsplit(',',1);mech.append(('hook '+os.path.basename(n),d.split()[-1]))
for l in open('m4_snapshots.csv').read().splitlines()[1:]:
    p=l.split(',')
    if p[5]=='1': mech.append(('CLAUDE.md >25% month '+p[0],p[0]+'-01'))
def win(a,b):
    s=collections.Counter()
    for c in commits:
        if a<=c['at']<b: s['pc']+=c['pc'];s['d1']+=c['d1'];s['d2']+=c['d2']
    return s
out=[];
for name,d in mech:
    t=D(d);B=win(t-60*86400,t);A=win(t,t+60*86400)
    complete=t+60*86400<=SNAPT
    rate=lambda s,k:(s[k] if k!='d12' else s['d1']+s['d2'])/s['pc'] if s['pc'] else None
    rb,ra=rate(B,'d12'),rate(A,'d12')
    drop=(1-ra/rb) if (rb and ra is not None) else None
    pcchg=(A['pc']/B['pc']-1) if B['pc'] else None
    out.append([name,d,complete,B['pc'],B['d1'],B['d2'],A['pc'],A['d1'],A['d2'],round(rb,3) if rb is not None else '',round(ra,3) if ra is not None else '',round(drop,3) if drop is not None else '',round(pcchg,3) if pcchg is not None else ''])
with open('h4_its.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['mechanism','date','after_window_complete','pc_before','d1_before','d2_before','pc_after','d1_after','d2_after','d12_rate_before','d12_rate_after','rate_drop_frac','pc_change_frac']);w.writerows(out)
print(open('h4_its.csv').read())
sup=[o for o in out if o[11]!='' and o[11]>=0.25 and o[12]!='' and o[12]>=-0.25 and o[2]]
ge10=[o for o in out if o[11]!='' and o[11]>=0.10]
print('mechanisms evaluated',len(out),'| supported-by-rule (>=25% lower d1+d2 per PC, PC not down >25%, window complete):',len(sup),[o[0] for o in sup])
print('mechanisms with >=10% drop:',len(ge10),[o[0] for o in ge10])
print('mechanisms with rate rising:',[o[0] for o in out if o[11]!='' and o[11]<0])
