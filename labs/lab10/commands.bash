#/bin/bash
clear
echo "Ready?"
read
tmux send-keys -t ${TMUX_SESSION}:0.0 C-l
sleep 0.1
tmux send-keys -t ${TMUX_SESSION}:0.1 C-c C-l
tmux send-keys -t ${TMUX_SESSION}:0.1 "b sys_vfork" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "b sys_fork" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "b sys_clone" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "b copy_files" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "b sys_execve" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "c" C-m
tmux send-keys -t ${TMUX_SESSION}:0.0 "./sleep" C-m

