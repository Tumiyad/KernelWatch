#include <linux/kernel.h>

int hello_kernel_watch(void){
    printk("Hello, kernel_watch\n");
    return 0;
}