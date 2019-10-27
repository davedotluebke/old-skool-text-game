import os
import debug

def findAllPythonFiles():
    files_list = []
    for root, dirs, files in os.walk("domains"):
        path = root.split(os.sep)
        debug.dbg.debug((len(path) - 1) * '---' + os.path.basename(root), 6)
        for file in files:
            debug.dbg.debug(len(path) * '---'+ file, 6)
            (head, sep, tail) = file.partition('.')
            if tail == "py":
                gameFilePath = ''
                for loc_dir in path:
                    gameFilePath += loc_dir
                    gameFilePath += '.'
                gameFilePath += file
                files_list.append(gameFilePath)
    return files_list
