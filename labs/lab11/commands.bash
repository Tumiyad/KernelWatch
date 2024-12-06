#/bin/bash
clear
echo "Ready?"
read
tmux send-keys -t ${TMUX_SESSION}:0.1 "c" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "c" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "c" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "c" C-m
echo "Please watch the process switch order."
echo "OK?"
read
tmux send-keys -t ${TMUX_SESSION}:0.1 "disable 1" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "disable 2" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "disable 3" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "c" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 C-l
tmux send-keys -t ${TMUX_SESSION}:0.1 "bt" C-m
echo "User process will be created in init_post."
echo "Do you see it?"
read
tmux send-keys -t ${TMUX_SESSION}:0.1 "b kernel_execve" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "c" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 C-l
tmux send-keys -t ${TMUX_SESSION}:0.1 "bt" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "p filename" C-m
echo "Look at the filename."
echo "/init will be executed."
read
#tmux send-keys -t ${TMUX_SESSION}:0.1 "b sys_vfork" C-m
#tmux send-keys -t ${TMUX_SESSION}:0.1 "b sys_fork" C-m
#tmux send-keys -t ${TMUX_SESSION}:0.1 "b sys_clone" C-m
#tmux send-keys -t ${TMUX_SESSION}:0.1 "b copy_files" C-m
#tmux send-keys -t ${TMUX_SESSION}:0.1 "b sys_execve" C-m
#tmux send-keys -t ${TMUX_SESSION}:0.1 "c" C-m
#tmux send-keys -t ${TMUX_SESSION}:0.0 "./sleep" C-m

