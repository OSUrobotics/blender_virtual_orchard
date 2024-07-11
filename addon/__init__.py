# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Orchard Image Generator",
    "author" : "Utsav Bhandari",
    "description" : "Addon to generate virtual apple orchards and capture images for machine learning datasets.",
    "blender" : (4, 1, 1),
    "version" : (1, 0, 0),
    "location" : "View3D > Tool Shelf",
    "warning" : "",
    "category" : "Object"
}


import bpy

from .orchard_panel import MY_PT_OrchardPanel
from .orchard_panel import My_PT_ParamsPanel
from .orchard_panel import My_PT_Render_OBJ_Panel
from .orchard_panel import My_PT_Render_Material_Panel
from .image_panel import MY_PT_RenderImagesPanel

from . props import MyProperties

from . ops import OBJECT_OT_apply_subdivision, GenerateOrchardOperator, OBJECT_OT_take_image

classes = (
    MY_PT_OrchardPanel,
    My_PT_ParamsPanel,
    My_PT_Render_OBJ_Panel,
    My_PT_Render_Material_Panel,
    MY_PT_RenderImagesPanel,
    MyProperties,
    OBJECT_OT_apply_subdivision,
    GenerateOrchardOperator,
    OBJECT_OT_take_image
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    # my_tool is initialized here, any changes here needs to reflect everywhere else
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MyProperties)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.my_tool