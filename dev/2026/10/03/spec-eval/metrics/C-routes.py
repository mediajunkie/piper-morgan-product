import re,os,json,glob
d=json.load(open('/tmp/claude-0/-home-user/03717665-1eb6-52ef-ab7b-3677cba046df/scratchpad/openapi.json'))
live=set((m.upper(),p) for p,v in d['paths'].items() for m in v)
rows=[]
for f in sorted(glob.glob('web/**/*.py',recursive=True)+['main.py']+glob.glob('services/**/*.py',recursive=True)):
    s=open(f).read()
    pre=re.findall(r'APIRouter\([^)]*prefix\s*=\s*["\']([^"\']*)',s)
    pre=pre[0] if pre else ''
    for m,p in re.findall(r'@\w+\.(get|post|put|patch|delete|websocket)\(\s*["\']([^"\']*)',s):
        full=(pre+p) or '/'
        ok=(m.upper(),full) in live or (m.upper(),full.rstrip('/')) in live
        rows.append((f,m.upper(),full,ok))
from collections import defaultdict
by=defaultdict(lambda:[0,0])
for f,m,p,ok in rows: by[f][0]+=1; by[f][1]+=ok
for f,(n,k) in by.items(): print(f"{k:3}/{n:3} {f}")
print('total',len(rows),'live-matched',sum(r[3] for r in rows))
print('NOT LIVE:'); [print(' ',m,p,f) for f,m,p,ok in rows if not ok]
