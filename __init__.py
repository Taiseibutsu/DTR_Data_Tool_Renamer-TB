# This software is MIT licensed (https://opensource.org/licenses/MIT) 
# This program is free software: you can redistribute it and/or modify it.
# Tested on 3.0 Alpha
# <2021> <Taiseibutsu>"

bl_info = {
    "name": "TB_Data_Renamer",
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
from bpy.types import AddonPreferences, Panel

class TB_E_Properties(bpy.types.PropertyGroup):
    nametorename : bpy.props.StringProperty(default = "Enter Name", description = "Name that will be assigned to active object")
    renamerfrom : bpy.props.EnumProperty(
        name = "Enumerator/Dropdown",
        description = "Object that will rename",
        items= [('OBJECT', 'Object', 'Import name from Object','OBJECT_DATA',0),
                ('DATABLOCK','Data-block','Import name from Data-Block', 'MESH_DATA', 1),
                ('MATERIAL','Material','Import name from Active Material', 'MATERIAL', 2),
                ('ACTION','Action','Import name from Animation', 'ACTION', 3)
        ]
    )
    renamermode : bpy.props.EnumProperty(
        name = "Enumerator/Dropdown",
        description = "Mode to rename",
        items= [('SCENE', 'Scene', 'Export name to Scene','SCENE_DATA',0),
                ('SELECTION','Selection','Export name to Selection', 'RESTRICT_SELECT_OFF', 1),
                ('COLLECTION','Collection','Export name to Selected Colection', 'OUTLINER_COLLECTION', 2),
                ('ALL','All','Export name to All Objects', 'BLENDER', 3)
        ]
    )
    renamertoscene : bpy.props.PointerProperty(type=bpy.types.Scene)
    renamertosceneactive : bpy.props.BoolProperty(default = True, description = "Transfer Name to Active Scene")

    renamertocollection : bpy.props.PointerProperty(type=bpy.types.Collection)
    renamertocollectionactive : bpy.props.BoolProperty(default = False, description = "Transfer Name to ActiveCollection")

    renamertoobject : bpy.props.BoolProperty(default = True, description = "Transfer Name to Object")
    renamertodatablock : bpy.props.BoolProperty(default = True, description = "Transfer Name to Data-Block")
    renamertoaction : bpy.props.BoolProperty(default = False, description = "Transfer Name to Animation")
    renamertomaterial : bpy.props.BoolProperty(default = False, description = "Transfer Name to Material")

def setrenamename(ob,renamename):
    tbtool = bpy.context.scene.tb_data_tool
    if tbtool.renamerfrom !='OBJECT' and tbtool.renamertoobject:
        ob.name = renamename
    if tbtool.renamerfrom !='DATABLOCK' and tbtool.renamertodatablock:
        ob.data.name = renamename
    if tbtool.renamerfrom !='ACTION' and tbtool.renamertoaction and ob.animation_data != None:   
        ob.animation_data.action.name = renamename
    if tbtool.renamerfrom !='MATERIAL' and tbtool.renamertomaterial and ob.active_material != None:
        ob.active_material.name = renamename
      
def renamerename(ob):
    tbtool = bpy.context.scene.tb_data_tool
    if tbtool.renamerfrom =='OBJECT':
        renamename = ob.name
        setrenamename(ob,renamename)
    if tbtool.renamerfrom =='DATABLOCK':
        renamename = ob.data.name
        setrenamename(ob,renamename)
    if tbtool.renamerfrom =='ACTION':
        if ob.animation_data != None:
            if ob.animation_data.action != None:
                renamename = ob.animation_data.action.name
                setrenamename(ob,renamename)
    if tbtool.renamerfrom =='MATERIAL':
        if ob.active_material != None:
            print("HAS MATERIAL")
            renamename = ob.active_material.name
            setrenamename(ob,renamename)        
    #return renamename

class TB_RENAMER(bpy.types.Operator):
    bl_idname = "tb_ops.renamercut"
    bl_label = "Renames data"
    bl_description = "Rename Data"
    
    def execute(self, context):
        acobj = bpy.context.active_object
        acobjt = acobj.type
        tbtool = context.scene.tb_data_tool
        #if tbtool.renamerfrom =='OBJECT':
        #    renamename = acobj.name
        #if tbtool.renamerfrom =='DATABLOCK':
        #    renamename = acobj.data.name
        #if tbtool.renamerfrom =='ACTION':
        #    renamename = acobj.animation_data.action.name
        #if tbtool.renamerfrom =='MATERIAL':
        #    renamename = acobj.active_material.name

        if tbtool.renamermode =='SELECTION':  
            for ob in bpy.context.selected_objects:
                renamerename(ob)        
        if tbtool.renamermode =='ALL':
            for ob in bpy.data.objects:
                renamerename(ob)                  
        if tbtool.renamermode =='SCENE':
            if tbtool.renamertosceneactive:
                for ob in bpy.context.scene.objects:
                    renamerename(ob) 
            else:
                if tbtool.renamertoscene != None:
                    for ob in tbtool.renamertoscene.objects:
                        renamerename(ob) 
        if tbtool.renamermode =='COLLECTION':
            if tbtool.renamertocollectionactive:
                for ob in bpy.context.collection.objects:
                    renamerename(ob) 
            else:
                if tbtool.renamertocollection != None:
                    for ob in tbtool.renamertocollection.objects:
                        renamerename(ob)
        return {"FINISHED"}



def tbdatarenamer(self, context):
    acobj = bpy.context.active_object
    acobjt = acobj.type
    if acobjt != 'EMPTY':
        tbtool = context.scene.tb_data_tool
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
        if tbtool.renamerfrom =='ACTION' or tbtool.renamerfrom =='MATERIAL' or tbtool.renamertomaterial and acobjt in ['MESH','META','HAIR','CURVE','POINTCLOUD','SURFACE','GPENCIL','VOLUME'] or tbtool.renamertoaction:
            row = layout.row(align=True)
        if tbtool.renamerfrom =='MATERIAL' or tbtool.renamertomaterial and acobjt in ['MESH','META','HAIR','CURVE','POINTCLOUD','SURFACE','GPENCIL','VOLUME']:
            row.template_ID(acobj, "active_material", new="material.new")
        if (tbtool.renamerfrom =='ACTION' or tbtool.renamertoaction) and (tbtool.renamerfrom =='MATERIAL' or tbtool.renamertomaterial and acobjt in ['MESH','META','HAIR','CURVE','POINTCLOUD','SURFACE','GPENCIL','VOLUME']):
            row.separator()
        if tbtool.renamertoaction or tbtool.renamerfrom =='ACTION':
            st = context.space_data          
            #layout.template_ID(st, "action", new="action.new", unlink="action.unlink")
            if acobj.animation_data != None:
                if acobj.animation_data.action != None:
                    row.prop(acobj.animation_data.action, "name" , text="",icon='ACTION')
                else:
                    row.label(text="No Active Action",icon='ACTION')
            else:
                row.label(text="No Active Action",icon='ACTION')
                #row.operator("action.new",(acobj))

        box = layout.box()
        #ALTERNATIVE WAY TO DISPLAY
        #row = box.row(align=True)
        #row.prop_enum(tbtool, "renamerfrom","OBJECT",icon='OBJECT_DATA')
        #row.prop_enum(tbtool, "renamerfrom","DATABLOCK",icon=datablockicon)
        #row.prop_enum(tbtool, "renamerfrom","ACTION",icon='ACTION')
        #row.prop_enum(tbtool, "renamerfrom","MATERIAL",icon='MATERIAL')
        row = box.row(align=True)
        if tbtool.renamerfrom == 'DATABLOCK':
            row.prop(tbtool, "renamerfrom",text="",icon=datablockicon)
        else:
            row.prop(tbtool, "renamerfrom",text="")
        row.label(icon='TRACKING_FORWARDS_SINGLE')
        if tbtool.renamerfrom != 'DATABLOCK':
            row.prop(tbtool, "renamertodatablock",text="",icon=datablockicon)
        if tbtool.renamerfrom != 'OBJECT':
            row.prop(tbtool, "renamertoobject",text="",icon='OBJECT_DATA')
        if tbtool.renamerfrom != 'ACTION':
            row.prop(tbtool, "renamertoaction",text="",icon='ACTION')
        if tbtool.renamerfrom != 'MATERIAL':
            row.prop(tbtool, "renamertomaterial",text="",icon='MATERIAL')

        if tbtool.renamermode =='SCENE':
            if tbtool.renamertosceneactive:
                row.prop(tbtool, "renamertosceneactive",text="Active Scene",icon='PIVOT_ACTIVE')
            else:
                row.prop(tbtool, "renamertoscene",text="",icon='SCENE_DATA')
                row.prop(tbtool, "renamertosceneactive",text="",icon='PIVOT_ACTIVE')
        if tbtool.renamermode =='COLLECTION':
            if tbtool.renamertocollectionactive:
                row.prop(tbtool, "renamertocollectionactive",text="Active Collection",icon='PIVOT_ACTIVE')
            else:
                row.prop(tbtool, "renamertocollection",text="",icon='OUTLINER_COLLECTION')
                row.prop(tbtool, "renamertocollectionactive",text="",icon='PIVOT_ACTIVE')
        
        if tbtool.renamermode in ['COLLECTION','SCENE']:
            icononlyrename = True
        else:
            icononlyrename = False

        row.prop(tbtool, "renamermode",text="",icon_only=icononlyrename)

        row = box.row(align=True)
        row.operator("tb_ops.renamercut",text="Rename",icon='SORTALPHA')

    else:
        layout = self.layout
        row = layout.row(align=True)
        row.label(text="Empty Data has nolinked Data Block",icon='EMPTY_DATA')
        row = layout.row(align=True)
        row.template_ID(context.view_layer.objects, "active", filter='AVAILABLE')
        if acobj.empty_display_type == 'IMAGE':
            row = layout.row(align=True)
            row.template_ID(acobj, "data", open="image.open", unlink="object.unlink_data")

class TB_DATA_TOOLS_PNL(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "TB"
    bl_label = "TB_Data_Tools"
    bl_idname = "TB_PNL_Data_Tools"
    @classmethod
    def poll(cls, context):
        return context.object is not None
    def draw_header(self,context):
        layout = self.layout
        layout.label(icon='FILE_TEXT')
    def draw (self,context):
        tbdatarenamer(self, context)

class TB_DATA_TOOLS_PNL_POP(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "context.tbdatarenamerpopup"
    bl_label = "Data Renamer"
    @classmethod
    def poll(cls, context):
        return context.object is not None
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    def draw(self, context):
        tbdatarenamer(self, context)
    def execute(self, context):
        return {'FINISHED'}

class TB_Datarenamer_PreferencesPanel(AddonPreferences):
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
    TB_E_Properties,
    TB_DATA_TOOLS_PNL,
    TB_DATA_TOOLS_PNL_POP,
    TB_Datarenamer_PreferencesPanel,
    TB_RENAMER,
    )
addon_keymaps = []         



def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.tb_data_tool = bpy.props.PointerProperty(type= TB_E_Properties)
 #KEYMAP
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
     #VIEW3D        
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new("context.tbdatarenamerpopup", 'F2', 'PRESS', alt=True, ctrl=False, shift=False)
        kmi.active = True
        addon_keymaps.append((km, kmi))


def unregister():
 #CLASSES
    for cls in classes:
        bpy.utils.unregister_class(cls)
        bpy.types.Scene.tb_data_tool
 #KEYMAP
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()        
if __name__ == "__main__":
    register()
