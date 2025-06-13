import bpy
import random
import math
from . helpers import load_scene
from .builders import (
    create_sky_color,
    create_sky_texture,
    create_sun,
    fibonacci_hemisphere,
    create_sine,
    make_camera_follow_curve,
)

sun_or = fibonacci_hemisphere(30)

def setup_composite_nodes(props, label = False):
    # Enable nodes in the compositor
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree

    # Clear existing nodes in the compositor
    tree.nodes.clear()

    # Add nodes
    render_layers = tree.nodes.new('CompositorNodeRLayers')
    math_greater_than = tree.nodes.new(type="CompositorNodeMath")
    set_value = tree.nodes.new(type="CompositorNodeValue")
    map_range = tree.nodes.new(type="CompositorNodeMapRange")
    normalize = tree.nodes.new(type="CompositorNodeNormalize")

    # Set the maximum depth threshold, simulating the D435 max range
    max_depth = 10.0  # Example: max range in meters

  

    # Configure output file node
    file_output = tree.nodes.new(type="CompositorNodeOutputFile")
    file_output.format.file_format = 'PNG'
    file_output.format.compression = 0
    #Set color depth to 16 bit
    file_output.format.color_depth = '16'
    file_output.base_path = props.image_dir_path  # Ensure props.image_dir_path is defined

    # Remove default slot and create named slots
    file_output.file_slots.clear()
    file_output.file_slots.new('rgb')
    if not label:
        file_output.file_slots.new('depth')
          # Set up the "greater than" condition for out-of-range depth
        math_greater_than.operation = 'GREATER_THAN'
        math_greater_than.inputs[1].default_value = max_depth  # Threshold for maximum depth

        # Set out-of-range values to 0
        set_value.outputs[0].default_value = 0

        # Use a Mix node to replace out-of-range depth with 0
        mix = tree.nodes.new(type="CompositorNodeMixRGB")
        mix.blend_type = 'MIX'
        mix.inputs[0].default_value = 1.0
        tree.links.new(math_greater_than.outputs[0], mix.inputs[0])  # Connect greater_than to Mix factor
        tree.links.new(render_layers.outputs['Depth'], mix.inputs[1])  # Original depth
        tree.links.new(set_value.outputs[0], mix.inputs[2])  # 0 if out of range

        # Configure the Map Range node to normalize depth
        map_range.inputs['From Min'].default_value = 0       # Minimum depth
        map_range.inputs['From Max'].default_value = max_depth # Maximum depth
        map_range.inputs['To Min'].default_value = 0         # Normalize from 0
        map_range.inputs['To Max'].default_value = 1         # Normalize to 1

        # Link nodes for depth output
        tree.links.new(render_layers.outputs['Depth'], math_greater_than.inputs[0])
        tree.links.new(mix.outputs[0], map_range.inputs[0])
        tree.links.new(map_range.outputs[0], normalize.inputs[0])
        tree.links.new(normalize.outputs[0], file_output.inputs['depth'])

    # Link RGB output
    tree.links.new(render_layers.outputs['Image'], file_output.inputs['rgb'])

    return file_output

