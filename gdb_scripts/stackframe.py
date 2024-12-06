from struct import unpack

import gdb


class Stackframe(gdb.Command):
    """通过直接访问寄存器打印 i386 架构中的函数调用栈"""

    def __init__(self):
        super(Stackframe, self).__init__("stackframe", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        try:
            # 获取当前帧的基指针（EBP）
            ebp = gdb.parse_and_eval("$ebp")
            ebp = unpack("I", ebp.bytes)[0]
            stack_frames = []

            # 迭代以获取栈帧
            for i in range(10):  # 最多打印 10 个栈帧
                # 去掉异常处理
                try:
                    # 从栈中读取返回地址（下一条执行指令）
                    # print("ebp: {}".format(hex(ebp)))
                    print("*((void**)({:#x} + 4))".format(ebp))
                    return_address = gdb.parse_and_eval("*((void**)({:#x} + 4))".format(ebp))
                    print("return_address: {}".format(return_address))
                    stack_frames.append("Frame {}: {}".format(i, return_address))

                    # 更新基指针到上一个帧
                    ebp = gdb.parse_and_eval("*({})".format(ebp))
                    ebp = int(str(ebp), 10)  # 从gdb.value int 转换为 int
                    ebp = ebp & 0xffffffff  # 负数转换为32位系统下补码一致的正数（python无限位数实现很奇妙，使获得负数16进制很繁琐）
                except gdb.error:
                    # 发生错误时退出（例如无效的内存访问）
                    print("获取栈帧直到失败")
                    break

            # 打印栈跟踪
            for frame_info in stack_frames:
                print(frame_info)
        except gdb.error as e:
            print("获取栈跟踪失败: {}".format(e))


# 注册自定义命令
Stackframe()
