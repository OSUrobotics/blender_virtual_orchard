import pymeshlab
from glob import glob
import os
remove = False
folder = "dataset"
for file_path in glob(folder+"/*/*.ply"):
    print("Processing {}".format(file_path))
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(file_path)
    ms.save_current_mesh(file_path[:-4]+'.obj')
    if remove:
        os.remove(file_path)
