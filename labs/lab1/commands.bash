#/bin/bash
sleep 5
tmux send-keys -t ${TMUX_SESSION}:0.0 "./loop" C-m
sleep 1
tmux send-keys -t ${TMUX_SESSION}:0.1 C-c
tmux send-keys -t ${TMUX_SESSION}:0.1 "bk" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "c" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "layout split" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "bt" C-m