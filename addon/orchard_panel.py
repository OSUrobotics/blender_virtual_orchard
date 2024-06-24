from bpy.types import Panel

class MY_PT_OrchardPanel(Panel):
    bl_label = "Orchard Panel"
    bl_idname = "MY_PT_orchard_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Orchard'

    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.4
        layout.scale_x = 1.4

        scene = context.scene
        my_props = scene.my_tool

        row = layout.row()
        row.operator("object.generate_orchard_operator")

        prop_names = [
            "tree_file_path", 
            "texture_path"
        ]
        
        for prop_name in prop_names:
            layout.prop(my_props, prop_name)

        row = layout.row(align=True)
        row.prop(my_props, "polygon_clipping")

        if my_props.polygon_clipping:
            row.prop(my_props, "pgon_sides")
            row.prop(my_props, "orchard_roll")

        row = layout.row(align=True)
        row.prop(my_props, "subdivision_level")
        row.operator("object.apply_subdivision")

class My_PT_ParamsPanel(Panel):
    bl_label = "Parameters"
    bl_idname = "PT_Panel_Params"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Orchard"
    bl_parent_id = "MY_PT_orchard_panel"
    bl_options = {"DEFAULT_CLOSED"}
    
    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.4
        
        scene = context.scene
        my_props = scene.my_tool

        prop_names = [
            "num_sun_positions",
            "wire_spacing"
            ]

        row = layout.row(align=True)
        row.prop(my_props, "tree_rows")
        row.prop(my_props, "tree_columns")

        row = layout.row()
        row.prop(my_props, "tree_angle")

        for prop_name in prop_names:
            layout.prop(my_props, prop_name)
    

class My_PT_Render_OBJ_Panel(Panel):
    bl_label = "Render Objects"
    bl_idname = "PT_Panel_Render_Obj"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Orchard"
    bl_parent_id = "MY_PT_orchard_panel"
    bl_options = {"DEFAULT_CLOSED"}
    
    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.4
        
        scene = context.scene
        my_props = scene.my_tool

        prop_names = [
            "render_trees",
            "render_cam", 
            "render_wires",
            "render_sky_and_sun", 
            "render_posts", 
            "render_plane"
            ]

        col = layout.split().column(align=True)
        col.scale_y = 0.7
        for prop_name in prop_names:
            col.prop(my_props, prop_name)

class My_PT_Render_Material_Panel(Panel):
    bl_label = "Render Materials"
    bl_idname = "PT_Panel_Render_Material"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Orchard"
    bl_parent_id = "MY_PT_orchard_panel"
    bl_options = {"DEFAULT_CLOSED"}
    
    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.4
        
        scene = context.scene
        my_props = scene.my_tool

        prop_names = [
            "render_tree_material",
            "render_wire_material",
            "render_post_material",
            "render_ground_material"
            ]

        col = layout.split().column(align=True)
        col.scale_y = 0.7
        for prop_name in prop_names:
            col.prop(my_props, prop_name)