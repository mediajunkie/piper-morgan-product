# V1 independent re-derivation: PC/month, total commits/month, revert rate. Own parser (no common.py).
import subprocess, collections, datetime, re, sys
R='/home/user/piper-morgan-product'; S='a191856164351cf59ba033d7dbc4a34f036c6122'
out=subprocess.run(['git','-C',R,'-c','core.quotepath=off','log',S,'--no-renames','--name-only','--format=@@@%H\t%P\t%at\t%ct\t%s'],capture_output=True,text=True,errors='replace').stdout
commits=[];cur=None
for line in out.split('\n'):
    if line.startswith('@@@'):
        h,p,at,ct,s=line[3:].split('\t',4); cur=dict(h=h,merge=len(p.split())>1,at=int(at),ct=int(ct),s=s,files=[]); commits.append(cur)
    elif line.strip() and cur: cur['files'].append(line.strip())
def mon(t): return datetime.datetime.fromtimestamp(t,datetime.timezone.utc).strftime('%Y-%m')
PCP=('services/','web/','templates/','alembic/','cli/')
tot=collections.Counter(); totnm=collections.Counter(); pc=collections.Counter(); rev=collections.Counter(); revstrict=collections.Counter(); pcct=collections.Counter()
for c in commits:
    m=mon(c['at']); tot[m]+=1
    if c['merge']: continue
    totnm[m]+=1
    if any(f.startswith(PCP) or f=='main.py' for f in c['files']): pc[m]+=1; pcct[mon(c['ct'])]+=1
    if re.search('revert',c['s'],re.I): rev[m]+=1
    if c['s'].startswith('Revert "'): revstrict[m]+=1
print('total commits reachable',len(commits))
print('month total nonmerge pc pc_by_committerdate revert_any revert_strict revert/pc')
for m in sorted(tot):
    if m<'2025-06': continue
    print(m,tot[m],totnm[m],pc[m],pcct[m],rev[m],revstrict[m],round(rev[m]/pc[m],3) if pc[m] else '')
B=['2026-01','2026-02','2026-03'];Rw=['2026-08','2026-09']
f=lambda C,W: sum(C[m] for m in W)/len(W)
for name,C in [('pc',pc),('total',tot),('nonmerge',totnm)]:
    print(name,'B',round(f(C,B),1),'R',round(f(C,Rw),1),'ratio',round(f(C,Rw)/f(C,B),2))
# d1 restricted to reverts that touch product or test paths (excludes 'cadence reverted' coordination subjects)
print('\nmonth d1_any d1_touching_pc_or_tests d1_strict_Revert"')
rc=collections.Counter()
for c in commits:
    if c['merge']: continue
    if re.search('revert',c['s'],re.I) and any(f.startswith(PCP+('tests/',)) or f=='main.py' for f in c['files']): rc[mon(c['at'])]+=1
for m in ['2026-03','2026-05','2026-06','2026-07','2026-08','2026-09']: print(m,rev[m],rc[m],revstrict[m])
for c in commits:
    if not c['merge'] and mon(c['at'])=='2026-09' and re.search('revert',c['s'],re.I) and any(f.startswith(PCP+('tests/',)) or f=='main.py' for f in c['files']): print('  ',c['h'][:10],c['s'][:110])
# granularity confound for d2: share of PCs whose subject starts with fix / feat
print('\nmonth pc fix_pc feat_pc fix_share')
fx=collections.Counter(); ft=collections.Counter()
for c in commits:
    if c['merge'] or not any(f.startswith(PCP) or f=='main.py' for f in c['files']): continue
    m=mon(c['at'])
    if re.match(r'fix\b',c['s'],re.I): fx[m]+=1
    if re.match(r'feat\b',c['s'],re.I): ft[m]+=1
for m in ['2026-01','2026-02','2026-03','2026-06','2026-07','2026-08','2026-09']: print(m,pc[m],fx[m],ft[m],round(fx[m]/pc[m],2))
