#include <stdio.h>

#define SYS_power 327  // 自定义 power 系统调用号

int my_power(int x, int power) {
    int result;

    asm volatile (
        "int $0x80"             // 系统调用指令
        : "=a" (result)         // 返回值存储在eax寄存器
        : "0" (SYS_power),      // 系统调用号存储在eax寄存器
          "b" (x),              // 第一个参数存储在ebx寄存器
          "c" (power)           // 第二个参数存储在ecx寄存器
        : "memory"
    );

    return result;
}

int main() {
    int base, exp;
    char input[10];

    while (1) {
        // 提示用户输入底数
        printf("Enter base (or 'q' to quit): ");
        if (scanf("%s", input) != 1 || input[0] == 'q') {
            break;  // 用户输入 'q' 或输入读取失败，退出循环
        }
        base = atoi(input);  // 将输入转换为整数

        // 提示用户输入指数
        printf("Enter exponent: ");
        if (scanf("%d", &exp) != 1) {
            printf("Invalid input. Please enter a valid number.\n");
            continue;  // 输入无效，重新开始循环
        }

        // 计算结果
        int result = my_power(base, exp);

        // 输出结果
        printf("%d^%d = %d\n", base, exp, result);
    }

    printf("Program terminated.\n");
    return 0;
}

