#include <stdio.h>
#include <time.h>

#define SYS_KERNEL_WATCH 328

void kernel_watch() {

    asm volatile (
        "int $0x80"              // 触发系统调用
        : /* 无输出操作数 */
        : "a"(SYS_KERNEL_WATCH)   // 系统调用号放入 EAX
    );
}

int main() {
    kernel_watch();
    return 0;
}
