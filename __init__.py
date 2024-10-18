import bpy
import os

bl_info = {
    "name": "Blender Icon List Viewer",
    "blender": (4, 2, 2),
    "category":"Fables Alive Games",
    "version": (2024,10,18),
    "author": "Fables Alive Games",
    "description": "Displays a list of icons from a file (icons.txt) located in the same folder as this add-on.",
    "location": "3D View > Fables Alive Games",
    "tracker_url": "",
    "support": "COMMUNITY",
}

# Veri depolamak için bir sınıf oluşturuyoruz
class IconItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()  # Simgenin adı
    icon: bpy.props.StringProperty()  # Simgenin simge adı

class OBJECT_UL_icon_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        self.use_filter_show=True
        # Liste içinde her bir simgeyi ve adını göster
        layout.label(text=item.name, icon=item.icon)

class OBJECT_PT_icon_panel(bpy.types.Panel):
    bl_label = "Blender Icon List"
    bl_idname = "OBJECT_PT_icon_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Fables Alive Games'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Listbox gösterimi için template_list kullanıyoruz
        layout.template_list("OBJECT_UL_icon_list", "", scene, "icon_list", scene, "icon_list_index",rows=20)

def load_icons_from_file():
    # Dosya yolunu dinamik olarak ayarlama (icons.txt)
    icons_file_path = os.path.join(os.path.dirname(__file__), "icons.txt")  # _init_.py ile aynı dizin

    # Dosya yolunu kontrol et
    #print(f"File Path: {icons_file_path}")

    try:
        # Dosya olup olmadığını kontrol et
        if os.path.exists(icons_file_path):
            print(f"File Found: {icons_file_path}")
        else:
            print(f"File not found: {icons_file_path}")
            return

        # Dosyayı oku
        with open(icons_file_path, 'r', encoding='utf-8') as file:
            icons = [line.strip() for line in file if line.strip()]  # Boş satırları atla
            print(f"İkonlar yüklendi: {icons}")

        # İkonları sahneye ekle
        for icon in icons:
            item = bpy.context.scene.icon_list.add()
            item.name = icon
            item.icon = icon

    except FileNotFoundError:
        print(f"Dosya bulunamadı: {icons_file_path}")

    except Exception as e:
        print(f"Hata: {e}")

    return None

def delayed_load_icons():
    """İkonları dosyadan yüklemeyi biraz geciktir."""
    bpy.app.timers.register(load_icons_from_file, first_interval=1.0)  # 1 saniye gecikme ekliyoruz

def register():
    try:
        bpy.utils.register_class(IconItem)
        bpy.utils.register_class(OBJECT_UL_icon_list)
        bpy.utils.register_class(OBJECT_PT_icon_panel)

        # Sahne özelliklerine yeni veri tipi ekliyoruz
        bpy.types.Scene.icon_list = bpy.props.CollectionProperty(type=IconItem)
        bpy.types.Scene.icon_list_index = bpy.props.IntProperty()

        # Gecikmeli ikon yükleme
        delayed_load_icons()

    except Exception as e:
        print(f"Register sırasında hata oluştu: {e}")

def unregister():
    try:
        bpy.utils.unregister_class(IconItem)
        bpy.utils.unregister_class(OBJECT_UL_icon_list)
        bpy.utils.unregister_class(OBJECT_PT_icon_panel)

        del bpy.types.Scene.icon_list
        del bpy.types.Scene.icon_list_index

    except Exception as e:
        print(f"Unregister sırasında hata oluştu: {e}")

if __name__ == "__main__":
    register()
