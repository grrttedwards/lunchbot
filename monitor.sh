#!/bin/bash
until python lunchbot.py >> log.log $2>1; do
    echo "'lunchbot.py' crashed with exit code $?. Restarting..." >&2
    sleep 1
done
