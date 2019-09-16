#!/bin/bash
echo Stop the pibox service
sudo systemctl stop pibox.service
echo Kill
pkill -9 python3

