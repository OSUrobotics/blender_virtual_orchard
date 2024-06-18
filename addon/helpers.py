import bpy
import glob
import numpy as np
import mathutils
import math
from typing import List

def add_cylinder(
        size: float = 1.0,
        location: List[float] = [0.0, 0.0, 0.0],
        rotation: List[float] = [0.0, 0.0, 0.0],
        scale: List[float] = [1.0, 1.0, 1.0]) -> None:
    bpy.ops.mesh.primitive_cylinder_add(
        
        calc_uvs=True,
        enter_editmode=False,
        align='WORLD',
        location=location,
        rotation=rotation,
        scale=scale,
    )

def create_post(num_posts, loc = [0,0,0], label = True, render_with_material: bool = True):
    post_dia_m = 0.07
    post_scale = (post_dia_m/2,post_dia_m/2,5/2)
    post_rotation = [0,0,0]
    add_cylinder(scale=post_scale, location = loc, rotation = post_rotation)
    name = 'post{}'.format(num_posts)
    bpy.context.active_object.name = name
    obj = bpy.data.objects[name]

    if render_with_material:
        if label:
            create_new_material_with_rgb_colors("post_mat",obj, (0,0,1, 1), "emission" )
        else:
            create_new_material_with_rgb_colors("post_mat",obj, (133/255 ,87/255, 35/255, 0.5), "diffuse" )
            
        
    
def create_wire(wire_count, loc = [0,0,0], label = False, render_with_material: bool = True):
    wire_dia_m = 0.004
    wire_scale = (wire_dia_m/2,wire_dia_m/2,10)
    wire_rotation = [0,np.pi/2,0]
    add_cylinder(scale=wire_scale, location = loc, rotation = wire_rotation)
    bpy.context.active_object.name = 'wire'
    name = 'wire{}'.format(wire_count)
    bpy.context.active_object.name = name
    obj = bpy.data.objects[name]

    if render_with_material:
        if label:
            create_new_material_with_rgb_colors("wire_mat",obj, (1,0,1, 1), "emission" )
        else:
            create_new_material_with_rgb_colors("wire_mat",obj, (192/255 ,192/255, 192/255, 0.5), "diffuse" )
        
    
def create_trellis_wires(wire_ground_offset, wire_spacing, num_wires, loc, label = False, render_with_material: bool = True):
    for i in range(num_wires):
        create_wire(i, [loc[0],loc[1],wire_ground_offset + i*wire_spacing], label, render_with_material)


def create_sine(numCycles = 1, stepsPerCycle = 16, curvelen=2, zscale=1.5, offset = (0,0,0), noise_var = (0,0,0)):

    curve = bpy.data.curves.new('path', type='CURVE')
    curve.dimensions = '2D'
    curve.resolution_u = 1
    spline = curve.splines.new('NURBS')
    
    #cursor = bpy.context.scene.cursor_location
    xscale = float(curvelen)/stepsPerCycle/numCycles
    
    for x in range(0, stepsPerCycle * numCycles+1):
        noise = np.random.normal(loc=0.0, scale=noise_var, size=3)
        z = math.sin(float(x) / stepsPerCycle * math.pi*2) 

        #Add first point for start of Nurbs (needs extra point)
        if x == 0:
            spline.points[0].co = (x*xscale+offset[0]+noise[0], 0+offset[1]+noise[1], z*zscale+offset[2]+noise[2],1) 

        # Add point
        spline.points.add(1)
        spline.points[-1].co = ((x*xscale+offset[0]+noise[0], 0+offset[1]+noise[1], z*zscale+offset[2]+noise[2],1))
    # Add end point
    spline.points.add(1)
    spline.points[-1].co =(x*xscale+offset[0]+noise[0], 0+offset[1]+noise[1], z*zscale+offset[2]+noise[2],1)
    curveObject = bpy.data.objects.new('campath', curve)
    bpy.context.scene.collection.objects.link(curveObject)

def new_plane(mylocation, mysize, myname):
    bpy.ops.mesh.primitive_plane_add(
        size=mysize,
        align='WORLD',
        location=mylocation,
        rotation=(0,0,0),
        scale=(5,5,5))
    current_name = bpy.context.selected_objects[0].name
    plane = bpy.data.objects[current_name]
    plane.name = myname
    plane.data.name = myname + "_mesh"
    return

