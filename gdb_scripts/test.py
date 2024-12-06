import gdb
from vfs_dir.file import File


class Test(gdb.Command):
    """Test command"""

    def __init__(self):
        super(Test, self).__init__("test", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        current = TaskStructPrinter.get_current_task()
        self.print_task_struct(current, mode=arg)

    def print_task_struct(self, task, mode="-b"):
        if not (isinstance(task, gdb.Value) and task.type.target().name == "task_struct"):
            print("Error: task is not a task_struct")
            return
        print("*** Task Info ***")
        if mode == "-b":  # brief
            pid = task['pid']
            comm = task['comm'].string()
            state = task['state']
            prio = task['prio']
            parent = task['parent']
            if not parent:
                parent = None
            else:
                parent = task['parent']['pid']
            if task['mm'] != 0:
                pgd = task['mm']['pgd']
            else:
                pgd = None

            print("PID: {}".format(pid))
            print("Command: {}".format(comm))
            print("State: {}".format(state))
            print("Priority: {}".format(prio))
            print("Parent pid: {}".format(parent))
            print("thread sp0: {:#08x}".format(int(task['thread']['sp0'])))
            if pgd is not None:
                print("pgd: {:#08x}".format(int(pgd)))
            else:
                print("pgd: None")
            print("\n")
        elif mode == "-n":  # normal
            print(task.dereference())
        elif mode == "-f": #file
            files = task['files']
            print("hi")
            print(files['fd_array'])
            for i in range(0, 3):
                print(f"fd_array[{i}]:")
                print(files['fd_array'][i].type)
                file= File(files['fd_array'][i])
                file.print("-a")


Test()
