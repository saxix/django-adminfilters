#!/bin/bash
shopt -s nullglob

for filename in $1/*.mov; do
  ffmpeg \
    -y \
    -v 0 \
    -i $filename \
    -r 15 \
    -vf scale=512:-1 \
    "$1/$(basename "$filename" .mov).gif"
done
