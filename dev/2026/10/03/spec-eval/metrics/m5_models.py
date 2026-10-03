# Model-timeline (prereg confound): first commit in which each model-name string appears in dev/, docs/, .claude/, CLAUDE.md
# (git log -S --reverse, author date). This is FIRST MENTION IN REPO, NOT the vendor release date; release dates are unsourced in-repo.
import csv
from common import *
names=['opus 4.1','Opus 4.5','Sonnet 4.5','Haiku 4.5','Sonnet 4.6','Opus 4.6','Opus 4.7','Opus 4.8','Opus 5','Sonnet 5','Opus 5.5','Sonnet 5.5']
w=csv.writer(open('m5_models_first_mention.csv','w',newline=''));w.writerow(['model_string','first_mention_date','sha','subject'])
for n in names:
    o=git('log',SNAP,'-i','-S'+n,'--reverse','--format=%h|%ad|%s','--date=short','--','dev','docs','.claude','CLAUDE.md').splitlines()
    if o: h,d,s=o[0].split('|',2);w.writerow([n,d,h,s[:90]]);print(n,d,h,s[:70])
    else: print(n,'none')