def take_images(self, context):
    global sun_or
    props = context.scene.my_tool

    focal_length = props.focal_length

    bpy.context.scene.render.pixel_aspect_x = props.aspect_X
    bpy.context.scene.render.pixel_aspect_y = props.aspect_Y

    bpy.context.scene.render.resolution_x = props.resolution_X
    bpy.context.scene.render.resolution_y = props.resolution_Y
    bpy.context.view_layer.use_pass_z = True



    nx, ny = (props.tree_rows, props.tree_columns)
    for cam in bpy.data.cameras:
        cam.lens = focal_length

    tree_list = []
    obj_list = list(bpy.data.objects)

    for obj in obj_list:
        if "tree" in obj.name:
            tree_list.append(obj)
        # remove this line if campath becomes obsolete
        elif "campath" in obj.name:
            bpy.data.objects.remove(bpy.data.objects["campath"], do_unlink=True)
    # tree_list.sort(key=lambda x: int(x.name[4:]))
    cam_obj = bpy.data.objects["Camera"]
    bpy.context.view_layer.objects.active = cam_obj



    for i in range(props.num_images):
        if props.random_tree:
            #TODO: This is a bug -- Choose only from first half of the trees
            #Choose number between 0 and nx*ny
            selected_tree = random.choice(list(range(nx*ny//2)))

        else:
            selected_tree = 0

        selected_tree_root = f"tree{selected_tree}"
        tree_spur = bpy.data.objects[selected_tree_root + "_SPUR"]
        tree_branch = bpy.data.objects[selected_tree_root + "_BRANCH"]
        tree_trunk = bpy.data.objects[selected_tree_root + "_TRUNK"]        # Get tree dimensions

        tree_dimensions = tree_branch.dimensions
        tree_length = tree_dimensions.x
        tree_height = tree_dimensions.z
        tree_spacing = 2 * math.tan(props.tree_angle[0]) * tree_height
        
        # Uniform sampling for offset
        offset_x = random.uniform(props.left_min, props.right_max) * tree_length
        offset_y = random.uniform(props.in_min, props.out_max) * tree_spacing
        offset_z = random.uniform(props.down_min, props.up_max) * tree_height

        tree_location = tree_trunk.location
        tree_rotation_z = tree_trunk.rotation_euler.z

        # Calculate the offset considering the tree's rotation
        # camera_x_offset = offset_x * math.cos(tree_rotation_z) - offset_y * math.sin(tree_rotation_z)
        # camera_y_offset = offset_x * math.sin(tree_rotation_z) + offset_y * math.cos(tree_rotation_z)

        camera_x = tree_location.x + offset_x
        camera_y = tree_location.y + offset_y
        camera_z = tree_location.z + offset_z

        cam_obj.location = (camera_x, camera_y, camera_z)

        # Gaussian sampling for angle, adjust the SD according to your needs
        camera_angle_x = random.gauss((props.min_x + props.max_x) / 2, (props.max_x - props.min_x) / 6)
        camera_angle_y = random.gauss((props.min_y + props.max_y) / 2, (props.max_y - props.min_y) / 6)
        camera_angle_z = random.gauss((props.min_z + props.max_z) / 2, (props.max_z - props.min_z) / 6)

        cam_obj.rotation_euler[0] = camera_angle_x
        cam_obj.rotation_euler[1] = camera_angle_y

        # Only change yaw of camera if specified in the panel for some reason
        # Otherwise it messes with the camera orientation
        # Sincec its default is specified as 0 in the properties
        if props.min_z != 0 and props.max_z != 0: # if not defualt
            cam_obj.rotation_euler[2] = camera_angle_z
            # Offset camera's z rotation by pi if offset_y is negative
            if offset_y < 0:
                cam_obj.rotation_euler[2] = camera_angle_z + math.pi  
        else:
            cam_obj.rotation_euler[2] = tree_rotation_z
            if offset_y < 0: 
                cam_obj.rotation_euler[2] = tree_rotation_z + math.pi
        mat_tex = []
        mat_ground = []
        #Get all materials with texture in name
        for mat in bpy.data.materials:
            if "texture_ground" in mat.name:
                mat_ground.append(mat)
            elif "texture" in mat.name:
                mat_tex.append(mat)


        load_scene()
        material = None
        material_name = "Unset"
        selected_tree_idx = selected_tree
        # Set render engine

        # Slight variation in camera's location for the second image
        slight_variation = random.uniform(-0.1, 0.1)  # Adjust this as needed
        for label in [False, True]:
            print(f"Label: {label}")
            if label:
                engine = "eevee"
                # bpy.context.scene.eevee.use_taa_render = False  # Disable TAA for final render
                # bpy.context.scene.eevee.use_taa_reprojection = False  # Disable TAA in viewport
                if engine == "eevee":
                    bpy.context.scene.render.engine = 'BLENDER_EEVEE'
                    # Settings for Eevee low-sample (true color) render
                    bpy.context.scene.eevee.taa_render_samples = 1  # Set render samples to 1
                    bpy.context.scene.eevee.taa_samples = 1  # Set viewport samples to 1
                    bpy.context.scene.eevee.use_ssr = False  # Disable Screen Space Reflections
                    bpy.context.scene.eevee.use_bloom = False  # Disable Bloom
                    bpy.context.scene.eevee.use_gtao = False  # Disable Ambient Occlusion
                    bpy.context.scene.eevee.use_soft_shadows = False  # Disable Soft Shadows

                    bpy.context.scene.view_settings.view_transform = 'Standard'

                elif engine == "cycles":
                    bpy.context.scene.render.engine = 'CYCLES'
                    bpy.context.scene.cycles.device = 'GPU'
                    # Settings for Cycles low-sample (true color) render
                    bpy.context.scene.cycles.samples = 1  # Set render samples to 1
                    bpy.context.scene.cycles.preview_samples = 1  # Set viewport samples to 1
                    bpy.context.scene.cycles.pixel_filter_type = 'BOX'
                    bpy.context.scene.cycles.filter_width = 1.0
                    bpy.context.scene.cycles.max_bounces = 0  # Disable all indirect light bounces
                    bpy.context.scene.cycles.diffuse_bounces = 0
                    bpy.context.scene.cycles.glossy_bounces = 0
                    bpy.context.scene.cycles.transmission_bounces = 0
                    bpy.context.scene.cycles.transparent_max_bounces = 0

                    bpy.context.scene.view_settings.view_transform = 'Standard'

                # High-quality render settings
                else:
                    engine = "cycles"
                    if engine == "eevee":
                        bpy.context.scene.render.engine = 'BLENDER_EEVEE'
                        # Settings for Eevee high-sample render
                        bpy.context.scene.eevee.taa_render_samples = 64  # Set render samples to 64
                        bpy.context.scene.eevee.taa_samples = 16  # Set viewport samples to 16
                        bpy.context.scene.eevee.use_ssr = True  # Enable Screen Space Reflections
                        bpy.context.scene.eevee.use_bloom = True  # Enable Bloom
                        bpy.context.scene.eevee.use_gtao = True  # Enable Ambient Occlusion
                        bpy.context.scene.eevee.use_soft_shadows = True  # Enable Soft Shadows

                    elif engine == "cycles":
                        bpy.context.scene.render.engine = 'CYCLES'
                        bpy.context.scene.cycles.device = 'GPU'
                        # Settings for Cycles high-sample render
                        bpy.context.scene.cycles.samples = 128  # Set render samples to 128 (or any desired high quality)
                        bpy.context.scene.cycles.preview_samples = 64  # Set viewport samples to 64
                        bpy.context.scene.cycles.pixel_filter_type = 'GAUSSIAN'
                        bpy.context.scene.cycles.filter_width = 1.5
                        bpy.context.scene.cycles.max_bounces = 12  # Set high bounces for more realistic lighting
                        bpy.context.scene.cycles.diffuse_bounces = 4
                        bpy.context.scene.cycles.glossy_bounces = 4
                        bpy.context.scene.cycles.transmission_bounces = 12
                        bpy.context.scene.cycles.transparent_max_bounces = 8

                    bpy.context.scene.view_settings.view_transform = 'Filmic'


                # Settings for unlabeled (realistic) images
                # pass
                # bpy.context.scene.render.engine = 'CYCLES'  # Or 'BLENDER_EEVEE'
                # bpy.context.scene.world.use_nodes = True  # Enable environmental lighting for realism
                # camera = bpy.data.objects['Camera']

                # # Set clipping parameters
                # camera.data.clip_start = 0.1  # Near clipping plane
                # camera.data.clip_end = 1000.0  # Far clipping plane

            if props.snap_image:
                #If label is False, set active materia for all tree objects to the first one
                for obj in bpy.data.objects:
                    if "sun" in obj.name:
                        bpy.data.objects.remove(obj, do_unlink=True)

                    try: #TODO: Fix this
                        bpy.context.view_layer.objects.active = obj
                        bpy.ops.object.mode_set(mode='OBJECT')
                        obj.data.materials.clear()
                    except:
                        continue

                    if "tree" in obj.name:
                        # Make the object active and ensure it's in Object mode

                        if label:
                            # Determine which material to assign based on the label
                            #Split obj name by _
                            obj_root, obj_label = obj.name.split("_")
                            material_name = "mat_labelled_tree" if obj_root==selected_tree_root else "mat_labelled_black"
                            # print(obj.name, material_name)
                            material = bpy.data.materials.get(material_name)
                        else:
                            material = random.choice(mat_tex)
                        # obj.data.materials.append(material)
                    elif "ground" in obj.name:
                        material_name = "mat_labelled_ground" if label else "mat_ground"
                        if label:
                            material = bpy.data.materials.get("mat_labelled_ground")
                        else:
                            material = random.choice(mat_ground)

                    elif "post" in obj.name:
                        post_idx = int(obj.name[4:])
                        if label:
                            if post_idx == selected_tree_idx*2 or post_idx == selected_tree_idx*2 + 1:
                                material_name = "mat_labelled_post"
                            else:
                                material_name = "mat_labelled_orange"
                        else:
                            material_name = "mat_post"
                        material = bpy.data.materials.get(material_name)
                    elif "wire" in obj.name:
                        trellis_idx = int(obj.name[4:5])
                        if label:
                            if trellis_idx == selected_tree_idx // 4: #nx
                                material_name = "mat_labelled_wire"
                            else:
                                material_name = "mat_labelled_cyan"
                        else:
                            material_name = "mat_wire"
                        material = bpy.data.materials.get(material_name)
                    else:
                        continue

                    # Ensure the material exists
                    if material is None:
                        raise ValueError(f"Material not found {material_name}")

                    # Assign the material to the first material slot, or add it if no slots exist
                    if obj.data.materials:
                        obj.data.materials[0] = material
                    else:
                        obj.data.materials.append(material)


                    # Print confirmation of the material assignment
                    print(f"Assigned material '{obj.data.materials[0].name}' to '{obj.name}'")
                    # Force a viewport update to ensure the material change is reflected
                    load_scene()


                if label:
                    create_sky_color()
                else:
                    create_sky_texture()
                    create_sun(random.choice(sun_or))

                # taking pairs of images
                if props.image_pairs:
                    cam_obj.location = (camera_x, camera_y, camera_z)
                    file_output = setup_composite_nodes(props, label=label)

                    # bpy.context.scene.render.filepath = f"{props.image_dir_path}tree_{i:04d}_pair_1_{str(label)}.png"
                    label_type = "labeled" if label else "unlabeled"
                    base_filename = f"tree_{i:04d}__pair_1_{label_type}"

                    rgb_filename = f"{base_filename}_rgb_"
                    depth_filename = f"{base_filename}_depth_"

                    file_output.file_slots['rgb'].path = rgb_filename
                    if not label:
                        file_output.file_slots['depth'].path = depth_filename
               
                    bpy.ops.render.render(write_still=True)

                    # Re-setup for second set of photos
                    file_output = setup_composite_nodes(props, label=label)
                    base_filename = f"tree_{i:04d}__pair_2_{label_type}"

                    rgb_filename = f"{base_filename}_rgb_"
                    depth_filename = f"{base_filename}_depth_"

                    file_output.file_slots['rgb'].path = rgb_filename
                    if not label:
                        file_output.file_slots['depth'].path = depth_filename
                    cam_obj.location = (camera_x + slight_variation, camera_y + slight_variation, camera_z + slight_variation)
                    
                    bpy.ops.render.render(write_still=True)
                    continue

            # Render the image and save it. Change the formatting to suit your needs

            if not props.image_pairs:
                file_output = setup_composite_nodes(props, label=label)
                label_type = "labeled" if label else "unlabeled"
                base_filename = f"tree_{i:04d}_{label_type}"

                rgb_filename = f"{base_filename}_rgb_"
                depth_filename = f"{base_filename}_depth_"

                file_output.file_slots['rgb'].path = rgb_filename
                if not label:
                    file_output.file_slots['depth'].path = depth_filename
               
                # bpy.context.scene.render.filepath = f"{props.image_dir_path}image_{i:04d}_{str(label)}.png"

                bpy.ops.render.render(write_still=True)


def take_video(self, context):
    """Animate the camera along a path and render a video"""
    props = context.scene.my_tool
    cam_obj = bpy.data.objects.get("Camera")
    if cam_obj is None:
        return

    # Remove any existing parent or follow path constraints
    cam_obj.parent = None
    for con in cam_obj.constraints:
        if con.type == 'FOLLOW_PATH':
            cam_obj.constraints.remove(con)

    # Remove existing path if present
    if "campath" in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects["campath"], do_unlink=True)

    # Recreate the path and attach the camera
    create_sine(numCycles=7, stepsPerCycle=8, zscale=0.7, curvelen=10, offset=props.cam_offset)
    curve = bpy.context.scene.objects["campath"]
    curve.data.animation_data_clear()
    cam_obj.animation_data_clear()

    make_camera_follow_curve(cam_obj, curve)

    constraint = None
    for con in cam_obj.constraints:
        if con.type == 'FOLLOW_PATH':
            constraint = con
            break
    if constraint is None:
        constraint = cam_obj.constraints.new('FOLLOW_PATH')
        constraint.target = curve

    constraint.use_fixed_location = True

    constraint.offset_factor = 0.0
    constraint.keyframe_insert(data_path="offset_factor", frame=1)

    constraint.offset_factor = 1.0
    constraint.keyframe_insert(data_path="offset_factor", frame=props.video_frame_count)
        

