import string

import gdb


def container_of(ptr, type_name, member):
    type_info = gdb.lookup_type(type_name)
    member_offset = gdb.parse_and_eval("&(({} *)0)->{}".format(type_name, member)).cast(
        gdb.lookup_type("unsigned long"))
    return (ptr.cast(gdb.lookup_type("unsigned long")) - member_offset).cast(type_info.pointer())


def print_ptr(ptr):
    # 确保传入的是指针类型
    if not ptr.type.pointer():
        raise TypeError("Provided value is not a pointer.")
    command = f'p/z *({ptr.type}){ptr}'
    gdb.execute(command)


def read_memory(addr, size):
    # 确保传入的是指针类型
    ptr = gdb.parse_and_eval(f"(unsigned char *){addr}")
    results = bytearray(size)
    for i in range(size):
        # print(ptr[i])
        # print(ptr[i].type)
        # print(type(ptr[i]))
        # print(type(ptr[i].bytes))
        # print(type(results[i]))
        results[i] = ptr[i]
    return bytes(results)


def get_var(type: string, address: int):
    return gdb.Value(address).cast(gdb.lookup_type(type).pointer()).dereference()


def print_struct_members(struct_type):
    # Get the type of the struct
    struct = gdb.lookup_type(struct_type).strip_typedefs()
    print(type(struct))

    # Ensure it is a struct
    if struct.code != gdb.TYPE_CODE_STRUCT:
        print(f"{struct_type} is not a struct")
        return

    # Iterate over the fields and print their names
    for field in struct.fields():
        print(field.name)


def is_address_str(arg):
    return arg.startswith("0x") or arg.startswith("0X")


# def is_pointer(val):
#     return val.type.code == gdb.TYPE_CODE_PTR

def print_hash_table(hash_table, size, type, memter):
    for i in range(size):
        head = hash_table + i * 4
        print_hlist(head, type, memter)


def print_hlist(head, type, memter):
    head = get_var("struct hlist_head", head)
    node = head.first
    while node:
        print(container_of(node, type, memter))
        node = node.next

def print_type(v):
    print(v.type)
    print(type(v))

#输入参数为地址或变量名字符串，返回gdb变量
def get_arg_from_string(arg):
    if is_address_str(arg):
        ptr = gdb.Value(int(arg, 16))
        return ptr
    else:
        return gdb.parse_and_eval(arg)

# todo PER_CPU变量读取


