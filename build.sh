#!/usr/bin/env bash

if [ -x "$(command -v nukita3)" ]; then
    echo "Missing required tool nukita3"
    exit 0
fi

if [[ $1 == "clean" ]]; then
    rm -rf ./tabby.dist ./tabby.build
else
    nuitka3 ./tabby/tabby.py --standalone
fi

