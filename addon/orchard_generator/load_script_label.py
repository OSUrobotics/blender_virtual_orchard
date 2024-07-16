import bpy
from .builders import *
from .helpers import *
from .generate_images import *
import numpy as np
import mathutils
import random
import json
import os
import datetime

def render(self, context):
    # All the custom properties are accessed through this variable
    props = context.scene.my_tool

    if props.load_props_from_json:
        properties_files_path = os.path.join(props.json_files_path, "gui_parameters.json")
        load_properties_from_json(props, properties_files_path)

    texture_path = props.texture_path
    
    tree_file_path = props.tree_file_path

    is_type_envy = "envy" in tree_file_path
    is_type_ufo = "ufo" in tree_file_path

    # Angle of tree
    tree_or = (
        props.tree_angle[0],
        props.tree_angle[1],
        props.tree_angle[2],
    )

    # sun_or = [(np.pi/3, 0, 0)] #, (-np.pi/3,0,0)] , (-0.523, 0 , -2.11), (-np.pi/2, 0, 4.38),]
    sun_or = fibonacci_hemisphere(props.num_sun_positions)
    
    noise_var = [0]
    # camera_offsets = [(-3,2.8,1.5)] #, (-3,3.1,1.5)]
    camera_offsets = [(
        props.cam_offset[0],
        props.cam_offset[1],
        props.cam_offset[2]
    )]

    nx, ny = (props.tree_rows, props.tree_columns)

    wire_spacing = props.wire_spacing

    orchard_yaw = props.orchard_yaw
    plane_unevenness = props.plane_unevenness

    parameters_file_name = "other_parameters.json" 
    json_dir = props.json_files_path
    file_path = os.path.join(json_dir, parameters_file_name)

    with open(file_path, "r") as f:
        json_data = json.load(f)
        
        pgon_coords = [tuple(coord) for coord in json_data["polygon_coordinates"]]
        envy_coords = [tuple(coord) for coord in json_data["envy_grid_square_coordinates"]]
        ufo_coords = [tuple(coord) for coord in json_data["ufo_grid_square_coordinates"]]
        
        tree_texture_paths = {texture: os.path.join(texture_path, texture) for texture in json_data["random_tree_texture_file_names"]}
        ground_texture_paths = {texture: os.path.join(texture_path, texture) for texture in json_data["random_ground_texture_file_names"]}

        realistic_tree_texture = json_data["realistic_tree_texture_file_name"]
        realistic_tree_texture_path = os.path.join(texture_path, realistic_tree_texture)

        realistic_ground_texture = json_data["realistic_ground_texture_file_name"]
        realistic_ground_texture_path = os.path.join(texture_path, realistic_ground_texture, realistic_ground_texture)

    for offset in camera_offsets:
        for sun_or_value in sun_or:
            for noise_var_value in noise_var: 
                clean_blender_data()
                
                # create the first camera object
                cam = bpy.data.cameras.new("Camera")
                cam_obj = bpy.data.objects.new("Camera", cam)
                bpy.context.scene.camera = cam_obj
                bpy.context.scene.collection.objects.link(cam_obj)

                # Render camera checkbox
                if props.render_cam:
                    # Create camera path
                    create_sine(numCycles = 7, stepsPerCycle = 8, zscale=0.7, curvelen=10, offset = offset, noise_var = (0,noise_var_value,0))
                    curve = bpy.context.scene.objects["campath"]
                    # Create camera
                    make_camera_follow_curve(cam_obj, curve)
                
                load_trees_from_folder(tree_file_path, nx*ny*2)

                #Set np seed
                random.seed()

                obj_list = list(bpy.data.objects)
                random.shuffle(obj_list)
                tree_list = []

                for label in [False]:
                    for tree in obj_list:
                        if "tree" in tree.name:
                            tree_list.append(tree)

                    if props.polygon_clipping:
                        bounding_box, (min_x, max_x, min_y, max_y) = bounding_box_coords(pgon_coords)
                        if props.render_polygons:
                            create_polygon([(x, y, 0) for (x, y) in bounding_box])
                            create_polygon([(x, y, 0) for (x, y) in pgon_coords])
                    elif is_type_envy:
                        bounding_box, (min_x, max_x, min_y, max_y) = bounding_box_coords(envy_coords)
                    elif is_type_ufo:
                        bounding_box, (min_x, max_x, min_y, max_y) = bounding_box_coords(ufo_coords)

                    a = np.linspace(min_x, max_x, nx)
                    b = np.linspace(min_y, max_y, ny)
                    xa, xb = np.meshgrid(a, b) 

                    coordinate_grid = np.array([xa, xb]).reshape(2,-1)

                    num = 0
                    num_trees = 0
                    num_posts = 0
                    orientation = (-tree_or[0], 0, 0)
                    
                    loc_x_noise = np.random.normal(0, 0.1, (nx,1))
                    loc_y_noise = np.random.normal(0, 0.1, (ny,1))

                    row_x_coords = []
                    row_y_coords = []
                    for idx, tree in enumerate(tree_list):
                        tree_dimensions = tree.dimensions
                        if num_trees == nx * ny:
                            num = 0
                            orientation = tree_or

                        x,y = (coordinate_grid[0, num], coordinate_grid[1, num])
                        
                        tree_x = x + loc_x_noise[num % nx]
                        tree_y = y + loc_y_noise[num % ny]

                        row_x_coords.append(tree_x)
                        row_y_coords.append(tree_y)
                        
                        tree.location = mathutils.Vector((tree_x, tree_y, 0))
                        tree.rotation_euler = mathutils.Euler((orientation), 'XYZ')
                        
                        if label:
                            if y != coordinate_grid[1,-1] or orientation[0] == tree_or[0]:
                                create_new_material_with_rgb_colors(num_trees, tree, (0, 0, 0, 0), mat_type)
                            else:
                                create_new_material_with_vertex_colors(num_trees, tree, mat_type)
                        else:
                            if props.random_textures:
                                texture_name, path = random.choice(list(tree_texture_paths.items()))
                                create_new_material_with_texture_bark('texture', tree, path, texture_name)
                            else:
                                create_new_material_with_texture_bark('texture', tree, realistic_tree_texture_path, realistic_tree_texture)

                        orientation_noise = np.random.normal(0, 0.025, (nx, 1))

                        # Render posts checkbox
                        if props.render_posts:
                            if orientation[0] > 0:
                                post_y = tree_y - (tree_dimensions.y / 2)
                            else:
                                post_y = tree_y + (tree_dimensions.y / 2)

                            if is_type_envy:
                                post_x =  tree_x + (tree_dimensions.x / 2)
                                create_post(num_posts, 
                                            orientation = orientation + orientation_noise[num % nx], 
                                            loc=(post_x + loc_x_noise[num % nx], post_y + loc_y_noise[num % ny], 1), 
                                            label=label)
                                num_posts += 1

                                post_x =  tree_x - (tree_dimensions.x / 2)
                                create_post(num_posts, 
                                            orientation = orientation + orientation_noise[num % nx], 
                                            loc=(post_x + loc_x_noise[num % nx], post_y + loc_y_noise[num % ny], 1), 
                                            label=label)
                                num_posts += 1

                            elif is_type_ufo:
                                post_x = tree_x
                                create_post(num_posts, 
                                            orientation = orientation + orientation_noise[num % nx], 
                                            loc=(post_x + loc_x_noise[num % nx], post_y + loc_y_noise[num % ny], 1), 
                                            label=label)
                                num_posts += 1

                                post_x = tree_x + tree_dimensions.x
                                create_post(num_posts, 
                                            orientation = orientation + orientation_noise[num % nx], 
                                            loc=(post_x + loc_x_noise[num % nx], post_y + loc_y_noise[num % ny], 1), 
                                            label=label)
                                num_posts += 1

                        # Render wires checkbox
                        if props.render_wires:
                            if (idx + 1) % nx == 0:
                                create_trellis_wires(0.3 , wire_spacing, 7, (row_x_coords, row_y_coords), orientation, label = label)
                                row_x_coords = []
                                row_y_coords = []
                        
                        num += 1
                        num_trees += 1

                    # Render sky/sun checkbox
                    if props.render_sky_and_sun:
                        if label:
                            mat_type = "emission"
                            create_sky_color()
                        else:
                            mat_type = "diffuse"
                            create_sky_texture()
                            create_sun(sun_or_value)

                    # Render ground checkbox
                    if props.render_plane:
                        new_plane((0,0,0), 500, 'ground')
                        plane = bpy.data.objects['ground']
                        # bumpy terrain
                        subdivide_plane(plane, 10)
                        subdivide_plane(plane, 10)
                        add_displacement_modifier_with_cloud_texture(plane, plane_unevenness)
                    
                        mat_name = 'ground_color'
                        if label:
                            create_new_material_with_rgb_colors(mat_name, plane, (0.6,0.2,0.,1), mat_type)
                        else:
                            if props.random_textures:
                                texture_name, path = random.choice(list(ground_texture_paths.items()))
                                tex_path = os.path.join(path, texture_name)
                                create_new_material_with_texture(mat_name, plane, tex_path)
                            else: 
                                create_new_material_with_texture(mat_name, plane, realistic_ground_texture_path)

                    if props.polygon_clipping:
                        # This line is crucial here
                        load_scene()
                        for obj in list(bpy.data.objects):
                            # Don't rotate the polygons if visualizing  
                            if "Polygon" not in obj.name:
                                # Calculate the rotation matrix around the global Z axis
                                rotation_matrix = mathutils.Matrix.Rotation(orchard_yaw, 4, 'Z') 
                                # Apply the rotation matrix to the object's world matrix
                                obj.matrix_world = rotation_matrix @ obj.matrix_world

                            if "tree" or "post" or "wire" in obj.name:
                                obj_loc = obj.location
                                # point is not inside polygon
                                if not is_point_in_polygon((obj_loc[0], obj_loc[1]), pgon_coords):
                                    bpy.data.objects.remove(bpy.data.objects[obj.name], do_unlink=True)
                                    load_scene()

                    bpy.ops.object.select_all(action="DESELECT")

                    if props.snap_image:
                        # remove this line if campath becomes obsolete
                        cam_obj.constraints.clear()
                        take_images(self, context)

                    # This line should run right after a complete render is done
                    # Cleans up unused data blocks to avoid memory leak and duplicate names 
                    bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    json_file_path = os.path.join(props.json_files_path, "dumps", f"props_dump_{timestamp}.json") 
    dump_properties_to_json(props, json_file_path)