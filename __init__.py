# This software is MIT licensed (https://opensource.org/licenses/MIT) 
# This program is free software: you can redistribute it and/or modify it.
# Tested on 3.0 Alpha
# <2021> <Taiseibutsu>"

bl_info = {
    "name": "TB_Groups_Tools_/_TB_GT",
    "author": "Taiseibutsu",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "3D View, N Panel",
    "description": "Custom tools for vertex group control",
    "warning": "",
    "wiki_url": "",
    "category": "TB",
}
import bpy, addon_utils, os, rna_keymap_ui
from bpy.types import AddonPreferences, Panel

class TB_GT_Properties(bpy.types.PropertyGroup):
    stringtoop : bpy.props.StringProperty(default = "Enter Name", description = "Name to operate VGT tools")

class TB_VERTEX_GROUP_RENAMER(bpy.types.Operator):
    bl_idname = "tb_ops.deletevertexgroupbyname"
    bl_label = "Delete_Vertex_Group_by_Name"
    bl_description = "Deletes Vertex Groups by Name" 
    def execute(self, context):
        for vg in bpy.context.active_object.vertex_groups:
            if bpy.context.scene.tb_group_tool.stringtoop in vg.name:
                bpy.ops.object.vertex_group_set_active(group=vg.name)
                bpy.ops.object.vertex_group_remove()  
        return {"FINISHED"}
                
def tbvertexgrouptools(self, context):
    pass
def tbgrouptools(self, layout):
    tb_group_tool = bpy.context.scene.tb_group_tool
    row = layout.row()   
    row.prop(tb_group_tool,"stringtoop",text="")
    row.operator("tb_ops.deletevertexgroupbyname",text="Delete by Name",icon='X')

class TB_GROUPS_TOOLS_PNL(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""    
    bl_idname = "TB_PNL_Vertex_Group_Tools"
    bl_label = "TB|Group Tools"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    def draw_header(self,context):
        layout = self.layout
        layout.label(icon='MESH_DATA')
    def draw (self,context):
        layout = self.layout
        tbgrouptools(self, layout)

class TB_GROUPS_TOOLS_PREFERENCES(AddonPreferences):
    bl_idname = __name__
    def draw(self, context):
        layout = self.layout
        box=layout.box()
        box.label(text="Hotkey:")
        col = box.column()
        kc = bpy.context.window_manager.keyconfigs.addon
        for km, kmi in addon_keymaps:
            km = km.active()
            col.context_pointer_set("keymap", km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
        row = layout.row()
        col = row.column()
        col.prop(self, "TBOVER", text="")


classes = (
    TB_GT_Properties,
    TB_VERTEX_GROUP_RENAMER,
    TB_GROUPS_TOOLS_PNL
    #TB_GROUPS_TOOLS_PREFERENCES,
    )
addon_keymaps = []         


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.tb_group_tool = bpy.props.PointerProperty(type= TB_GT_Properties)
 #KEYMAP
    #wm = bpy.context.window_manager
    #kc = wm.keyconfigs.addon
    #if kc:
     #VIEW3D        
        #km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        #kmi = km.keymap_items.new("context.tbdatarenamerpopup", 'F2', 'PRESS', alt=True, ctrl=False, shift=False)
        #kmi.active = True
        #addon_keymaps.append((km, kmi))


def unregister():
 #CLASSES
    for cls in classes:
        bpy.utils.unregister_class(cls)
        bpy.types.Scene.tb_group_tool
 #KEYMAP
    #for km, kmi in addon_keymaps:
    #    km.keymap_items.remove(kmi)
    #addon_keymaps.clear()        
if __name__ == "__main__":
    register()