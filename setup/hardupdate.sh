#!/bin/bash
cd ..
git reset --hard origin/master
git clean -fxd
git pull
cp config.linux.py config.py