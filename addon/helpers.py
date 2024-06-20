import bpy
from . builders import *

def create_polygon(points):
    # Create a new mesh
    mesh = bpy.data.meshes.new("PolygonMesh")
    obj = bpy.data.objects.new("Polygon", mesh)

    # Link the object to the current scene
    bpy.context.collection.objects.link(obj)

    # Create the mesh from the points
    mesh.from_pydata(points, [], [[i for i in range(len(points))]])

# def render_polygon(self, context):
#     props = context.scene.my_tool
#     sides = props.pgon_sides     
#     radius = props.pgon_radius
#     rotation = props.pgon_rotation
#     translation = [
#         props.pgon_translation[0],
#         props.pgon_translation[1],
#         0.0,
#         ]
    
#     bpy.ops.object.select_all(action='DESELECT')
#     for obj in list(bpy.data.objects):
#         if obj.name == "Polygon":
#             obj.select_set(True)
#             bpy.ops.object.delete()
#             break

#     create_polygon(polygon(sides, radius, rotation, translation))

def get_center_and_half_length(bounding_box):
    if not bounding_box or len(bounding_box) != 4:
        return None, None
    
    # Extract x and y coordinates from the bounding box corners
    xs, ys, zs = zip(*bounding_box)
    
    # Calculate the center of the square
    center_x = np.mean(xs)
    center_y = np.mean(ys)
    
    # Calculate the half length of the square's side
    # We can take the distance between the first two points (which are adjacent)
    half_length = np.sqrt((xs[1] - xs[0])**2 + (ys[1] - ys[0])**2) / 2
    
    return (center_x, center_y, 0), half_length