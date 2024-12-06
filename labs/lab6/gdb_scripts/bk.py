import gdb


class Bk(gdb.Command):
    """Load the VFS script in GDB"""

    def __init__(self):
        super(Bk, self).__init__("bk", gdb.COMMAND_USER)  # load script

    def invoke(self, arg, from_tty):
        # breakpoints
        self.breakpoints()

    def breakpoints(self):
        # b = gdb.Breakpoint("sys_kernel_watch")
        # b.commands = "bk2"
        # gdb.Breakpoint("sched.c:4202")
        # gdb.Breakpoint("do_notify_resume")
        # b = gdb.Breakpoint("serial8250_interrupt")
        # b.ignore_count = 40
        # b.commands = "bk2"
        # 8250.c 1470

        # user_start.commands = "bk2"
        pass


# Register commands
Bk()


class Bk2(gdb.Command):
    """Load the VFS script in GDB"""

    def __init__(self):
        super(Bk2, self).__init__("bk2", gdb.COMMAND_USER)  # load script

    def invoke(self, arg, from_tty):
        # gdb.Breakpoint("8250.c:1470")
        sys_kill=gdb.Breakpoint("sys_kill")
        # sched_c_4191=gdb.Breakpoint("sched.c:4191")
        # sched_c_4201=gdb.Breakpoint("sched.c:4201")
        # sys_kill.commands="b sched.c:4191\nb sched.c:4201\nb do_notify_resume\n"
        # do_notify_resume=gdb.Breakpoint("do_notify_resume")
        # apic_timer_interrupt=gdb.Breakpoint("smp_apic_timer_interrupt")
        # gdb.Breakpoint("*0x8048e3b")

        # gdb.execute("c")


# Register commands
Bk2()
