#!/bin/sh

echo "${FLAG:-flag{fluxxx\}}" > /flag
unset FLAG
socat -T600 tcp-listen:1024,fork,reuseaddr exec:./declass
