#!/usr/bin/env bash
dir=${0%/*}; if [ "$dir" = "$0" ]; then dir="."; fi; cd "$dir"; 

echo "$" build-push-all.command

sh ./build.command

sh ./push-all.command

open 'http://twardoch.github.io/markdown-steroids/'
