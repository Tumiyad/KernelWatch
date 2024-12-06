import gdb


class Bk(gdb.Command):
    """Load the VFS script in GDB"""

    def __init__(self):
        super(Bk, self).__init__("bk", gdb.COMMAND_USER)  # load script

    def invoke(self, arg, from_tty):
        # breakpoints
        self.breakpoints()

    def breakpoints(self):
        # start_kernel = gdb.Breakpoint("start_kernel")
        # start_kernel.commands="b tty_register_device"
        # gdb.Breakpoint("tty_register_device")
        sys_kernel_watch = gdb.Breakpoint("sys_kernel_watch")
        sys_kernel_watch.commands = "bk2"
        # serial8250_startup = gdb.Breakpoint("serial8250_startup")
        # uart_open = gdb.Breakpoint("uart_open")
        pass


# Register commands
Bk()


class Bk2(gdb.Command):
    """Load the VFS script in GDB"""

    def __init__(self):
        super(Bk2, self).__init__("bk2", gdb.COMMAND_USER)  # load script

    def invoke(self, arg, from_tty):
        # gdb.Breakpoint("n_tty_receive_buf")
        # gdb.Breakpoint("tty_insert_flip_char")
        # serial8250_interrupt=gdb.Breakpoint("serial8250_interrupt")
        # serial8250_handle_port=gdb.Breakpoint("serial8250_handle_port")
        flush_to_ldisc=gdb.Breakpoint("flush_to_ldisc")
        # serial8250_interrupt.commands="p dev_id"
        # serial_out=gdb.Breakpoint("serial_out")
        # serial_out.commands="p up->port->dev->driver->name\np up->port->dev->kobj->name\np offset\n p value\n c"
        # gdb.Breakpoint("*0xc037a7e4")
        pass

# Register commands
Bk2()
