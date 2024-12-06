// tcp_echo_server.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define DEFAULT_PORT 12345
#define DEFAULT_IP "127.0.0.1"
#define BUFFER_SIZE 1024

// 接收两个参数，依次是IP和端口号
int main(int argc, char *argv[]) {
    int server_fd, client_fd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_addr_len = sizeof(client_addr);
    char buffer[BUFFER_SIZE];
    ssize_t bytes_read;

    // 配置服务器地址
    server_addr.sin_family = AF_INET;
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <ip> <port>\n", argv[0]);
        fprintf(stderr, "Using default IP and port: %s:%d\n", DEFAULT_IP, DEFAULT_PORT);
        server_addr.sin_addr.s_addr = inet_addr(DEFAULT_IP);
        server_addr.sin_port = htons(DEFAULT_PORT);
    } else {
        server_addr.sin_addr.s_addr = inet_addr(argv[1]);
        server_addr.sin_port = htons(atoi(argv[2]));
    }

    // 创建 socket
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    // 绑定 socket
    if (bind(server_fd, (struct sockaddr *)&server_addr, sizeof(server_addr)) == -1) {
        perror("bind");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    // 监听连接
    if (listen(server_fd, 5) == -1) {
        perror("listen");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    printf("Server listening on port %d...\n", ntohs(server_addr.sin_port));

    // 接受连接
    if ((client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &client_addr_len)) == -1) {
        perror("accept");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    // 输出客户端的IP和端口
    char client_ip[INET_ADDRSTRLEN];
    inet_ntop(AF_INET, &client_addr.sin_addr, client_ip, sizeof(client_ip));
    printf("Client connected from %s:%d\n", client_ip, ntohs(client_addr.sin_port));

    // 处理客户端数据
    while ((bytes_read = read(client_fd, buffer, sizeof(buffer) - 1)) > 0) {
        buffer[bytes_read] = '\0'; // 添加字符串终止符
        printf("Received from %s:%d: %s", client_ip, ntohs(client_addr.sin_port), buffer);

        // 发送数据回客户端
        if (write(client_fd, buffer, bytes_read) == -1) {
            perror("write");
            close(client_fd);
            close(server_fd);
            exit(EXIT_FAILURE);
        }
    }

    if (bytes_read == -1) {
        perror("read");
    }

    printf("Client disconnected.\n");

    // 关闭 sockets
    close(client_fd);
    close(server_fd);

    return 0;
}
