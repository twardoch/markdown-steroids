#!/usr/bin/env bash
dir=${0%/*}; if [ "$dir" = "$0" ]; then dir="."; fi; cd "$dir"; 
git add --all; 
git commit -am "$(echo $(git status -s -uno) | cut -c1-50) ($(whoami) $(date +'%Y-%m-%d %H:%M:%S'))"; 
git pull; git push;