#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>

int main() {
    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);

    // 设置目标地址
    struct sockaddr_in dest_addr;
    dest_addr.sin_family = AF_INET;
    dest_addr.sin_port = htons(12345);
    dest_addr.sin_addr.s_addr = htonl(INADDR_LOOPBACK); // 本地回环地址

    // 连接到目标地址
    connect(sockfd, (struct sockaddr*)&dest_addr, sizeof(dest_addr));

    // 发送数据
    const char *message = "Hello, UDP!";
    send(sockfd, message, strlen(message), 0);

    // 关闭套接字
    close(sockfd);
    return 0;
}
