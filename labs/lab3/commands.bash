#/bin/bash
clear
echo "Ready?"
read
tmux send-keys -t ${TMUX_SESSION}:0.0 C-l
tmux send-keys -t ${TMUX_SESSION}:0.0 "./sleep" C-m
#tmux send-keys -t ${TMUX_SESSION}:0.1 C-l C-m #会崩溃 不知道为什么，手动输入也崩溃
tmux send-keys -t ${TMUX_SESSION}:0.1 C-l "vm" C-m
