from PIL import Image
import numpy as np
import glob

def find_closest_colors(image_array, label_colors):
    """
    Adjust colors in an image array to the closest label color for each pixel using vectorization.
    """
    # Convert label colors to numpy array for vectorized operations
    label_colors = np.array(label_colors)

    # Reshape image array for broadcasting, so we have a shape (height, width, 1, 3)
    pixels = image_array[:, :, np.newaxis, :]
    #Convert rgb to lab
    # Compute the Euclidean distance between each pixel and each label color
    distances = np.linalg.norm(pixels/255- label_colors/255, axis=3)

    # Find the index of the closest label color for each pixel
    closest_color_indices = np.argmin(distances, axis=2)

    # Map each pixel to its closest label color
    adjusted_image_array = label_colors[closest_color_indices]

    return adjusted_image_array

def adjust_colors(image_path, label_colors, output_path):
    """
    Read an image, adjust each pixel color to the closest label color, and save the result.
    """
    # Open image and convert to RGB
    image = Image.open(image_path).convert('RGB')
    #Print set of unique colors
    print(set(image.getdata()))
    image_array = np.array(image)

    # Vectorized adjustment of colors
    adjusted_image_array = find_closest_colors(image_array, label_colors)

    # Convert adjusted array back to image and save
    adjusted_image = Image.fromarray(adjusted_image_array.astype(np.uint8))
    adjusted_image.save(output_path)
    print(f"Adjusted image saved to {output_path}")

# Define label colors in RGB format
# label_colors = [
#     (0, 0, 255),         # Post
#     (255, 0, 255),       # Wire
#     (0.27 * 255, 0.27 * 255, 0.27 * 255),  # Sky
#     (0.6 * 255, 0.5 * 255, 255),           # Ground
#
#     (255, 0, 0),         # Trunk
#     (0, 255, 0),         # Spur
#     (255, 255 * 0.588235, 0),              # Branch
#     (0, 0, 0),          # Background trees
#     (0, 255, 255),          # Background wires
#     (165, 0, 120),      # Background posts
# ]


label_colors = [
    (255, 0, 0),         # Spur
    (0, 0, 255),         # Trunk
    (255, 255, 0),       # Branch
    (255/2, 255/2, 255/2), # Sky
    (255, 0, 255), #Labelled wire
    (0, 255/2, 255/2), #Bg Post
    (0, 0, 0), #Bg Tree
    (255, 192, 203), #Ground
    (0, 255, 255), #Bg Wire
    (0, 0, 255), #Labelled Post

]
# Process all images in the specified folder
folder = "."
for image_folder in glob.glob(f"{folder}/test_3"):
    for image_path in glob.glob(f"{image_folder}/*_labeled_rgb*.png"):
        output_path = image_path
        adjust_colors(image_path, label_colors, output_path)
