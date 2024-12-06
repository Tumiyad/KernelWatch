import gdb
from prettytable import PrettyTable, ALL
import vfs
import process

class VMAStructPrinter(gdb.Command):
    """GDB command to print the VMAs of the current process."""

    def __init__(self):
        super(VMAStructPrinter, self).__init__("vm", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        current_task = process.TaskStructPrinter.get_current_task()
        if current_task is None:
            gdb.write("Could not get the current task.\n")
            return

        gdb.write("Current Task: {}\n".format(current_task['pid']))
        mm_struct = current_task['mm']

        if mm_struct == 0:
            gdb.write("No memory management structure found.\n")
            return

        vma = mm_struct['mmap']
        if vma == 0:
            gdb.write("No VMAs found.\n")
            return

        table = PrettyTable()
        table.field_names = ["Start", "End", "Flags", "Prot", "File"]
        table.align = "l"
        table.max_width = 20
        table.hrules = ALL  # 增加行间分隔线

        while vma != 0:
            start = vma['vm_start']
            end = vma['vm_end']
            flags = vma['vm_flags']
            prot = vma['vm_page_prot']
            file = vma['vm_file']
            if file != 0:
                dentry = file['f_path']['dentry']
                name = vfs.build_full_path(dentry)
                # name = dentry['d_name']['name'].string()
                # print(name)
            else:
                name = "None"

            flag_descriptions = self.parse_flags(flags)
            prot_descriptions = self.parse_prot(prot)

            table.add_row([
                "0x%08x" % start,
                "0x%08x" % end,
                "0x%x\n%s" % (flags, flag_descriptions),
                "0x%x\n%s" % (prot['pgprot'], prot_descriptions),
                name
            ])

            vma = vma['vm_next']

        gdb.write(str(table) + "\n")

    def parse_flags(self, flags):
        flag_descriptions = []
        if flags & 0x00000001:
            flag_descriptions.append("READ")
        if flags & 0x00000002:
            flag_descriptions.append("WRITE")
        if flags & 0x00000004:
            flag_descriptions.append("EXEC")
        if flags & 0x00000008:
            flag_descriptions.append("SHARED")
        if flags & 0x00000010:
            flag_descriptions.append("MAYREAD")
        if flags & 0x00000020:
            flag_descriptions.append("MAYWRITE")
        if flags & 0x00000040:
            flag_descriptions.append("MAYEXEC")
        if flags & 0x00000080:
            flag_descriptions.append("MAYSHARE")
        if flags & 0x00000100:
            flag_descriptions.append("GROWSDOWN")
        if flags & 0x00000200:
            flag_descriptions.append("GROWSUP")
        if flags & 0x00000400:
            flag_descriptions.append("PFNMAP")
        if flags & 0x00000800:
            flag_descriptions.append("DENYWRITE")
        if flags & 0x00001000:
            flag_descriptions.append("EXECUTABLE")
        if flags & 0x00002000:
            flag_descriptions.append("LOCKED")
        if flags & 0x00004000:
            flag_descriptions.append("IO")
        if flags & 0x00008000:
            flag_descriptions.append("SEQ_READ")
        if flags & 0x00010000:
            flag_descriptions.append("RAND_READ")
        if flags & 0x00020000:
            flag_descriptions.append("DONTCOPY")
        if flags & 0x00040000:
            flag_descriptions.append("DONTEXPAND")
        if flags & 0x00080000:
            flag_descriptions.append("RESERVED")
        if flags & 0x00100000:
            flag_descriptions.append("ACCOUNT")
        if flags & 0x00400000:
            flag_descriptions.append("HUGETLB")
        if flags & 0x00800000:
            flag_descriptions.append("NONLINEAR")
        if flags & 0x01000000:
            flag_descriptions.append("MAPPED_COPY")
        if flags & 0x02000000:
            flag_descriptions.append("INSERTPAGE")
        if flags & 0x04000000:
            flag_descriptions.append("ALWAYSDUMP")
        if flags & 0x08000000:
            flag_descriptions.append("CAN_NONLINEAR")
        if flags & 0x10000000:
            flag_descriptions.append("MIXEDMAP")

        return "|".join(flag_descriptions)

    def parse_prot(self, prot):
        prot_descriptions = []
        pgprot = prot['pgprot']
        if pgprot & 0x1:
            prot_descriptions.append("PRESENT")
        if pgprot & 0x2:
            prot_descriptions.append("WRITE")
        if pgprot & 0x4:
            prot_descriptions.append("USER")
        if pgprot & 0x8:
            prot_descriptions.append("PWT")
        if pgprot & 0x10:
            prot_descriptions.append("PCD")
        if pgprot & 0x20:
            prot_descriptions.append("ACCESSED")
        if pgprot & 0x40:
            prot_descriptions.append("DIRTY")
        if pgprot & 0x80:
            prot_descriptions.append("PSE")
        if pgprot & 0x100:
            prot_descriptions.append("GLOBAL")
        if pgprot & 0x200:
            prot_descriptions.append("PAT")
        if pgprot & 0x400:
            prot_descriptions.append("PK")

        return "\n".join(prot_descriptions)


VMAStructPrinter()
