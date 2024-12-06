#!/usr/bin/python3

import os
import re
import sys

oldgcc = os.getenv("OLDGCC")
kernel_source_path = os.getenv("KERNEL_SOURCE_PATH")

if not oldgcc:
    print("OLDGCC is not set.")
    sys.exit(1)

def macro_expansion(target):
    '''
    This function expands the macros in the target file.
    :param target: .o file path
    :return:
    '''
    directory, filename = os.path.split(target)
    target_cmd = f"{directory}/.{filename}.cmd"
    with open(target_cmd) as f:
        first_line = f.readline()
    command = re.sub(r'^.* := gcc', '', first_line)
    new_command = f"cd {kernel_source_path} && {oldgcc} -save-temps=obj {command.rstrip()}"
    # print(new_command)
    os.system(new_command)
    preprocessed_file = f"{filename[:-2]}.i"
    return f"{directory}/{preprocessed_file}"
    # with open(preprocessed_file, 'r') as file:
    #     content = file.read()
    # return content


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 macro_expansion.py <target>")
        print(sys.argv)
        sys.exit(1)
    preprocessed_file = macro_expansion(sys.argv[1])
    print(preprocessed_file)