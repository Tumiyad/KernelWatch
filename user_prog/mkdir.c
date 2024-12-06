#include <stdio.h>
#include <stdlib.h>

#define SYS_mkdir 40  // mkdir 系统调用号

int my_mkdir(const char *pathname, int mode) {
    int result;

    asm volatile (
        "int $0x80"             // 系统调用指令
        : "=a" (result)         // 返回值存储在 eax 寄存器
        : "0" (SYS_mkdir),      // 系统调用号存储在 eax 寄存器
          "b" (pathname),       // 第一个参数存储在 ebx 寄存器
          "c" (mode)            // 第二个参数存储在 ecx 寄存器
        : "memory"
    );

    return result;
}

int main() {
    const char *dir = "testdir";
    int mode = 0755;  // rwxr-xr-x

    int ret = my_mkdir(dir, mode);
    if (ret == 0) {
        printf("Directory created successfully\n");
    } else {
        printf("Failed to create directory\n");
    }

    return 0;
}

