import re
import struct

import gdb
from prettytable import PrettyTable
from utilities import read_memory


class CR3:
    def __init__(self):
        cr3 = gdb.parse_and_eval("$cr3")
        self.addr = int(cr3)
        input_str = str(cr3)
        match = re.search(r'PDBR=(\d+)', input_str)
        self.PDBR = int(match.group(1))

        # cr3_type=gdb.parse_and_eval("$cr3").type
        # # print(cr3_type.code)
        # code_dic={}
        # for x in dir(gdb):
        #     if x.startswith("TYPE_CODE"):
        #         code_dic[getattr(gdb, x)]=x
        #         # print(f"{x}: {getattr(gdb, x)}")
        # if cr3_type.code in [gdb.TYPE_CODE_STRUCT, gdb.TYPE_CODE_UNION, gdb.TYPE_CODE_ENUM, gdb.TYPE_CODE_FUNC]:
        #     print(cr3_type.fields())
        # else:
        #     print(f"cr3_type is not a structure, union, enum, or function type, it is {code_dic[cr3_type.code]}")

    def __repr__(self):
        return ("CR3(PDBR=0x%08x)" % (self.PDBR))


class PDT(gdb.Command):
    '''
    Print Page Directory Table
    Usage: pdt [u|k]
    u: user mode
    k: kernel mode
    default: both
    '''

    def __init__(self):
        super(PDT, self).__init__("pdt", gdb.COMMAND_USER)  # load script

    def invoke(self, arg, from_tty):
        mode = arg
        if mode == "-u":
            start_pde, end_pde = 0, 0xbfffffff >> 22
        elif mode == "-k":
            start_pde, end_pde = 0xc0000000 >> 22, 1023
        else:
            start_pde, end_pde = 0, 1023
        pdt_phy = CR3().addr
        pdt_vir = pdt_phy + 0xc0000000
        table = PrettyTable()
        table.field_names = ["virtual_address", "physical_address", "size"]
        pdt = read_memory(pdt_vir, 4096)
        print("PDT:")
        for i in range(start_pde, end_pde + 1):
            pde = struct.unpack("I", pdt[i * 4:i * 4 + 4])[0]
            virtual_address = i << 22
            valid = pde & 1
            if valid:
                if pde & (1 << 7):
                    # print(f"virtual_address: {virtual_address:08x} physical_address: {pde & 0xffc00000:08x} 4MB")
                    table.add_row([f"{virtual_address:#010x}", f"{(pde & 0xffc00000):#010x}", "4MB"])
                else:
                    try:
                        pgt_phy = pde & 0xfffff000
                        pgt_vir = pgt_phy + 0xc0000000
                        pgt = read_memory(pgt_vir, 4096)
                        # print("hhh")
                        for j in range(0, 1024):
                            pge = struct.unpack("I", pgt[j * 4:j * 4 + 4])[0]
                            valid2 = pge & 1
                            if valid2:
                                physical_address = pge & 0xfffff000
                                table.add_row(
                                    [f"{virtual_address + (j << 12):#010x}", f"{physical_address:#010x}", "4KB"])
                    except Exception as e:
                        # print(e)
                        pass
        print(table)


PDT()
