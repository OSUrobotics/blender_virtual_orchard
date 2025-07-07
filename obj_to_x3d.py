import pymeshlab
from glob import glob
import os
remove = False
folder = "dataset_envy_instance"
#Regex to match tree_[4-9]_*.obj
#glob(folder+"/tree_[4-9]_*.obj")
#Doesnt work

for file_path in glob(folder+"/tree_*.obj"):
    print("Processing {}".format(file_path))
    ms = pymeshlab.MeshSet()
    ms.load_new_mesh(file_path)
    ms.save_current_mesh(file_path[:-4]+'.x3d')
    if remove:
        os.remove(file_path)
