#!/bin/bash

set -e

sudo apt install python3 python3-pip ffmpeg
sudo pip3 install virtualenv

virtualenv venv
source venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt