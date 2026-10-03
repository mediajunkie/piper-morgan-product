import json,collections,datetime as dt
rows=[json.loads(l) for l in open('G-issues.jsonl')]
iss=[r for r in rows if not r['pr']]; prs=[r for r in rows if r['pr']]
nums=[r['n'] for r in rows]
print('rows',len(rows),'issues',len(iss),'prs',len(prs),'max#',max(nums),'unique',len(set(nums)))
now=dt.datetime(2026,10,3,tzinfo=dt.timezone.utc)
P=lambda s:dt.datetime.fromisoformat(s.replace('Z','+00:00'))
op=[r for r in iss if r['s']=='open']; cl=[r for r in iss if r['s']=='closed']
print('open',len(op),'closed',len(cl), 'open PRs',sum(1 for r in prs if r['s']=='open'))
b=collections.Counter()
for r in op:
    d=(now-P(r['c'])).days
    b['<30' if d<30 else '30-90' if d<90 else '90-180' if d<180 else '180-365' if d<365 else '>=365']+=1
print('open age',dict(b))
ages=sorted((now-P(r['c'])).days for r in op); print('median open age',ages[len(ages)//2])
lab=collections.Counter(l for r in op for l in r['l']); print('open labels top',lab.most_common(35))
pri=collections.Counter(next((l for l in r['l'] if l.lower().startswith(('priority','p0','p1','p2','p3'))),'none') for r in op); print('open priority',pri.most_common())
print('closed reasons',collections.Counter(r['r'] for r in cl))
# by month created/closed
cm=collections.Counter(r['c'][:7] for r in iss); xm=collections.Counter(r['x'][:7] for r in cl if r['x'])
for m in sorted(set(cm)|set(xm)): print(m,cm[m],xm[m])
auth=collections.Counter(r['u'] for r in iss); print('authors',auth.most_common(10))
kw=('feedback','alpha','tester','user-report','beta')
fl=collections.Counter(l for r in iss for l in r['l'] if any(k in l.lower() for k in kw)); print('feedback-ish labels',fl)
tt=[r for r in iss if any(k in r['t'].lower() for k in ('tester','feedback','alpha user','ted','beatrice','windows'))]
print('title mentions',len(tt)); 
for r in tt[:40]: print(r['n'],r['s'],r['c'][:10],r['l'][:3],r['t'][:90])
