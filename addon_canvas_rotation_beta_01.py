#addon Info
bl_info={
    "name":"Rotate Canvas",
    "desctiption":"Creates a new camera parented to the active one and a driver in Z rotation in order to rotate the camera canvas like. Usefull to 2D artist who want to start using Grease Pencil",
    "author":"Francisco Paez",
    "version":(0,1,0),
    "blender":(2,80,0),
    "location": "View3D > Tool Shelf > Addons Tab",
    "warning":"Very experimantal. Known bugs: Rotation property looks for an object called 'canvas' that doesen't exists before a canvas system is created. Planned Feautures: Flip canvas. Shortcut to the rotation. Reset function deletes keyframes",
    "wiki_url":"",
    "category":"Camera"
    }

import bpy
from bpy.types import Panel
from bpy import context



#classes


#operator01
class OBJECT_OT_createCameras(bpy.types.Operator):
    """Adds two cameras linked together"""
    bl_label="Create Camera and Canvas"
    bl_idname="cam.add_canvas"
    bl_options= {'REGISTER','UNDO'}
   
   
    #execution
    def execute(self,context):
        
        
     #GoToObjectMode
        MiObjeto=bpy.context.active_object
        MiModo= bpy.context.mode
        bpy.ops.object.mode_set(mode='OBJECT')
        
        #limpieza de otras instancias del addon
        for obj in bpy.context.scene.objects:
            if obj.name == 'canvas':
                obj.hide_select = False
                obj.name='excanvas'                
            elif obj.name =='Cam_anim':
                obj.name='excamAnim'
                
       
            
            
        bpy.ops.gpencil.paintmode_toggle()
        bpy.ops.object.camera_add( rotation=(1.5708, 0, 0))
        bpy.context.object.name = 'Cam_anim' 
        bpy.ops.object.camera_add( location=(0,0,0), rotation=(0, 0, 0))
        bpy.context.object.name = 'canvas'    
        bpy.ops.object.constraint_add(type='CHILD_OF')
        bpy.context.object.constraints["Child Of"].target = bpy.data.objects['Cam_anim']
        bpy.context.object.lock_location[0] = True
        bpy.context.object.lock_location[1] = True
        bpy.context.object.lock_location[2] = True
        bpy.context.object.lock_rotation[0] = True
        bpy.context.object.lock_rotation[1] = True
        bpy.context.scene.camera = bpy.data.objects['canvas']
        bpy.context.object.data.display_size = 2
        bpy.context.object.hide_select = True
       
         #volver al objeto seleccionado
        MiObjeto.select_set (state=True)
        bpy.context.view_layer.objects.active = MiObjeto
        bpy.ops.object.mode_set(mode=MiModo)


        
        return {'FINISHED'}
 


    
#operator02
class OBJECT_OT_createCanvas(bpy.types.Operator):
    """Cretes canvas from an existing one"""
    bl_label="Create Canvas"
    bl_idname="cam.add_canvas_for_cam"
    bl_options= {'REGISTER','UNDO'}
    
    
    #execution
    def execute(self,context):
        
        #GoToObjectMode
        MiObjeto=bpy.context.active_object
        MiModo= bpy.context.mode
        bpy.ops.object.mode_set(mode='OBJECT')
        
        #limpieza de otras instancias del addon
        for obj in bpy.context.scene.objects:
            if obj.name == 'canvas':
                obj.hide_select = False
                obj.name='excanvas'                
            elif obj.name =='Cam_anim':
                obj.name='excamAnim'
        
        
            
            
        bpy.ops.object.select_camera()
        bpy.context.object.name = 'Cam_anim' 
        bpy.ops.object.camera_add(location=(0,0,0), rotation=(0, 0, 0))
        bpy.context.object.name = 'canvas'    
        bpy.ops.object.constraint_add(type='CHILD_OF')
        bpy.context.object.constraints["Child Of"].target = bpy.data.objects['Cam_anim']
        bpy.context.object.lock_location[0] = True
        bpy.context.object.lock_location[1] = True
        bpy.context.object.lock_location[2] = True
        bpy.context.object.lock_rotation[0] = True
        bpy.context.object.lock_rotation[1] = True
        bpy.context.scene.camera = bpy.data.objects['canvas']
        bpy.data.objects['canvas'].select_set (state=True)
        bpy.context.view_layer.objects.active = bpy.data.objects['canvas']
        bpy.context.object.data.display_size = 2
        bpy.context.object.hide_select = True
       
       
        #volver al objeto seleccionado
        MiObjeto.select_set (state=True)
        bpy.context.view_layer.objects.active = MiObjeto
        bpy.ops.object.mode_set(mode=MiModo)
      
      



        
        return {'FINISHED'}


