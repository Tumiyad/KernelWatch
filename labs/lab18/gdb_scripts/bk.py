import gdb


class Bk(gdb.Command):

    def __init__(self):
        super(Bk, self).__init__("bk", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        # sys_kernel_watch = gdb.Breakpoint("sys_kernel_watch")
        d_alloc= gdb.Breakpoint("d_alloc")
        # d_alloc.condition="name->name==\"listen\""
        d_alloc.condition="$_streq(name->name, \"hard2\")"

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
