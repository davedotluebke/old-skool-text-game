import os

# 
#  Note this is too expensive to run as an interactive command!
#

def findAllPythonFiles():
    files_list = []
    for root, dirs, files in os.walk("domains"):
        path = root.split(os.sep)
        for file in files:
            (head, sep, tail) = file.partition('.')
            if tail == "py":
                gameFilePath = ''
                for loc_dir in path:
                    gameFilePath += loc_dir
                    gameFilePath += '.'
                gameFilePath += file
                files_list.append(gameFilePath)
    return files_list
