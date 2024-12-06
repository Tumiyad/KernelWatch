#include <stdio.h>
#define SYS_KERNEL_WATCH 328

void kernel_watch() {

    asm volatile (
        "int $0x80"              // 触发系统调用
        : /* 无输出操作数 */
        : "a"(SYS_KERNEL_WATCH)   // 系统调用号放入 EAX
    );
}

void print_code_segment_header(char *addr) {
    printf("code segment header:\n");
    int page_num=(0x0810f000-0x08048000) /4096;
    for (int i = 0; i < page_num*4096/16; i++) {
        printf("%08x ", addr+i*16);
        for (int j = 0; j < 16; j++) {
            printf("%02x ", addr[i*16+j]&0xff);
        }
        printf("\n");
    }
    printf("\n");
}

int main()
{
    kernel_watch();
    print_code_segment_header((char *)0x08048000);
    kernel_watch();
    return 0;
}