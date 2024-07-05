import bpy
from .builders import *
from .helpers import *
from .generate_images import *
import numpy as np
import mathutils
import random
import json
import os

def render(self, context):
    # All the custom properties are accessed through this variable
    props = context.scene.my_tool

    tree_file_path = props.tree_file_path
    
    texture_path = props.texture_path

    # texture_paths = list(glob.glob(texture_path+'/bark*'))
    texture_paths = ["C:\\Users\\Utsav Bhandari\\Documents\\blenderStuff\\virtual_orchard\\textures\\bark_brown"]

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

    loc_x_noise = np.random.normal(0.1, 0.1, (nx,1))
    loc_y_noise = np.random.normal(0.1, 0.1, (ny,1))

    wire_spacing = props.wire_spacing

    parameters_file_name = "parameters.json" 
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, parameters_file_name)
    
    with open(file_path, "r") as f:
        data = json.load(f)
        pgon_coords = [tuple(coord) for coord in data["polygon_coordinates"]]
        envy_coords = [tuple(coord) for coord in data["envy_grid_square_coordinates"]]
        ufo_coords = [tuple(coord) for coord in data["ufo_grid_square_coordinates"]]

    for offset in camera_offsets:
        for tex_path in texture_paths:
            for sun_or_value in sun_or:
                for noise_var_value in noise_var:
                    
                    clean_blender_data()

                    num_posts = 0
                    
                    # create the first camera object
                    cam = bpy.data.cameras.new("Camera")
                    cam_obj = bpy.data.objects.new("Camera", cam)
                    bpy.context.scene.camera = cam_obj
                    bpy.context.scene.collection.objects.link(cam_obj)

                    # Render camera checkbox
                    if props.render_cam:
                        # Create camera path
                        create_sine(numCycles = 7, stepsPerCycle = 8, zscale=0.7,curvelen=10, offset = offset, noise_var = (0,noise_var_value,0))
                        curve = bpy.context.scene.objects["campath"]
                        # Create camera
                        make_camera_follow_curve(cam_obj, curve)
                    # Render trees checkbox
                    if props.render_trees:
                        load_trees_from_folder(tree_file_path, nx*ny*2)
                    
                    #Set np seed
                    random.seed()
                    
                    obj_list = list(bpy.data.objects)
                    random.shuffle(obj_list)
                    tree_list = []

                    for label in [False]:
                        # Render sky/sun checkbox
                        if props.render_sky_and_sun:
                            if label:
                                mat_type = "emission"
                                create_sky_color()
                            else:
                                mat_type = "diffuse"
                                create_sky_texture()
                                create_sun(sun_or_value)
                        # Render trees checkbox
                        if props.render_trees:

                            is_type_envy = "envy" in tree_file_path
                            is_type_ufo = "ufo" in tree_file_path

                            if props.polygon_clipping:
                                bounding_box, (min_x, max_x, min_y, max_y) = bounding_box_coords(pgon_coords)
                            elif is_type_envy:
                                bounding_box, (min_x, max_x, min_y, max_y) = bounding_box_coords(envy_coords)
                            elif is_type_ufo:
                                bounding_box, (min_x, max_x, min_y, max_y) = bounding_box_coords(ufo_coords)

                            a = np.linspace(min_x, max_x, nx)
                            b = np.linspace(min_y, max_y, ny)
                            xa, xb = np.meshgrid(a, b) 

                        # Render wires checkbox
                        if props.render_wires:
                            create_trellis_wires(0.3 , wire_spacing, 7, loc = (0, 1), label = label, render_with_material = props.render_wire_material)
                        # Render trees checkbox
                        if props.render_trees:
                            coordinate_grid = np.array([xa, xb]).reshape(2,-1)
                            
                            num = 0
                            num_trees = 0
                            orientation = (-tree_or[0], 0, 0)
                            
                            for obj in obj_list:
                                if "tree" in obj.name:
                                    tree_list.append(obj)
                            
                            for _, obj in enumerate(tree_list):
                                if num_trees == nx*ny*2:
                                    break
                                if num_trees == nx*ny:
                                    num = 0
                                    orientation = tree_or
                                x,y = (coordinate_grid[0, num], coordinate_grid[1,num])
                                
                                # Render posts checkbox
                                if props.render_posts:
                                    #post distance from tree variable
                                    create_post(num_posts, loc = (x,y,1), label = label, render_with_material = props.render_post_material)
                                    num_posts += 1

                                obj.location = mathutils.Vector((x+loc_x_noise[num%nx], y+loc_y_noise[num%ny], 0))
                                obj.rotation_euler = mathutils.Euler((orientation), 'XYZ')
                                
                                
                                if props.render_tree_material:
                                    if label:
                                        if y != coordinate_grid[1,-1] or orientation[0] == tree_or[0]:
                                            create_new_material_with_rgb_colors(num_trees, obj, (0, 0, 0, 0), mat_type)
                                        else:
                                            create_new_material_with_vertex_colors(num_trees, obj, mat_type)
                                    else:
                                        create_new_material_with_texture_bark('texture', obj, tex_path, 'bark_willow')
                                
                                num+=1
                                num_trees+=1
                        
                        if props.polygon_clipping:

                            if props.render_polygons:
                                create_polygon(bounding_box)
                                create_polygon(pgon_coords)

                            bpy.context.view_layer.update()
                            for obj in list(bpy.data.objects):
                                # remove this if line when done  
                                if "Polygon" not in obj.name:
                                    # Calculate the rotation matrix around the global Z axis
                                    rotation_matrix = mathutils.Matrix.Rotation(props.orchard_yaw, 4, 'Z') 
                                    # Apply the rotation matrix to the object's world matrix
                                    obj.matrix_world = rotation_matrix @ obj.matrix_world

                                # if "tree" or "post" in obj.name:
                                #     tree_loc = obj.location
                                #     if not is_point_in_polygon((tree_loc[0], tree_loc[1]), [(x, y) for (x, y, z) in pgon_coords]):
                                #         bpy.data.objects.remove(bpy.data.objects[obj.name], do_unlink=True)

                        # Render ground checkbox
                        if props.render_plane:
                            new_plane((0,0,0), 1000, 'ground')
                            plane = bpy.data.objects['ground']
     
                        if props.render_ground_material:
                            mat_name = 'ground_color'
                            if label:
                                create_new_material_with_rgb_colors(mat_name, plane, (0.6,0.2,0.,1), mat_type)
                            else:
                                create_new_material_with_texture(mat_name, plane, texture_path+'\\dirt_floor\\', 'dirt_floor')

                    bpy.ops.object.select_all(action="DESELECT")

                if props.take_image:
                    # remove this line once campath is obsolete
                    cam_obj.constraints.clear()
                    take_image(self, context)

                # This line should run right after a complete render is done
                # Cleans up unused data blocks to avoid memory leak and duplicate names 
                bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)