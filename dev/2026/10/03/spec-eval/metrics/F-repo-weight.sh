#!/bin/bash
# F-repo-weight.sh — share of repo history (unique blob bytes, uncompressed; and on-disk compressed size) by top-level area, at snapshot.
cd /home/user/piper-morgan-product
SNAP=a191856164351cf59ba033d7dbc4a34f036c6122
git rev-list --objects $SNAP | git cat-file --batch-check='%(objecttype) %(objectsize) %(objectsize:disk) %(rest)' |
awk '$1=="blob"{p=$4; split(p,a,"/"); k=a[1]; if(k=="dev"||k=="docs") k=a[1]"/"a[2]; u[k]+=$2; d[k]+=$3; n[k]++; U+=$2; D+=$3}
END{for(k in u) printf "%-28s blobs=%7d uncompressed_MB=%8.1f disk_MB=%7.1f disk_share=%5.1f%%\n",k,n[k],u[k]/1e6,d[k]/1e6,100*d[k]/D; printf "TOTAL uncompressed_MB=%.1f disk_MB=%.1f\n",U/1e6,D/1e6}' | sort -t= -k4 -rn | head -16
echo "tracked files at snapshot:"; git ls-tree -r --name-only $SNAP | awk -F/ '{print $1}' | sort | uniq -c | sort -rn | head -8
