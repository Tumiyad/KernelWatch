import gdb
from tss import *
import os
from utilities import print_ptr


class TaskStructPrinter(gdb.Command):
    """Print the task_struct of the current process."""

    def __init__(self):
        super(TaskStructPrinter, self).__init__("print_task_struct_chain", gdb.COMMAND_USER)

    # def printf_task_struct(task):
    #


    @staticmethod
    def print_task_struct(task):
        print("*** Task Info ***")
        pid = task['pid']
        comm = task['comm'].string()
        state = task['state']
        prio = task['prio']
        parent = task['parent']
        if not parent:
            parent = None
        else:
            parent = task['parent']['pid']
        if task['mm']!=0:
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

    def invoke(self, arg, from_tty):
        task = self.get_current_task()
        # print(task.dereference())
        self.print_task_struct(task)
        # 沿着task_struct链打印task_struct的信息
        while task:
            print_task_struct(task)
            if task['pid'] == 0:
                break
            else:
                task = task['parent']

    #注意此方法依靠内核栈地址，若断点命中时在用户态，esp指向用户栈，会出错。
    # @staticmethod
    # def get_current_task():
    #     esp_value = gdb.parse_and_eval("$esp")
    #     thread_info_addr = int(esp_value) & ~0x1fff
    #     # print("thread_info_addr: %x" % (thread_info_addr))
    #     gdb.execute("set $thread_info = 0x%x" % (thread_info_addr))
    #     thread_info_p = gdb.parse_and_eval("$thread_info")
    #     thread_info = thread_info_p.cast(gdb.lookup_type("struct thread_info").pointer())
    #     # 获取 task_struct 的指针
    #     task = thread_info['task']
    #     return task

    @staticmethod
    def get_current_task():
        esp_value = gettss()["x86_tss"]["sp0"]
        thread_info_addr = int(esp_value) & ~0x1fff
        # print("thread_info_addr: %x" % (thread_info_addr))
        gdb.execute("set $thread_info = 0x%x" % (thread_info_addr))
        thread_info_p = gdb.parse_and_eval("$thread_info")
        thread_info = thread_info_p.cast(gdb.lookup_type("struct thread_info").pointer())
        # 获取 task_struct 的指针
        task = thread_info['task']
        return task

    @staticmethod
    def get_init_task():
        init_task = gdb.parse_and_eval("init_task")
        return init_task

    @staticmethod
    def get_init_root_path():
        init_task = TaskStructPrinter.get_init_task()
        return init_task['fs']['root']

TaskStructPrinter()

#create a new command to print the current task_struct pid
class CurrentTaskPid(gdb.Command):
    """Print the current task_struct pid."""

    def __init__(self):
        super(CurrentTaskPid, self).__init__("current_task", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        task = TaskStructPrinter.get_current_task()
        print("task_struct: {:#08x}".format(int(task)))
        TaskStructPrinter.print_task_struct(task)
        # pid = task['pid']
        # print("Current Task PID: {}".format(pid))

CurrentTaskPid()