import os
import gdb

project_root_path = os.getenv('PROJECT_ROOT_PATH')
lab_path = os.getenv('LAB_PATH')


def list_py_files(directory):
    py_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                py_files.append(os.path.join(root, file))
    return py_files


class LoadVfsScript(gdb.Command):
    """Load the VFS script in GDB"""

    def __init__(self):
        super(LoadVfsScript, self).__init__("lscript", gdb.COMMAND_USER)  # load script

    def invoke(self, arg, from_tty):
        #general scripts
        general_script_paths = list_py_files(project_root_path + "/gdb_scripts")
        for script_path in general_script_paths:
            if not script_path.endswith("init.py") and not script_path.endswith("lscript.py") :
                gdb.execute("source {}".format(script_path))
        # lab specific scipts
        lab_script_paths = list_py_files(lab_path + "/gdb_scripts")
        for script_path in lab_script_paths:
            gdb.execute("source {}".format(script_path))


LoadVfsScript()
