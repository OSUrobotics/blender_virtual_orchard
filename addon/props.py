from bpy.types import PropertyGroup
import bpy.props
from . load_script_label import render, render_polygon

# This is done in VSCode to suppess warning caused by Blender Python API
# constraints when dealing with UI related property definitions (annotations)
#   "python.analysis.diagnosticSeverityOverrides": {
#     "reportInvalidTypeForm": "none"
#   }

# Property Group to define custom properties
class MyProperties(PropertyGroup):

    tree_file_path: bpy.props.StringProperty(
        name="Tree files",
        description="Select tree files path",
        default="path to tree files dir...",
        maxlen=1024,
        subtype="DIR_PATH")
    
    texture_path: bpy.props.StringProperty(
        name="Textures",
        description="Select textures folder",
        default="path to textures dir...",
        maxlen=1024,
        subtype="DIR_PATH")

    tree_rows: bpy.props.IntProperty(
        name="rows",
        description="Number of trees in a row of the orchard",
        default=1,
        min=1,
        max=100,
    )

    tree_columns: bpy.props.IntProperty(
        name="columns",
        description="Number of trees in a column of the orchard",
        default=1,
        min=1,
        max=100,
    )

    pgon_sides: bpy.props.IntProperty(
        name="Sides",
        description="No. of sides of polygon",
        default=5,
        min=3,
        max=50,
        update=render_polygon
    )

    pgon_radius: bpy.props.FloatProperty(
        name="Radius",
        description="Radius of circle encircling the polygon",
        default=1,
        min=1,
        max=1000,
        step=10,
        update=render_polygon
    )

    pgon_rotation: bpy.props.FloatProperty(
        name="Rotation",
        description="Orientation of polygon",
        default=0,
        step=10,
        subtype="ANGLE",
        update=render_polygon
    )

    pgon_translation: bpy.props.FloatVectorProperty(
        name="Translation",
        description="Translation vector of polygon",
        default=[0, 0, 0],
        step=10,
        subtype="XYZ",
        update=render_polygon
    )

    tree_angle: bpy.props.FloatVectorProperty(
        name="Angle of tree",
        default=[0.3, 0, 0],
        step=10,
        subtype="XYZ"
    )

    num_sun_positions: bpy.props.IntProperty(
        name="No. of sun positions",
        description="Number of evenly spaced sun positions",
        default=1,
        min=1,
        max=100,
        update=render
    )
    
    wire_spacing: bpy.props.FloatProperty(
        name="wire spacing",
        description="Spacing between each wire",
        default=0.5,
        min=0,
        max=5,
        update=render
    )

    subdivision_level: bpy.props.IntProperty(
        name="Subdiv. Level",
        default=0,
        min=0,
        max=6
    )

    render_trees: bpy.props.BoolProperty(
        name="Render trees",
        default=True
    )

    render_cam: bpy.props.BoolProperty(
        name="Render campath",
        default=True
    )
    
    render_wires: bpy.props.BoolProperty(
        name="Render wires",
        default=True
    )
    
    render_sky_and_sun:  bpy.props.BoolProperty(
        name="Render sun/sky",
        default=True
    )
    
    render_posts: bpy.props.BoolProperty(
        name="Render posts",
        default=True
    )

    render_plane: bpy.props.BoolProperty(
        name="Render ground",
        default=True
    )


    render_tree_material: bpy.props.BoolProperty(
        name="trees",
        default=True
    )

    render_ground_material: bpy.props.BoolProperty(
        name="ground",
        default=True
    )

    render_post_material: bpy.props.BoolProperty(
        name="posts",
        default=True
    )
    
    render_wire_material: bpy.props.BoolProperty(
        name="wires",
        default=True
    )

    focal_length: bpy.props.FloatProperty(
        name="focal length",
        description="Perspective Camera focal length value in millimeters",
        default=18,
        min=1,
        max=5000,
        step=100,
        subtype="DISTANCE_CAMERA"
    )

    aspect_X: bpy.props.FloatProperty(
        name="Aspect X",
        description="Horizontal aspect ratio - for anamorphic or non-square pixel output.",
        default=1,
        min=1,
        max=200,
        step=10,
        subtype="NONE"
    )

    aspect_Y: bpy.props.FloatProperty(
        name="Aspect Y",
        description="Vertical aspect ratio - for anamorphic or non-square pixel output.",
        default=1,
        min=1,
        max=200,
        step=10,
        subtype="NONE"
    )

    resolution_X: bpy.props.IntProperty(
        name="Res X",
        description="Number of horizontal pixels in the rendered image",
        default=1920,
        min=4,
        max=65536,
        subtype="PIXEL"
    )

    resolution_Y: bpy.props.IntProperty(
        name="Res Y",
        description="Number of vertical pixels in the rendered image",
        default=1080,
        min=4,
        max=65536,
        subtype="PIXEL"
    )

    cam_offset: bpy.props.FloatVectorProperty(
        name="Cam offset",
        default=[-3, 2.8, 1.5],
        step=5,
        subtype="XYZ",
        update=render
    )