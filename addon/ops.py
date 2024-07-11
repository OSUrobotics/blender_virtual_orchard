import bpy
from . load_script_label import render
from . generate_images import take_images

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
    bl_idname = "object.take_images"
    bl_label = "TAKE IMAGES"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.scene.my_tool.snap_image and context.scene.my_tool.orchard_generated

    def execute(self, context):
        take_images(self, context)
        return {'FINISHED'}

class OBJECT_OT_apply_subdivision(bpy.types.Operator):
    """Apply Subdivision Modifier to all Mesh Objects"""
    bl_idname = "object.apply_subdivision"
    bl_label = "Apply"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        subdivision_level = context.scene.my_tool.subdivision_level
        bpy.ops.object.select_all(action='DESELECT')

        # Loop through all objects in the scene
        for obj in bpy.data.objects:
            # Check if the object is a mesh (subdividable)
            if obj.type == 'MESH':
                # Select the object
                obj.select_set(True)
                # Set the active object
                bpy.context.view_layer.objects.active = obj
                
                # Check if the object already has a Subdivision Surface modifier
                subsurf_modifier = None
                for mod in obj.modifiers:
                    if mod.type == 'SUBSURF':
                        subsurf_modifier = mod
                        break
                
                if subsurf_modifier is None:
                    # Add a Subdivision Surface modifier if it doesn't exist
                    subsurf_modifier = obj.modifiers.new(name="Subdivision", type='SUBSURF')
                
                # Set the subdivision levels
                subsurf_modifier.levels = subdivision_level
                subsurf_modifier.render_levels = subdivision_level

                # Deselect the object after applying the modifier
                obj.select_set(False)
        
        return {'FINISHED'}


    