Data files - https://oregonstate.box.com/s/h64vg0sa5ttyqx5hocgpcak77mkzsj6b

# Blender Orchard Generator Addon

## Installation

1. Download the addon files from the `orchard_generator` directory:
    - Go to [this link](https://github.com/OSUrobotics/blender_virtual_orchard/tree/addon/addon/orchard_generator).
    - Copy the URL and go to [download-directory.github.io](https://download-directory.github.io/).
    - Paste the URL to get the zip file of the addon.

2. Open Blender.

3. Go to `Edit` -> `Preferences` -> `Add-ons` -> `Install...` (top right).

4. Choose the zip file you just downloaded and ensure the addon is toggled on.

5. To use the addon, press `N` to bring up the sidebar in the View3D menu, and it should be there.

### Alternative (Highly recommended for development)

 1. Download the Blender Development Visual Studio Code Extension by Jacques Lucke.
 2. Have all the addon files in a workspace and simply follow the extension guide and you are good to go.

## Usage

### Setting Up the Render

1. **Loading Properties:**
   - If you want to load properties from a JSON file, enable the `Load Properties from JSON` \
   option and specify the path to your JSON files directory. Then, in that directory, you should \
   have a `gui_parameters` json file with all the parameters from the panel that you want to manually specify (see example below). You also need a `other_parameters` json file with parameters as specified in the example
   below.
   \
   \
   Otherwise, specify them in the `Orchard` and `Image Render` panels.

2. **Specifying Paths:**
   - Set the `Texture Path` and `Tree Files Path` to the respective directories containing your textures and tree models. Also, set the `Images dir Path` if you are taking images of the trees.

3. **Setting parameters:**
   - Set all parameters as you desire in both the panels 

### Rendering

1. **Clean Blender Data:**
   - The script starts by cleaning Blender data to ensure a fresh start.

2. **Creating the Camera:**
   - A camera object is created and optionally follows a sine wave path if `Render Camera` is enabled.

3. **Loading Trees:**
   - Trees are loaded from the specified directory.

4. **Tree Placement:**
   - Trees are placed on a grid with slight random noise for realism.

5. **Texture Application:**
   - Textures are applied to the trees. You can choose between random textures or a specific realistic texture in the json file `other_parameters`.

6. **Rendering Posts and Wires:**
   - If enabled, posts and wires are rendered along with the trees.

7. **Rendering Sky and Sun:**
   - The sky and sun are rendered based on the specified properties.

8. **Rendering Ground:**
   - A ground plane is created and subdivided with a displacement modifier to create a bumpy terrain. Textures are applied to the ground plane.

9. **Polygon Clipping:**
   - Objects outside the specified polygon coordinates are removed after rotation if `Polygon Clipping` is enabled.

10. **Taking Images:**
    - Images are taken if and only if `Take image` is enabled. They can also be taken by pressing the `TAKE IMAGES` button.
    \
    \
    The formatting for how the images are stored should be tweaked to fit your needs. Currently the \
    files get overridden each render

11. **Dumping Properties:**
    - All properties are saved to a JSON file in the `dumps' directory with a timestamp for future reference.

### JSON Configuration

The addon can load all the gui parameters from a JSON file. The file will look something like this:

### Example JSON File

```json
{
    "tree_file_path": "path to tree files dir...",
    "texture_path": "path to textures dir...",
    "json_files_path": "path to json files dir...",
    "load_props_from_json": true,
    "random_textures": false,
    "plane_unevenness": 2.5,
    "polygon_clipping": false,
    "tree_rows": 1,
    "tree_columns": 1,
    "orchard_yaw": 0.0,
    "tree_angle": [
        0.30000001192092896,
        0.0,
        0.0
    ],
    "num_sun_positions": 1,
    "wire_spacing": 0.5,
    "render_cam": false,
    "render_wires": true,
    "render_sky_and_sun": true,
    "render_posts": true,
    "render_plane": true,
    "render_polygons": false,
    "orchard_generated": false,
    "snap_image": false,
    "random_tree": true,
    "image_pairs": false,
    "image_dir_path": "path to dir for image storage...",
    "num_images": 2,
    "focal_length": 18.0,
    "aspect_X": 1.0,
    "aspect_Y": 1.0,
    "resolution_X": 1920,
    "resolution_Y": 1080,
    "cam_offset": [
        -3.0,
        2.799999952316284,
        1.5
    ],
    "left_min": 0.0,
    "right_max": 0.0,
    "in_min": 1.0,
    "out_max": 1.0,
    "down_min": 0.5,
    "up_max": 0.5,
    "camera_angle": [
        -1.5700000524520874,
        -3.140000104904175,
        0.0
    ],
    "min_x": -1.5707963705062866,
    "max_x": -1.5707963705062866,
    "min_y": -3.1415927410125732,
    "max_y": -3.1415927410125732,
    "min_z": 0.0,
    "max_z": 0.0
}
```

The addon can load additional parameters from a JSON file. The file should contain:

- Polygon coordinates
- Grid square coordinates for different tree types
- Random tree and ground texture file names
- Realistic tree and ground texture file names

### Example JSON File

```json
{
    "polygon_coordinates": [[x1, y1], [x2, y2], ...],
    "envy_grid_square_coordinates": [[x1, y1], [x2, y2], ...],
    "ufo_grid_square_coordinates": [[x1, y1], [x2, y2], ...],
    "random_tree_texture_file_names": ["texture1", "texture2", ...],
    "random_ground_texture_file_names": ["texture1", "texture2", ...],
    "realistic_tree_texture_file_name": "realistic_tree",
    "realistic_ground_texture_file_name": "realistic_ground"
}
```

### Example dump JSON File name

`props_dump_2024-07-17_00-32-32.json`

### Example image taken in Blender's 3-D Environment
![image_0000](https://github.com/user-attachments/assets/bf88253b-6720-42a8-8718-a78da64270fb)


