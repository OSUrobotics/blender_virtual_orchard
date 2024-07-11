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
        row.operator("object.take_images")

        row = layout.row(align=True)
        row.prop(props, "snap_image")
        row.prop(props, "random_tree")
        row.prop(props, "image_pairs")

        if props.snap_image:
            row = layout.row()
            row.prop(props, "image_dir_path")
            
            row = layout.row()
            row.prop(props, "num_images")

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

        layout.label(text="Toggle off take image before manipulating the following:")
        layout.label(text="Cam location:")

        row = layout.row(align=True)
        row.prop(props, "left_min")
        row.prop(props, "right_max")

        row = layout.row(align=True)
        row.prop(props, "in_min")
        row.prop(props, "out_max")

        row = layout.row(align=True)
        row.prop(props, "down_min")
        row.prop(props, "up_max")

        layout.label(text="Cam angles:")

        row = layout.row(align=True)
        row.prop(props, "min_x")
        row.prop(props, "max_x")

        row = layout.row(align=True)
        row.prop(props, "min_y")
        row.prop(props, "max_y")
        
        row = layout.row(align=True)
        row.prop(props, "min_z")
        row.prop(props, "max_z")