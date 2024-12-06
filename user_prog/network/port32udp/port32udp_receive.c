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

struct port32udp_addr {
    int port;
    struct in_addr	sin_addr;	/* Internet address		*/
    sa_family_t family;
    char padding[6];
};


int main() {
    int sockfd;
    struct port32udp_addr server_addr;
    const char *message = "hellohellohelohellohello";

    sockfd = create_socket(AF_INET, 11, 137);
    if (sockfd < 0) {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.family = AF_INET;
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
    server_addr.port =  0x12345678;
    
    if (bind(sockfd, (const struct sockaddr *)&server_addr, sizeof(server_addr)) < 0 ) {
        perror("绑定失败");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    //接收数据
    char buffer[2048];
    struct port32udp_addr client_addr;
    int n = recvfrom(sockfd, (char *)buffer, 2048, 0,
             (struct sockaddr *)&client_addr, sizeof(client_addr));
    printf("n=%d", n);
//    buffer[100] = '\0'; // 确保字符串终止
    printf("Client : %s\n", buffer);


    // 关闭套接字
    close(sockfd);
    return 0;
}
