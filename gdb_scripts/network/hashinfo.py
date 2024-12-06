import gdb

def container_of(ptr, type_name, member):
    """计算结构体指针的真实地址"""
    type_info = gdb.lookup_type(type_name)
    member_offset = gdb.parse_and_eval("&(({} *)0)->{}".format(type_name, member)).cast(
        gdb.lookup_type("unsigned long"))
    return (ptr.cast(gdb.lookup_type("unsigned long")) - member_offset).cast(type_info.pointer())

class PrintPortsCommand(gdb.Command):
    """打印 inet_hashinfo 变量的 bhash 中的每一个端口"""

    def __init__(self):
        super(PrintPortsCommand, self).__init__(
            "print_ports",  # 命令名称
            gdb.COMMAND_USER,  # 命令类别
            gdb.COMPLETE_NONE  # 自动补全模式
        )

    def invoke(self, arg, from_tty):
        # 使用默认参数 tcp_hashinfo
        if not arg:
            arg = "tcp_hashinfo"

        # 获取 inet_hashinfo 变量
        try:
            inet_hashinfo = gdb.parse_and_eval(arg)
        except gdb.error as e:
            print(f"无法解析变量 '{arg}': {e}")
            return

        # 解析 bhash 和 bhash_size
        try:
            bhash = inet_hashinfo['bhash']
            bhash_size = inet_hashinfo['bhash_size']
        except gdb.error as e:
            print(f"无法解析 bhash 或 bhash_size: {e}")
            return

        # 遍历 bhash
        # print(f"bhash_size: {bhash_size}")
        for i in range(bhash_size):
            try:
                bucket = bhash[i]
                # 解析 bucket 的 chain 字段
                chain = bucket['chain']
                # 遍历 chain 中的每个元素
                node = chain['first']  # 假设 hlist_head 有一个 first 字段
                # print(node)
                while node:
                    try:
                        # 使用 container_of 函数获取 inet_bind_bucket 对象
                        bind_bucket = container_of(node, 'struct inet_bind_bucket', 'node')
                        port = bind_bucket['port']
                        print(f"端口: {port}")
                    except gdb.error as e:
                        print(f"读取链表节点端口失败: {e}")
                    # 获取下一个节点
                    node = node['next']  # 假设 hlist_node 有一个 next 字段
            except gdb.error as e:
                print(f"读取 bhash 元素失败: {e}")

# 注册新命令
PrintPortsCommand()
