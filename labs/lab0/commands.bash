#/bin/bash
clear
echo "Starting kernel_watch..."
sleep 5
tmux send-keys -t ${TMUX_SESSION}:0.0 "./kernel_watch" C-m
#tmux send-keys -t ${TMUX_SESSION}:0.1 C-l
