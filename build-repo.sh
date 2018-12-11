#/bin/bash

read -p "Have you finished your source code changes and BUMPED your version numbers? " choice
echo    # (optional) move to a new line
if [[ $choice =~ ^[Yy]$ ]]
then
    cd _tools
    python2 generate_repo.py
fi
