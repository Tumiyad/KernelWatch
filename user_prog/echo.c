#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

//#define SYS_KERNEL_WATCH 328

//void kernel_watch() {
//
//    asm volatile (
//        "int $0x80"              // 触发系统调用
//        : /* 无输出操作数 */
//        : "a"(SYS_KERNEL_WATCH)   // 系统调用号放入 EAX
//    );
//}


int main() {
    char buffer[1024];
    ssize_t bytesRead;
//
//    kernel_watch();

    while (1) {
        // 从标准输入读取数据
        printf("echo> \n");
        bytesRead = read(STDIN_FILENO, buffer, sizeof(buffer) - 1);

        if (bytesRead <= 0) {
            // 读取失败或到达文件结束符
            if (bytesRead == 0) {
                break;  // 到达文件结束符
            } else {
                perror("read");
                exit(EXIT_FAILURE);
            }
        }
        // 添加字符串结束符
        buffer[bytesRead] = '\0';

        // 将读取的数据回显到标准输出
        if (write(STDOUT_FILENO, buffer, bytesRead) != bytesRead) {
            perror("write");
            exit(EXIT_FAILURE);
        }
    }

    return 0;
}
