import gdb


class Bk(gdb.Command):
    """Load the VFS script in GDB"""

    def __init__(self):
        super(Bk, self).__init__("bk", gdb.COMMAND_USER)  # load script

    def invoke(self, arg, from_tty):
        # breakpoints
        self.breakpoints()

    def breakpoints(self):
        user_start = gdb.Breakpoint("sys_kernel_watch")
        user_start.commands = "bk2"
        pass


# Register commands
Bk()


class PageFaultTest(gdb.Command):

    def __init__(self):
        self.new_address = 0
        self.old_address = 0
        super(PageFaultTest, self).__init__("pagefaulttest", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        gdb.execute("shell clear")
        gdb.execute("pdt -u")
        address = gdb.parse_and_eval("address")
        self.old_address = self.new_address
        self.new_address = int(address)
        print(f"page fault at address {self.new_address:#x}")
        if self.old_address:
            print(f"last page fault at address {self.old_address:#x}")


PageFaultTest()


# Bk5
class Bk2(gdb.Command):
    """Load the VFS script in GDB"""

    def __init__(self):
        super(Bk2, self).__init__("bk2", gdb.COMMAND_USER)  # load script

    def invoke(self, arg, from_tty):
        page_fault = gdb.Breakpoint("fault.c:605")
        page_fault.commands = 'pagefaulttest'
        page_fault.ignore_count = 20
        gdb.execute("c")




# Register commands
Bk2()
