#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <arpa/inet.h> // 用于 AF_INET
#include <unistd.h>    // 用于 close

int main(int argc, char *argv[]) {
    int sockfd;

    // 检查参数个数
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <type> <protocol>\n", argv[0]);
        fprintf(stderr, "Type and protocol should be numeric values.\n");
        return 1;
    }

    // 解析 type 和 protocol 参数
    int type = atoi(argv[1]);
    int protocol = atoi(argv[2]);

    // 创建套接字
    sockfd = socket(AF_INET, type, protocol);
    if (sockfd < 0) {
        perror("socket creation failed");
        return 1;
    }

    printf("套接字已创建，类型：%d，协议：%d\n", type, protocol);

    //send hello
    char *hello = "Hello from client";
    char buffer[1024] = {0};
    struct sockaddr_in servaddr;

//     关闭套接字
    close(sockfd);

    return 0;
}
