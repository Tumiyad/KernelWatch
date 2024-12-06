import gdb

class SkbCommand(gdb.Command):
    """This class defines the 'skb' command in gdb."""

    def __init__(self):
        super(SkbCommand, self).__init__(
            "pskb", gdb.COMMAND_USER
        )

    def invoke(self, arg, from_tty):
        gdb.execute("p/z *(struct iphdr *)(skb->network_header)")
        gdb.execute("p/z *(struct tcphdr *)(skb->transport_header)")

SkbCommand()
