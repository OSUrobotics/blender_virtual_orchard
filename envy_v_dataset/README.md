This is a semantic segmentation dataset for trees in a V-trellis architecture.

The labels are as follows:

label_colors = [
    (0, 0, 1),           # Post
    (1, 0, 1),         	 # Wire
    (0.27, 0.27, 0.27),  # Sky
    (0.6, 0.5, 1),       # Ground
    (1, 0, 0),           # Trunk
    (0, 1, 0),           # Spur
    (1, 0.588235, 0),    # Branch
    (0, 0, 0)            # Other
]


For each image we provide the corresponding depth input. We also provide pairs of images, i.e., images of the same scene captured with slight variations in the camera position to make possible use structure from motion techniques.


File naming:
The file name has the following parameters
image_number - A unique number for each image
pair - The pair number {0,1}
labeled - If the image is labeled or not {labeled, unlabelled}
type - If the image type is rgb or depth {rgb, depth}

The files are named as {image_number}_{pair}_{labeled}_{type}.png