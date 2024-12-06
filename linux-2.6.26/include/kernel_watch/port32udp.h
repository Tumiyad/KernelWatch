#ifndef __PORT32UDP_H__
#define __PORT32UDP_H__

#include <linux/types.h>
#include <linux/net.h>
#include <linux/in.h>
#include <linux/socket.h>
#include <net/inet_sock.h>

int port32udp_init(void);
extern const struct proto_ops inet_sockraw_ops;

struct port32udp_hdr {
	__be32	source;
	__be32	dest;
	__be16	len;
	__sum16	check;
};


struct port32udp_sock {
	struct inet_sock inet;
	__u32 sport;
	__u32 dport;
};

struct port32udp_addr {
    int port;
    struct in_addr	sin_addr;	/* Internet address		*/
    sa_family_t family;
    char padding[6];
};

#endif /* __PORT32UDP_H__ */