#operator03
class OBJECT_OT_resetRotation(bpy.types.Operator):
    """Adds two cameras linked togheter"""
    bl_label="Reset Rotation"
    bl_idname="camera.reset_rotacion"
    bl_options= {'REGISTER','UNDO'}
    
   
    #execution
    def execute(self,context):
        bpy.data.objects['canvas'].rotation_euler[2]=0
        return {'FINISHED'}



#panel 01
class PANEL_PT_AddCanvasPanel(Panel):
    """Add Canvas Panel"""
    #revisar la ubicacion en Blender2.8
    bl_label = 'Create Canvas'
    bl_idname = 'OBJECT_PT_CreateCanvas'
    bl_space_type = 'VIEW_3D'
    bl_region_type = "UI"
    bl_category = "Rotate Canvas"
    bl_label = "Create Canvas"
     
    #Agregar funcionalidad
    def draw(self, context):
       
        scene = context.scene
        layout = self.layout
        
       
        
          # Create a simple row.
        #layout.label(text="Create a Canvas")
         
        layout.operator(OBJECT_OT_createCanvas.bl_idname, text='Using existing Camera', icon="OUTLINER_OB_CAMERA")
        layout.operator(OBJECT_OT_createCameras.bl_idname, text='Create New Canvas', icon="PLUS")
        
        
       
#panel 02         
class PANEL_PT_RotateCanvasPanel(Panel):
    
    bl_label = 'Rotate Canvas'
    bl_idname = 'object_pt_RotateCanvas'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Rotate Canvas"
    bl_label = "Rotate Canvas"
     
    #Agregar funcionalidad
    def draw(self, context):
       
        scene = context.scene
        layout = self.layout
        canvas=bpy.data.objects['canvas']
       
        #layout.label(text=" Canvas Rotation:")
        row = layout.row(align=True)
        row.prop(canvas, "rotation_euler", index=2,text='rot')
        row.operator(OBJECT_OT_resetRotation.bl_idname, text='reset', icon="FILE_REFRESH")
       
       
#agregar boton en otras partes
def add_object_button(self,context):
    self.layout.operator(
            OBJECT_OT_createCameras.bl_idname,
            icon="OUTLINER_OB_CAMERA"          
            )
       

      


#register
def register():
    
     
    bpy.utils.register_class(OBJECT_OT_createCameras)
    bpy.utils.register_class(OBJECT_OT_createCanvas)
    bpy.utils.register_class(OBJECT_OT_resetRotation)
    bpy.utils.register_class(PANEL_PT_AddCanvasPanel)
    bpy.utils.register_class(PANEL_PT_RotateCanvasPanel)
   


    
#unregister
def unregister():
    
    bpy.utils.unregister_class(OBJECT_OT_createCameras)
    bpy.utils.unregister_class(OBJECT_OT_createCanvas)
    bpy.utils.unregister_class(OBJECT_OT_resetRotation)
    bpy.utils.unregister_class(PANEL_PT_AddCanvasPanel)
    bpy.utils.unregister_class(PANEL_PT_RotateCanvasPanel)
    
    

    

#Needed to run sctipt in Text Editor
if __name__ == '__main__':
    register()