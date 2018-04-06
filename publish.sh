#!/bin/bash
for i in $( ls *.ipynb ); do
    jupyter-nbconvert --to slides $i --reveal-prefix=reveal.js
done
mkdir -p /tmp/workspace
cp -r * /tmp/workspace/
git add -A .
git commit -m "Update"
git checkout -B gh-pages
cp -r /tmp/workspace/* .
git add -A .
git commit -m "new version"
git push origin master gh-pages
git checkout master
rm -rf /tmp/workspace
