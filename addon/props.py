from bpy.types import PropertyGroup
import bpy.props
from . load_script_label import render
from . builders import take_image

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

    polygon_clipping: bpy.props.BoolProperty(
        name="Polygon clipping",
        description="Clips the orchard via specified polygon",
        default= False
    )

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

    orchard_roll: bpy.props.FloatProperty(
        name="roll",
        description="Roll of the entire orchard in radians",
        default=0,
        step=1
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

    take_image: bpy.props.BoolProperty(
        name="Take image",
        description="Toggle if taking an image of a random tree from the orchard",
        default= False,
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

    left_right_offset: bpy.props.FloatProperty(
        name="lr offset",
        description="Spacing",
        default=0.5,
        min=0,
        max=1,
        update=take_image
    )
    
    in_out_offset: bpy.props.FloatProperty(
        name="io offset",
        description="Spacing",
        default=1,
        min=0,
        max=1,
        update=take_image
    )
    
    up_down_offset: bpy.props.FloatProperty(
        name="ud offset",
        description="Spacing",
        default=0.5,
        min=0,
        max=1,
        update=take_image
    )

    camera_angle: bpy.props.FloatVectorProperty(
        name="Angle of camera",
        description= "Pitch, roll, and yaw of the camera",
        default=[-1.57, 3.14, 0],
        step=10,
        subtype="XYZ",
        update=take_image
    )
