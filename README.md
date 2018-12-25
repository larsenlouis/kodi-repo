# Kodi addons

repo: [https://larsenlouis.github.io/kodi-repo/_repo/](https://larsenlouis.github.io/kodi-repo/_repo/)


## build

```
# create addon project and code there
# mkdir plugin.foo.bar
# code your stuff

# generate repo
cd _tool
python2 generate_repo.py
# generate html
cp index.sh ../_repo/
cp autoindex.html ../_repo/
cd ../_repo/
bash index.sh
```

## deploy

```
git add .
git commit -m "your message"
git push
```