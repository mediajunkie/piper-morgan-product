# V1 independent: PM-addressed share of memos, last 8 weeks, read from the SNAPSHOT tree (not working tree).
# Unit: unique filename under mailboxes/*/sent/. Date: frontmatter date, else filename date.
# PM-addressed (strict): a to/cc token equal to pm|xian|ceo|xian (ceo) or containing 'xian'. (loose = F's rule incl. ' pm'/'pm ' substrings)
import subprocess, re, datetime as dt, collections
R='/home/user/piper-morgan-product'; S='a191856164351cf59ba033d7dbc4a34f036c6122'
names=[n for n in subprocess.run(['git','-C',R,'-c','core.quotepath=off','ls-tree','-r','--name-only',S,'mailboxes'],capture_output=True,text=True).stdout.splitlines() if '/sent/' in n and n.endswith('.md') and not n.endswith('MANIFEST.md')]
seen={};
for n in names:
    b=n.rsplit('/',1)[1]
    if b not in seen: seen[b]=n
inp='\n'.join(f'{S}:{p}' for p in seen.values())+'\n'
raw=subprocess.run(['git','-C',R,'cat-file','--batch'],input=inp.encode(),capture_output=True).stdout
blobs=[];i=0
while i<len(raw):
    j=raw.index(b'\n',i); hdr=raw[i:j].split(); size=int(hdr[2]); blobs.append(raw[j+1:j+1+size].decode('utf-8','replace')); i=j+1+size+1
END=dt.date(2026,10,3)
tot=collections.Counter(); strict=collections.Counter(); loose=collections.Counter(); words=collections.Counter(); tostrict=collections.Counter()
for (b,p),txt in zip(seen.items(),blobs):
    m=re.match(r'---\n(.*?)\n---\n',txt,re.S); fm={}
    if m:
        for l in m.group(1).splitlines():
            if ':' in l: k,v=l.split(':',1); fm[k.strip().lower()]=v.strip()
    d=None
    for src in (fm.get('date',''),b):
        mm=re.search(r'(20\d\d)-(\d\d)-(\d\d)',src)
        if mm:
            try: d=dt.date(*map(int,mm.groups())); break
            except ValueError: pass
    if not d: continue
    w=(END-d).days//7
    if w<0 or w>=8: continue
    tot[w]+=1
    toks=[t.strip().strip('"\'').lower() for k in ('to','cc') for t in re.split(r'[,;\[\]]',fm.get(k,'')) if t.strip()]
    s=any(t in ('pm','xian','ceo','xian (ceo)') or 'xian' in t or t.startswith('pm ') or t.startswith('pm(') for t in toks)
    l=any(('xian' in t or 'ceo' in t or ' pm' in t or 'pm ' in t or t in('pm','xian')) for t in toks)
    tt=[t.strip().strip('"\'').lower() for t in re.split(r'[,;\[\]]',fm.get('to','')) if t.strip()]
    if s: strict[w]+=1; words[w]+=len((txt[m.end():] if m else txt).split())
    if l: loose[w]+=1
    if any(t in ('pm','xian','ceo','xian (ceo)') or 'xian' in t for t in tt): tostrict[w]+=1
T=sum(tot.values())
print('unique memos (snapshot sent/ mirrors):',len(seen),' in 8w window:',T)
print('PM-addressed strict:',sum(strict.values()),f'{sum(strict.values())/T:.1%}','| loose (F rule):',sum(loose.values()),f'{sum(loose.values())/T:.1%}','| PM in to: only',sum(tostrict.values()),f'{sum(tostrict.values())/T:.1%}')
print('PM-addressed body words/week (strict):',round(sum(words.values())/8))
for w in range(8): print(END-dt.timedelta(days=7*w),tot[w],strict[w],loose[w],tostrict[w],words[w])
