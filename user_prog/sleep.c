#include <stdio.h>
#include <time.h>

#define SYS_nanosleep 162

void my_sleep(unsigned int seconds) {
    struct timespec req = { seconds, 0 };

    asm volatile (
        "int $0x80"              // 触发系统调用
        : /* 无输出操作数 */
        : "a"(SYS_nanosleep),   // 系统调用号放入 EAX
          "b"(&req),            // 第一个参数放入 EBX
          "c"(0)                // 第二个参数放入 ECX (为 NULL)
        : "memory"              // 被修改的内存
    );
}

int main() {
    for (int i = 0; i < 5; ++i) {
        printf("Sleeping for 1 second...\n");
        my_sleep(1);
        printf("Awoke after 1 second\n");
    }
    printf("bye");
    return 0;
}
