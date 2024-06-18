import bpy
from . builders import polygon

def create_polygon(points):
    # Create a new mesh
    mesh = bpy.data.meshes.new("PolygonMesh")
    obj = bpy.data.objects.new("Polygon", mesh)

    # Link the object to the current scene
    bpy.context.collection.objects.link(obj)

    # Create the mesh from the points
    mesh.from_pydata(points, [], [[i for i in range(len(points))]])

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