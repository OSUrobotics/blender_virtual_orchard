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

def is_point_in_polygon(point, polygon):
    """
    Determines if a point is inside a polygon.

    :param point: A tuple (x, y) representing the point to check.
    :param polygon: A list of tuples [(x1, y1), (x2, y2), ..., (xn, yn)] representing the vertices of the polygon.
    :return: True if the point is inside the polygon, False otherwise.
    """
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