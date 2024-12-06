import gdb

class Bk(gdb.Command):
    """Load the VFS script in GDB"""

    def __init__(self):
        super(Bk, self).__init__("bk", gdb.COMMAND_USER)  # load script

    def invoke(self, arg, from_tty):
        # breakpoints
        self.breakpoints()

    def breakpoints(self):
        gdb.Breakpoint("sys_nanosleep")
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