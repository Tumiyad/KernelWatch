#/bin/bash
#clear
#echo "Ready?"
#read
sleep 5
tmux send-keys -t ${TMUX_SESSION}:0.0 C-l
tmux send-keys -t ${TMUX_SESSION}:0.0 "./page_fault_test" C-m
#tmux send-keys -t ${TMUX_SESSION}:0.1 "c" C-m