def create_new_material_with_vertex_colors(name, obj, type):
    materials = bpy.data.materials
    mat_name = 'mat_{}'.format(name)
    material = materials.get( mat_name )
    if material:
        bpy.data.materials.remove(material)
   
    material = materials.new( mat_name )
    
    # We clear it as we'll define it completely
    material.use_nodes = True
    clear_material( material )
    
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    output = nodes.new( type = 'ShaderNodeOutputMaterial' )
    input = nodes.new( type = 'ShaderNodeVertexColor')
    if type == "diffuse":
        diffuse = nodes.new( type = 'ShaderNodeBsdfPrincipled' )
        links.new( input.outputs['Color'], diffuse.inputs['Base Color'])
        links.new( diffuse.outputs['BSDF'], output.inputs['Surface'] )
    elif type == "emission":
        diffuse = nodes.new( type = 'ShaderNodeEmission' )
        diffuse.inputs['Strength'].default_value= 10
        links.new( input.outputs['Color'], diffuse.inputs['Color'])
        links.new( diffuse.outputs['Emission'], output.inputs['Surface'] )
    
    if obj.data.materials:
        # assign to 1st material slot
        obj.data.materials[0] = material
    else:
        # no slots
        obj.data.materials.append(material)
        
def create_new_material_with_rgb_colors(name, obj, color, type):
    materials = bpy.data.materials
    mat_name = 'mat_{}'.format(name)
    material = materials.get( mat_name )

    if not material:
        material = materials.new( mat_name )

    # We clear it as we'll define it completely
    clear_material( material )
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    output = nodes.new( type = 'ShaderNodeOutputMaterial' )
    input = nodes.new( type = 'ShaderNodeRGB')
    input.outputs['Color'].default_value = mathutils.Vector(color)
    if type == "diffuse":
        diffuse = nodes.new( type = 'ShaderNodeBsdfPrincipled' )
        links.new( input.outputs['Color'], diffuse.inputs['Base Color'])
        links.new( diffuse.outputs['BSDF'], output.inputs['Surface'] )
    elif type == "emission":
        diffuse = nodes.new( type = 'ShaderNodeEmission' )
        diffuse.inputs['Strength'].default_value= 10
        links.new( input.outputs['Color'], diffuse.inputs['Color'])
        links.new( diffuse.outputs['Emission'], output.inputs['Surface'] )
    
    if obj.data.materials:
        # assign to 1st material slot
        obj.data.materials[0] = material
    else:
        # no slots
        obj.data.materials.append(material)
        
def create_new_material_with_texture_bark(name, obj, texture_path, texture_name):
    materials = bpy.data.materials
    mat_name = 'mat_{}'.format(name)
    
    material = materials.get(mat_name)
    
    
    if not material:
        material = materials.new( mat_name )

    # We clear it as we'll define it completely
    clear_material( material )
    
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
#        clear_material( material )
    diffuse = nodes.new( type = 'ShaderNodeBsdfPrincipled' )
    output = nodes.new( type = 'ShaderNodeOutputMaterial' )
    input = nodes.new( type = 'ShaderNodeTexCoord')
    mapping = nodes.new( type = 'ShaderNodeMapping')
    mapping.inputs[3].default_value[0] = 2

    links.new(input.outputs['UV'], mapping.inputs['Vector'])
    
    texture_a = nodes.new( type = 'ShaderNodeTexImage')
    texture_b = nodes.new( type = 'ShaderNodeTexImage')
    texture_c = nodes.new( type = 'ShaderNodeTexImage')
    texture_d = nodes.new( type = 'ShaderNodeTexImage')
    print(texture_path)
    diff_tex = glob.glob(texture_path+'/*diff*')[0]
    disp_tex = glob.glob(texture_path+'/*disp*')[0]
    gl_tex = glob.glob(texture_path+'/*gl*')[0]
    rough_tex = glob.glob(texture_path+'/*rough*')[0]
    texture_a.image = bpy.data.images.load(diff_tex)
#        texture_a.image.colorspace_settings.name = 'Non-Color'
    texture_b.image = bpy.data.images.load(disp_tex)
#        texture_b.image.colorspace_settings.name = 'Non-Color'
    texture_c.image = bpy.data.images.load(gl_tex)
    texture_d.image = bpy.data.images.load(rough_tex)
