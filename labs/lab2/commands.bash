#/bin/bash
sleep 3
tmux send-keys -t ${TMUX_SESSION}:0.0 "./server &" C-m
tmux send-keys -t ${TMUX_SESSION}:0.0 "./connect_flood" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "c" C-m C-l "bt" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "c" C-m "c" C-m C-l "bt" C-m
