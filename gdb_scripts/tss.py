import gdb
from utilities import *

def gettss():
    tss = gdb.parse_and_eval("(struct tss_struct *)((void *)(& per_cpu__init_tss) + (__per_cpu_offset[0]))")
    return tss

class TSS(gdb.Command):
    """percpu变量 init_tss访问TSS"""

    def __init__(self):
        super(TSS, self).__init__("tss", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        tss = gettss()
        print("esp0 %#08x" % tss["x86_tss"]["sp0"].address)
        print_ptr(tss)


TSS()