#        texture_d.image.colorspace_settings.name = 'Non-Color'
    links.new( mapping.outputs['Vector'], texture_a.inputs['Vector'])
    links.new( mapping.outputs['Vector'], texture_b.inputs['Vector'])
    links.new( mapping.outputs['Vector'], texture_c.inputs['Vector'])
    links.new( mapping.outputs['Vector'], texture_d.inputs['Vector'])
    normal_map = nodes.new( type = 'ShaderNodeNormalMap')
    normal_map.inputs[0].default_value = 0.1

    displacement = nodes.new( type = 'ShaderNodeDisplacement')
    
    links.new( texture_c.outputs['Color'], normal_map.inputs['Color'])
    links.new( texture_b.outputs['Color'], displacement.inputs['Height'])
   
#       
#       
    links.new( diffuse.inputs['Base Color'], texture_a.outputs['Color'])
    links.new( diffuse.inputs['Roughness'], texture_d.outputs['Color'])
    links.new( diffuse.inputs['Normal'], normal_map.outputs['Normal'])
   
    links.new( diffuse.outputs['BSDF'], output.inputs['Surface'] )
    links.new( displacement.outputs['Displacement'], output.inputs['Displacement'] ) 
    
        
    if obj.data.materials:
        # assign to 1st material slot
        obj.data.materials[0] = material
    else:
        # no slots
        obj.data.materials.append(material)
    
def create_new_material_with_texture(name, obj, texture_path, texture_name):
    materials = bpy.data.materials
    mat_name = 'mat_{}'.format(name)
    
    material = materials.get(mat_name)
    
    
    if not material:
        material = materials.new( mat_name )

    # We clear it as we'll define it completely
    clear_material( material )
    
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
#        clear_material( material )
    diffuse = nodes.new( type = 'ShaderNodeBsdfPrincipled' )
    output = nodes.new( type = 'ShaderNodeOutputMaterial' )
    input = nodes.new( type = 'ShaderNodeTexCoord')
    mapping = nodes.new( type = 'ShaderNodeMapping')
    mapping.inputs[3].default_value[0] = 2

    links.new(input.outputs['UV'], mapping.inputs['Vector'])
    
    texture_a = nodes.new( type = 'ShaderNodeTexImage')
    texture_b = nodes.new( type = 'ShaderNodeTexImage')
    texture_c = nodes.new( type = 'ShaderNodeTexImage')
    texture_d = nodes.new( type = 'ShaderNodeTexImage')
   
    texture_a.image = bpy.data.images.load(texture_path+texture_name+'_diff_4k.jpg')
#        texture_a.image.colorspace_settings.name = 'Non-Color'
    texture_b.image = bpy.data.images.load(texture_path+texture_name+'_disp_4k.png')
#        texture_b.image.colorspace_settings.name = 'Non-Color'
    texture_c.image = bpy.data.images.load(texture_path+texture_name+'_nor_gl_4k.exr')
    texture_d.image = bpy.data.images.load(texture_path+texture_name+'_rough_4k.exr')
#        texture_d.image.colorspace_settings.name = 'Non-Color'
    links.new( mapping.outputs['Vector'], texture_a.inputs['Vector'])
    links.new( mapping.outputs['Vector'], texture_b.inputs['Vector'])
    links.new( mapping.outputs['Vector'], texture_c.inputs['Vector'])
    links.new( mapping.outputs['Vector'], texture_d.inputs['Vector'])
    normal_map = nodes.new( type = 'ShaderNodeNormalMap')
    normal_map.inputs[0].default_value = 0.1

    displacement = nodes.new( type = 'ShaderNodeDisplacement')

    links.new( texture_c.outputs['Color'], normal_map.inputs['Color'])
    links.new( texture_b.outputs['Color'], displacement.inputs['Height'])
        
    links.new( diffuse.inputs['Base Color'], texture_a.outputs['Color'])
    links.new( diffuse.inputs['Roughness'], texture_d.outputs['Color'])
    links.new( diffuse.inputs['Normal'], normal_map.outputs['Normal'])
   
    links.new( diffuse.outputs['BSDF'], output.inputs['Surface'] )
    links.new( displacement.outputs['Displacement'], output.inputs['Displacement'] ) 

        
    if obj.data.materials:
        # assign to 1st material slot
        obj.data.materials[0] = material
    else:
        # no slots
        obj.data.materials.append(material)
    
