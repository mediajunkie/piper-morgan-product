# Measures (prereg H1 M1.1, M1.2 commit counts, C/P ratio; H4 d1/d2 inputs):
# per month (author date, UTC): PC count, PC lines added+deleted (product paths only),
# TC count (non-merge commits touching ONLY tests/ among PC/TC paths), coordination commits by subject class,
# merge commits, total commits. Bounded by snapshot SHA. Also dumps per-commit table commits.csv for other scripts.
import csv,collections
from common import *
rows=[];cur=None
def flush():
    if cur: rows.append(cur)
for l in stream('log',SNAP,'--numstat','--format=@@%H|%P|%at|%s'):
    if l.startswith('@@'):
        flush(); h,par,at,subj=l[2:].split('|',3)
        cur=dict(h=h,merge=len(par.split())>1,at=int(at),subj=subj,pcl=0,pcn=0,tcn=0,files=[])
    elif l and cur:
        a,d,p=l.split('\t',2)
        a=int(a) if a.isdigit() else 0; d=int(d) if d.isdigit() else 0
        cur['files'].append(p)
        if is_pc(p): cur['pcl']+=a+d; cur['pcn']+=1
        elif is_tc(p): cur['tcn']+=1
flush()
with open('commits.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['sha','epoch','month','merge','coord_class','is_pc','is_tc','pc_lines','subject'])
    for r in rows:
        pc=(not r['merge']) and r['pcn']>0; tc=(not r['merge']) and r['pcn']==0 and r['tcn']>0
        r['pc']=pc;r['tc']=tc
        w.writerow([r['h'],r['at'],month(r['at']),int(r['merge']),coord_class(r['subj']) or '',int(pc),int(tc),r['pcl'] if pc else 0,r['subj']])
cls=['mail','log','hb','hb-last-invoked','stop','heartbeat']
M=collections.defaultdict(lambda:collections.Counter())
for r in rows:
    m=month(r['at']);c=M[m];c['total']+=1
    if r['merge']: c['merge']+=1
    else:
        k=coord_class(r['subj'])
        if k: c[k]+=1
        if r['pc']: c['pc']+=1; c['pc_lines']+=r['pcl']
        if r['tc']: c['tc']+=1
with open('m1_monthly.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['month','total','pc','pc_lines','tc']+cls+['merge','coord_total','C_over_P'])
    for m in months():
        c=M[m]; ct=sum(c[k] for k in cls)+c['merge']
        w.writerow([m,c['total'],c['pc'],c['pc_lines'],c['tc']]+[c[k] for k in cls]+[c['merge'],ct,round(ct/c['pc'],3) if c['pc'] else ''])
print(open('m1_monthly.csv').read())
