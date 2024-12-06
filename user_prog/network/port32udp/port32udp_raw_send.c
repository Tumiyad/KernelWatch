#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/ip.h>
#include <netinet/udp.h>

// 计算校验和
unsigned short checksum(void *b, int len) {
    unsigned short *buf = b;
    unsigned int sum = 0;
    unsigned short result;

    for (sum = 0; len > 1; len -= 2)
        sum += *buf++;
    if (len == 1)
        sum += *(unsigned char *)buf;
    sum = (sum >> 16) + (sum & 0xFFFF);
    sum += (sum >> 16);
    result = ~sum;
    return result;
}

int main() {
    int sockfd;
    struct iphdr ip;
    struct sockaddr_in dest;

    // 创建原始套接字
    sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_RAW);
    if (sockfd < 0) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // 构建 IP 头部
    memset(&ip, 0, sizeof(ip));
    ip.ihl = 5; // IP 头部长度
    ip.version = 4; // IPv4
    ip.tos = 0;
    ip.tot_len = sizeof(ip);
    ip.id = htons(54321);
    ip.frag_off = 0;
    ip.ttl = 255;
    ip.protocol = 137; // 协议字段设置为 137
    ip.check = 0; // 校验和会在下面计算
    ip.saddr = inet_addr("127.0.0.1"); // 源地址
    ip.daddr = inet_addr("127.0.0.1"); // 目标地址

    // 计算校验和
    ip.check = checksum(&ip, sizeof(ip));

    // 目标地址结构
    dest.sin_family = AF_INET;
    dest.sin_addr.s_addr = ip.daddr;

    // 发送数据包
    if (sendto(sockfd, &ip, sizeof(ip), 0, (struct sockaddr *)&dest, sizeof(dest)) < 0) {
        perror("Send failed");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    printf("Packet sent\n");

    close(sockfd);
    return 0;
}