def make_camera_follow_curve(cam, cam_obj, curve):
    
    # create the first camera object
    cam_obj.location = (0,0,0)
    cam_obj.rotation_euler = mathutils.Euler((np.pi/2,0,-np.pi/2), 'XYZ')
   
    bpy.context.scene.collection.objects.link(cam_obj)
    
    cam_obj.select_set(True)
    bpy.context.view_layer.objects.active = curve
    bpy.ops.object.parent_set(type='FOLLOW')
    bpy.context.object.track_axis = 'NEG_Y'
    constraint = cam_obj.constraints.new("LIMIT_ROTATION")
    constraint.use_limit_x = True
    constraint.use_limit_y = True
    constraint.use_limit_z = True
    constraint.max_x = 1.5707
    constraint.min_x = 1.5707
    constraint.max_z = -3.14
    constraint.min_z = -3.14
    constraint.max_y = 0
    constraint.min_y = 0

    
# Clear all nodes in a mat
def clear_material( material ):
    material.use_nodes = True
    if material.node_tree:
        material.node_tree.links.clear()
        material.node_tree.nodes.clear()
#        for i in material.node_tree:
#            print(i)
#            i.node_tree.nodes.remove( node_to_delete )

# Create a node corresponding to a defined group
def instanciate_group( nodes, group_name ):
    group = nodes.new( type = 'ShaderNodeGroup' )
    group.node_tree = bpy.data.node_groups[group_name]
    
def create_sun(orient):
    # Create light datablock
    light_data = bpy.data.lights.new(name="sun-data", type='SUN')
    light_data.energy =1
    # Create new object, pass the light data 
    light_object = bpy.data.objects.new(name="sun", object_data=light_data)

    # Link object to collection in context
    bpy.context.collection.objects.link(light_object)

    # Change light position
    light_object.location = (0, 0, 100)
    light_object.rotation_euler = mathutils.Euler((orient), 'XYZ')

def create_sky_texture():
    bpy.data.worlds['World'].use_nodes = True
    sky_texture = bpy.context.scene.world.node_tree.nodes.new("ShaderNodeTexSky")
    bg = bpy.data.worlds['World'].node_tree.nodes['Background']
    bpy.context.scene.world.node_tree.links.new(bg.inputs["Color"], sky_texture.outputs["Color"])
    sky_texture.sky_type = 'HOSEK_WILKIE' # or 'PREETHAM'
    sky_texture.turbidity = 2.0
    sky_texture.ground_albedo = 0.4

    
def create_sky_color():
    bpy.data.worlds['World'].use_nodes = True
    bg = bpy.data.worlds['World'].node_tree.nodes['Background']
    try:
        l = bg.inputs["Color"].links[0]
        bpy.data.worlds['World'].node_tree.links.remove(l)
    except:
        pass
    
def clean_blender_data():
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)

    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

    for block in bpy.data.textures:
        if block.users == 0:
            bpy.data.textures.remove(block)

    for block in bpy.data.images:
        if block.users == 0:
            bpy.data.images.remove(block)
    
    for m in bpy.data.materials:
        bpy.data.materials.remove(m)
            
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    
def load_trees_from_folder(folder_path, num):
    num_trees = 0

    for files in glob.glob("{}/*.x3d".format(folder_path)):
        bpy.ops.import_scene.x3d(filepath=files)
        bpy.context.selected_objects[0].name = 'tree'
        num_trees+=1
        if num_trees == num:
            return

def fibonacci_hemisphere(samples):

    points = []
    phi = math.pi * (math.sqrt(5.) - 1.)  # golden angle in radians
    print(phi)

    if samples == 1:
        points.append((0,0,0))
    else:
        for i in range(samples):
            y = 1 - (i / float(samples - 1))  # y goes from 1 to 0
            radius = math.sqrt(1 - y * y)  # radius at y

            theta = phi * i  # golden angle increment

            x = math.cos(theta) * radius
            z = math.sin(theta) * radius

            pitch = math.acos(z)  
            yaw = math.atan2(y, x)  
            roll = 0  
            points.append((pitch, yaw, roll))
            # print(pitch, yaw)

    return points