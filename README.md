# Kodi addons

## build

```
# create addon project and code there
# mkdir plugin.foo.bar
# code your stuff

# generate repo
cd _tool
python2 generate_repo.py
# generate html
cd ../_repo
bash index.sh
```

## deploy

```
git add .
git commit -m "your message"
git push
```