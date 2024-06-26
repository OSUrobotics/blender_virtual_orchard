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
        props = scene.my_tool

        row = layout.row()
        row.prop(props, "take_image")

        layout.label(text="Camera intrinsics:")
        layout.prop(props, "focal_length")

        row = layout.row()
        row.prop(props, "aspect_X")
        row.prop(props, "aspect_Y")
        
        row = layout.row()
        row.prop(props, "resolution_X")
        row.prop(props, "resolution_Y")
        
        layout.label(text="Camera extrinsics:")
        row = layout.row()
        row.prop(props, "cam_offset")

        row = layout.row(align=True)
        row.prop(props, "left_right_offset")
        row.prop(props, "in_out_offset")
        row.prop(props, "up_down_offset")

        row = layout.row()
        row.prop(props, "camera_angle")