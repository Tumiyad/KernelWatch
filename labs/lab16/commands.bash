#/bin/bash
clear
echo "Ready?"
read
tmux send-keys -t ${TMUX_SESSION}:0.0 C-l
sleep 0.1
tmux send-keys -t ${TMUX_SESSION}:0.1 C-c C-l
#tmux send-keys -t ${TMUX_SESSION}:0.1 "b sys_sendto" C-m
#tmux send-keys -t ${TMUX_SESSION}:0.1 "b inet_create" C-m
#tmux send-keys -t ${TMUX_SESSION}:0.1 "b inet_autobind" C-m
#tmux send-keys -t ${TMUX_SESSION}:0.1 "b sys_close" C-m
#tmux send-keys -t ${TMUX_SESSION}:0.1 "b filp_close" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "b port32udp_rcv" C-m
#tmux send-keys -t ${TMUX_SESSION}:0.1 "b port32udp_get_port" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "b inet_port32udp_bind" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "b port32udp_sendmsg" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "b port32udp_lookup" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "b port32udp_recvmsg" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "b port32udp.c:80" C-m
tmux send-keys -t ${TMUX_SESSION}:0.1 "c" C-m

#tmux send-keys -t ${TMUX_SESSION}:0.1 "p skb->data" C-m
#tmux send-keys -t ${TMUX_SESSION}:0.1 C-x "a" C-m
tmux send-keys -t ${TMUX_SESSION}:0.0 "./port32udp_receive &" C-m
tmux send-keys -t ${TMUX_SESSION}:0.0 "./port32udp_send" C-m

