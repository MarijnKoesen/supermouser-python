#!/bin/sh
set -e 

cd "$(dirname "$0")"

if [ ! -d build  ]; then
	mkdir build
fi

cd build

pyinstaller --name 'SuperMouser' \
            --icon '../supermouser.ico' \
            --windowed \
            ../supermouser.py
