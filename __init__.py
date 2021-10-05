# This software is MIT licensed (https://opensource.org/licenses/MIT) 
# This program is free software: you can redistribute it and/or modify it.
# Tested on 3.0 Alpha
# <2021> <Taiseibutsu>"

bl_info = {
    "name": "TS_Data_Renamer",
    "author": "Taiseibutsu",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "3D View, N Panel",
    "description": "Custom tools for assigning names between object name and data-blocks",
    "warning": "",
    "wiki_url": "",
    "category": "Panels",
}
import bpy, addon_utils, os, rna_keymap_ui

class TS_E_Properties(bpy.types.PropertyGroup):
    nametorename : bpy.props.StringProperty(default = "Enter Name", description = "Name that will be assigned to active object")

class TS_RENAME_DATABLOCK_AND_OBJ(bpy.types.Operator):
    bl_idname = "ts_ops.renamedataandobj"
    bl_label = "Renames current Data-Block and Object name"
    bl_description = "Rename DATA-BLOCK & OBJ"
    def execute(self, context):
        for ob in bpy.context.selected_objects:
            tstool = context.scene.ts_data_tool
            ob.name = tstool.nametorename
            ob.data.name = tstool.nametorename
        return {"FINISHED"}
class TS_RENAME_OBJ_TO_DATABLOCK_SCENE(bpy.types.Operator):
    bl_idname = "ts_ops.renameobjtodatascene"
    bl_label = "Renames all object names in the scene to the data-block property name"
    bl_description = "Rename Scene OBJ > DATA-BLOCK"
    def execute(self, context):
        for ob in bpy.data.objects:
            ob.data.name = ob.name
        return {"FINISHED"}
class TS_RENAME_DATABLOCK_TO_OBJ_SCENE(bpy.types.Operator):
    bl_idname = "ts_ops.renamedatatoobjkscne"
    bl_label = "Renames all data-block names in the scene to the object name"
    bl_description = "Rename Scene DATA-BLOCK > OBJ"
    def execute(self, context):
        for ob in bpy.data.objects:
            ob.name = ob.data.name
        return {"FINISHED"}
class TS_RENAME_OBJ_TO_DATABLOCK_SELECTION(bpy.types.Operator):
    bl_idname = "ts_ops.renameobjtodataselect"
    bl_label = "Renames all object names in the scene to the data-block property name"
    bl_description = "Rename Scene OBJ > DATA-BLOCK"
    def execute(self, context):
        for ob in bpy.context.selected_objects:
            ob.data.name = ob.name
        return {"FINISHED"}
class TS_RENAME_DATABLOCK_TO_OBJ_SELECTION(bpy.types.Operator):
    bl_idname = "ts_ops.renamedatatoobjselect"
    bl_label = "Renames all data-block names in the scene to the object name"
    bl_description = "Rename Scene DATA-BLOCK > OBJ"
    def execute(self, context):
        for ob in bpy.context.selected_objects:
            ob.name = ob.data.name
        return {"FINISHED"}

