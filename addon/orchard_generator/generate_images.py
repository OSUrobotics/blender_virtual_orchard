import bpy
import random
import math
from . helpers import load_scene
from .builders import create_sky_color, create_sky_texture, create_sun, fibonacci_hemisphere

sun_or = fibonacci_hemisphere(100)

def setup_composite_nodes(props):
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree

    tree.nodes.clear()
    
    render_layers = tree.nodes.new('CompositorNodeRLayers')

    normalize = tree.nodes.new(type="CompositorNodeNormalize")

    map_range = tree.nodes.new(type="CompositorNodeMapRange")
    
    map_range.inputs['From Min'].default_value = 0
    map_range.inputs['From Max'].default_value = 1
    map_range.inputs['To Min'].default_value = 1
    map_range.inputs['To Max'].default_value = 0

    file_output = tree.nodes.new(type="CompositorNodeOutputFile")
    file_output.format.file_format = 'PNG'
    file_output.base_path = props.image_dir_path
    
    # Remove default slot and create named slots
    file_output.file_slots.clear()
    file_output.file_slots.new('rgb')
    file_output.file_slots.new('depth')

    tree.links.new(render_layers.outputs['Image'], file_output.inputs['rgb'])
    tree.links.new(render_layers.outputs['Depth'], normalize.inputs[0])
    tree.links.new(normalize.outputs[0], map_range.inputs[0])
    tree.links.new(map_range.outputs[0], file_output.inputs['depth'])

    return file_output


def take_images(self, context):
    global sun_or
    props = context.scene.my_tool

    focal_length = props.focal_length

    bpy.context.scene.render.pixel_aspect_x = props.aspect_X
    bpy.context.scene.render.pixel_aspect_y = props.aspect_Y

    bpy.context.scene.render.resolution_x = props.resolution_X
    bpy.context.scene.render.resolution_y = props.resolution_Y
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
        # Slight variation in camera's location for the second image
        slight_variation = random.uniform(-0.1, 0.1)  # Adjust this as needed
        for label in [True, False]:
            print(f"Label: {label}")
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
                            material_name = "mat_labelled_tree" if selected_tree_root in obj.name else "mat_labelled_black"
                            # print(obj.name, material_name)
                            material = bpy.data.materials.get(material_name)
                        else:
                            material = random.choice(mat_tex)
                        obj.data.materials.append(material)
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
                                material_name = "mat_labelled_black"
                        else:
                            material_name = "mat_post"
                        material = bpy.data.materials.get(material_name)
                    elif "wire" in obj.name:
                        trellis_idx = int(obj.name[4:5])
                        if label:
                            if trellis_idx == selected_tree_idx // 4: #nx
                                material_name = "mat_labelled_wire"
                            else:
                                material_name = "mat_labelled_black"
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
                    setup_composite_nodes(props)

                    bpy.context.scene.render.filepath = f"{props.image_dir_path}tree_{i:04d}_pair_1_{str(label)}.png"
                    bpy.ops.render.render(write_still=True)

                    # Re-setup for second set of photos
                    setup_composite_nodes(props)
                    
                    cam_obj.location = (camera_x + slight_variation, camera_y + slight_variation, camera_z + slight_variation)
                    
                    bpy.context.scene.render.filepath = f"{props.image_dir_path}tree_{i:04d}_pair_1_{str(label)}.png"
                    bpy.ops.render.render(write_still=True)
                    continue

            # Render the image and save it. Change the formatting to suit your needs

            if not props.image.pairs:
                file_output = setup_composite_nodes(props)

                bpy.context.scene.render.filepath = f"{props.image_dir_path}image_{i:04d}_{str(label)}.png"

                bpy.ops.render.render(write_still=True)

        

