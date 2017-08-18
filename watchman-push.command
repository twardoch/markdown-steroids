#!/usr/bin/env bash
# watchman-push.command
dir=${0%/*}; if [ "$dir" = "$0" ]; then dir="."; fi; cd "$dir"; 
brew install watchman coreutils; brew upgrade watchman coreutils; 
watchman watch "$dir";
watchman -- trigger "$dir" auto-push-$(basename $(grealpath "$dir" | tr ' ' '-')) '*' -- '$(grealpath "$dir")/git-push.command';
