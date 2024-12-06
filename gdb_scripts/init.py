import gdb
import os


project_root_path = os.getenv('PROJECT_ROOT_PATH')
lab_path = os.getenv('LAB_PATH')
lab_number= os.getenv('LAB_NUMBER')




gdb.execute(f"source {project_root_path}/gdb_scripts/lscript.py")
gdb.execute("lscript")
gdb.execute(f"init_lab{lab_number}")
print(f"Lab {lab_number} is ready!")
