#!/usr/bin/env bash
dir=${0%/*}; if [ "$dir" = "$0" ]; then dir="."; fi; cd "$dir"; 

echo "$" build.command

echo "$" mkdocs build --clean -f markdown-steroids.yml
mkdocs build --clean -f markdown-steroids.yml

