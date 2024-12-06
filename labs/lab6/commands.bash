#/bin/bash
clear
echo "Ready?"
read
tmux send-keys -t ${TMUX_SESSION}:0.0 C-l
sleep 0.1
tmux send-keys -t ${TMUX_SESSION}:0.1 C-c C-l
# start
tmux send-keys -t ${TMUX_SESSION}:0.1 "c" C-m
tmux send-keys -t ${TMUX_SESSION}:0.0 "./loop" C-m
sleep 0.5
tmux send-keys -t ${TMUX_SESSION}:0.1 C-c C-l
#tmux send-keys -t ${TMUX_SESSION}:0.1 "b n_tty_receive_char" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "b kill_pgrp" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "c" C-m
tmux send-keys -t ${TMUX_SESSION}:0.0 C-c



