#!/bin/bash
# Update except local changes (config.py)
cd ..
git stash
git pull
git stash pop