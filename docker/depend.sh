#!/bin/sh

apt update && apt install -y python3.7* ffmpeg python3-pip git
pip3 install pipenv
cd tmp
LC_ALL=C.UTF-8 LANG=C.UTF-8 pipenv install --system --skip-lock --dev
