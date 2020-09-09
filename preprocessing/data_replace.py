from shutil import copy

import os

dirs = ("test", "train")
if not os.listdir("../images/test") and not os.listdir("../images/train"):
    for filename in os.listdir("rawdata"):
        copy_from = os.getcwd() + "\\rawdata" + "\\" + filename
        copy_to = os.getcwd() + "\\images"
        if dirs[0] in filename:
            copy_to += "\\" + dirs[0]
        elif dirs[1] in filename:
            copy_to += "\\" + dirs[1]
        copy(copy_from, copy_to)
