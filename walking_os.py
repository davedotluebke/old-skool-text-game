import os
import debug

def findAllPythonFiles():
    files_list = []
    for root, dirs, files in os.walk("domains"):
        path = root.split(os.sep)
        debug.dbg.debug((len(path) - 1) * '---' + os.path.basename(root), 2)
        for file in files:
            debug.dbg.debug(len(path) * '---'+ file, 2)
            (head, sep, tail) = file.partition('.')
            if tail == ".py":
                files_list.append(file)
    return files_list
