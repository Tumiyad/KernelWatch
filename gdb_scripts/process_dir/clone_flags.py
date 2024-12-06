# # 以下代码不可用
# import gdb
#
# # Define the clone flags constants
# CLONE_FLAGS = {
#     'CSIGNAL': 0x000000ff,
#     'CLONE_VM': 0x00000100,
#     'CLONE_FS': 0x00000200,
#     'CLONE_FILES': 0x00000400,
#     'CLONE_SIGHAND': 0x00000800,
#     'CLONE_PTRACE': 0x00002000,
#     'CLONE_VFORK': 0x00004000,
#     'CLONE_PARENT': 0x00008000,
#     'CLONE_THREAD': 0x00010000,
#     'CLONE_NEWNS': 0x00020000,
#     'CLONE_SYSVSEM': 0x00040000,
#     'CLONE_SETTLS': 0x00080000,
#     'CLONE_PARENT_SETTID': 0x00100000,
#     'CLONE_CHILD_CLEARTID': 0x00200000,
#     'CLONE_DETACHED': 0x00400000,
#     'CLONE_UNTRACED': 0x00800000,
#     'CLONE_CHILD_SETTID': 0x01000000,
#     'CLONE_STOPPED': 0x02000000,
#     'CLONE_NEWUTS': 0x04000000,
#     'CLONE_NEWIPC': 0x08000000,
#     'CLONE_NEWUSER': 0x10000000,
#     'CLONE_NEWPID': 0x20000000,
#     'CLONE_NEWNET': 0x40000000,
#     'CLONE_IO': 0x80000000
# }
#
#
# class CloneFlagsCommand(gdb.Command):
#     """Display the clone flags in a readable format."""
#
#     def __init__(self):
#         super(CloneFlagsCommand, self).__init__("clone_flags", gdb.COMMAND_USER, gdb.COMPLETE_NONE)
#
#     def invoke(self, arg, from_tty):
#         # Parse the argument (expected to be the address of the clone_flags)
#         try:
#             addr = int(arg, 16)
#         except ValueError:
#             print("Invalid address format. Use hexadecimal format.")
#             return
#
#         # Read the value at the given address
#         try:
#             value = int(gdb.execute(f"x/wx {addr}", to_string=True).split()[1], 16)
#         except gdb.error as e:
#             print(f"Error reading memory: {e}")
#             return
#
#         # Display the flags
#         print(f"Clone flags at {addr:#x} (value: {value:#x}):")
#         for flag, mask in CLONE_FLAGS.items():
#             if value & mask:
#                 print(f"  {flag}")
#
#
# # Register the command with GDB
# CloneFlagsCommand()
