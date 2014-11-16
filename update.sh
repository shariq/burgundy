#!/bin/bash

cp index.* /usr/share/nginx/html
cp favicon.ico /usr/share/nginx/html

git add .
git commit
git push
