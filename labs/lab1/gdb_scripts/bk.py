import gdb


class Bk(gdb.Command):

    def __init__(self):
        super(Bk, self).__init__("bk", gdb.COMMAND_USER)  # load script

    def invoke(self, arg, from_tty):
        gdb.Breakpoint("apic_timer_interrupt")
        pass

Bk()
