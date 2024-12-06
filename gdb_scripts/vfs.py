import gdb
from prettytable import PrettyTable
from process import TaskStructPrinter
from utilities import container_of

def build_full_path(dentry):
    if dentry == dentry['d_parent']:
        return "/"
    path = []
    while True:
        name = dentry['d_name']['name'].string()
        path.insert(0, name)
        path.insert(0, "/")
        dentry = dentry['d_parent']
        if dentry == dentry['d_parent']:
            break
    res = "".join(path)
    return res



def get_filesystem_name(vfsmount):
    super_block = vfsmount['mnt_sb']
    filesystem_type = super_block['s_type']
    filesystem_name = filesystem_type['name'].string()
    return filesystem_name


def print_vfsmount_tree(vfsmount, indent=0):
    # 获取挂载点的基本信息
    # mount_point = vfsmount['mnt_mountpoint']['d_name']['name'].string()
    mount_point = build_full_path(vfsmount['mnt_mountpoint'])
    filesystem_name = get_filesystem_name(vfsmount)

    # 打印当前挂载点的信息
    # print(" " * indent + "Mount point: {}, Filesystem: {}".format(mount_point, filesystem_name))
    print(" " * indent + "{}, {}".format(mount_point, filesystem_name))

    # 获取子挂载点列表
    submount_list = vfsmount['mnt_mounts']
    submount = submount_list['next']

    while submount != vfsmount['mnt_mounts'].address:
        child_vfsmount = container_of(submount, "struct vfsmount", "mnt_child")
        print_vfsmount_tree(child_vfsmount, indent + 4)
        submount = submount['next']


class VFSmountPrinter(gdb.Command):

    def __init__(self):
        super(VFSmountPrinter, self).__init__("vfs", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        init_root_vfsmount = TaskStructPrinter.get_init_root_path()['mnt']
        print_vfsmount_tree(init_root_vfsmount)


class ndPrinter(gdb.Command):

    def __init__(self):
        super(ndPrinter, self).__init__("nd", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        gdb.execute("print nd->path->dentry")
        gdb.execute("print nd->path->dentry->d_name")


class DentryCachePrinter(gdb.Command):
    """Print all entries in the dentry cache"""

    def __init__(self):
        super(DentryCachePrinter, self).__init__("print_dentry_cache", gdb.COMMAND_DATA)

    def invoke(self, arg, from_tty):
        dentry_hashtable = gdb.parse_and_eval("dentry_hashtable")
        # get size from d_hash_mask
        hashtable_size = gdb.parse_and_eval("d_hash_mask+1")
        # print("Hashtable size: {}".format(hashtable_size))
        for i in range(int(hashtable_size)):
            head = dentry_hashtable[i]
            dentry_p = head['first']
            if dentry_p:
                count = 0
                dentry_list = []
                while dentry_p:
                    dentry = container_of(dentry_p, "struct dentry", "d_hash")
                    dentry_list.append(dentry_info(dentry))
                    dentry_p = dentry['d_hash']['next']
                    count += 1
                print("Bucket {}: {} entries".format(i, count))
                for info in dentry_list:
                    print("  {}".format(info))


def dentry_info(dentry):
    address = dentry
    name = dentry['d_name']['name'].string()
    inode = dentry['d_inode']
    if inode:
        inode_num = inode['i_ino']
    else:
        inode_num = "No inode"
    return "dentry: {}, address: {}, inode: {}".format(name, address, inode_num)


class DentryCacheLookUp(gdb.Command):
    """Print all entries in the dentry cache"""

    def __init__(self):
        super(DentryCacheLookUp, self).__init__("dentry_find", gdb.COMMAND_DATA)

    def invoke(self, arg, from_tty):
        dentry_hashtable = gdb.parse_and_eval("dentry_hashtable")
        # get size from d_hash_mask
        hashtable_size = gdb.parse_and_eval("d_hash_mask+1")
        for i in range(int(hashtable_size)):
            head = dentry_hashtable[i]
            dentry_p = head['first']
            while dentry_p:
                dentry = container_of(dentry_p, "struct dentry", "d_hash")
                if dentry['d_name']['name'].string() == arg:
                    print(dentry_info(dentry))
                dentry_p = dentry['d_hash']['next']


class SuperBlockPrinter(gdb.Command):
    """打印超级块链表中的所有超级块信息"""

    def __init__(self):
        super(SuperBlockPrinter, self).__init__("super_blocks", gdb.COMMAND_DATA)

    def invoke(self, arg, from_tty):
        self.print_super_blocks()

    def print_super_blocks(self):
        # 初始化表格
        table = PrettyTable()
        table.field_names = ["fs type name", "root dentry address", "super block address"]

        # 获取超级块链表的头
        head = gdb.parse_and_eval("super_blocks")
        sb = head.cast(gdb.lookup_type("struct super_block").pointer())
        node = sb['s_list']['next']

        # 遍历超级块链表并收集信息
        while node != head.address:
            sb = node.cast(gdb.lookup_type("struct super_block").pointer())
            row = self.get_super_block_info(sb)
            table.add_row(row)
            node = sb['s_list']['next']

        # 打印表格
        print(table)

    def get_super_block_info(self, sb):
        fs_type_name = sb['s_type']['name'].string()
        # root_dentry = sb['s_root']
        # hex(int(value))
        root_dentry = hex(int(sb['s_root']))
        address = hex(int(sb))
        return [fs_type_name, root_dentry, address]


# 注册命令到 GDB
VFSmountPrinter()
ndPrinter()
DentryCachePrinter()
DentryCacheLookUp()
SuperBlockPrinter()
