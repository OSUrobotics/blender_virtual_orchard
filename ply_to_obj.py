import pymeshlab
from glob import glob
import os
remove = False
folder = "tree_dataset/dataset_envy_split"
for file_path in glob(folder+"/*.obj"):
    print("Processing {}".format(file_path))
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(file_path)
    ms.save_current_mesh(file_path[:-4]+'.x3d')
    if remove:
        os.remove(file_path)
