#!/usr/bin/env python3
"""M2.3 narrative share over every line of CLAUDE.md @ a191856.
Rule (per line, first match wins):
 FORMAT: blank, heading (#), hr (---), code-fence line, table separator, html comment/blockquote marker-only.
 RATIONALE/HISTORY (narrow, 'strict'): line has a calendar date (YYYY-MM-DD or 'Mon D'), OR an incident/history marker
   (incident|root-caus|diagnos|ratified|PM-ruled|PM ruling|PM directive|found|learned|real instance|history|was |were |previously|used to|originally|wiped|lost|caused|since 20|revised|corrected|added 20|investigat|evidence behind).
 BROAD adds: explanatory markers (because|why|so that|reason|the point|rationale|principle|metaphor|reality|this is normal|means that|e\.g\.|—.*(which|that) )
 INSTRUCTION: everything else (imperatives, commands, pointers/tables, rules, code lines).
Lines inside fenced code blocks are INSTRUCTION unless blank.
"""
import re,random,csv,sys
L=open('/home/user/audit-wt/CLAUDE.md',encoding='utf-8').read().split('\n')
if L and L[-1]=='':L=L[:-1]
date=re.compile(r'20\d\d-\d\d-\d\d|\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}\b|\b(June|July|August|September) 20\d\d|2026')
hist=re.compile(r'incident|root-caus|diagnos|ratified|PM-ruled|PM ruling|PM directive|PM-mandated|PM-approved|\bfound\b|learned|real instance|history|\bwas\b|\bwere\b|previously|used to|originally|wiped|\blost\b|caused|revised|corrected|investigat|concrete incident|\bnow fixed\b|measured at|surfaced|\bhad been\b|\bdid\b.*\bnot\b',re.I)
broad=re.compile(r'because|\bwhy\b|so that|reason|the point|rationale|principle|metaphor|the reality|this is normal|that is why|which is why|exists (to|because)|the cost of|is what|failure mode|antipattern|anti-pattern',re.I)
def classify(i,l,infence,mode):
    s=l.strip()
    if s=='' : return 'format'
    if s.startswith('```'): return 'format'
    if infence: return 'instruction'
    if re.match(r'^#{1,6} ',s) or re.match(r'^[-*_]{3,}$',s) or re.match(r'^\|[\s:|-]+\|?$',s) or s in('>','<!--','-->') : return 'format'
    if date.search(s) or hist.search(s): return 'rationale'
    if mode=='broad' and broad.search(s): return 'rationale'
    return 'instruction'
res={}
for mode in('strict','broad'):
    inf=False;out=[]
    for i,l in enumerate(L,1):
        if l.strip().startswith('```'):
            c=classify(i,l,False,mode);inf=not inf
        else: c=classify(i,l,inf,mode)
        out.append(c)
    res[mode]=out
from collections import Counter
for m in res:
    c=Counter(res[m]);n=len(L);ne=n-c['format']
    print(m,dict(c),'N',n,'rationale/N=%.3f'%(c['rationale']/n),'rationale/nonformat=%.3f'%(c['rationale']/ne))
w=csv.writer(open('D-m23-lines.csv','w'));w.writerow(['line','strict','broad','text']);[w.writerow([i+1,res['strict'][i],res['broad'][i],L[i][:200]]) for i in range(len(L))]
# nonblank-line variant & char-weighted
for m in res:
    ch=Counter()
    for c,l in zip(res[m],L): ch[c]+=len(l)
    print(m,'char share',{k:round(v/sum(ch.values()),3) for k,v in ch.items()})
random.seed(7);idx=sorted(random.sample([i for i,l in enumerate(L) if l.strip()],50))
w=csv.writer(open('D-m23-spot50.csv','w'));w.writerow(['line','auto_strict','auto_broad','text'])
for i in idx: w.writerow([i+1,res['strict'][i],res['broad'][i],L[i][:240]])
print(len(idx))
