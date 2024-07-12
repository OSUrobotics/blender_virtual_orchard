import bpy
import mathutils

def create_polygon(points):
    # Create a new mesh
    mesh = bpy.data.meshes.new("PolygonMesh")
    obj = bpy.data.objects.new("Polygon", mesh)

    # Link the object to the current scene
    bpy.context.collection.objects.link(obj)

    # Create the mesh from the points
    mesh.from_pydata(points, [], [[i for i in range(len(points))]])

def is_point_in_polygon(point, polygon):
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
    props = context.scene.my_tool

    if len(bpy.data.objects) == 0:
        return

    for obj in bpy.data.objects:  
        if "Polygon" not in obj.name:
            # Calculate the rotation matrix around the global Z axis
            rotation_matrix = mathutils.Matrix.Rotation(props.orchard_yaw, 4, 'Z') 
            # Apply the rotation matrix to the object's world matrix
            obj.matrix_world = rotation_matrix @ obj.matrix_world

def displacement_modifier_strength_update(self, context):
    props = context.scene.my_tool
    plane_obj = bpy.data.objects["ground"]
    plane_obj.modifiers["Displace"].strength = props.plane_unevenness


def subdivide_plane(obj, cuts):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=cuts)
    bpy.ops.object.mode_set(mode='OBJECT')

def add_displacement_modifier(obj, strength):
    """Add displacement modifier with a cloud texture"""
    # Add displacement modifier
    displace_modifier = obj.modifiers.new(name="Displace", type='DISPLACE')
    
    # Create a new texture
    tex = bpy.data.textures.new("DisplaceTexture", type='CLOUDS')
    
    # Assign the texture to the displacement modifier
    displace_modifier.texture = tex
    
    # Set the strength of the displacement
    displace_modifier.strength = strength