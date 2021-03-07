#!/usr/bin/env bash
dir=${0%/*}
if [ "$dir" = "$0" ]; then dir="."; fi
cd "$dir"

echo "$" build.command

scss docs/style/_keys.scss docs/style/keys.css
echo "$" python3 -m mkdocs build -v --clean -f markdown-steroids.yml
python3 -m mkdocs build -v --clean -f markdown-steroids.yml
