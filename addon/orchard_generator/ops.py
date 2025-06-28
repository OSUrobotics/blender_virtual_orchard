import bpy
from . load_script_label import render
from . generate_images import take_images, take_video

class GenerateOrchardOperator(bpy.types.Operator):
    """Calls the render function to generate orchard"""
    bl_idname = "object.generate_orchard_operator"
    bl_label = "GENERATE"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Call the custom function
        render(self, context)
        context.scene.my_tool.orchard_generated = True
        return {'FINISHED'}

class OBJECT_OT_take_image(bpy.types.Operator):
    """Calls the take_images function to start taking images of trees"""
    bl_idname = "object.take_images"
    bl_label = "TAKE IMAGES"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.scene.my_tool.snap_image and context.scene.my_tool.orchard_generated

    def execute(self, context):
        take_images(self, context)
        return {'FINISHED'}


class OBJECT_OT_take_video(bpy.types.Operator):
    """Render video following the sine path"""
    bl_idname = "object.take_video"
    bl_label = "TAKE VIDEO"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.scene.my_tool.make_video and context.scene.my_tool.orchard_generated

    def execute(self, context):
        take_video(self, context)
        return {'FINISHED'}



    
