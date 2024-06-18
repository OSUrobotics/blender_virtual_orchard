from bpy.types import Panel

class MY_PT_RenderImagesPanel(Panel):
    bl_label = "Render Panel"
    bl_idname = "MY_PT_render_images_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Image Render'

    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.4
        layout.scale_x = 1.4

        scene = context.scene
        my_props = scene.my_tool

        layout.label(text="Camera intrinsics:")
        layout.prop(my_props, "focal_length")

        row = layout.row()
        row.prop(my_props, "aspect_X")
        row.prop(my_props, "aspect_Y")
        
        row = layout.row()
        row.prop(my_props, "resolution_X")
        row.prop(my_props, "resolution_Y")
        
        layout.label(text="Camera extrinsics:")
        row = layout.row()
        row.prop(my_props, "cam_offset")