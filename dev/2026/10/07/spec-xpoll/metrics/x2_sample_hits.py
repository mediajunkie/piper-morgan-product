import os,re,random,sys
root='/home/user/piper-morgan-product/dev/2026'
files=[]
for m in ['07','08','09','10']:
    for dp,_,fs in os.walk(os.path.join(root,m)):
        for f in fs:
            if f.endswith('.md') and 'log' in f.lower(): files.append(os.path.join(dp,f))
pat=re.compile(r'cross-poll|xpoll',re.I)
hits=[f for f in files if pat.search(open(f,errors='ignore').read())]
print('log files',len(files),'with mention',len(hits))
random.seed(20261007)
s=random.sample(hits,15)
for f in sorted(s):
    print('\n###',os.path.relpath(f,root))
    n=0
    for i,l in enumerate(open(f,errors='ignore')):
        if pat.search(l):
            n+=1
            if n<=3: print('  L%d: %s'%(i+1,l.strip()[:420]))
    print('  (matching lines: %d)'%n)
