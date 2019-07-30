#!/bin/bash
git pull https://github.com/cyrilvincent/CovEasyCasting pibox
cd pibox
mv config.py config.old
cp config.linux.py config.py