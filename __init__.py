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
from bpy.types import AddonPreferences, Panel

class TS_E_Properties(bpy.types.PropertyGroup):
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
    tstool = bpy.context.scene.ts_data_tool
    if tstool.renamerfrom !='OBJECT' and tstool.renamertoobject:
        ob.name = renamename
    if tstool.renamerfrom !='DATABLOCK' and tstool.renamertodatablock:
        ob.data.name = renamename
    if tstool.renamerfrom !='ACTION' and tstool.renamertoaction and ob.animation_data != None:   
        ob.animation_data.action.name = renamename
    if tstool.renamerfrom !='MATERIAL' and tstool.renamertomaterial and ob.active_material != None:
        ob.active_material.name = renamename
      
def renamerename(ob):
    tstool = bpy.context.scene.ts_data_tool
    if tstool.renamerfrom =='OBJECT':
        renamename = ob.name
        setrenamename(ob,renamename)
    if tstool.renamerfrom =='DATABLOCK':
        renamename = ob.data.name
        setrenamename(ob,renamename)
    if tstool.renamerfrom =='ACTION':
        if ob.animation_data != None:
            if ob.animation_data.action != None:
                renamename = ob.animation_data.action.name
                setrenamename(ob,renamename)
    if tstool.renamerfrom =='MATERIAL':
        if ob.active_material != None:
            print("HAS MATERIAL")
            renamename = ob.active_material.name
            setrenamename(ob,renamename)        
    #return renamename

class TS_RENAMER(bpy.types.Operator):
    bl_idname = "ts_ops.renamercut"
    bl_label = "Renames data"
    bl_description = "Rename Data"
    
    def execute(self, context):
        acobj = bpy.context.active_object
        acobjt = acobj.type
        tstool = context.scene.ts_data_tool
        #if tstool.renamerfrom =='OBJECT':
        #    renamename = acobj.name
        #if tstool.renamerfrom =='DATABLOCK':
        #    renamename = acobj.data.name
        #if tstool.renamerfrom =='ACTION':
        #    renamename = acobj.animation_data.action.name
        #if tstool.renamerfrom =='MATERIAL':
        #    renamename = acobj.active_material.name

        if tstool.renamermode =='SELECTION':  
            for ob in bpy.context.selected_objects:
                renamerename(ob)        
        if tstool.renamermode =='ALL':
            for ob in bpy.data.objects:
                renamerename(ob)                  
        if tstool.renamermode =='SCENE':
            if tstool.renamertosceneactive:
                for ob in bpy.context.scene.objects:
                    renamerename(ob) 
            else:
                if tstool.renamertoscene != None:
                    for ob in tstool.renamertoscene.objects:
                        renamerename(ob) 
        if tstool.renamermode =='COLLECTION':
            if tstool.renamertocollectionactive:
                for ob in bpy.context.collection.objects:
                    renamerename(ob) 
            else:
                if tstool.renamertocollection != None:
                    for ob in tstool.renamertocollection.objects:
                        renamerename(ob)
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
        if tstool.renamerfrom =='ACTION' or tstool.renamerfrom =='MATERIAL' or tstool.renamertomaterial and acobjt in ['MESH','META','HAIR','CURVE','POINTCLOUD','SURFACE','GPENCIL','VOLUME'] or tstool.renamertoaction:
            row = layout.row(align=True)
        if tstool.renamerfrom =='MATERIAL' or tstool.renamertomaterial and acobjt in ['MESH','META','HAIR','CURVE','POINTCLOUD','SURFACE','GPENCIL','VOLUME']:
            row.template_ID(acobj, "active_material", new="material.new")
        if (tstool.renamerfrom =='ACTION' or tstool.renamertoaction) and (tstool.renamerfrom =='MATERIAL' or tstool.renamertomaterial and acobjt in ['MESH','META','HAIR','CURVE','POINTCLOUD','SURFACE','GPENCIL','VOLUME']):
            row.separator()
        if tstool.renamertoaction or tstool.renamerfrom =='ACTION':
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
        #row.prop_enum(tstool, "renamerfrom","OBJECT",icon='OBJECT_DATA')
        #row.prop_enum(tstool, "renamerfrom","DATABLOCK",icon=datablockicon)
        #row.prop_enum(tstool, "renamerfrom","ACTION",icon='ACTION')
        #row.prop_enum(tstool, "renamerfrom","MATERIAL",icon='MATERIAL')
        row = box.row(align=True)
        if tstool.renamerfrom == 'DATABLOCK':
            row.prop(tstool, "renamerfrom",text="",icon=datablockicon)
        else:
            row.prop(tstool, "renamerfrom",text="")
        row.label(icon='TRACKING_FORWARDS_SINGLE')
        if tstool.renamerfrom != 'DATABLOCK':
            row.prop(tstool, "renamertodatablock",text="",icon=datablockicon)
        if tstool.renamerfrom != 'OBJECT':
            row.prop(tstool, "renamertoobject",text="",icon='OBJECT_DATA')
        if tstool.renamerfrom != 'ACTION':
            row.prop(tstool, "renamertoaction",text="",icon='ACTION')
        if tstool.renamerfrom != 'MATERIAL':
            row.prop(tstool, "renamertomaterial",text="",icon='MATERIAL')

        if tstool.renamermode =='SCENE':
            if tstool.renamertosceneactive:
                row.prop(tstool, "renamertosceneactive",text="Active Scene",icon='PIVOT_ACTIVE')
            else:
                row.prop(tstool, "renamertoscene",text="",icon='SCENE_DATA')
                row.prop(tstool, "renamertosceneactive",text="",icon='PIVOT_ACTIVE')
        if tstool.renamermode =='COLLECTION':
            if tstool.renamertocollectionactive:
                row.prop(tstool, "renamertocollectionactive",text="Active Collection",icon='PIVOT_ACTIVE')
            else:
                row.prop(tstool, "renamertocollection",text="",icon='OUTLINER_COLLECTION')
                row.prop(tstool, "renamertocollectionactive",text="",icon='PIVOT_ACTIVE')
        
        if tstool.renamermode in ['COLLECTION','SCENE']:
            icononlyrename = True
        else:
            icononlyrename = False

        row.prop(tstool, "renamermode",text="",icon_only=icononlyrename)

        row = box.row(align=True)
        row.operator("ts_ops.renamercut",text="Rename",icon='SORTALPHA')

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

class TS_Datarenamer_PreferencesPanel(AddonPreferences):
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
        col.prop(self, "TSOVER", text="")


classes = (
    TS_E_Properties,
    TS_DATA_TOOLS_PNL,
    TS_DATA_TOOLS_PNL_POP,
    TS_Datarenamer_PreferencesPanel,
    TS_RENAMER,
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