import bpy
from .builders import *
from .helpers import *
import numpy as np
import mathutils
import random
import re

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

    loc_x_noise = np.random.normal(0.2, 0.2, (nx,1))
    loc_y_noise = np.random.normal(0.2, 0.2, (ny,1))

    wire_spacing = props.wire_spacing

    focal_length = props.focal_length

    bpy.context.scene.render.pixel_aspect_x = props.aspect_X
    bpy.context.scene.render.pixel_aspect_y = props.aspect_Y

    bpy.context.scene.render.resolution_x = props.resolution_X
    bpy.context.scene.render.resolution_y = props.resolution_Y



    for offset in camera_offsets:
        for tex_path in texture_paths:
            for sun_or_value in sun_or:
                for noise_var_value in noise_var:
                    
                    clean_blender_data()

                    num_posts = 0
                    
                    cam = bpy.data.cameras.new("Camera")
                    cam_obj = bpy.data.objects.new("Camera", cam)

                    for cam in bpy.data.cameras:
                        cam.lens = focal_length

                    # Render camera checkbox
                    if props.render_cam:
                        # Create camera path
                        create_sine(numCycles = 7, stepsPerCycle = 8, zscale=0.7,curvelen=10, offset = offset, noise_var = (0,noise_var_value,0))
                        curve = bpy.context.scene.objects["campath"]
                        # Create camera
                        make_camera_follow_curve(cam, cam_obj, curve)
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
                                type = "emission"
                                create_sky_color()
                            else:
                                type = "diffuse"
                                create_sky_texture()
                                create_sun(sun_or_value)
                        # Render trees checkbox
                        if props.render_trees:
                            # returns a regex to find given string 
                            envy_reg = re.compile(r'envy', re.IGNORECASE)
                            ufo_reg = re.compile(r'ufo', re.IGNORECASE)
                            # returns true if the pattern is found in path 
                            is_type_envy = envy_reg.search(tree_file_path)
                            is_type_ufo = ufo_reg.search(tree_file_path)
                            if is_type_envy:
                                a = np.linspace(-7.5, 2.5, nx)  
                                b = np.linspace(-5, 5, ny)
                            elif is_type_ufo:
                                a = np.linspace(-7.5, 2.5, nx) 
                                b = np.linspace(-10, 1, ny)
                                
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
                                            create_new_material_with_rgb_colors(num_trees, obj, (0, 0, 0, 0), type)
                                        else:
                                            create_new_material_with_vertex_colors(num_trees, obj, type)
                                    else:
                                        create_new_material_with_texture_bark('texture', obj, tex_path, 'bark_willow')
                                
                                num+=1
                                num_trees+=1
                        # Render ground checkbox
                        if props.render_plane:
                            new_plane((0,0,0), 1000, 'ground')
                            plane = bpy.data.objects['ground']
                        
                        if props.render_ground_material:
                            mat_name = 'ground_color'
                            if label:
                                create_new_material_with_rgb_colors(mat_name, plane, (0.6,0.2,0.,1), type)
                            else:
                                create_new_material_with_texture(mat_name, plane, texture_path+'\\dirt_floor\\', 'dirt_floor')

                        bpy.ops.object.select_all(action='DESELECT')

                # This line should run right after a complete render is done
                # Cleans up unused data blocks to avoid memory leak
                bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

                        # bpy.context.scene.camera = cam_obj

    #                     if label:
    #                         bpy.context.scene.render.filepath = 'C:/Users/abhin/PycharmProjects/blender/noiseconcat{}{}{}{}/labelled'.format(noise_var_value, sun_or_value, os.path.split(tex_path)[-1], offset)
    #                     else:
    #                         bpy.context.scene.render.filepath = 'C:/Users/abhin/PycharmProjects/blender/noiseconcat{}{}{}{}/unlabelled'.format(noise_var_value, sun_or_value, os.path.split(tex_path)[-1], offset)
    #                     bpy.context.scene.render.resolution_x = 1024 #perhaps set resolution in code
    #                     bpy.context.scene.render.resolution_y = 1024
    #                     curve.data.path_duration = 5000
    #                     bpy.ops.render.render(animation = True, write_still = False)
    #                    break
    #                break
    #            break
    #        break
    #    break

def render_polygon(self, context):
    props = context.scene.my_tool
    sides = props.pgon_sides     
    radius = props.pgon_radius
    rotation = props.pgon_rotation
    translation = [
        props.pgon_translation[0],
        props.pgon_translation[1],
        0.0,
        ]
    
    for obj in list(bpy.data.objects):
        if obj.name == "Polygon":
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.delete()
            break

    create_polygon(polygon(sides, radius, rotation, translation))