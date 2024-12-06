import gdb
import os

project_root_path = os.getenv('PROJECT_ROOT_PATH')
lab_path = os.getenv('LAB_PATH')
lab_number= os.getenv('LAB_NUMBER')

class Init(gdb.Command):
    """Load the VFS script in GDB"""

    def __init__(self):
        super(Init, self).__init__(f"init_lab{lab_number}", gdb.COMMAND_USER)  # load script

    def invoke(self, arg, from_tty):
        pass

Init()