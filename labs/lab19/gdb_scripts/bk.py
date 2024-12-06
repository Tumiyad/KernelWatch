import gdb


class Bk(gdb.Command):

    def __init__(self):
        super(Bk, self).__init__("bk", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        proc_alloc_inode=gdb.Breakpoint("proc_alloc_inode")
        pass


Bk()


# Bk5
class Bk2(gdb.Command):

    def __init__(self):
        super(Bk2, self).__init__("bk2", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        # do_lookup=gdb.Breakpoint("do_lookup")
        # do_lookup.commands="p name.name \n p nd.path.dentry.d_name.name"
        pass


# Register commands
Bk2()
