import gdb
from utilities import is_address_str
from utilities import container_of


class PrintDentry(gdb.Command):

    def __init__(self):
        super(PrintDentry, self).__init__("pdentry", gdb.COMMAND_USER)
        self.dentry = None

    def invoke(self, arg, from_tty):
        arg = arg.split()
        if len(arg) == 2:
            target, mode = arg
        elif len(arg) == 1:
            mode = "-a"
            target = arg[0]
        else:
            print("Usage: pdentry <dentry> [-a | -b]")
            return
        if is_address_str(arg[0]):
            ptr = gdb.Value(int(arg[0], 16))
            self.dentry = ptr.cast(gdb.lookup_type("struct dentry").pointer()).dereference()
        else:
            res = gdb.parse_and_eval(arg[0])
            # test whether a pointer
            if res.type.code == gdb.TYPE_CODE_PTR:
                self.dentry = res.dereference()
            else:
                self.dentry = res

        self.print_dentry(mode)

    def print_dentry(self, mode):
        if mode == "-a":
            print(self.dentry)
        elif mode == "-b":#briefly
            print("hello")#test
            # print(f"address: {self.dentry.address}")
            # print(f"parent: {self.dentry['d_parent']}")
            # print(f"mount: {self.dentry['d_mount']}")
            # print(f"inode: {self.dentry['d_inode']}")
            # print(f"hash: {self.dentry['d_hash']}")
            # print(f"child: {self.dentry['d_child']}")
            # print(f"d_subdirs: {self.dentry['d_subdirs']}")
            # print(f"d_alias: {self.dentry['d_alias']}")
            # print(f"d_lru: {self.dentry['d_lru']}")
            # print(f"d_time: {self.dentry['d_time']}")
            # print(f"d_flags: {self.dentry['d_flags']}")
            # print(f"d_seq: {self.dentry['d_seq']}")
            # print(f"d_name: {self.dentry['d_name']}")
            # print(f"d_op: {self.dentry['d_op']}")
            # print(f"d_sb: {self.dentry['d_sb']}")
            # print(f"d_fsdata: {self.dentry['d_fsdata']}")
            # print(f"d_lockref: {self.dentry['d_lockref']}")
            # print(f"d_iname: {self.dentry['d_iname']}")
            # print(f"d_cookie: {self.dentry['d_cookie']}")
        elif mode == "-c":#child
            header=self.dentry['d_subdirs'].address
            ptr=header['next']
            while ptr!=header:
                v=container_of(ptr,"struct dentry","d_u")
                print(v,v['d_name']['name'].string())
                ptr=ptr['next']


# 注册命令
PrintDentry()
