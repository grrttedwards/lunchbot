#!/bin/bash
until lunchbot.py; do
    echo "'lunchbot.py' crashed with exit code $?. Restarting..." >&2
    sleep 1
done