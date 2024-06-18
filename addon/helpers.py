import bpy

def create_polygon(points):
    # Create a new mesh
    mesh = bpy.data.meshes.new("PolygonMesh")
    obj = bpy.data.objects.new("Polygon", mesh)

    # Link the object to the current scene
    bpy.context.collection.objects.link(obj)

    # Create the mesh from the points
    mesh.from_pydata(points, [], [[i for i in range(len(points))]])