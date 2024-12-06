import gdb

kernel_thread = None


class Bk(gdb.Command):

    def __init__(self):
        super(Bk, self).__init__("bk", gdb.COMMAND_USER)  # load script

    def invoke(self, arg, from_tty):
        # breakpoints
        self.breakpoints()

    def breakpoints(self):
        global kernel_thread
        kernel_thread = gdb.Breakpoint("kernel_thread")
        # kernel_thread.commands = "bk2"


Bk()


class Bk2(gdb.Command):

    def __init__(self):
        super(Bk2, self).__init__("bk2", gdb.COMMAND_USER)  # load script

    def invoke(self, arg, from_tty):
        print("bk2 is running")
        # gdb.execute("delete 1")
        gdb.execute("bt")
        gdb.execute("current_task")
        create_workqueue_thread=gdb.Breakpoint("create_workqueue_thread")
        create_workqueue_thread.commands="bk3"
        # gdb.execute("c")
        gdb.write("bk2 is finished\n")

Bk2()

class Bk3(gdb.Command):

    def __init__(self):
        super(Bk3, self).__init__("bk3", gdb.COMMAND_USER)  # load script

    def invoke(self, arg, from_tty):
        print("bk3 is running")
        # gdb.execute("bt")
        # gdb.execute("current_task")
        kernel_thread_2 = gdb.Breakpoint("kernel_thread")
        kernel_thread_2.commands = "bt\ncurrent_task\n"
        gdb.execute("c")

Bk3()