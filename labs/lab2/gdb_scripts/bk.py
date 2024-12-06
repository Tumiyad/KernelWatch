import gdb

class Bk(gdb.Command):
    """Load the VFS script in GDB"""

    def __init__(self):
        super(Bk, self).__init__("bk", gdb.COMMAND_USER)  # load script

    def invoke(self, arg, from_tty):
        # breakpoints
        self.breakpoints()

    def breakpoints(self):
        # b1=gdb.Breakpoint("sys_listen")
        # b1.commands="info args"
        # sys_connect=gdb.Breakpoint("sys_connect")
        # gdb.Breakpoint("neighbour.c:939")
        ip_finish_output2=gdb.Breakpoint("ip_finish_output2")
        ip_finish_output2.commands="bk2"
        # neigh_resolve_output=gdb.Breakpoint("neigh_resolve_output")

        # sys_accept=gdb.Breakpoint("sys_accept")
        # inet_csk_wait_for_connect=gdb.Breakpoint("inet_csk_wait_for_connect")
        # b sys_write

        pass

# Register commands
Bk()

# Bk5
class Bk2(gdb.Command):
    """Load the VFS script in GDB"""

    def __init__(self):
        super(Bk2, self).__init__("bk2", gdb.COMMAND_USER)  # load script

    def invoke(self, arg, from_tty):
        syn_skb=gdb.parse_and_eval("skb")
        tcp_v4_rcv=gdb.Breakpoint("tcp_v4_rcv")
        tcp_v4_rcv.condition="skb=="+str(syn_skb)
        tcp_v4_rcv.commands="b loopback_xmit"

# Register commands
Bk2()