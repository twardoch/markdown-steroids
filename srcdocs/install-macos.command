#!/usr/bin/env bash
dir=${0%/*}; if [ "$dir" = "$0" ]; then dir="."; fi; cd "$dir"; 

echo "###"
echo "### Run this when tools are updated"
echo "###"
echo
echo "$" install.command

echo "Please enter your administrator password!"

sudo chown -R $(whoami) $HOME/Library/Logs/pip
sudo chown -R $(whoami) $HOME/Library/Caches/pip

# Check if brew is installed
if [ ! -x "$(which brew)" ]; then
	echo "# Installing 'brew'..."
	/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
else
	echo "# Updating 'brew'..."
	brew update
fi 

brew install git 2>/dev/null
brew upgrade git 2>/dev/null

# Install pandoc if needed
if [ ! -x "$(which pandoc)" ]; then
	echo "$ brew install pandoc"
	brew install pandoc
else
	echo "$ brew upgrade pandoc && brew cleanup pandoc"
	brew upgrade pandoc && brew cleanup pandoc
fi 

# Update Python tools

echo "$" pip install --user --upgrade -r py-requirements.txt
pip install --user --upgrade -r py-requirements.txt

echo "### INSTALLATION FINISHED!"
