import bpy
import os

bl_info = {
    "name": "Blender Icon List Viewer",
    "blender": (4, 2, 2),
    "category":"Fables Alive Games",
    "version": (2024, 10, 18),
    "author": "Fables Alive Games",
    "description": "Displays a list of icons from a file (icons.txt) located in the same folder as this add-on.",
    "location": "Text Editor > Fables Alive Games",
    "tracker_url": "",
    "support": "COMMUNITY",
}

class IconItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    icon: bpy.props.StringProperty()

class OBJECT_UL_icon_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        self.use_filter_show = True
        row = layout.row()
        row.label(text=item.name, icon=item.icon)
        row.operator("text.write_icon_name", text="📝").icon_name = item.name

class OBJECT_PT_icon_panel(bpy.types.Panel):
    bl_label = "Blender Icon List"
    bl_idname = "OBJECT_PT_icon_panel"
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Blender Icon List'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.template_list("OBJECT_UL_icon_list", "", scene, "icon_list", scene, "icon_list_index", rows=20)

class TEXT_OT_write_icon_name(bpy.types.Operator):
    bl_idname = "text.write_icon_name"
    bl_label = "Write Icon Name"
    
    icon_name: bpy.props.StringProperty()

    def execute(self, context):
        text = bpy.context.space_data.text
        if text is not None:
            text.write(f"\"{self.icon_name}\"")
            self.report({'INFO'}, f"Icon {self.icon_name} written to text editor.")
        else:
            self.report({'ERROR'}, "No active text editor found.")
        return {'FINISHED'}

def load_icons_from_file():
    icons_file_path = os.path.join(os.path.dirname(__file__), "icons.txt")
    try:
        if not os.path.exists(icons_file_path):
            return
        with open(icons_file_path, 'r', encoding='utf-8') as file:
            icons = [line.strip() for line in file if line.strip()]
        for icon in icons:
            item = bpy.context.scene.icon_list.add()
            item.name = icon
            item.icon = icon
    except Exception as e:
        print(f"Error: {e}")

def delayed_load_icons():
    bpy.app.timers.register(load_icons_from_file, first_interval=1.0)

def register():
    bpy.utils.register_class(IconItem)
    bpy.utils.register_class(OBJECT_UL_icon_list)
    bpy.utils.register_class(OBJECT_PT_icon_panel)
    bpy.utils.register_class(TEXT_OT_write_icon_name)
    bpy.types.Scene.icon_list = bpy.props.CollectionProperty(type=IconItem)
    bpy.types.Scene.icon_list_index = bpy.props.IntProperty()
    delayed_load_icons()

def unregister():
    bpy.utils.unregister_class(IconItem)
    bpy.utils.unregister_class(OBJECT_UL_icon_list)
    bpy.utils.unregister_class(OBJECT_PT_icon_panel)
    bpy.utils.unregister_class(TEXT_OT_write_icon_name)
    del bpy.types.Scene.icon_list
    del bpy.types.Scene.icon_list_index

if __name__ == "__main__":
    register()
