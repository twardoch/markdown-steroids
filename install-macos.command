#!/usr/bin/env bash
dir=${0%/*}
if [ "$dir" = "$0" ]; then dir="."; fi
cd "$dir"

# Install me
pip3 install --user --upgrade -r py-requirements.txt
pip3 install --user --upgrade .
echo "# Done!"
