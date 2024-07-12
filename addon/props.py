from bpy.types import PropertyGroup
import bpy.props
from . generate_images import take_images
from . helpers import change_yaw, displacement_modifier_strength_update 
import numpy as np

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

    random_textures: bpy.props.BoolProperty(
        name="Random textures",
        description="Toggle on to use random textures for trees and gorund and off to use single realistic texture",
        default= False
    )

    plane_unevenness: bpy.props.FloatProperty(
        name="Plane unevenness",
        description="Controls the bumpyness of the plane",
        default=2.5,
        min=0,
        update=displacement_modifier_strength_update
    )

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
        max=500
    )

    tree_columns: bpy.props.IntProperty(
        name="columns",
        description="Number of trees in a column of the orchard",
        default=1,
        min=1,
        max=500
    )

    orchard_yaw: bpy.props.FloatProperty(
        name="yaw",
        description="Yaw of the entire orchard to be applied as transformation in radians",
        default=0,
        step=1,
        update=change_yaw
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
    )
    
    wire_spacing: bpy.props.FloatProperty(
        name="wire spacing",
        description="Spacing between each wire",
        default=0.5,
        min=0,
        max=5
    )
    
    subdivision_level: bpy.props.IntProperty(
        name="Subdiv. Level",
        default=0,
        min=0,
        max=6
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

    render_polygons: bpy.props.BoolProperty(
        name="Render polygons",
        description="Visualization/debugging tool for polygon clipping",
        default=False
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

    orchard_generated: bpy.props.BoolProperty(
        name="Orchard generated",
        description= "Flag to check if orchard has done generating",
        default=False
    )

    snap_image: bpy.props.BoolProperty(
        name="Take image",
        description="Toggle on if taking images of random trees from the orchard",
        default= False,
    )

    random_tree: bpy.props.BoolProperty(
        name="random",
        description="""Toggle on if taking images of random trees and off for the same one.
Useful for adjusting desired camera parameters""",
        default= True,
    )

    image_pairs: bpy.props.BoolProperty(
        name="Do pairs",
        description="Toggle on if taking pairs of images of trees from the orchard",
        default= False,
    )

    image_dir_path: bpy.props.StringProperty(
        name="Images dir path",
        description="Select the directory to store images taken",
        default="path to dir for image storage...",
        maxlen=1024,
        subtype="DIR_PATH")    

    num_images: bpy.props.IntProperty(
        name="No. of images",
        description="Number of images to be taken",
        default=1,
        min=0,
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
        description= "Campath offset",
        default=[-3, 2.8, 1.5],
        step=5,
        subtype="XYZ",
    )
    
    left_min: bpy.props.FloatProperty(
        name="Left-min",
        description="Minimum distance the camera is placed from the tree's origin in this direction. Goes form -1 to 1",
        default=0,
        min=-1,
        max=1,
        step=10,
        update=take_images
    )
    
    right_max: bpy.props.FloatProperty(
        name="Right-max",
        description="Maximum distance the camera is placed from the tree's origin in this direction. Goes form -1 to 1",
        default=0,
        min=-1,
        max=1,
        step=10,
        update=take_images
    )
    
    in_min: bpy.props.FloatProperty(
        name="In-min",
        description="Minimum distance the camera is placed from the tree's origin in this direction. Goes form -1 to 1",
        default=1,
        min=-1,
        max=1,
        step=10,
        update=take_images
    )
    
    out_max: bpy.props.FloatProperty(
        name="Out-max",
        description="Maximum distance the camera is placed from the tree's origin in this direction. Goes form -1 to 1",
        default=1,
        min=-1,
        max=1,
        step=10,
        update=take_images
    )

    down_min: bpy.props.FloatProperty(
        name="Down-min",
        description="Minimum distance the camera is placed from the tree's origin in this direction. Goes form 0 to 1",
        default=0.5,
        min=0,
        max=1,
        step=10,
        update=take_images
    )

    up_max: bpy.props.FloatProperty(
        name="Up-max",
        description="Maximum distance the camera is placed from the tree's origin in this direction. Goes form 0 to 1",
        default=0.5,
        min=0,
        max=1,
        step=10,
        update=take_images
    )

    camera_angle: bpy.props.FloatVectorProperty(
        name="Angle of camera",
        description= "Pitch, roll, and yaw of the camera",
        default=[-1.57, -3.14, 0],
        step=10,
        subtype="XYZ",
        update=take_images
    )

    min_x: bpy.props.FloatProperty(
        name="X-min",
        description="Minimum angle the camera might face in this axis",
        default=-np.pi/2,
        min=-2*np.pi,
        max=2*np.pi,
        update=take_images
    )
    
    max_x: bpy.props.FloatProperty(
        name="X-max",
        description="Maximum angle the camera might face in this axis",
        default=-np.pi/2,
        min=-2*np.pi,
        max=2*np.pi,
        update=take_images
    )

    min_y: bpy.props.FloatProperty(
        name="Y-min",
        description="Minimum angle the camera might face in this axis",
        default=-np.pi,
        min=-2*np.pi,
        max=2*np.pi,
        update=take_images
    )
    
    max_y: bpy.props.FloatProperty(
        name="Y-max",
        description="Maximum angle the camera might face in this axis",
        default=-np.pi,
        min=-2*np.pi,
        max=2*np.pi,
        update=take_images
    )

    min_z: bpy.props.FloatProperty(
        name="Z-min",
        description="Minimum angle the camera might face in this axis",
        default=0,
        min=-2*np.pi,
        max=2*np.pi,
        update=take_images
    )
    
    max_z: bpy.props.FloatProperty(
        name="Z-max",
        description="Maximum angle the camera might face in this axis",
        default=0,
        min=-2*np.pi,
        max=2*np.pi,
        update=take_images
    )

