import gdb


class Bk(gdb.Command):

    def __init__(self):
        super(Bk, self).__init__("bk", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        sys_kernel_watch = gdb.Breakpoint("sys_kernel_watch")
        port32udp_init = gdb.Breakpoint("port32udp_init")
        pass


Bk()


# Bk5
class Bk2(gdb.Command):

    def __init__(self):
        super(Bk2, self).__init__("bk2", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        pass


# Register commands
Bk2()
