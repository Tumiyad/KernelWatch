#/bin/bash
#sleep 5
clear
tmux send-keys -t ${TMUX_SESSION}:0.0 "./loop" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "bt" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "current_task" C-m
read -p "Press enter to continue"
tmux send-keys -t ${TMUX_SESSION}:0.1 "delete 1" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "b create_workqueue_thread" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "c" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "b kthread_create" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "c" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 C-l
tmux send-keys -t ${TMUX_SESSION}:0.1 "bt" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "current_task" C-m
