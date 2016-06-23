#!/bin/bash
until python -u lunchbot.py $> lunchbot.log; do
    echo "'lunchbot.py' crashed with exit code $?. Restarting..." >&2
    sleep 1
done
