bl_info = {
    "name" : "test_addon",
    "author" : "test",
    "description" : "",
    "blender" : (4, 1, 1),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

import bpy

from .orchard_panel import MY_PT_OrchardPanel
from .orchard_panel import My_PT_ParamsPanel
from .orchard_panel import My_PT_Render_OBJ_Panel
from .orchard_panel import My_PT_Render_Material_Panel
from .render_panel import MY_PT_RenderImagesPanel

from . props import MyProperties

from . ops import OBJECT_OT_apply_subdivision, GenerateOrchardOperator

classes = (
    MY_PT_OrchardPanel,
    My_PT_ParamsPanel,
    My_PT_Render_OBJ_Panel,
    My_PT_Render_Material_Panel,
    MY_PT_RenderImagesPanel,
    MyProperties,
    OBJECT_OT_apply_subdivision,
    GenerateOrchardOperator
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MyProperties)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.my_tool