import os,re,collections
root='/home/user/piper-morgan-product/dev/2026'
pat=re.compile(r'cross-poll|xpoll',re.I)
files=[]
for m in ['07','08','09','10']:
    for dp,_,fs in os.walk(os.path.join(root,m)):
        for f in fs:
            if f.endswith('.md') and 'log' in f.lower(): files.append(os.path.join(dp,f))
cls=collections.Counter(); ex=collections.defaultdict(list)
nf=0
for f in files:
    L=open(f,errors='ignore').read().split('\n')
    idx=[i for i,l in enumerate(L) if pat.search(l)]
    if not idx: continue
    nf+=1
    # classify file by strongest signal among matching lines
    labels=set()
    for i in idx:
        ctx=' '.join(L[max(0,i-3):i+1]).lower()
        if 'loaded but not referenced' in ctx or 'not referenced' in L[i].lower() or 'not read' in L[i].lower(): labels.add('loaded-not-referenced')
        elif re.search(r'wanted but not found',ctx): labels.add('wanted-not-found')
        elif re.search(r'\*\*referenced\*\*|^- referenced|referenced:',ctx): labels.add('referenced-bucket')
        elif re.search(r'cross-pollination (brief )?(says|flagged|surfaced|item|insight|suggested)|acted on|per the (xpoll|cross-poll)',L[i].lower()): labels.add('acted/cited')
        else: labels.add('other-mention')
    for pri in ['acted/cited','referenced-bucket','wanted-not-found','other-mention','loaded-not-referenced']:
        if pri in labels: cls[pri]+=1; ex[pri].append(os.path.relpath(f,root)); break
print('log files',len(files),'with xpoll mention',nf)
print(cls)
for k in ['acted/cited','referenced-bucket','wanted-not-found','other-mention']:
    print(k); [print('   ',x) for x in ex[k][:60]]
