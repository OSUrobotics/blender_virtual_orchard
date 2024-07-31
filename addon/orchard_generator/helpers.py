import bpy
import mathutils
import json

def create_polygon(points):
    # Create a new mesh
    mesh = bpy.data.meshes.new("PolygonMesh")
    obj = bpy.data.objects.new("Polygon", mesh)

    # Link the object to the current scene
    bpy.context.collection.objects.link(obj)

    # Create the mesh from the points
    mesh.from_pydata(points, [], [[i for i in range(len(points))]])

def is_point_in_polygon(point: tuple, polygon: list[tuple[float, float]]) -> bool:
    """Determines if given 2D coordinate lies in the polygon or not"""
    x, y = point
    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]   
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

def change_yaw(self, context):
    """Applys rotation matrix for rotation along global Z-axis for all objects"""
    props = context.scene.my_tool
    if not props.orchard_generated:
        return

    for obj in bpy.data.objects:  
        if "Polygon" not in obj.name:
            # Calculate the rotation matrix around the global Z axis
            rotation_matrix = mathutils.Matrix.Rotation(props.orchard_yaw, 4, 'Z') 
            # Apply the rotation matrix to the object's world matrix
            obj.matrix_world = rotation_matrix @ obj.matrix_world

def displacement_modifier_strength_update(self, context):
    props = context.scene.my_tool
    if not props.orchard_generated:
        return
    
    plane_obj = bpy.data.objects["ground"]
    plane_obj.modifiers["Displace"].strength = props.plane_unevenness


def subdivide_plane(obj, cuts):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=cuts)
    bpy.ops.object.mode_set(mode='OBJECT')

def add_displacement_modifier_with_cloud_texture(obj, strength):
    """Adds a displacement modifier to the object with a cloud texture to replicate unevenness"""
    # Add displacement modifier
    displace_modifier = obj.modifiers.new(name="Displace", type='DISPLACE')
    
    # Create a new texture
    tex = bpy.data.textures.new("DisplaceTexture", type='CLOUDS')
    
    # Assign the texture to the displacement modifier
    displace_modifier.texture = tex
    
    # Set the strength of the displacement
    displace_modifier.strength = strength

def serialize_value(value):
    if isinstance(value, mathutils.Vector):
        return list(value)
    # Add other types as needed later on
    return value

def deserialize_value(value, type_hint):
    if type_hint == mathutils.Vector:
        return mathutils.Vector(value)
    # Add other types as needed later on
    return value

def dump_properties_to_json(prop_group, file_path):
    """Dumps all properties of the PropertyGroup into the json file"""

    # Create a dictionary to hold the properties and their values
    properties_dict = {}
    
    # Iterate through all properties of the PropertyGroup
    for prop_name in prop_group.__annotations__:
        value = getattr(prop_group, prop_name)
        properties_dict[prop_name] = serialize_value(value)
    
    # Write the dictionary to a JSON file
    with open(file_path, 'w') as json_file:
        json.dump(properties_dict, json_file, indent=4)

def load_properties_from_json(prop_group, file_path):
    """Sets all properties of the PropertyGroup to ones defined in the json file"""
    with open(file_path, 'r') as json_file:
        properties_dict = json.load(json_file)
    
    for prop_name, value in properties_dict.items():
        if hasattr(prop_group, prop_name):
            type_hint = type(getattr(prop_group, prop_name))
            setattr(prop_group, prop_name, deserialize_value(value, type_hint))

def load_scene():
    """Updates scene and also throws a warning in the terminal"""
    bpy.context.view_layer.update()
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
