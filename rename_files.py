#Read images from the specified folder
import glob
import os

folder = "C://Users//abhin//PycharmProjects//blender_virtual_orchard//blender_virtual_orchard//envy_v_dataset//far_with_trunk"

for image_file in glob.glob(f"{folder}/*.png"):
    #File format: tree_{image_number}__pair_{1,2}_{labeled, unlabelled}_{rgb, depth}_0001
    #Get file name
    print(image_file)
    try:
        image_file_name = os.path.basename(image_file)
        image_file_dir = os.path.dirname(image_file)

        image_number = image_file_name.split("_")[1]
        pair_number = image_file_name.split("_")[4]
        pair_number = int(pair_number) - 1
    except:
        continue
    labeled = image_file_name.split("_")[5]
    rgb = image_file_name.split("_")[6]

    new_file_name = f"{image_number}_{pair_number}_{labeled}_{rgb}.png"

    save_folder = os.path.join(image_file_dir, new_file_name)
    os.rename(image_file, save_folder)
    print(image_file, new_file_name)