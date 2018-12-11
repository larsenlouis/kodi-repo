#!/bin/bash
# make this static site that mimics nginx autoindex

set -ex

echo "" > index.html

AUTOINDEX_HTML=$(pwd -P)/autoindex.html
for DIR in . $(ls -l | grep '^d' | awk '{print $NF}'); do
    pushd ${DIR}
    ls -phl --time-style='+%d-%b-%Y %H:%M' | awk 'NR>1' | grep -v -w 'index.html' | grep -v -w 'push.sh' | sort -k1,1 -k8,8 | awk 'BEGIN{print "<html><head><title>Index of /</title><meta charset=\"UTF-8\"></head><body><pre>"} {printf("<a href=\"%s\">%s</a>\t%s %s %s\n", $8, $8, $6, $7, $5)} END{print "</pre></body></html>"}' >index.html
    cat ${AUTOINDEX_HTML} >>index.html
    popd
done