def tsdatarenamer(self, context):
    acobj = bpy.context.active_object
    acobjt = acobj.type
    if acobjt != 'EMPTY':
        tstool = context.scene.ts_data_tool
        if acobjt != 'GPENCIL' and acobjt != 'LIGHT_PROBE' and acobjt != 'SPEAKER':
            datablockicon = bpy.context.active_object.type + '_DATA'
        elif acobjt == 'GPENCIL':
            datablockicon = 'OUTLINER_DATA_GREASEPENCIL'
        elif acobjt == 'LIGHT_PROBE':
            datablockicon = 'OUTLINER_DATA_LIGHTPROBE'
        elif acobjt == 'SPEAKER':
            datablockicon = 'SPEAKER'
        layout = self.layout
        row = layout.row(align=True)
        row.template_ID(context.view_layer.objects, "active", filter='AVAILABLE')
        row.template_ID(context.view_layer.objects.active, "data")
        row = layout.row(align=True)
        row.label(text="Insert Text to Name")
        row = layout.row(align=True)
        row.prop(tstool, "nametorename",text="")
        row.operator("ts_ops.renamedataandobj",text="Rename Both",icon='FILE_TEXT')   
        #row.label(text=str(bpy.context.active_object.name),icon='OBJECT_DATA')
        #row.label(text=str(bpy.context.active_object.data.name),icon=datablockicon)
        row = layout.row(align=True)
        box = layout.box() 
        row = box.row(align=True)
        row.label(text="Rename Selected Objects",icon='RESTRICT_SELECT_OFF')
        row = box.row(align=True)
        row.label(icon='OBJECT_DATA')
        row.separator()
        row.operator("ts_ops.renameobjtodataselect",text=" ",icon='TRACKING_FORWARDS_SINGLE')    
        row.operator("ts_ops.renamedatatoobjselect",text=" ",icon='TRACKING_BACKWARDS_SINGLE') 
        row.separator()
        row.label(icon=datablockicon)    
        box = layout.box() 
        row = box.row(align=True)
        row.label(text="Rename Scene Objects",icon='SCENE_DATA')
        row = box.row(align=True)
        row.label(icon='OBJECT_DATA')
        row.separator()
        row.operator("ts_ops.renameobjtodatascene",text=" ",icon='TRACKING_FORWARDS_SINGLE')    
        row.operator("ts_ops.renamedatatoobjkscne",text=" ",icon='TRACKING_BACKWARDS_SINGLE') 
        row.separator()
        row.label(icon=datablockicon)
    else:
        layout = self.layout
        row = layout.row(align=True)
        row.label(text="Empty Data has nolinked Data Block",icon='EMPTY_DATA')
        row = layout.row(align=True)
        row.template_ID(context.view_layer.objects, "active", filter='AVAILABLE')
        if acobj.empty_display_type == 'IMAGE':
            row = layout.row(align=True)
            row.template_ID(acobj, "data", open="image.open", unlink="object.unlink_data")

class TS_DATA_TOOLS_PNL(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "TS_OPS"
    bl_label = "TS_Data_Tools"
    bl_idname = "TSPNL_Data_Tools"
    @classmethod
    def poll(cls, context):
        return context.object is not None
    def draw_header(self,context):
        layout = self.layout
        layout.label(icon='FILE_TEXT')
    def draw (self,context):
        tsdatarenamer(self, context)

class TS_DATA_TOOLS_PNL_POP(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "context.tsdatarenamerpopup"
    bl_label = "Data Renamer"
    @classmethod
    def poll(cls, context):
        return context.object is not None
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    def draw(self, context):
        tsdatarenamer(self, context)
    def execute(self, context):
        return {'FINISHED'}

    
classes = (
    TS_E_Properties,
    TS_RENAME_OBJ_TO_DATABLOCK_SCENE,
    TS_RENAME_DATABLOCK_TO_OBJ_SCENE,
    TS_RENAME_OBJ_TO_DATABLOCK_SELECTION,
    TS_RENAME_DATABLOCK_TO_OBJ_SELECTION,
    TS_RENAME_DATABLOCK_AND_OBJ,
    TS_DATA_TOOLS_PNL,
    TS_DATA_TOOLS_PNL_POP,
    )
addon_keymaps = []            
    
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.ts_data_tool = bpy.props.PointerProperty(type= TS_E_Properties)
 #KEYMAP
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
     #VIEW3D        
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new("context.tsdatarenamerpopup", 'F2', 'PRESS', alt=True, ctrl=False, shift=False)
        kmi.active = True
        addon_keymaps.append((km, kmi))


def unregister():
 #CLASSES
    for cls in classes:
        bpy.utils.unregister_class(cls)
        bpy.types.Scene.ts_data_tool
 #KEYMAP
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()        
if __name__ == "__main__":
    register()