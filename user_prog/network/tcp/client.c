// tcp_echo_client.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 12345
#define BUFFER_SIZE 1024

int main() {
    int sock_fd;
    struct sockaddr_in server_addr;
    char buffer[BUFFER_SIZE];
    ssize_t bytes_sent, bytes_received;

    // 创建 socket
    if ((sock_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    // 配置服务器地址
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    if (inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr) <= 0) {
        perror("inet_pton");
        close(sock_fd);
        exit(EXIT_FAILURE);
    }

    // 连接到服务器
    if (connect(sock_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) == -1) {
        perror("connect");
        close(sock_fd);
        exit(EXIT_FAILURE);
    }

    printf("Connected to server.\n");

    // 发送和接收数据
    while (1) {
        printf("Enter message: ");
        if (fgets(buffer, sizeof(buffer), stdin) == NULL) {
            perror("fgets");
            break;
        }

        // 发送数据
        if ((bytes_sent = write(sock_fd, buffer, strlen(buffer))) == -1) {
            perror("write");
            break;
        }
        printf("Sent to server: %s", buffer);

        // 读取服务器响应
        if ((bytes_received = read(sock_fd, buffer, sizeof(buffer) - 1)) == -1) {
            perror("read");
            break;
        }
        buffer[bytes_received] = '\0'; // 添加字符串终止符
        printf("Received from server: %s", buffer);
    }

    // 关闭 socket
    close(sock_fd);

    return 0;
}
