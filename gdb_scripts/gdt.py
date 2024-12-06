import gdb
from prettytable import PrettyTable


class desc_struct:
    def __init__(self, base, limit, type, dpl, s, p, avl, l, db, g):
        self.base = base
        self.limit = limit
        self.type = type
        self.dpl = dpl
        self.s = s
        self.p = p
        self.avl = avl
        self.l = l
        self.db = db
        self.g = g

    def __repr__(self):
        return ("desc_struct(base=0x%08x, limit=0x%05x, "
                "type=%d, dpl=%d, s=%d, p=%d, "
                "avl=%d, l=%d, db=%d, g=%d)" % (
                    self.base, self.limit, self.type, self.dpl, self.s, self.p,
                    self.avl, self.l, self.db, self.g))


def parse_desc_struct(value):
    """
    Parses a gdb.Value representing a struct desc_struct into a Python desc_struct object.

    Args:
        value (gdb.Value): gdb.Value object representing the struct desc_struct.

    Returns:
        desc_struct: A Python object representing the parsed struct desc_struct.
    """
    # Extracting fields from gdb.Value
    limit0 = int(value['limit0'])
    base0 = int(value['base0'])
    base1 = int(value['base1'])
    base2 = int(value['base2'])
    limit = int(value['limit'])
    avl = int(value['avl'])
    l = int(value['l'])
    d = int(value['d'])
    g = int(value['g'])
    type = int(value['type'])
    s = int(value['s'])
    dpl = int(value['dpl'])
    p = int(value['p'])

    # Create and return desc_struct object
    return desc_struct(
        base=(base0 | (base1 << 16) | (base2 << 24)),
        limit=(limit0 | (limit << 16)),
        type=type,
        dpl=dpl,
        s=s,
        p=p,
        avl=avl,
        l=l,
        db=d,
        g=g
    )


def print_desc_list(desc_list):
    """
    Build and print a table from a list of desc_struct objects.

    Args:
        desc_list (list): List of desc_struct objects.
    """
    # Create a PrettyTable object with appropriate column headers
    table = PrettyTable()
    table.field_names = [
        "Index", "Base Address", "Limit", "Type", "DPL", "S", "P", "AVL", "L", "D/B", "G"
    ]

    # Populate the table with desc_struct data
    for index, desc in enumerate(desc_list, start=0):
        table.add_row([
            index,
            "0x%08x" % desc.base,
            "0x%05x" % desc.limit,
            "{0:04b}".format(desc.type),
            desc.dpl,
            desc.s,
            desc.p,
            desc.avl,
            desc.l,
            desc.db,
            desc.g
        ])

    # Print the table
    print(table)


class PrintGDTCommand(gdb.Command):
    """Prints the GDT table entries."""

    def __init__(self):
        super(PrintGDTCommand, self).__init__(
            "gdt",
            gdb.COMMAND_USER,
            gdb.COMPLETE_NONE
        )

    def invoke(self, arg, from_tty):

        base=gdb.parse_and_eval("(void *)&per_cpu__gdt_page + __per_cpu_offset[0]").cast(gdb.lookup_type("unsigned long"))
        num_descriptors = 32 # 32 descriptors in GDT linux 2.6.26
        descriptor_size = 8
        desc_table = []


        for i in range(num_descriptors):
            entry_address = base + i * descriptor_size
            tmp_d = gdb.parse_and_eval("*((struct desc_struct *)0x%x)" % entry_address)
            d = parse_desc_struct(tmp_d)
            desc_table.append(d)
            # print(d)
        print("GDT Table:")
        print_desc_list(desc_table)


# Register the new command
PrintGDTCommand()

