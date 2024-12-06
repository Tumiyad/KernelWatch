import gdb


class Bk(gdb.Command):

    def __init__(self):
        super(Bk, self).__init__("bk", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        start_kernel = gdb.Breakpoint("start_kernel")
        kernel_init = gdb.Breakpoint("kernel_init")
        context_switch = gdb.Breakpoint("context_switch")
        context_switch.commands="current_task"
        init_post = gdb.Breakpoint("init_post")
        # schedule_ret = gdb.Breakpoint("sched.c:4202")
        # sys_kernel_watch = gdb.Breakpoint("sys_kernel_watch")
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
