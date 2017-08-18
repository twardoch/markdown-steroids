#!/usr/bin/env bash
dir=${0%/*}; if [ "$dir" = "$0" ]; then dir="."; fi; cd "$dir"; 

echo "$" push-all.command

echo "$" git add --all
git add --all

echo "$" git commit -am "$(echo $(git status -s -uno) | cut -c1-50) ($(whoami) $(date +'%Y-%m-%d %H:%M:%S'))"  
git commit -am "$(echo $(git status -s -uno) | cut -c1-50) ($(whoami) $(date +'%Y-%m-%d %H:%M:%S'))" 

echo "$" git fetch origin
git fetch origin

echo "$" git merge origin/master -m "$(echo $(git status -s -uno) | cut -c1-50) ($(whoami) $(date +'%Y-%m-%d %H:%M:%S'))" 
git merge origin/master -m "$(echo $(git status -s -uno) | cut -c1-50) ($(whoami) $(date +'%Y-%m-%d %H:%M:%S'))" 

echo "$" git push -u origin master 
git push -u origin master 
