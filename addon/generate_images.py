import bpy
import random
import math

def take_image(self, context):
    props = context.scene.my_tool

    focal_length = props.focal_length

    bpy.context.scene.render.pixel_aspect_x = props.aspect_X
    bpy.context.scene.render.pixel_aspect_y = props.aspect_Y

    bpy.context.scene.render.resolution_x = props.resolution_X
    bpy.context.scene.render.resolution_y = props.resolution_Y

    for cam in bpy.data.cameras:
        cam.lens = focal_length

    tree_list = []
    obj_list = list(bpy.data.objects)

    for obj in obj_list:
        if "tree" in obj.name:
            tree_list.append(obj)
        # remove once campath is obsolete
        elif "campath" in obj.name:
            bpy.data.objects.remove(bpy.data.objects["campath"], do_unlink=True)

    cam_obj = bpy.data.objects["Camera"]
    bpy.context.view_layer.objects.active = cam_obj

    for i in range(props.num_images):
        if props.random_tree:
            selected_tree = random.choice(tree_list)
        else:
            selected_tree = tree_list[0]

        # Get tree dimensions
        tree_dimensions = selected_tree.dimensions
        tree_length = tree_dimensions.x
        tree_height = tree_dimensions.z
        tree_spacing = 2 * math.tan(props.tree_angle[0]) * tree_height

        # Define percentages for offset
        left_right_percentage = props.left_right_offset
        in_out_percentage = props.in_out_offset
        up_down_percentage = props.up_down_offset
        
        offset_x = left_right_percentage * tree_length
        offset_y = in_out_percentage * tree_spacing
        offset_z = up_down_percentage * tree_height

        tree_location = selected_tree.location
        tree_rotation_z = selected_tree.rotation_euler.z

        # Calculate the offset considering the tree's rotation
        camera_x_offset = offset_x * math.cos(tree_rotation_z) - offset_y * math.sin(tree_rotation_z)
        camera_y_offset = offset_x * math.sin(tree_rotation_z) + offset_y * math.cos(tree_rotation_z)

        camera_x = tree_location.x + camera_x_offset
        camera_y = tree_location.y + camera_y_offset
        camera_z = tree_location.z + offset_z

        cam_obj.location = (camera_x, camera_y, camera_z)

        # The default for the camera pitch and roll. Shouldn't be changed unless
        # intentionally needed for variation
        cam_obj.rotation_euler[0] = props.camera_angle[0]
        cam_obj.rotation_euler[1] = props.camera_angle[1]

        # Only change yaw of camera if specified in the panel for some reason
        # Otherwise it messes with the camera orientation
        # Sincec its default is specified as 0 in the properties
        if props.camera_angle[2] != 0: # if not defualt
            cam_obj.rotation_euler[2] = props.camera_angle[2]
            # Offset camera's z rotation by pi if offset_y is negative
            if offset_y < 0:
                cam_obj.rotation_euler[2] = props.camera_angle[2] + math.pi  
        else:
            cam_obj.rotation_euler[2] = tree_rotation_z
            if offset_y < 0: 
                cam_obj.rotation_euler[2] = tree_rotation_z + math.pi
            
        if props.take_image:
            # Render the image and save it
            bpy.context.scene.render.filepath = f"{props.image_dir_path}image_{i:04d}.png"
            bpy.ops.render.render(write_still=True)

        

