#/bin/bash
clear
sleep 5
tmux send-keys -t ${TMUX_SESSION}:0.0 "./loop" C-m
sleep 0.5
tmux send-keys -t ${TMUX_SESSION}:0.1 "disable" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "c" C-m
sleep 0.1
tmux send-keys -t ${TMUX_SESSION}:0.1 C-c
tmux send-keys -t ${TMUX_SESSION}:0.1 "enable" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "c" C-m
sleep 0.1
tmux send-keys -t ${TMUX_SESSION}:0.0 "a" C-m
#tmux send-keys -t ${TMUX_SESSION}:0.1 "c" C-m
#tmux send-keys -t ${TMUX_SESSION}:0.1 "c" C-m
#tmux send-keys -t ${TMUX_SESSION}:0.0 "kill -9 1019" C-m
