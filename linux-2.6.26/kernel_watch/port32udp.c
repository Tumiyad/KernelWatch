#include "linux/proc_fs.h"
#pragma GCC optimize("O0")
#include <kernel_watch/port32udp.h>
#include <linux/module.h>
#include <linux/in.h>
#include <linux/skbuff.h>
#include <net/protocol.h>
#include <net/inet_common.h>
#include <net/sock.h>
#include <net/ip.h>
#include <net/inet_sock.h>
#include <asm-x86/uaccess_32.h>
#include <asm-generic/errno-base.h>
// #include <linux/netdevice.h>


#define PORT32UDP_HTABLE_SIZE 1024
static struct hlist_head port32udp_table[PORT32UDP_HTABLE_SIZE];

// struct proto functions
static int port32udp_sendmsg(struct kiocb *iocb, struct sock *sk, struct msghdr *msg, size_t len)
{
    struct sk_buff *skb;
    int err;
    void *data;
    struct port32udp_sock *pudp_sock = (struct port32udp_sock *)sk;
    struct port32udp_hdr *port32udp_hdr;
    int dport = 0;

    // alloc_skb() 会分配一个 struct sk_buff 结构体，以及一个数据区，数据区的大小为 len + MAX_HEADER
    skb = alloc_skb(len + MAX_HEADER, GFP_KERNEL);
    //    skb = alloc_skb(len + sizeof(struct port32udp_hdr), GFP_KERNEL);
    if (!skb)
        return -ENOMEM;

    skb->sk = sk;
    // 调整headroom, 保证头部有足够的空间
    skb_reserve(skb, MAX_HEADER);

    // 分配数据区
    data = skb_put(skb, len);

    // 从用户空间拷贝数据到内核空间
    if (__copy_from_user(data, msg->msg_iov->iov_base, len))
    {
        kfree_skb(skb);
        return -EFAULT;
    }

    if (msg->msg_name)
    {
        struct port32udp_addr *addr = (struct port32udp_addr *)msg->msg_name;
        dport = addr->port;
    }
    else
    {
        printk("msg->msg_name is NULL\n");
        return -1;
    }

    //      add header
    skb_push(skb, sizeof(struct port32udp_hdr));
    skb_reset_transport_header(skb);
    port32udp_hdr = (struct port32udp_hdr *)skb_transport_header(skb);
    port32udp_hdr->source = htonl(pudp_sock->sport);
    port32udp_hdr->dest = htonl(dport);
    //    port32udp_hdr->len = htons(len);

    // 发送数据
    err = ip_queue_xmit(skb, 1);
    if (err)
    {
        kfree_skb(skb);
        return err;
    }

    return len; // 返回发送的字节数
}

int port32udp_recvmsg(struct kiocb *iocb, struct sock *sk, struct msghdr *msg, size_t len, int noblock, int flags, int *addr_len)
{
    struct sk_buff *skb;
    // struct inet_sock *inet = inet_sk(sk);
    int peeked;
    int err;
    skb = __skb_recv_datagram(sk, flags, &peeked, &err);
    // todo set return value to be length of data
    __copy_to_user(msg->msg_iov->iov_base, skb->data + 12, skb->len); // 12 is the length of port32udp header
    return 0;
}

static int port32udp_get_port(struct sock *sk, unsigned int snum)
{
    struct hlist_head *port32udptable = sk->sk_prot->h.udp_hash;
    struct hlist_head *head;
    struct port32udp_sock *pudp_sock = (struct port32udp_sock *)sk;
    int allocated_port = 0;
    printk("port32udp_get_port\n");
    if (!snum)
    {
        // todo 端口分配算法改为随机
        static int port = 0x23456789;
        allocated_port = port++;
    }
    else
    {
        // todo 检查端口是否已经被占用
        allocated_port = snum;
    }
    pudp_sock->sport = allocated_port;
    sk->sk_hash = allocated_port;
    if (sk_unhashed(sk))
    {
        head = &port32udptable[allocated_port & (PORT32UDP_HTABLE_SIZE - 1)];
        sk_add_node(sk, head);
    }
    return 0;
}

static void port32udp_close(struct sock *sk, long timeout)
{
    //    sk_common_release(sk);//sk->sk_prot->destroy(sk); + sk->sk_prot->unhash(sk);
    printk("port32udp_close\n");
}

// struct net_protocol functions

static struct sock *port32udp_lookup(int port)
{
    struct sock *sk, *result = ((void *)0);
    struct hlist_node *node;
    for (node = (&port32udp_table[port & (1024 - 1)])->first; node && ({ prefetch(node->next); 1; }) && ({ sk = ({ const typeof( ((typeof(*sk) *)0)->__sk_common.skc_node ) *__mptr = (node); (typeof(*sk) *)( (char *)__mptr - __builtin_offsetof(typeof(*sk),__sk_common.skc_node) );}); 1; }); node = node->next)
    {
        struct port32udp_sock *pudp_sock = (struct port32udp_sock *)sk;
        if (pudp_sock->sport == port)
        {
            result = sk;
            break;
        }
    }
    return result;
}

