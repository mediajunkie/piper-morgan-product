# Per-role activity. (a) commits/month by role slug parsed from subjects of form mail(role)/log(role)/hb(role)/hb-last-invoked(role)/
# stop(role)/heartbeat(role) [first token inside parens, lowercased, trimmed of '-code']; (b) NEW session-log files per month by role from
# filenames dev/**/YYYY-MM-DD-HHMM-{role}-*-log.md (role = tokens after the HHMM up to the tool token 'code'/'opus'/'sonnet'; first add only).
# Git author is NOT used.
import csv,re,collections
from common import *
S=re.compile(r'^(mail|log|hb-last-invoked|hb|stop|heartbeat)\(([^)]*)\)',re.I)
a=collections.defaultdict(collections.Counter)
for l in stream('log',SNAP,'--no-merges','--format=%at|%s'):
    at,s=l.split('|',1);m=S.match(s)
    if m:
        r=re.split(r'[ ,/→>+]',m.group(2).strip().lower())[0].replace('-code','');a[month(at)][r]+=1
roles=collections.Counter()
for m in a:roles.update(a[m])
top=[r for r,_ in roles.most_common(25)]
with open('m6_roles_commits.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['month']+top+['other'])
    for m in months():
        c=a[m];w.writerow([m]+[c[r] for r in top]+[sum(v for k,v in c.items() if k not in top)])
b=collections.defaultdict(collections.Counter);F=re.compile(r'(\d{4}-\d\d-\d\d)-(\d{4})-(.+?)-log\.md$')
cur=None
for l in stream('log',SNAP,'--no-renames','--diff-filter=A','--name-only','--format=@@%at','--','dev'):
    if l.startswith('@@'):cur=l[2:];continue
    if l.endswith('-log.md'):
        m=F.search(l.rsplit('/',1)[-1])
        if m:
            r=re.sub(r'-(code|opus|sonnet|haiku)(-.*)?$','',m.group(3));b[month(cur)][r]+=1
rl=collections.Counter()
for m in b:rl.update(b[m])
top2=[r for r,_ in rl.most_common(25)]
with open('m6_roles_sessionlogs.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['month']+top2+['other'])
    for m in months():
        c=b[m];w.writerow([m]+[c[r] for r in top2]+[sum(v for k,v in c.items() if k not in top2)])
print('subject-role totals',roles.most_common(20));print('logfile-role totals',rl.most_common(20))
