#!/bin/bash
python generate-config-files.py -n 4 -t 1 localhost:9001 localhost:9002 localhost:9003 localhost:9004
K=${1:-32}
PROGRAM="shuffler.py -K ${K} --no-ssl --statistics --deferred-debug"
set -x
tmux new-session "python ${PROGRAM} player-1.ini; bash" \; \
     splitw -h -p 50 "python ${PROGRAM} player-2.ini; bash" \; \
     splitw -v -p 50 "python ${PROGRAM} player-3.ini; bash" \; \
     selectp -t 0 \; \
     splitw -v -p 50 "python ${PROGRAM} player-4.ini; bash"
