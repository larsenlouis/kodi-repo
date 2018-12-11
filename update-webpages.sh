#!/bin/bash

cd _repo
bash index.sh
echo
echo "=== web files briefing ==="
git status --porcelain .