// static struct sock *port32udp_lookup(int port){
//     struct sock *sk, *result = NULL;
//     struct hlist_node *node;
//     sk_for_each(sk, node, &port32udp_table[port & (PORT32UDP_HTABLE_SIZE - 1)]) {
//         struct port32udp_sock *pudp_sock = (struct port32udp_sock *)sk;
//         if (pudp_sock->sport == port) {
//             result = sk;
//             break;
//         }
//     }
//     return result;
// }

// This function is responsible for receiving packets for the PORT32UDP protocol.
// It looks up the socket associated with the destination port in the packet,
// and if found, queues the packet in the socket's receive queue and notifies
// the socket that data is ready to be read.
int port32udp_rcv(struct sk_buff *skb)
{
    struct port32udp_hdr *port32udp_hdr = (struct port32udp_hdr *)skb_transport_header(skb); // todo skb_transport_header right?
    struct sock *sk;
    sk = port32udp_lookup(ntohl(port32udp_hdr->dest));
    if (!sk)
    {
        printk("port32udp_rcv: no socket\n");
        return 1;
    }
    // todo receive
    skb_queue_tail(&sk->sk_receive_queue, skb);
    sk->sk_data_ready(sk, 0); // 0?
    return 1;
}

void port32udp_err(struct sk_buff *skb, u32 info)
{
    printk("port32udp_err\n");
}

// struct inet_port32udp_ops fucntions
static int port32udp_autobind(struct sock *sk)
{
    // struct port32udp_sock *pudp_sock = (struct port32udp_sock *)sk;
    if (port32udp_get_port(sk, 0))
        return -1;
    return 0;
}

int inet_port32udp_sendmsg(struct kiocb *iocb, struct socket *sock, struct msghdr *msg,
                           size_t size)
{
    struct port32udp_sock *pudp_sock = (struct port32udp_sock *)sock->sk;
    struct sock *sk = sock->sk;
    if (!pudp_sock->sport && port32udp_autobind(sk))
        return -EAGAIN;
    return sk->sk_prot->sendmsg(iocb, sk, msg, size);
}

int inet_port32udp_bind(struct socket *sock, struct sockaddr *uaddr, int addr_len)
{
    // struct port32udp_sock *pudp_sock = (struct port32udp_sock *)sock->sk;
    struct port32udp_addr addr;
    int snum = 0;
    int (*get_port)(struct sock *sk, unsigned int snum) = (void *)sock->sk->sk_prot->get_port;
    if (__copy_from_user(&addr, uaddr, sizeof(struct port32udp_addr))) // todo __copy_from_user -> copy_from_user
        return -1;
    snum = addr.port;
    get_port(sock->sk, snum);
    return 0;
}

static struct net_protocol port32udp_protocol = {
    .handler = port32udp_rcv,
    .err_handler = port32udp_err,
    .no_policy = 1,
    .netns_ok = 1,
};

static const struct proto_ops inet_port32udp_ops = {
    .family = PF_INET,
    .owner = THIS_MODULE,
    .release = inet_release,
    .bind = inet_port32udp_bind,
    .sendmsg = inet_port32udp_sendmsg,
    .recvmsg = sock_common_recvmsg,
};

static struct proto port32udp_prot = {
    .name = "PORT32UDP",
    .owner = THIS_MODULE, //???
    .obj_size = sizeof(struct port32udp_sock),
    .sendmsg = port32udp_sendmsg,
    .recvmsg = port32udp_recvmsg,
    // 32 bit port , so we cannot use the default get_port definition with snum type short
    .get_port = (int (*)(struct sock *sk, unsigned short snum))port32udp_get_port,
    .close = port32udp_close,
    .h.udp_hash = port32udp_table,
};

static struct inet_protosw port32udp_protosw = {
    .type = SOCK_PORT32UDP,
    .protocol = IPPROTO_PORT32UDP,
    .prot = &port32udp_prot,
    .ops = &inet_port32udp_ops,
    .capability = -1,
    .no_check = 0,
    .flags = INET_PROTOSW_PERMANENT,
};


static ssize_t port32udp_proc_read(struct file *file, char __user *buf, size_t count, loff_t *ppos)
{
    char data[] = "999\n";
    size_t datalen = sizeof(data);

    if (*ppos >= datalen)
        return 0;

    if (count > datalen - *ppos)
        count = datalen - *ppos;

    if (copy_to_user(buf, data + *ppos, count))
        return -EFAULT;

    *ppos += count;
    return count;
}

static const struct file_operations port32udp_proc_fops = {
    .owner = THIS_MODULE,
    .read = port32udp_proc_read,
};

int port32udp_proc_init(void){
    // 创建一个proc文件 值为固定的999
    struct proc_dir_entry *entry;
    entry = proc_create("port32udp", 0, NULL, &port32udp_proc_fops);
    if (!entry)
        return -ENOMEM;
    return 0;
}


int port32udp_init(void)
{
    int err = proto_register(&port32udp_prot, 1);

    if (err != 0)
        goto out;

    port32udp_proc_init();

    err = inet_add_protocol(&port32udp_protocol, IPPROTO_PORT32UDP);
    if (err != 0)
        goto out_proto_unregister;

    inet_register_protosw(&port32udp_protosw);

out:
    return err;

out_proto_unregister:
    proto_unregister(&port32udp_prot);
    goto out;
}



