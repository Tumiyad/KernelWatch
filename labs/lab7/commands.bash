#/bin/bash
clear
sleep 5
tmux send-keys -t ${TMUX_SESSION}:0.0 "./loop" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "c" C-m
sleep 1
tmux send-keys -t ${TMUX_SESSION}:0.0 "a"
tmux send-keys -t ${TMUX_SESSION}:0.1 "until 3758" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 C-x "2" C-x "2"
tmux send-keys -t ${TMUX_SESSION}:0.1 "b uart_flush_chars" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "c" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "b drivers/serial/8250.c:433" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "commands 4" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "p up->port.iobase + offset" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "p value" C-m
#tmux send-keys -t ${TMUX_SESSION}:0.1 "end" C-m
#tmux send-keys -t ${TMUX_SESSION}:0.1 "c" C-m
#tmux send-keys -t ${TMUX_SESSION}:0.1 "c" C-m
#tmux send-keys -t ${TMUX_SESSION}:0.0 "kill -9 1019" C-m
