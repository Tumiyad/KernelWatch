import gdb


class File:
    def __init__(self, ptr):
        if not isinstance(ptr, gdb.Value):
            raise ValueError("ptr must be a gdb.Value")
        elif ptr.type.target().name != "file":
            raise ValueError("ptr must be a pointer to a file")
        file = ptr.dereference()
        self.file = file
        self.address = self.file.address
        self.ops = file["f_op"].dereference()

    def __str__(self):
        return "file: {:#x}".format(int(self.address))

    def print(self, mode="-a"):
        print(f"file struct address: {self.address}")
        if mode == "-a":
            print(self.file)
        elif mode == "-b":
            print(f"address: {self.address}")
            # print(f"file_operations: {self.ops.address}")
            print("file_operations:")
            print(self.ops)
