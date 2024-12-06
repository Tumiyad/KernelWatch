#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <arpa/inet.h>

#define TARGET_IP "127.0.0.1"
//#define TARGET_IP "202.112.51.116"
#define TARGET_PORT 12345
#define SOURCE_IP "127.0.1.1"
//#define SOURCE_IP "10.0.2.15"
#define NUM_CHILDREN 1
#define SLEEP_TIME 10

int main() {
    int i;
    pid_t pid;

    for (i = 0; i < NUM_CHILDREN; i++) {
        pid = fork();
        if (pid < 0) {
            perror("fork failed");
            exit(EXIT_FAILURE);
        } else if (pid == 0) {
            // 子进程代码
            int sockfd;
            struct sockaddr_in server_addr, source_addr;
            char message[256];
            int msg_len;

            // 创建套接字
            sockfd = socket(AF_INET, SOCK_STREAM, 0);
            if (sockfd < 0) {
                perror("socket creation failed");
                exit(EXIT_FAILURE);
            }
            printf("Child PID %d: Socket created\n", getpid());

            // 设置源地址
            source_addr.sin_family = AF_INET;
            source_addr.sin_addr.s_addr = inet_addr(SOURCE_IP);
            source_addr.sin_port = 0; // 让系统自动选择源端口

            if (bind(sockfd, (struct sockaddr*)&source_addr, sizeof(source_addr)) < 0) {
                perror("bind failed");
                close(sockfd);
                exit(EXIT_FAILURE);
            }
            printf("Child PID %d: Bound to source IP and port %d %s\n", getpid(), ntohs(source_addr.sin_port) ,SOURCE_IP);

            // 设置目标地址
            server_addr.sin_family = AF_INET;
            server_addr.sin_addr.s_addr = inet_addr(TARGET_IP);
            server_addr.sin_port = htons(TARGET_PORT);

            // 连接到目标地址
            if (connect(sockfd, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
                perror("connect failed");
                close(sockfd);
                exit(EXIT_FAILURE);
            }
            printf("Child PID %d: Connected to %s:%d\n", getpid(), TARGET_IP, TARGET_PORT);

            // 发送数据
            snprintf(message, sizeof(message), "%d hello", getpid());
            msg_len = strlen(message);

            if (send(sockfd, message, msg_len, 0) != msg_len) {
                perror("send failed");
                close(sockfd);
                exit(EXIT_FAILURE);
            }
            printf("Child PID %d: Sent message: %s\n", getpid(), message);

            // 睡眠10秒
            sleep(SLEEP_TIME);

            // 关闭套接字
            close(sockfd);
            printf("Child PID %d: Socket closed\n", getpid());

            exit(EXIT_SUCCESS);
        }
    }

    // 等待所有子进程结束
    for (i = 0; i < NUM_CHILDREN; i++) {
        wait(NULL);
    }

    return 0;
}
