#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <unistd.h>

#define SYS_SOCKETCALL 102
#define SYS_SOCKET 1

// 内联汇编函数创建套接字
int create_socket(int domain, int type, int protocol) {
    int sockfd;
    struct {
        int domain;
        int type;
        int protocol;
    } args;

    // 填充参数
    args.domain = domain;
    args.type = type;
    args.protocol = protocol;

    __asm__ (
        "movl %1, %%eax\n"    // syscall number (sys_socketcall)
        "movl %2, %%ebx\n"    // argument 1: socketcall number (SYS_SOCKET)
        "movl %3, %%ecx\n"    // argument 2: pointer to struct with (domain, type, protocol)
        "int $0x80\n"         // call kernel
        "movl %%eax, %0\n"    // return value
        : "=r" (sockfd)       // output
        : "i" (SYS_SOCKETCALL), "i" (SYS_SOCKET), "r" (&args) // input
        : "%eax", "%ebx", "%ecx" // clobbered registers
    );
    return sockfd;
}

//struct sockaddr {
//	sa_family_t	sa_family;	/* address family, AF_xxx	*/
//	char		sa_data[14];	/* 14 bytes of protocol address	*/
//};

struct port32udp_addr {
    int port;
    struct in_addr	sin_addr;	/* Internet address		*/
    sa_family_t family;
    char padding[6];
};


int main() {
    int sockfd;
//    struct sockaddr_in dest_addr;
    struct port32udp_addr dest_addr;
    const char *message = "hellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohello";

    // 创建原始套接字
    sockfd = create_socket(AF_INET, 11, 137);
    if (sockfd < 0) {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    memset(&dest_addr, 0, sizeof(dest_addr));
    dest_addr.family = AF_INET;
    dest_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
    dest_addr.port =  0x12345678;

    // 发送数据
    if (sendto(sockfd, message, strlen(message), 0, (struct sockaddr *)&dest_addr, sizeof(dest_addr)) < 0) {
        perror("sendto");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    printf("Message sent successfully\n");

    // 关闭套接字
    close(sockfd);
    return 0;
}
