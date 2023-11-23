import os
import sys

import c4d
from c4d import plugins, gui, storage, documents
import maxon

REAWOTE_SORTER_ID=1060870

dialog = None

checkbox_list = []
same_path_dirs = []
material_to_add = []
materialCount = []
child_id_list = []
child_name_list = []
map_id_list = []
material_id_list = []
material_name_list = []
selected_materials = []
selected_maps = []
selected_files = []
selected_paths = []
tex_list = []
folder_path_list = []
uploaded_indexes = []
uploaded_files = []
uploaded_maps = []
uploaded_paths = []
map_names_list = ["AO_Ambient occlusion", "NRM_Normal map", "DISP_Displacement", "DIFF_Diffuse","COL_Color", "GLOSS_Glossiness", "ROUGH_Roughness", "METAL_Metallic", "SPEC_Specular", "SSS_Subsurface scattering", "SSSABSORB_SSS absorbtion", "OPAC_Opacit", "ANIS_Anisotropy", "SHEEN_Sheen"]    
newID = 0
count = 1
path = " "

ID_CHECKBOX = 999
ID_NAME = 998
ID_MAP_NAME = 997
ID_MATERIAL_NAME = 996
ID_CHILD = 9000

IDS_REAWOTE_PBR_CONVERTER = 20000
IDS_DIALOG_BROWSE = 10001
IDS_DIALOG_TEXTURE_FOLDER = 10002

IDS_DIALOG_MAIN_GROUP = 10014
IDS_DIALOG_SCROLL_GROUP = 10012
IDS_DIALOG_SCROLL_GROUP_TWO = 10016
IDS_DIALOG_SECONDARY_GROUP = 10015
IDS_DIALOG_LIST_CHECKBOX = 10011
IDS_DIALOG_LIST_BUTTON = 10017
IDS_DIALOG_SELECT_ALL_BUTTON = 10018
IDS_DIALOG_FOLDER_LIST = 10013

IDS_DIALOG_INCLUDE_AO = 10003
IDS_DIALOG_INCLUDE_DISPLACEMENT = 10004
IDS_DIALOG_USE_16_BIT_DISPLACEMENT_MAPS = 10005
IDS_DIALOG_LOAD = 10006
IDS_DIALOG_USE_16_BIT_NORMAL_MAPS = 10007

class ID(): 
    DIALOG_FOLDER_GROUP = 100000
    DIALOG_FOLDER_TEXT =  100001
    DIALOG_FOLDER_BUTTON = 100002
    # TODO zde pridat textove pole se slozkama

    DIALOG_MAIN_GROUP = 100014
    DIALOG_SECONDARY_GROUP = 100019
    DIALOG_SCROLL_GROUP = 100012
    DIALOG_SCROLL_GROUP_TWO = 100016
    DIALOG_SECONDARY_GROUP = 10011
    DIALOG_FOLDER_LIST = 100015
    FILTER_MATERIALS_BUTTON = 100017

    DIALOG_GROUP4_BUTTONS = 100038
    DIALOG_ADD_TO_LIST_BUTTON = 100030
    DIALOG_LIST_CHECKBOX = 100013
    
    DIALOG_MAP_AO_CB = 100003
    DIALOG_MAP_DISPL_CB = 100004
    DIALOG_MAP_16B_DISPL_CB = 100005
    DIALOG_MAP_IOR_CB = 100006
    DIALOG_LOAD_BUTTON = 100007
    DIALOG_ERROR = 100008
    DIALOG_MAP_16B_NORMAL_CB = 100009

    DIALOG_GROUP_DROPBOXES = 1000200
    DIALOG_DROPBOX_BUTTON1= 100021
    DIALOG_DROPBOX_BUTTON2 = 100022
    DIALOG_DROPBOX_MAIN = 100023

    DIALOG_GROUP2_DOPBOXES = 100024
    DIALOG_TEXT2_DROPBOX = 100029
    DIALOG_DROPBOX_MAIN2 = 100025

    DIALOG_GROUP3_DOPBOXES = 100027
    DIALOG_TEXT_DROPBOX = 100028
    DIALOG_NEXT_MATERIAL_BUTTON = 100035
    DIAlOG_PREVIOUS_MATERIAL_BUTTON = 100036
    DIALOG_DROPBOX_MAIN3 = 100026

    DIALOG_GROUP_MINI_BUTTONS = 100031
    DIALOG_SELECT_ALL_BUTTON = 100018
    DIALOG_ADD_TO_QUEUE_BUTTON = 100032
    DIALOG_DELETE_BUTTON = 100033

    DIALOG_CB_GROUP = 100034

    DIALOG_GROUP_RENDERER = 100037
    DIALOG_RENDERER_TEXT = 100038
    DIALOG_SETTINGS_BUTTON = 100039
    DIALOG_RENDERER_COMBOBOX = 100040

    ID_CHILD = 9000

    MATERIAL_PREVIEW = 800

    # Todo: generate this with swig
    PLUGINID_CORONA4D_MATERIAL = 1032100
    PLUGINID_CORONA4D_NORMALSHADER = 1035405
    PLUGINID_CORONA4D_AOSHADER = 1034433

    CORONA_MATERIAL_PREVIEWSIZE = 4050
    CORONA_MATERIAL_PREVIEWSIZE_1024 = 10

    CORONA_DIFFUSE_TEXTURE = 4301
    CORONA_NORMALMAP_TEXTURE = 11321

    CORONA_MATERIAL_BUMPMAPPING = 4108
    CORONA_BUMPMAPPING_STRENGTH = 4850
    CORONA_BUMPMAPPING_TEXTURE = 4851

    CORONA_MATERIAL_DISPLACEMENT = 4106
    CORONA_DISPLACEMENT_TEXTURE = 4802
    CORONA_DISPLACEMENT_MIN_LEVEL = 4800
    CORONA_DISPLACEMENT_MAX_LEVEL = 4801

    CORONA_AO_UNOCCLUDED_TEXTURE = 11021
    CORONA_AO_CALCULATE_FROM = 11007
    CORONA_AO_CALCULATE_FROM_BOTH = 2

    CORONA_MATERIAL_ALPHA = 4109
    CORONA_ALPHA_TEXTURE = 4751

    CORONA_REFLECT_GLOSSINESS_TEXTURE = 4512

    CORONA_MATERIAL_REFLECT = 4103
    CORONA_REFLECT_TEXTURE = 4501

    CORONA_MATERIAL_VOLUME = 4110
    CORONA_VOLUME_SCATTER_TEXTURE = 4681
    CORONA_VOLUME_ABSORPTION_TEXTURE = 4631

    CORONA_REFLECT_FRESNELLOR_VALUE = 4541
    CORONA_REFLECT_FRESNELLOR_TEXTURE = 4542

    
    CORONA_STR_MATERIAL_PHYSICAL = 1056306
    CORONA_PHYSICAL_MATERIAL_HEADER = 20000

    CORONA_PHYSICAL_MATERIAL_GENERAL         = 20001
    CORONA_PHYSICAL_MATERIAL_BASE_LAYER      = 20002
    CORONA_PHYSICAL_MATERIAL_REFRACT         = 20003
    CORONA_PHYSICAL_MATERIAL_ALPHA           = 20004
    CORONA_PHYSICAL_MATERIAL_DISPLACEMENT    = 20005
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT       = 20006
    CORONA_PHYSICAL_MATERIAL_SHEEN           = 20007
    CORONA_PHYSICAL_MATERIAL_VOLUMETRICS     = 20008
    CORONA_PHYSICAL_MATERIAL_SSS             = 20009
    CORONA_PHYSICAL_MATERIAL_EMISSION        = 20010
    CORONA_PHYSICAL_MATERIAL_THIN_ABSORPTION = 20012
    CORONA_PHYSICAL_MATERIAL_TRANSLUCENCY    = 20013

    ID_CORONA_PHYSICAL_MATERIAL_GENERAL         = 20051
    ID_CORONA_PHYSICAL_MATERIAL_BASE_LAYER      = 20052
    ID_CORONA_PHYSICAL_MATERIAL_REFRACT         = 20053
    ID_CORONA_PHYSICAL_MATERIAL_ALPHA           = 20054
    ID_CORONA_PHYSICAL_MATERIAL_DISPLACEMENT    = 20055
    ID_CORONA_PHYSICAL_MATERIAL_CLEARCOAT       = 20056
    ID_CORONA_PHYSICAL_MATERIAL_SHEEN           = 20057
    ID_CORONA_PHYSICAL_MATERIAL_VOLUMETRICS     = 20058
    ID_CORONA_PHYSICAL_MATERIAL_SSS             = 20059
    ID_CORONA_PHYSICAL_MATERIAL_EMISSION        = 20060
    ID_CORONA_PHYSICAL_MATERIAL_THIN_ABSORPTION = 20062
    ID_CORONA_PHYSICAL_MATERIAL_TRANSLUCENCY    = 20063

    CORONA_PHYSICAL_MATERIAL_METALLIC_MODE            = 20101
    CORONA_PHYSICAL_MATERIAL_METALLIC_MODE_VALUE      = 20102
    CORONA_PHYSICAL_MATERIAL_METALLIC_MODE_METALLIC   = 0
    CORONA_PHYSICAL_MATERIAL_METALLIC_MODE_DIELECTRIC = 1
    CORONA_PHYSICAL_MATERIAL_METALLIC_MODE_TEXTURE    = 20103

    CORONA_PHYSICAL_MATERIAL_PRESET           = 20104
    CORONA_PHYSICAL_MATERIAL_PRESET_NO_PRESET = 0 #Used when any presetable param is changed by the user
    CORONA_PHYSICAL_MATERIAL_PRESET_DEFAULT = 1 #Default settings


    CORONA_PHYSICAL_MATERIAL_BASE_COLOR                 = 20201
    CORONA_PHYSICAL_MATERIAL_BASE_COLOR_TEXTURE         = 20202
    CORONA_PHYSICAL_MATERIAL_BASE_COLOR_LEVEL           = 20203
    CORONA_PHYSICAL_MATERIAL_BASE_COLOR_MIX_VALUE       = 20204
    CORONA_PHYSICAL_MATERIAL_BASE_COLOR_MIX_MODE        = 20205
    CORONA_PHYSICAL_MATERIAL_BASE_ROUGHNESS             = 20207
    CORONA_PHYSICAL_MATERIAL_BASE_ROUGHNESS_VALUE       = 20208
    CORONA_PHYSICAL_MATERIAL_BASE_ROUGHNESS_TEXTURE     = 20209
    CORONA_PHYSICAL_MATERIAL_BASE_IOR                   = 20210
    CORONA_PHYSICAL_MATERIAL_BASE_IOR_VALUE             = 20211
    CORONA_PHYSICAL_MATERIAL_BASE_IOR_TEXTURE           = 20212
    CORONA_PHYSICAL_MATERIAL_BASE_EDGECOLOR             = 20226
    CORONA_PHYSICAL_MATERIAL_BASE_EDGECOLOR_COLOR       = 20227
    CORONA_PHYSICAL_MATERIAL_BASE_EDGECOLOR_TEXTURE     = 20228
    CORONA_PHYSICAL_MATERIAL_BASE_EDGECOLOR_LEVEL       = 20229
    CORONA_PHYSICAL_MATERIAL_BASE_EDGECOLOR_MIX_VALUE   = 20230
    CORONA_PHYSICAL_MATERIAL_BASE_EDGECOLOR_MIX_MODE    = 20231
    CORONA_PHYSICAL_MATERIAL_BASE_BUMPMAPPING           = 20216
    CORONA_PHYSICAL_MATERIAL_BASE_BUMPMAPPING_VALUE     = 20217
    CORONA_PHYSICAL_MATERIAL_BASE_BUMPMAPPING_TEXTURE   = 20218
    CORONA_PHYSICAL_MATERIAL_BASE_BUMPMAPPING_ENABLE    = 20225
    CORONA_PHYSICAL_MATERIAL_BASE_ANISOTROPY            = 20219
    CORONA_PHYSICAL_MATERIAL_BASE_ANISOTROPY_VALUE      = 20220
    CORONA_PHYSICAL_MATERIAL_BASE_ANISOTROPY_TEXTURE    = 20221
    CORONA_PHYSICAL_MATERIAL_BASE_ANISOROTATION         = 20222
    CORONA_PHYSICAL_MATERIAL_BASE_ANISOROTATION_VALUE   = 20223
    CORONA_PHYSICAL_MATERIAL_BASE_ANISOROTATION_TEXTURE = 20224

    CORONA_PHYSICAL_MATERIAL_TRANSLUCENCY_FRACTION         = 21307
    CORONA_PHYSICAL_MATERIAL_TRANSLUCENCY_FRACTION_VALUE   = 21308
    CORONA_PHYSICAL_MATERIAL_TRANSLUCENCY_FRACTION_TEXTURE = 21309
    CORONA_PHYSICAL_MATERIAL_TRANSLUCENCY_COLOR_TITLE      = 21301
    CORONA_PHYSICAL_MATERIAL_TRANSLUCENCY_COLOR            = 21302
    CORONA_PHYSICAL_MATERIAL_TRANSLUCENCY_TEXTURE          = 21303
    CORONA_PHYSICAL_MATERIAL_TRANSLUCENCY_LEVEL            = 21304
    CORONA_PHYSICAL_MATERIAL_TRANSLUCENCY_MIX_VALUE        = 21305
    CORONA_PHYSICAL_MATERIAL_TRANSLUCENCY_MIX_MODE         = 21306

    CORONA_PHYSICAL_MATERIAL_REFRACT_AMOUNT           = 20301
    CORONA_PHYSICAL_MATERIAL_REFRACT_AMOUNT_VALUE     = 20302
    CORONA_PHYSICAL_MATERIAL_REFRACT_AMOUNT_TEXTURE   = 20303
    CORONA_PHYSICAL_MATERIAL_REFRACT_BEHAVIOR         = 20311
    CORONA_PHYSICAL_MATERIAL_REFRACT_CAUSTICS         = 20312
    CORONA_PHYSICAL_MATERIAL_REFRACT_THIN             = 20313
    CORONA_PHYSICAL_MATERIAL_REFRACT_DISPERSION       = 20314
    CORONA_PHYSICAL_MATERIAL_REFRACT_DISPERSION_VALUE = 20315
    CORONA_PHYSICAL_MATERIAL_REFRACT_ABBE_NUMBER      = 20316

    CORONA_PHYSICAL_MATERIAL_ALPHA_COLOR     = 20401
    CORONA_PHYSICAL_MATERIAL_ALPHA_TEXTURE   = 20402
    CORONA_PHYSICAL_MATERIAL_ALPHA_LEVEL     = 20403
    CORONA_PHYSICAL_MATERIAL_ALPHA_MIX_VALUE = 20404
    CORONA_PHYSICAL_MATERIAL_ALPHA_MIX_MODE  = 20405
    CORONA_PHYSICAL_MATERIAL_ALPHA_CLIP      = 20407

    CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_MIN_LEVEL           = 20501
    CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_MAX_LEVEL           = 20502
    CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_TEXTURE             = 20503
    CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_WATER_LEVEL_ENABLE  = 20504
    CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_WATER_LEVEL         = 20505
    CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_MODE                = 20506
    CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_MODE_NORMAL         = 0
    CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_MODE_VECTOR_TANGENT = 1
    CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_MODE_VECTOR_OBJECT  = 2

    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_AMOUNT               = 20601
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_AMOUNT_VALUE         = 20602
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_AMOUNT_TEXTURE       = 20603
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_ROUGHNESS            = 20604
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_ROUGHNESS_VALUE      = 20605
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_ROUGHNESS_TEXTURE    = 20606
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_IOR                  = 20607
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_IOR_VALUE            = 20608
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_IOR_TEXTURE          = 20609
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_ABSORPTION           = 20610
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_ABSORPTION_COLOR     = 20611
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_ABSORPTION_TEXTURE   = 20612
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_ABSORPTION_LEVEL     = 20613
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_ABSORPTION_MIX_VALUE = 20614
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_ABSORPTION_MIX_MODE  = 20615
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_BUMPMAPPING          = 20617
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_BUMPMAPPING_VALUE    = 20618
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_BUMPMAPPING_TEXTURE  = 20619
    CORONA_PHYSICAL_MATERIAL_CLEARCOAT_BUMPMAPPING_ENABLE   = 20620


    CORONA_PHYSICAL_MATERIAL_SHEEN_AMOUNT            = 20701
    CORONA_PHYSICAL_MATERIAL_SHEEN_AMOUNT_VALUE      = 20702
    CORONA_PHYSICAL_MATERIAL_SHEEN_AMOUNT_TEXTURE    = 20703
    CORONA_PHYSICAL_MATERIAL_SHEEN_ROUGHNESS         = 20704
    CORONA_PHYSICAL_MATERIAL_SHEEN_ROUGHNESS_VALUE   = 20705
    CORONA_PHYSICAL_MATERIAL_SHEEN_ROUGHNESS_TEXTURE = 20706
    CORONA_PHYSICAL_MATERIAL_SHEEN_COLOR             = 20707
    CORONA_PHYSICAL_MATERIAL_SHEEN_COLOR_VALUE       = 20708
    CORONA_PHYSICAL_MATERIAL_SHEEN_COLOR_TEXTURE     = 20709
    CORONA_PHYSICAL_MATERIAL_SHEEN_COLOR_LEVEL       = 20710
    CORONA_PHYSICAL_MATERIAL_SHEEN_COLOR_MIX_VALUE   = 20711
    CORONA_PHYSICAL_MATERIAL_SHEEN_COLOR_MIX_MODE    = 20712

    CORONA_PHYSICAL_MATERIAL_VOLUME_MODE_VOLUMETRIC        = 20801
    CORONA_PHYSICAL_MATERIAL_VOLUME_MODE_SSS               = 20802
    CORONA_PHYSICAL_MATERIAL_VOLUME_ABSORPTION             = 20803
    CORONA_PHYSICAL_MATERIAL_VOLUME_ABSORPTION_COLOR       = 20804
    CORONA_PHYSICAL_MATERIAL_VOLUME_ABSORPTION_TEXTURE     = 20805
    CORONA_PHYSICAL_MATERIAL_VOLUME_ABSORPTION_LEVEL       = 20806
    CORONA_PHYSICAL_MATERIAL_VOLUME_ABSORPTION_MIX_VALUE   = 20807
    CORONA_PHYSICAL_MATERIAL_VOLUME_ABSORPTION_MIX_MODE    = 20808
    CORONA_PHYSICAL_MATERIAL_VOLUME_ABSORPTION_DISTANCE    = 20810
    CORONA_PHYSICAL_MATERIAL_VOLUME_SCATTER                = 20811
    CORONA_PHYSICAL_MATERIAL_VOLUME_SCATTER_COLOR          = 20812
    CORONA_PHYSICAL_MATERIAL_VOLUME_SCATTER_TEXTURE        = 20813
    CORONA_PHYSICAL_MATERIAL_VOLUME_SCATTER_LEVEL          = 20814
    CORONA_PHYSICAL_MATERIAL_VOLUME_SCATTER_MIX_VALUE      = 20815
    CORONA_PHYSICAL_MATERIAL_VOLUME_SCATTER_MIX_MODE       = 20816
    CORONA_PHYSICAL_MATERIAL_VOLUME_SCATTER_DIRECTIONALITY = 20818
    CORONA_PHYSICAL_MATERIAL_VOLUME_SCATTER_SINGLE         = 20819
    CORONA_PHYSICAL_MATERIAL_VOLUME_SCATTER_OTHER          = 20821

    CORONA_PHYSICAL_MATERIAL_VOLUME_SSS_FRACTION         = 20901
    CORONA_PHYSICAL_MATERIAL_VOLUME_SSS_FRACTION_VALUE   = 20902
    CORONA_PHYSICAL_MATERIAL_VOLUME_SSS_FRACTION_TEXTURE = 20903
    CORONA_PHYSICAL_MATERIAL_VOLUME_SSS_RADIUS           = 20904
    CORONA_PHYSICAL_MATERIAL_VOLUME_SSS_RADIUS_VALUE     = 20905
    CORONA_PHYSICAL_MATERIAL_VOLUME_SSS_RADIUS_TEXTURE   = 20906
    CORONA_PHYSICAL_MATERIAL_VOLUME_SSS                  = 20907
    CORONA_PHYSICAL_MATERIAL_VOLUME_SSS_BLEED            = 20908
    CORONA_PHYSICAL_MATERIAL_VOLUME_SSS_TEXTURE          = 20909
    CORONA_PHYSICAL_MATERIAL_VOLUME_SSS_LEVEL            = 20910
    CORONA_PHYSICAL_MATERIAL_VOLUME_SSS_MIX_VALUE        = 20911
    CORONA_PHYSICAL_MATERIAL_VOLUME_SSS_MIX_MODE         = 20912

    CORONA_PHYSICAL_MATERIAL_EMISSION_COLOR_LEVEL     = 21004
    CORONA_PHYSICAL_MATERIAL_EMISSION_COLOR_MIX_VALUE = 21005
    CORONA_PHYSICAL_MATERIAL_EMISSION_COLOR_MIX_MODE  = 21006
    CORONA_PHYSICAL_MATERIAL_SELFILLUM_NOTE           = 21008

    CORONA_PHYSICAL_MATERIAL_ROUGHNESS_MODE            = 21101
    CORONA_PHYSICAL_MATERIAL_ROUGHNESS_MODE_ROUGHNESS  = 0
    CORONA_PHYSICAL_MATERIAL_ROUGHNESS_MODE_GLOSSINESS = 1

    CORONA_PHYSICAL_MATERIAL_IOR_MODE          = 21109
    CORONA_PHYSICAL_MATERIAL_IOR_MODE_IOR      = 0
    CORONA_PHYSICAL_MATERIAL_IOR_MODE_SPECULAR = 1

    CORONA_PHYSICAL_MATERIAL_COMPLEX_IOR         = 21102
    CORONA_PHYSICAL_MATERIAL_COMPLEX_IOR_ENABLED = 21103
    CORONA_PHYSICAL_MATERIAL_COMPLEX_IOR_R       = 21104
    CORONA_PHYSICAL_MATERIAL_COMPLEX_IOR_G       = 21105
    CORONA_PHYSICAL_MATERIAL_COMPLEX_IOR_B       = 21106
    CORONA_PHYSICAL_MATERIAL_COMPLEX_IOR_ETA     = 21107
    CORONA_PHYSICAL_MATERIAL_COMPLEX_IOR_KAPPA   = 21108

    CORONA_PHYSICAL_MATERIAL_BASE_TAIL         = 21400
    CORONA_PHYSICAL_MATERIAL_BASE_TAIL_VALUE   = 21401
    CORONA_PHYSICAL_MATERIAL_BASE_TAIL_TEXTURE = 21402

    CORONA_PHYSICAL_MATERIAL_ABSORPTION_COLOR     = 21201
    CORONA_PHYSICAL_MATERIAL_ABSORPTION_TEXTURE   = 21202
    CORONA_PHYSICAL_MATERIAL_ABSORPTION_LEVEL     = 21203
    CORONA_PHYSICAL_MATERIAL_ABSORPTION_MIX_VALUE = 21204
    CORONA_PHYSICAL_MATERIAL_ABSORPTION_MIX_MODE  = 21205

    _CORONA_PHYSICAL_MATERIAL_REFRACT_ABSORPTION_COLOR     = 20305
    _CORONA_PHYSICAL_MATERIAL_REFRACT_ABSORPTION_TEXTURE   = 20306
    _CORONA_PHYSICAL_MATERIAL_REFRACT_ABSORPTION_MIX_VALUE = 20308
    _CORONA_PHYSICAL_MATERIAL_REFRACT_ABSORPTION_MIX_MODE  = 20309

    # xnormalshader.h
    CORONA_NORMALMAP_TEXTURE = 11321
    CORONA_NORMALMAP_ = 11319
    CORONA_NORMALMAP_MODE = 11301
    CORONA_NORMALMAP_MODE_TANGENT = 0
    CORONA_NORMALMAP_MODE_OBJECT = 1
    CORONA_NORMALMAP_MODE_WORLD = 2
    CORONA_NORMALMAP_FLIP_R = 11311
    CORONA_NORMALMAP_FLIP_G = 11312
    CORONA_NORMALMAP_FLIP_B = 11313
    CORONA_NORMALMAP_SWAP_RG = 11317
    CORONA_NORMALMAP_BUMP = 11330
    CORONA_NORMALMAP_BUMP_STRENGTH = 11331
    CORONA_NORMALMAP_BUMP_TEXTURE = 11332
    CORONA_NORMALMAP_NOTE = 11338
    CORONA_NORMALMAP_NOTE2 = 11339
    CORONA_NORMALMAP_CUSTOM_UVW_OVERRIDE = 11341
    CORONA_NORMALMAP_CUSTOM_UVW_CHANNEL = 11342

    OCTANE_MATERIAL = 1029501
    OCTANE_BSDF_MODEL = 2585
    OCTANE_BITMAP = 5833
    OCTANE_TEXTURE = 1029508
    OCTANE_MULTIPLY = 1029516
    OCTANE_DISPLACEMENT = 1031901

class MaterialPreview(c4d.gui.GeUserArea):
    def __init__(self, bmp):
      super(MaterialPreview, self).__init__()
      self._bmp = bmp

    def DrawMsg(self, x1, y1, x2, y2, msg):
      #self.DrawSetPen(c4d.Vector(0))
      #self.DrawRectangle(0, 0, 42, 42)
      if not self._bmp: return

      coords = self.Local2Global()
      self.DrawBitmap(self._bmp, 0, 0, 42, 42, 0, 0, 42, 42, c4d.BMP_NORMAL | c4d.BMP_ALLOWALPHA)

    def GetMinSize(self):
      return 42, 42

    def setBitmap(self, bmp):
      self._bmp = bmp

class TextureObject(object):
    texturePath = "TexPath"
    mapNameData = ""
    material_nameData = ""
    materialData = "MatData"
    mapsData = "MapData"
    _selected = False

    def __init__(self, texturePath, mapNameData, material_nameData):
        self.texturePath = texturePath
        self.materialData+= texturePath
        self.mapsData = texturePath
        self.mapNameData = mapNameData
        self.material_nameData = material_nameData
        # self.selectedEntry = None

    @property
    def IsSelected(self):
        return self._selected
 
    def Select(self):
        self._selected = True
 
    def Deselect(self):
        self._selected = False
 
    def __repr__(self):
        return str(self)
 
    def __str__(self):
        return self.texturePath


class ListView(c4d.gui.TreeViewFunctions):
 
    def __init__(self):
        self.listOfTexture = list()
        self.maps = list()
        # self.selectedEntry = 1003
 
    def IsResizeColAllowed(self, root, userdata, lColID):
        return True
 
    def IsTristate(self, root, userdata):
        return False
 
    def GetColumnWidth(self, root, userdata, obj, col, area):
        return 55  # All have the same initial width
 
    def IsMoveColAllowed(self, root, userdata, lColID):
        return True
 
    def GetFirst(self, root, userdata):
        rValue = None if not self.listOfTexture else self.listOfTexture[0]
        return rValue
 
    def GetDown(self, root, userdata, obj):
        return None
 
    def GetNext(self, root, userdata, obj):
        rValue = None
        currentObjIndex = self.listOfTexture.index(obj)
        nextIndex = currentObjIndex + 1
        if nextIndex < len(self.listOfTexture):
            rValue = self.listOfTexture[nextIndex]
 
        return rValue

    def GetPred(self, root, userdata, obj):
        rValue = None
        currentObjIndex = self.listOfTexture.index(obj)
        predIndex = currentObjIndex - 1
        if 0 <= predIndex < len(self.listOfTexture):
            rValue = self.listOfTexture[predIndex]
 
        return rValue
 
    def GetId(self, root, userdata, obj):
        return hash(obj)
 
    def Select(self, root, userdata, obj, mode):
        if mode == c4d.SELECTION_NEW:
            for tex in self.listOfTexture:
                tex.Deselect()
            obj.Select()
        elif mode == c4d.SELECTION_ADD:
            obj.Select()
        elif mode == c4d.SELECTION_SUB:
            obj.Deselect()
 
    def IsSelected(self, root, userdata, obj):
        return obj.IsSelected
 
    def SetCheck(self, root, userdata, obj, column, checked, msg):
        if checked:
            obj.Select()
        else:
            obj.Deselect()
 
    def IsChecked(self, root, userdata, obj, column):
        if obj.IsSelected:
            return c4d.LV_CHECKBOX_CHECKED | c4d.LV_CHECKBOX_ENABLED
        else:
            return c4d.LV_CHECKBOX_ENABLED
 
    def GetName(self, root, userdata, obj):
        return str(obj) # Or obj.texturePath
 
    def DrawCell(self, root, userdata, obj, col, drawinfo, bgColor):
        if col == ID_MAP_NAME:
            name = obj.mapNameData
            geUserArea = drawinfo["frame"]
            w = geUserArea.DrawGetTextWidth(name)
            h = geUserArea.DrawGetFontHeight()
            xpos = drawinfo["xpos"]
            ypos = drawinfo["ypos"] + drawinfo["height"]
            drawinfo["frame"].DrawText(name, int(xpos), int(ypos - h * 1.1))

        if col == ID_MATERIAL_NAME:
            name = obj.material_nameData
            geUserArea = drawinfo["frame"]
            w = geUserArea.DrawGetTextWidth(name)
            h = geUserArea.DrawGetFontHeight()
            xpos = drawinfo["xpos"]
            ypos = drawinfo["ypos"] + drawinfo["height"]
            drawinfo["frame"].DrawText(name, int(xpos), int(ypos - h * 1.1))
 
    def DoubleClick(self, root, userdata, obj, col, mouseinfo):
        c4d.gui.MessageDialog("You clicked on " + str(obj))
        return True
 
    def DeletePressed(self, root, userdata):
        "Called when a delete event is received."
        for tex in reversed(self.listOfTexture):
            if tex.IsSelected:
                id_tex = self.listOfTexture.index(tex)
                print("Odstranuju tento index: ", id_tex)
                selected_maps.pop(id_tex)
                print(selected_maps)
                selected_materials.pop(id_tex)
                print(selected_materials)
                selected_files.pop(id_tex)
                print(selected_files)
                selected_paths.pop(id_tex)
                print(selected_paths)
                self.listOfTexture.remove(tex)
                tex_list.pop(id_tex)
    
    # map_names_list = ["AO_Ambient occlusion", "NRM_Normal map", "DISP_Displacement", "DIFF_Diffuse","COL_Color", "GLOSS_Glossiness", "ROUGH_Roughness", "METAL_Metallic", "SPEC_Specular", "SSS_Subsurface scattering", "SSSABSORB_SSS absorbtion", "OPAC_Opacit", "ANIS_Anisotropy", "SHEEN_Sheen"]    

    def GetDropDownMenu(self, root, userdata, obj, lColumn, menuInfo):
        doc = c4d.documents.GetActiveDocument()

    def SetDropDownMenu(self, root, userdata, obj, lColumn, entry):
        # self.selectedEntry = entry
        print(f"User selected the entry with the ID: {entry}")

class ReawoteSorterDialog(gui.GeDialog):
    has16bDisp = False
    has16bNormal = False
    hasDisp = False
    hasAO = False
    hasIor = False
    materialFolder = None   
    path = ""

    _treegui = None
    _listView = ListView()

    def __init__(self):
        self._area = MaterialPreview(None)
        self.MaterialPreviewBmp = c4d.bitmaps.BaseBitmap()
        self.MaterialPreviewBmpTmp = c4d.bitmaps.BaseBitmap()
        self.MaterialPreviewBmp.Init(42, 42)
        super(ReawoteSorterDialog, self).__init__()
        pass

    def CreateLayout(self):
        defaultFlags: int = c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT

        self.SetTitle("Reawote Sorter")

        self.ScrollGroupBegin(ID.DIALOG_SCROLL_GROUP, defaultFlags, c4d.SCROLLGROUP_VERT | c4d.SCROLLGROUP_HORIZ)
        self.GroupBegin(ID.DIALOG_MAIN_GROUP, defaultFlags, 1)

        self.GroupBegin(ID.DIALOG_FOLDER_GROUP, c4d.BFH_SCALEFIT, 2, 1, "Material folder", 0, 10, 10)
        self.GroupBorderSpace(8, 0, 0, 2)
        self.AddStaticText(ID.DIALOG_FOLDER_TEXT, c4d.BFH_SCALEFIT, 0, 0, "Material folder", 0)
        self.AddButton(ID.DIALOG_FOLDER_BUTTON, c4d.BFH_SCALEFIT, 1, 1, "Browse")
        self.GroupEnd()

        self.GroupBegin(ID.DIALOG_GROUP_DROPBOXES, c4d.BFH_SCALEFIT, 4, 1, "File Select", 0, 10, 10)
        self.GroupBorderSpace(8, 2, 0, 2)
        self.AddUserArea(ID.MATERIAL_PREVIEW, c4d.BFH_CENTER, 42, 42)
        self.AttachUserArea(self._area, ID.MATERIAL_PREVIEW)
        self.AddButton(ID.DIALOG_DROPBOX_BUTTON1,c4d.BFH_LEFT, initw=10,inith=0, name="<")
        self.AddComboBox(ID.DIALOG_DROPBOX_MAIN,c4d.BFH_SCALEFIT, allowfiltering=True)
        self.AddButton(ID.DIALOG_DROPBOX_BUTTON2,c4d.BFH_RIGHT, initw=10,inith=0, name=">")
        self.GroupBegin(ID.DIALOG_SECONDARY_GROUP, c4d.BFH_CENTER, 1, 1, "Preview", 0, 0, 10)
        self.GroupEnd()
        self.GroupEnd()
        
        self.GroupBegin(ID.DIALOG_GROUP2_DOPBOXES, c4d.BFH_SCALEFIT, 2, 1, "Dropbox", 0, 10, 10)
        self.GroupBorderSpace(8, 2, 36, 2)
        self.AddStaticText(ID.DIALOG_TEXT2_DROPBOX, c4d.BFH_SCALEFIT, 0, 0, "Select map", 0)
        self.AddComboBox(ID.DIALOG_DROPBOX_MAIN3, c4d.BFH_CENTER, initw=250, inith=0)
        self.GroupEnd()

        self.GroupBegin(ID.DIALOG_GROUP3_DOPBOXES, c4d.BFH_SCALEFIT, 4, 1, "Map Select", 0, 10, 10)
        self.GroupBorderSpace(8, 2, 0, 2)
        self.AddStaticText(ID.DIALOG_TEXT_DROPBOX, c4d.BFH_SCALEFIT, 0, 0, "Select material", 0)
        self.AddButton(ID.DIAlOG_PREVIOUS_MATERIAL_BUTTON, c4d.BFH_CENTER, 1, 1, "<")
        self.AddComboBox(ID.DIALOG_DROPBOX_MAIN2, c4d.BFH_CENTER, initw=250, inith=0)
        self.AddButton(ID.DIALOG_NEXT_MATERIAL_BUTTON, c4d.BFH_CENTER, 1, 1, ">")
        self.GroupEnd()

        self.GroupBegin(ID.DIALOG_GROUP_RENDERER,  c4d.BFH_SCALEFIT, 3, 1, "Renderer", 0, 10, 10)
        self.GroupBorderSpace(8, 2, 36, 2)
        self.AddStaticText(ID.DIALOG_RENDERER_TEXT, c4d.BFH_SCALEFIT, 0, 0, "Select renderer", 0)
        header = c4d.BaseContainer()
        header.SetInt32(c4d.BITMAPBUTTON_IGNORE_BITMAP_WIDTH, False)
        header.SetInt32(c4d.BITMAPBUTTON_IGNORE_BITMAP_HEIGHT, True)
        header.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        header.SetBool(c4d.BITMAPBUTTON_TOGGLE, False)
        header.SetString(c4d.BITMAPBUTTON_TOOLTIP, "settings")
        if c4d.GetC4DVersion() // 1000 >= 21:
            idIconPrefs = 1026694
        else:
            idIconPrefs = 1026693
        header.SetInt32(c4d.BITMAPBUTTON_ICONID1, idIconPrefs)
        self.AddCustomGui(ID.DIALOG_SETTINGS_BUTTON, c4d.CUSTOMGUI_BITMAPBUTTON, "", c4d.BFH_LEFT, 32, 16, header)
        renderers = self.AddComboBox(ID.DIALOG_RENDERER_COMBOBOX, c4d.BFH_RIGHT, inith=10, initw=250)
        physical = self.AddChild(renderers, 6400, "Physical")
        corona = self.AddChild(renderers, 6401, "Corona")
        vray = self.AddChild(renderers, 6402, "V-ray")
        redshift = self.AddChild(renderers, 6403, "Redshift")
        octane = self.AddChild(renderers, 6404, "Octane")
        self.GroupEnd()
        
        customgui = c4d.BaseContainer()
        customgui.SetBool(c4d.TREEVIEW_BORDER, c4d.BORDER_THIN_IN)
        customgui.SetBool(c4d.TREEVIEW_HAS_HEADER, True)
        customgui.SetBool(c4d.TREEVIEW_HIDE_LINES, False)
        customgui.SetBool(c4d.TREEVIEW_MOVE_COLUMN, True)
        customgui.SetBool(c4d.TREEVIEW_RESIZE_HEADER, True)
        customgui.SetBool(c4d.TREEVIEW_FIXED_LAYOUT, True)
        customgui.SetBool(c4d.TREEVIEW_ALTERNATE_BG, True)
        customgui.SetBool(c4d.TREEVIEW_CURSORKEYS, True)
        customgui.SetBool(c4d.TREEVIEW_NOENTERRENAME, False)

        self.GroupBegin(ID.DIALOG_GROUP4_BUTTONS, c4d.BFH_SCALEFIT, 1, 1, "Main Buttons", 0, 10, 10)
        self.GroupBorderSpace(8, 2, 0, 2)
        self.AddButton(ID.DIALOG_ADD_TO_LIST_BUTTON, c4d.BFH_SCALEFIT, 1, 1, "Add to list")
        self.AddButton(ID.FILTER_MATERIALS_BUTTON, c4d.BFH_SCALEFIT, 1, 1, "Filter materials")
        self.GroupEnd()

        # self.GroupBegin(ID.DIALOG_CB_GROUP, c4d.BFH_SCALEFIT, 1, 4, "Checkboxes", 0, 10, 10)
        # self.GroupBorderSpace(8, 2, 0, 2)
        # self.AddCheckbox(ID.DIALOG_MAP_AO_CB, c4d.BFH_SCALEFIT, 1, 1, "Include ambient occlusion (AO) maps")
        # self.AddCheckbox(ID.DIALOG_MAP_DISPL_CB, c4d.BFH_SCALEFIT, 1, 1, "Include displacement maps")
        # self.AddCheckbox(ID.DIALOG_MAP_16B_DISPL_CB, c4d.BFH_SCALEFIT, 1, 1, "Use 16 bit displacement maps (when available)")
        # self.AddCheckbox(ID.DIALOG_MAP_16B_NORMAL_CB, c4d.BFH_SCALEFIT, 1, 1, "Use 16 bit normal maps (when available)")
        # self.GroupEnd()
        
        self.GroupBegin(ID.DIALOG_GROUP_MINI_BUTTONS, c4d.BFH_SCALEFIT, 3, 1, "Mini Buttons", 0, 10, 10)
        self.GroupBorderSpace(8, 2, 0, 2)
        self.AddButton(ID.DIALOG_SELECT_ALL_BUTTON, c4d.BFH_LEFT, 70, 5, "Select All")
        self.AddButton(ID.DIALOG_DELETE_BUTTON, c4d.BFH_LEFT, 50, 5, "Delete")
        self.AddButton(ID.DIALOG_ADD_TO_QUEUE_BUTTON, c4d.BFH_LEFT, 110, 5, "Add To Queue")
        self.GroupEnd()

        self._treegui = self.AddCustomGui(9300, c4d.CUSTOMGUI_TREEVIEW, "", c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 300, 300, customgui)
        if not self._treegui:
            print ("[ERROR]: Could not create TreeView")
            return False
    
        self.GroupBegin(ID.DIALOG_SCROLL_GROUP, c4d.BFH_SCALEFIT, 2, 1, "Material folder", 0, 10, 10)
        self.GroupEnd()
        self.GroupEnd()
        self.GroupEnd()
        self.Reset()

        self.SetTimer(1000)

        return True
    
    def InitValues(self):
        self.materialFolder = None
    
        self.has16bDisp = False
        self.has16bNormal = False
        self.hasDisp = False
        self.hasAO = False
        self.hasIor = False
        
        self.SetBool(ID.DIALOG_MAP_AO_CB, False)
        self.Enable(ID.DIALOG_MAP_AO_CB, False)
        self.SetBool(ID.DIALOG_MAP_DISPL_CB, False)
        self.Enable(ID.DIALOG_MAP_DISPL_CB, False)
        self.SetBool(ID.DIALOG_MAP_16B_DISPL_CB, False)
        self.Enable(ID.DIALOG_MAP_16B_DISPL_CB, False)
        self.SetBool(ID.DIALOG_MAP_16B_NORMAL_CB, False)
        self.Enable(ID.DIALOG_MAP_16B_NORMAL_CB, False)
        self.SetBool(ID.DIALOG_MAP_IOR_CB, False)
        self.Enable(ID.DIALOG_MAP_IOR_CB, False)

        self.Enable(ID.DIALOG_LOAD_BUTTON, False)

        self.Enable(ID.FILTER_MATERIALS_BUTTON, False)
        self.Enable(ID.DIALOG_SELECT_ALL_BUTTON, False)

        self.Enable(ID.DIALOG_DROPBOX_BUTTON1, False)
        self.Enable(ID.DIALOG_DROPBOX_MAIN, False)
        self.Enable(ID.DIALOG_DROPBOX_BUTTON2, False)

        self.Enable(ID.DIALOG_TEXT2_DROPBOX, False)
        self.Enable(ID.DIALOG_DROPBOX_MAIN3, False)

        self.Enable(ID.DIALOG_TEXT_DROPBOX, False)
        self.Enable(ID.DIALOG_DROPBOX_MAIN2, False)
        self.Enable(ID.DIALOG_NEXT_MATERIAL_BUTTON, False)
        self.Enable(ID.DIAlOG_PREVIOUS_MATERIAL_BUTTON, False)

        self.Enable(ID.DIALOG_ADD_TO_QUEUE_BUTTON, False)
        self.Enable(ID.DIALOG_DELETE_BUTTON, False)
        self.Enable(ID.DIALOG_ADD_TO_LIST_BUTTON, False)

        layout = c4d.BaseContainer()
        layout.SetLong(ID_CHECKBOX, c4d.LV_CHECKBOX)
        layout.SetLong(ID_NAME, c4d.LV_TREE)
        layout.SetLong(ID_MAP_NAME, c4d.LV_USER)
        layout.SetLong(ID_MATERIAL_NAME, c4d.LV_USER)

        self._treegui.SetLayout(4, layout)

        # set the header titles.
        self._treegui.SetHeaderText(ID_CHECKBOX, "Check")
        self._treegui.SetHeaderText(ID_NAME, "Name")
        self._treegui.SetHeaderText(ID_MAP_NAME, "Map")
        self._treegui.SetHeaderText(ID_MATERIAL_NAME, "Material")
        self._treegui.Refresh()
 
        # set TreeViewFunctions instance used by our CUSTOMGUI_TREEVIEW
        root = self._treegui.SetRoot(self._treegui, self._listView, None)

        # deletes all items in treeview and lists if not empty
        if len(self._listView.listOfTexture) != 0:
            self._listView.listOfTexture.clear()
        self._treegui.Refresh()

        if len(checkbox_list) != 0:
            checkbox_list.clear()
        
        if len(material_to_add) != 0:
            material_to_add.clear()

        if len(same_path_dirs) != 0:
            same_path_dirs.clear()

        if len(materialCount) != 0:
            materialCount.clear()

        if len(child_id_list) != 0:
            child_id_list.clear()
        
        if len(child_name_list) != 0:
            child_name_list.clear()

        if len(map_id_list) != 0:
            map_id_list.clear()

        if len(material_id_list) != 0:
            material_id_list.clear()

        if len(material_name_list) != 0:
            material_name_list.clear()
        
        if len(selected_materials) != 0:
            selected_materials.clear()

        if len(selected_files) != 0:
            selected_files.clear()
        
        if len(selected_paths) != 0:
            selected_paths.clear()

        if len(selected_maps) != 0:
            selected_maps.clear()
        
        if len(tex_list) != 0:
            tex_list.clear()

        if len(folder_path_list) != 0:
            folder_path_list.clear()

        return True

    def auto_assign(self, actual_name):
        # if there is a variable set
        if actual_name:
            # check all possible map names and types
            if "AO" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4500)
            elif "ambient" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4500)
            elif "Ambient" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4500)
            elif "ao" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4500)
            elif "NRM" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4501)
            elif "nrm" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4501)
            elif "NRM16" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4501)
            elif "Normal" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4501)
            elif "normal" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4501)
            elif "DISP" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4502)
            elif "Displacement" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4502)
            elif "disp" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4502)
            elif "DISP16" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4502)
            elif "HEIGHT" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4502)
            elif "height" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4502)
            elif "COL" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4503)
            elif "col" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4503)
            elif "COLOR" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4503)
            elif "color" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4503)
            elif "diff" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4503)
            elif "DIFF" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4503)
            elif "albedo" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4503)
            elif "GLOSS" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4504)
            elif "gloss" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4504)
            elif "Glosiness" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4504)
            elif "ROUGH" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4505)
            elif "rough" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4505)
            elif "METAL" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4506)
            elif "metal" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4506)
            elif "OPAC" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4507)
            elif "opac" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4507)
            elif "BUMP" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4508)
            elif "bump" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4508)

    # gets the name from id of the list
    def get_name_from_id(self, id: int, index_list: list, name_list: list):
        index = index_list.index(id)
        name = name_list[index]
        return name

    # gets the next item in the dropbox        
    def get_next_item(self, dropbox_id: int, file_id_list: list, file_name_list: list):
        actual = self.GetLong(dropbox_id)
        if actual+1 in file_id_list:
            next = actual+1
            self.SetInt32(dropbox_id, next)
            index = file_id_list.index(next)
            actual_name = file_name_list[index]
            self.auto_assign(actual_name)
            index = child_id_list.index(actual) + 1
            file_path = folder_path_list[index]
            self.set_preview_material(file_path)


    # gets the previous item in the dropbox
    def get_previous_item(self, dropbox_id: int, file_list: list, file_name_list: list):
        actual = self.GetLong(dropbox_id)
        if actual-1 in file_list:
            previous = actual-1
            self.SetInt32(dropbox_id, previous)
            index = file_list.index(previous)
            actual_name = file_name_list[index]
            self.auto_assign(actual_name)
            index = child_id_list.index(actual) - 1
            file_path = folder_path_list[index]
            self.set_preview_material(file_path)

    # sets the image to preview window
    def set_preview_material(self, path):
        self.MaterialPreviewBmpTmp.InitWith(path)
        if (self.MaterialPreviewBmpTmp.GetBw()-1 > 41 and self.MaterialPreviewBmpTmp.GetBh()-1 > 41):
            self.MaterialPreviewBmpTmp.ScaleBicubic(self.MaterialPreviewBmp,
             0, 0, self.MaterialPreviewBmpTmp.GetBw()-1, self.MaterialPreviewBmpTmp.GetBh()-1,
             0, 0, 41, 41)
        else:
            self.MaterialPreviewBmpTmp.ScaleIt(self.MaterialPreviewBmp, 256, True, False)
        self._area.setBitmap(self.MaterialPreviewBmp)
        self._area.Redraw()

    def Command(self, id, msg):
        count = 1
        # browse button
        if id == ID.DIALOG_FOLDER_BUTTON:
            path = c4d.storage.LoadDialog(title="Choose material folder", flags=c4d.FILESELECT_DIRECTORY)
            if path == None:
                return True
            try:
                path = path.decode("utf-8")
            except: 
                pass
            # textbox fills up with path of the selected folder
            self.SetString(ID.DIALOG_FOLDER_LIST, path)

            print(path)
            # saves all files in path as dir
            dir = os.listdir(path)
            map_names_list = ["AO_Ambient occlusion", "NRM_Normal map", "DISP_Displacement", "COL_Color", "GLOSS_Glossiness", "ROUGH_Roughness", "METAL_Metallic", "OPAC_Opacit"]
            first_file = None
            num = 0
            ID_CHILD = 9000
            for file in dir:
                folder_path = os.path.join(path, file)
                # saves the first file as first_file
                while num <= 0:
                    print(f"Tohle je folder_path: {folder_path}")
                    first_file = file
                    self.set_preview_material(folder_path)
                    num += 1
                ID_CHILD += 1
                # adds the file to the dropbox
                self.AddChild(ID.DIALOG_DROPBOX_MAIN, ID_CHILD, file)
                child_id_list.append(ID_CHILD)
                child_name_list.append(file)
                checkbox_list.append(file)
                folder_path_list.append(folder_path)
                self._treegui.Refresh()
            
            print(f"child_id_list: {child_id_list}")
            print(f"child_name_list: {child_name_list}")
            print(f"checkbox_list: {checkbox_list}")
            print(f"folder_path_list: {folder_path_list}")

            self.Enable(ID.FILTER_MATERIALS_BUTTON, True)
            self.Enable(ID.DIALOG_SELECT_ALL_BUTTON, True)

            self.Enable(ID.DIALOG_DROPBOX_BUTTON1, True)
            self.Enable(ID.DIALOG_DROPBOX_MAIN, True)
            self.Enable(ID.DIALOG_DROPBOX_BUTTON2, True)

            self.Enable(ID.DIALOG_TEXT2_DROPBOX, True)
            self.Enable(ID.DIALOG_DROPBOX_MAIN3, True)

            self.Enable(ID.DIALOG_TEXT_DROPBOX, True)
            self.Enable(ID.DIALOG_DROPBOX_MAIN2, True)
            self.Enable(ID.DIALOG_NEXT_MATERIAL_BUTTON, True)
            self.Enable(ID.DIAlOG_PREVIOUS_MATERIAL_BUTTON, True)

            self.Enable(ID.DIALOG_ADD_TO_QUEUE_BUTTON, True)
            self.Enable(ID.DIALOG_DELETE_BUTTON, True)
            self.Enable(ID.DIALOG_ADD_TO_LIST_BUTTON, True)

            self.Enable(ID.DIALOG_MAP_AO_CB, True)
            self.Enable(ID.DIALOG_MAP_DISPL_CB, True)
            self.Enable(ID.DIALOG_MAP_16B_DISPL_CB, True)
            self.Enable(ID.DIALOG_MAP_16B_NORMAL_CB, True)
            
            id_mat = 4000
            while 20 >= count:
                material_name = "Material " + str(count)
                self.AddChild(ID.DIALOG_DROPBOX_MAIN2, id_mat, material_name)
                count+=1
                material_id_list.append(id_mat)
                material_name_list.append(material_name)
                id_mat+=1
            # sets the first item in materials list to the dropbox, most likely Material
            self.SetInt32(ID.DIALOG_DROPBOX_MAIN2, material_id_list[0])
            
            id_map = 4500
            map_names_list = ["AO_Ambient occlusion", "NRM_Normal map", "DISP_Displacement", "COL_Color", "GLOSS_Glossiness", "ROUGH_Roughness", "METAL_Metallic", "OPAC_Opacit", "BUMP_Bump map"]
            # fills the dropbox with all maps
            for map in map_names_list:
                self.AddChild(ID.DIALOG_DROPBOX_MAIN3, id_map, map)
                map_id_list.append(id_map)                
                id_map+=1
            # sets the default value for the dropbox as the first item in the list or matches the one that is in the list already
            self.SetInt32(ID.DIALOG_DROPBOX_MAIN, child_id_list[0])
            print(f"Tohle je first file: {first_file}")
            self.auto_assign(first_file)
            self.Enable(ID.DIALOG_FOLDER_BUTTON, False)

        # adds another folder to the list of files in the dropbox
        if id == ID.DIALOG_ADD_TO_QUEUE_BUTTON:
            path = c4d.storage.LoadDialog(title="Choose folder to be added to the list", flags=c4d.FILESELECT_DIRECTORY)
            if path == None:
                return True
            try:
                path = path.decode("utf-8")
            except:
                pass

            self.SetString(ID.DIALOG_FOLDER_LIST, path)
            dir = os.listdir(path)
            ID_CHILD = child_id_list[-1]
            for file in dir:
                folder_path = os.path.join(path,file)
                ID_CHILD += 1
                self.AddChild(ID.DIALOG_DROPBOX_MAIN, ID_CHILD, file)
                child_id_list.append(ID_CHILD)
                child_name_list.append(file)
                checkbox_list.append(file)
                print(ID_CHILD)
                folder_path_list.append(folder_path)

        # deletes file that has checked checkbox
        if id == ID.DIALOG_DELETE_BUTTON:
            for tex in reversed(self._listView.listOfTexture):
                if tex.IsSelected:
                    id_tex = self._listView.listOfTexture.index(tex)
                    print("Index to be deleted: ", id_tex)
                    selected_maps.pop(id_tex)
                    selected_materials.pop(id_tex)
                    selected_files.pop(id_tex)
                    selected_paths.pop(id_tex)
                    self._listView.listOfTexture.remove(tex)
                    tex_list.pop(id_tex)
                    self._treegui.Refresh()

        # file go back button <
        if id == ID.DIALOG_DROPBOX_BUTTON1:
            self.get_previous_item(ID.DIALOG_DROPBOX_MAIN, child_id_list, child_name_list)
            # file_path = self.GetLong(ID.DIALOG_DROPBOX_MAIN)
            # self.set_preview_material(file_path)
        
        # file go forward button >
        if id == ID.DIALOG_DROPBOX_BUTTON2:
            self.get_next_item(ID.DIALOG_DROPBOX_MAIN, child_id_list, child_name_list)

        # material go back button <
        if id == ID.DIALOG_NEXT_MATERIAL_BUTTON:
            self.get_next_item(ID.DIALOG_DROPBOX_MAIN2, material_id_list, material_name_list)

        # material go forward button >
        if id == ID.DIAlOG_PREVIOUS_MATERIAL_BUTTON:
            self.get_previous_item(ID.DIALOG_DROPBOX_MAIN2, material_id_list, material_name_list)

        if id == ID.DIALOG_DROPBOX_MAIN:
            print("kliknuto na checkbox")
            actual = self.GetLong(ID.DIALOG_DROPBOX_MAIN)
            index = child_id_list.index(actual)
            actual_name = child_name_list[index]
            index = child_id_list.index(actual)
            file_path = folder_path_list[index]
            self.set_preview_material(file_path)
            self.auto_assign(actual_name)

        
        if id == ID.DIALOG_ADD_TO_LIST_BUTTON:

            selected_file_id = self.GetInt32(ID.DIALOG_DROPBOX_MAIN)
            selected_file_name = self.get_name_from_id(selected_file_id, child_id_list, child_name_list)
            print("")
            selected_file_path = self.get_name_from_id(selected_file_id,child_id_list, folder_path_list)
            print("Selected file: ", selected_file_name, " and his ID: ", selected_file_id, " and his path: ", selected_file_path)

            map_names_list = ["AO_Ambient occlusion", "NRM_Normal map", "DISP_Displacement", "COL_Color", "GLOSS_Glossiness", "ROUGH_Roughness", "METAL_Metallic", "OPAC_Opacit", "BUMP_Bump map"]            
            map_shortcuts = ["AO", "NRM", "DISP", "COL", "GLOSS", "ROUGH", "METAL", "OPAC", "BUMP"]
            selected_map_id = self.GetInt32(ID.DIALOG_DROPBOX_MAIN3)
            selected_map_name = self.get_name_from_id(selected_map_id, map_id_list, map_shortcuts)
            print("Selected map: ", selected_map_name, " and his ID: ", selected_map_id)
            
            selected_material_id = self.GetInt32(ID.DIALOG_DROPBOX_MAIN2)
            selected_material_name = self.get_name_from_id(selected_material_id, material_id_list, material_name_list)
            print("Selected material:", selected_material_name, " and his ID: ", selected_material_id)

            newID = len(self._listView.listOfTexture) + 1
            tex = TextureObject(selected_file_name.format(newID),selected_map_name, selected_material_name)
            self._listView.listOfTexture.append(tex)
            self._treegui.Refresh()
            tex_list.append(tex)

            selected_files.append(selected_file_name)
            selected_materials.append(selected_material_name)
            selected_maps.append(selected_map_name)
            selected_paths.append(selected_file_path)
            
            self.get_next_item(ID.DIALOG_DROPBOX_MAIN, child_id_list, child_name_list)

        # filtering and uploading materials
        if id == ID.FILTER_MATERIALS_BUTTON:
            print("")
            print(f"selected_maps: {selected_maps}")
            print(f"selected_materials: {selected_materials}")
            print(f"selected_files: {selected_files}")                        
            print("")
            assigned_material = ""
            materials_to_upload = []

            # goes through all checkboxes
            for index, checkbox in enumerate(tex_list):
                # if the checkbox is checked
                if checkbox.IsSelected:
                    print("Checked checkbox: ", checkbox)
                    # saves the material number that is assigned to the checkbox in selected_materials list e.g. Material 2
                    assigned_material = selected_materials[index]
                    # condition to avoid duplicates - if the material is not already there
                    if assigned_material not in materials_to_upload:
                        # then add it into the list
                        materials_to_upload.append(assigned_material)
                        print(f"{assigned_material} was added to materials_to_upload")
            
            # goes through materials that were selected in the dropbox e.g. Material 2, Material 5, ...
            for assigned_material in materials_to_upload:
                # # cycle to get the index of the selected material
                uploaded_files.clear()
                uploaded_maps.clear()
                uploaded_paths.clear()
                uploaded_indexes.clear()
                for index, selected_material in enumerate(selected_materials):
                    if selected_material == assigned_material:
                        uploaded_indexes.append(index)
                # goes through all indexes that belong to selected materials
                for index in uploaded_indexes:
                    file = selected_files[index]
                    map = selected_maps[index]
                    path = selected_paths[index]
                    uploaded_files.append(file)
                    uploaded_maps.append(map)
                    uploaded_paths.append(path)
                # control prints
                
                print("")
                print("Assigned material: ", assigned_material)
                print("Assigned material indexes: ", uploaded_indexes)
                print("Selected files: ", uploaded_files)
                print("Selected maps: ", uploaded_maps)
                print("Assigned paths of the files: ", uploaded_paths)
                print(" ")

                folder_path = self.GetString(ID.DIALOG_FOLDER_LIST)
                hasColor = False
                loadAO = self.GetBool(ID.DIALOG_MAP_AO_CB)
                loadDispl = self.GetBool(ID.DIALOG_MAP_DISPL_CB)
                load16bdispl = self.GetBool(ID.DIALOG_MAP_16B_DISPL_CB)
                # loadIor = self.GetBool(ID.DIALOG_MAP_IOR_CB

                # for index, mapID in enumerate(uploaded_maps):
                #     # gets the path of the actual file through its index
                #     fullPath = uploaded_paths[index]
                    # sets the name of the final material same as the material that is attached to the file e.g. Material 2
                    

                ##############
                ### Corona ###
                ##############
                    
                if self.GetInt32(ID.DIALOG_RENDERER_COMBOBOX) == 6401:
                    if not c4d.plugins.FindPlugin(1030480):
                        c4d.gui.MessageDialog("Corona is not installed")
                        return
                    mat = c4d.BaseMaterial(ID.CORONA_STR_MATERIAL_PHYSICAL)
                    mat.SetParameter(ID.CORONA_MATERIAL_PREVIEWSIZE, ID.CORONA_MATERIAL_PREVIEWSIZE_1024, c4d.DESCFLAGS_SET_NONE)
                    mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_IOR_VALUE, 1.56, c4d.DESCFLAGS_SET_NONE)
                    mat.SetName(assigned_material)
                    fusionShader = None
                    for index, mapID in enumerate(uploaded_maps):
                        # gets the path of the actual file through its index
                        fullPath = uploaded_paths[index]
                        if mapID == "COL":
                            if "AO" not in uploaded_maps:
                                bitmap = c4d.BaseShader(c4d.Xbitmap)
                                bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                                mat.InsertShader(bitmap)
                                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_COLOR_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                            # else:
                            else: 
                                if not fusionShader:
                                    fusionShader = c4d.BaseShader(c4d.Xfusion)
                                    fusionShader.SetParameter(c4d.SLA_FUSION_MODE, c4d.SLA_FUSION_MODE_MULTIPLY, c4d.DESCFLAGS_SET_NONE)
                                    fusionShader.SetParameter(c4d.SLA_FUSION_BLEND, 1.0, c4d.DESCFLAGS_SET_NONE)
                                    mat.InsertShader(fusionShader)
                                    mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_COLOR_TEXTURE, fusionShader, c4d.DESCFLAGS_SET_NONE)
                                bitmap = c4d.BaseShader(c4d.Xbitmap)
                                bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                                fusionShader.InsertShader(bitmap)
                                fusionShader.SetParameter(c4d.SLA_FUSION_BASE_CHANNEL, bitmap, c4d.DESCFLAGS_SET_NONE)
                        elif mapID == "NRM":
                            bitmap = c4d.BaseShader(c4d.Xbitmap)
                            bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                            texture = c4d.BaseShader(ID.PLUGINID_CORONA4D_NORMALSHADER)
                            texture.SetParameter(ID.CORONA_NORMALMAP_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                            texture.SetParameter(ID.CORONA_NORMALMAP_FLIP_G, True, c4d.DESCFLAGS_SET_NONE)
                            mat.InsertShader(bitmap)
                            mat.InsertShader(texture)
                            mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_BUMPMAPPING_ENABLE, True, c4d.DESCFLAGS_SET_NONE)
                            mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_BUMPMAPPING_VALUE, 1.0, c4d.DESCFLAGS_SET_NONE)
                            mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_BUMPMAPPING_TEXTURE, texture, c4d.DESCFLAGS_SET_NONE)
                        # elif loadDispl and (load16bdispl and mapID == "DISP16") or (not load16bdispl and mapID == "DISP"):
                        elif mapID == "DISP":
                            bitmap = c4d.BaseShader(c4d.Xbitmap)
                            bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                            mat.InsertShader(bitmap)
                            mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_DISPLACEMENT, True, c4d.DESCFLAGS_SET_NONE)
                            mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                            mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_MIN_LEVEL, 0, c4d.DESCFLAGS_SET_NONE)
                            mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_MAX_LEVEL, 1, c4d.DESCFLAGS_SET_NONE)
                        # elif loadAO and mapID == "AO":
                        elif mapID == "AO":
                            if not fusionShader:
                                fusionShader = c4d.BaseShader(c4d.Xfusion)
                                fusionShader.SetParameter(c4d.SLA_FUSION_MODE, c4d.SLA_FUSION_MODE_MULTIPLY, c4d.DESCFLAGS_SET_NONE)
                                fusionShader.SetParameter(c4d.SLA_FUSION_BLEND, 1.0, c4d.DESCFLAGS_SET_NONE)
                                mat.InsertShader(fusionShader)
                                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_COLOR_TEXTURE, fusionShader, c4d.DESCFLAGS_SET_NONE)
                            bitmap = c4d.BaseShader(c4d.Xbitmap)
                            bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                            fusionShader.InsertShader(bitmap)
                            fusionShader.SetParameter(c4d.SLA_FUSION_BLEND_CHANNEL, bitmap, c4d.DESCFLAGS_SET_NONE)
                        elif mapID == "OPAC":
                            bitmap = c4d.BaseShader(c4d.Xbitmap)
                            bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                            mat.InsertShader(bitmap)
                            mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_ALPHA, True, c4d.DESCFLAGS_SET_NONE)
                            mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_ALPHA_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                        elif mapID == "GLOSS":
                            print(f"Tohle nechapu mam byt Roughness, ale jsem {mapID} a tohle je moje fullPath {fullPath}")
                            bitmap = c4d.BaseShader(c4d.Xbitmap)
                            bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                            mat.InsertShader(bitmap)
                            mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_ROUGHNESS_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                            mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_ROUGHNESS_VALUE, 100.0, c4d.DESCFLAGS_SET_NONE)
                            mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_ROUGHNESS_MODE, ID.CORONA_PHYSICAL_MATERIAL_ROUGHNESS_MODE_GLOSSINESS, c4d.DESCFLAGS_SET_NONE)
                        elif mapID == "ROUGH":
                            print(f"Tohle nechapu mam byt Roughness, ale jsem {mapID} a tohle je moje fullPath {fullPath}")
                            bitmap = c4d.BaseShader(c4d.Xbitmap)
                            bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                            mat.InsertShader(bitmap)
                            mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_ROUGHNESS_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                            mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_ROUGHNESS_VALUE, 100.0, c4d.DESCFLAGS_SET_NONE)
                            mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_ROUGHNESS_MODE, ID.CORONA_PHYSICAL_MATERIAL_ROUGHNESS_MODE_ROUGHNESS, c4d.DESCFLAGS_SET_NONE)
                        elif mapID == "REFL":
                            bitmap = c4d.BaseShader(c4d.Xbitmap)
                            bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                            mat.InsertShader(bitmap)
                            mat.SetParameter(ID.CORONA_MATERIAL_REFLECT, True, c4d.DESCFLAGS_SET_NONE)
                            mat.SetParameter(ID.CORONA_REFLECT_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                        elif mapID == "SSS":
                            bitmap = c4d.BaseShader(c4d.Xbitmap)
                            bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                            mat.InsertShader(bitmap)
                            mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_SSS, True, c4d.DESCFLAGS_SET_NONE)
                            mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_VOLUME_SSS_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                        elif mapID == "SSSABSORB":
                            bitmap = c4d.BaseShader(c4d.Xbitmap)
                            bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                            mat.InsertShader(bitmap)
                            mat.SetParameter(ID.CORONA_MATERIAL_VOLUME, True, c4d.DESCFLAGS_SET_NONE)
                            mat.SetParameter(ID.CORONA_VOLUME_ABSORPTION_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                        # elif loadIor and mapID == "IOR":
                        #     bitmap = c4d.BaseShader(c4d.Xbitmap)
                        #     bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                        #     mat.InsertShader(bitmap)
                        #     mat.SetParameter(ID.CORONA_REFLECT_FRESNELLOR_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                        elif mapID == "METAL":
                            bitmap = c4d.BaseShader(c4d.Xbitmap)
                            bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                            mat.InsertShader(bitmap)
                            mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_METALLIC_MODE_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                        elif mapID == "BUMP":
                            if "NRM" not in uploaded_maps:
                                bitmap = c4d.BaseShader(c4d.Xbitmap)
                                bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                                mat.InsertShader(bitmap)
                                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_BUMPMAPPING_ENABLE, True, c4d.DESCFLAGS_SET_NONE)
                                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_BUMPMAPPING_VALUE, 1.0, c4d.DESCFLAGS_SET_NONE)
                                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_BUMPMAPPING_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                    doc = c4d.documents.GetActiveDocument()
                    doc.StartUndo()
                    doc.InsertMaterial(mat)
                    doc.AddUndo(c4d.UNDOTYPE_NEW, mat)
                    doc.EndUndo()
                    material_to_add.append(mat)                                   
                    self.SetString(ID.DIALOG_ERROR, "")

                ################
                ### Physical ###
                ################
                
                if self.GetInt32(ID.DIALOG_RENDERER_COMBOBOX) == 6400:
                    mat = c4d.BaseMaterial(c4d.Mmaterial)
                    mat[c4d.MATERIAL_PREVIEWSIZE] = 10
                    bitmap = c4d.BaseShader(c4d.Xbitmap)
                    fusion_shader = None
                    mat.SetName(assigned_material)
                    for index, mapID in enumerate(uploaded_maps):
                        # gets the path of the actual file through its index
                        fullPath = uploaded_paths[index]
                        if mapID == "COL" or mapID == "COLOR":
                            if "AO" not in uploaded_maps:
                                bitmap[c4d.BITMAPSHADER_FILENAME] = fullPath
                                mat.InsertShader(bitmap)
                                mat[c4d.MATERIAL_COLOR_SHADER] = bitmap
                            else:
                                if not fusion_shader:
                                    fusion_shader = c4d.BaseShader(c4d.Xfusion)
                                    fusion_shader.SetParameter(c4d.SLA_FUSION_MODE, c4d.SLA_FUSION_MODE_MULTIPLY, c4d.DESCFLAGS_SET_NONE)
                                    fusion_shader.SetParameter(c4d.SLA_FUSION_BLEND, 1.0, c4d.DESCFLAGS_SET_NONE)
                                    mat.InsertShader(fusion_shader)
                                    mat[c4d.MATERIAL_COLOR_SHADER] = fusion_shader
                                bitmap = c4d.BaseShader(c4d.Xbitmap)
                                bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                                fusion_shader.InsertShader(bitmap)
                                fusion_shader.SetParameter(c4d.SLA_FUSION_BASE_CHANNEL, bitmap, c4d.DESCFLAGS_SET_NONE)
                        elif mapID == "AO":
                            if not fusion_shader:
                                fusion_shader = c4d.BaseShader(c4d.Xfusion)
                                fusion_shader.SetParameter(c4d.SLA_FUSION_MODE, c4d.SLA_FUSION_MODE_MULTIPLY, c4d.DESCFLAGS_SET_NONE)
                                fusion_shader[c4d.SLA_FUSION_BLEND] = 1.0
                                mat.InsertShader(fusion_shader)
                                mat[c4d.MATERIAL_COLOR_SHADER] = fusion_shader
                            bitmap = c4d.BaseShader(c4d.Xbitmap)
                            bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                            fusion_shader.InsertShader(bitmap)
                            fusion_shader[c4d.SLA_FUSION_BLEND_CHANNEL] = bitmap
                        elif mapID == "NRM":
                            normal_shader = c4d.BaseShader(c4d.Xbitmap)
                            mat[c4d.MATERIAL_USE_NORMAL] = True
                            normal_shader[c4d.BITMAPSHADER_FILENAME] = fullPath
                            mat[c4d.MATERIAL_NORMAL_SHADER] = normal_shader
                            normal_shader[c4d.BITMAPSHADER_COLORPROFILE] = 1
                            mat.InsertShader(normal_shader)
                        elif mapID == "BUMP":
                            bump_shader = c4d.BaseShader(c4d.Xbitmap)
                            bump_shader[c4d.BITMAPSHADER_FILENAME] = fullPath
                            mat[c4d.MATERIAL_BUMP_SHADER] = bump_shader
                            mat.InsertShader(bump_shader)
                            mat[c4d.MATERIAL_USE_BUMP] = True
                        elif mapID == "ROUGH":
                            rough_shader = c4d.BaseShader(c4d.Xbitmap)
                            rough_shader.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                            rough_shader[c4d.BITMAPSHADER_FILENAME] = fullPath
                            mat.InsertShader(rough_shader)
                            bases = [c4d.REFLECTION_LAYER_LAYER_DATA + c4d.REFLECTION_LAYER_LAYER_SIZE * 4]
                            for base in bases:
                                mat[base + c4d.REFLECTION_LAYER_MAIN_DISTRIBUTION] = 3
                                mat[base + c4d.REFLECTION_LAYER_MAIN_VALUE_ROUGHNESS] = 100
                                mat[base + c4d.REFLECTION_LAYER_MAIN_SHADER_ROUGHNESS] = rough_shader
                        elif mapID == "DISP":
                            disp_shader = c4d.BaseShader(c4d.Xbitmap)
                            disp_shader[c4d.BITMAPSHADER_FILENAME] = fullPath
                            mat[c4d.MATERIAL_DISPLACEMENT_SHADER] = disp_shader
                            disp_shader[c4d.BITMAPSHADER_COLORPROFILE] = 1
                            mat.InsertShader(disp_shader)
                            mat[c4d.MATERIAL_USE_DISPLACEMENT] = True
                        elif mapID == "OPAC":
                            opac_shader = c4d.BaseShader(c4d.Xbitmap)
                            opac_shader[c4d.BITMAPSHADER_FILENAME] = fullPath
                            mat[c4d.MATERIAL_ALPHA_SHADER] = opac_shader
                            mat.InsertShader(opac_shader)
                            mat[c4d.MATERIAL_USE_ALPHA] = True
                    doc = c4d.documents.GetActiveDocument()
                    doc.StartUndo()
                    doc.InsertMaterial(mat)
                    doc.AddUndo(c4d.UNDOTYPE_NEW, mat)
                    doc.EndUndo()
                    material_to_add.append(mat)                                   
                    self.SetString(ID.DIALOG_ERROR, "")

            ##############
            ### Octane ###
            ##############

            if self.GetInt32(ID.DIALOG_RENDERER_COMBOBOX) == 6404:
                if not c4d.plugins.FindPlugin(1029525):
                    c4d.gui.MessageDialog("Octane is not installed")
                    return
                
                mat = c4d.BaseMaterial(ID.OCTANE_MATERIAL)
                mat[c4d.OCT_MATERIAL_TYPE] = 2516
                mat[ID.OCTANE_BSDF_MODEL] = 2
                mat[c4d.OCT_MATERIAL_PREVIEWSIZE] = 10
                mat.SetName(assigned_material)

                multiply_loaded = False
                multiply = None

                for index, mapID in enumerate(uploaded_maps):
                    # gets the path of the actual file through its index
                    fullPath = uploaded_paths[index]
                    if mapID == "COL":
                        if "AO" not in uploaded_maps:
                            bitmap = c4d.BaseShader(ID.OCTANE_TEXTURE)
                            bitmap[c4d.IMAGETEXTURE_FILE] = fullPath
                            mat.InsertShader(bitmap)
                            mat[c4d.OCT_MATERIAL_DIFFUSE_LINK] = bitmap
                        else:
                            bitmap = c4d.BaseShader(ID.OCTANE_TEXTURE)
                            if multiply_loaded == False:
                                multiply = c4d.BaseShader(ID.OCTANE_MULTIPLY)
                                mat.InsertShader(multiply)
                                multiply_loaded = True
                            multiply[c4d.MULTIPLY_TEXTURE1] = bitmap
                            bitmap[c4d.IMAGETEXTURE_FILE] = fullPath
                            mat.InsertShader(bitmap)  
                            mat[c4d.OCT_MATERIAL_DIFFUSE_LINK] = multiply
                                        
                    elif mapID == "AO":
                        bitmap = c4d.BaseShader(ID.OCTANE_TEXTURE)
                        if multiply_loaded == False:
                            multiply = c4d.BaseShader(ID.OCTANE_MULTIPLY)
                            mat.InsertShader(multiply)
                            multiply_loaded = True
                        multiply[c4d.MULTIPLY_TEXTURE2] = bitmap
                        bitmap[c4d.IMAGETEXTURE_FILE] = fullPath
                        mat.InsertShader(bitmap)
                        mat[c4d.OCT_MATERIAL_DIFFUSE_LINK] = multiply
                                        
                    elif mapID == "ROUGH":
                        bitmap = c4d.BaseShader(ID.OCTANE_TEXTURE)
                        bitmap[c4d.IMAGETEXTURE_FILE] = fullPath
                        bitmap[c4d.IMAGETEXTURE_GAMMA] = 1.0
                        bitmap[c4d.IMAGETEXTURE_MODE] = 1
                        mat.InsertShader(bitmap)
                        mat[c4d.OCT_MATERIAL_ROUGHNESS_LINK] = bitmap

                    elif mapID == "NRM":
                        bitmap = c4d.BaseShader(ID.OCTANE_TEXTURE)
                        bitmap[c4d.IMAGETEXTURE_FILE] = fullPath
                        mat.InsertShader(bitmap)
                        mat[c4d.OCT_MATERIAL_NORMAL_LINK] = bitmap
                    
                    elif mapID == "DISP":
                        bitmap = c4d.BaseShader(ID.OCTANE_TEXTURE)
                        displacement = c4d.BaseShader(ID.OCTANE_DISPLACEMENT)
                        displacement[c4d.DISPLACEMENT_AMOUNT] = 1.0
                        displacement[c4d.DISPLACEMENT_LEVELOFDETAIL] = 10
                        displacement[c4d.DISPLACEMENT_TEXTURE] = bitmap
                        bitmap[c4d.IMAGETEXTURE_FILE] = fullPath
                        bitmap[c4d.IMAGETEXTURE_GAMMA] = 1.0
                        bitmap[c4d.IMAGETEXTURE_MODE] = 1
                        mat.InsertShader(displacement)
                        mat.InsertShader(bitmap)
                        mat[c4d.OCT_MATERIAL_DISPLACEMENT_LINK] = displacement
                                        
                    elif mapID == "OPAC":
                        bitmap = c4d.BaseShader(ID.OCTANE_TEXTURE)
                        bitmap[c4d.IMAGETEXTURE_FILE] = fullPath
                        bitmap[c4d.IMAGETEXTURE_GAMMA] = 1.0
                        bitmap[c4d.IMAGETEXTURE_MODE] = 1
                        mat.InsertShader(bitmap)
                        mat[c4d.OCT_MATERIAL_OPACITY_LINK] = bitmap
                                        
                    elif mapID == "METAL":
                        bitmap = c4d.BaseShader(ID.OCTANE_TEXTURE)
                        bitmap[c4d.IMAGETEXTURE_FILE] = fullPath
                        bitmap[c4d.IMAGETEXTURE_GAMMA] = 1.0
                        bitmap[c4d.IMAGETEXTURE_MODE] = 1
                        mat.InsertShader(bitmap)
                        mat[c4d.OCT_MAT_SPECULAR_MAP_LINK] = bitmap

                    elif mapID == "SHEEN":
                        bitmap = c4d.BaseShader(ID.OCTANE_TEXTURE)
                        bitmap[c4d.IMAGETEXTURE_FILE] = fullPath
                        mat.InsertShader(bitmap)
                        mat[c4d.OCT_MAT_SHEEN_LINK] = bitmap
                                    
                doc = c4d.documents.GetActiveDocument()
                doc.StartUndo()
                doc.InsertMaterial(mat)   
            
            #############
            ### V-ray ###
            #############

            if self.GetInt32(ID.DIALOG_RENDERER_COMBOBOX) == 6402:

                if not c4d.plugins.FindPlugin(1053272):
                    c4d.gui.MessageDialog("V-ray is not installed")
                    return

                mat = c4d.BaseMaterial(ID.VRAY_MATERIAL)
                fusion_shader = None
                mat[c4d.VRAY_SETTINGS_MATERIAL_PREVIEW_OVERRIDE] = True
                mat[c4d.VRAY_SETTINGS_MATERIAL_PREVIEW_VIEWPORT_SIZE] = 10
                mat.SetName(assigned_material)

                for index, mapID in enumerate(uploaded_maps):
                    fullPath = uploaded_paths[index]
                    if mapID == "COL":
                        if "AO" not in uploaded_maps:
                            bitmap = c4d.BaseShader(ID.VRAY_BITMAP)
                            bitmap[c4d.BITMAPSHADER_FILENAME] = fullPath
                            mat.InsertShader(bitmap)
                            mat[c4d.BRDFVRAYMTL_DIFFUSE_TEXTURE] = bitmap
                        else:
                            if not fusion_shader:
                                fusion_shader = c4d.BaseShader(c4d.Xfusion)
                                fusion_shader[c4d.SLA_FUSION_MODE] = c4d.SLA_FUSION_MODE_MULTIPLY
                                mat.InsertShader(fusion_shader)
                                mat[c4d.BRDFVRAYMTL_DIFFUSE_TEXTURE] = fusion_shader
                            bitmap = c4d.BaseShader(ID.VRAY_BITMAP)
                            bitmap[c4d.BITMAPSHADER_FILENAME] = fullPath
                            fusion_shader.InsertShader(bitmap)
                            fusion_shader[c4d.SLA_FUSION_BASE_CHANNEL] = bitmap
                                    
                    elif mapID == "AO":
                        if not fusion_shader:
                            fusion_shader = c4d.BaseShader(c4d.Xfusion)
                            fusion_shader[c4d.SLA_FUSION_MODE] = c4d.SLA_FUSION_MODE_MULTIPLY
                            mat.InsertShader(fusion_shader)
                            mat[c4d.BRDFVRAYMTL_DIFFUSE_TEXTURE] = fusion_shader
                        bitmap = c4d.BaseShader(ID.VRAY_BITMAP)
                        bitmap[c4d.BITMAPSHADER_FILENAME] = fullPath
                        fusion_shader.InsertShader(bitmap)
                        fusion_shader[c4d.SLA_FUSION_BLEND_CHANNEL] = bitmap

                    elif mapID == "NRM":
                        bitmap = c4d.BaseShader(ID.VRAY_BITMAP)
                        bitmap[c4d.BITMAPSHADER_FILENAME] = fullPath
                        bitmap[c4d.BITMAPSHADER_COLORPROFILE] = 1
                        mat.InsertShader(bitmap)
                        texture = c4d.BaseShader(ID.VRAY_NORMAL_MAP)
                        texture[c4d.TEXNORMALBUMP_BUMP_TEX_COLOR] = bitmap
                        texture[c4d.TEXNORMALBUMP_MAP_TYPE] = 1
                        mat.InsertShader(texture)
                        mat[c4d.BRDFVRAYMTL_BUMP_MAP] = texture

                    elif mapID == "GLOSS":
                        bitmap = c4d.BaseShader(ID.VRAY_BITMAP)
                        bitmap[c4d.BITMAPSHADER_FILENAME] = fullPath
                        mat.InsertShader(bitmap)
                        mat[c4d.BRDFVRAYMTL_REFLECT_GLOSSINESS_TEXTURE] = bitmap
                        vec = c4d.Vector(255,255,255)
                        mat[c4d.BRDFVRAYMTL_REFLECT_VALUE] = vec

                    elif mapID == "METAL":
                        bitmap = c4d.BaseShader(ID.VRAY_BITMAP)
                        bitmap[c4d.BITMAPSHADER_FILENAME] = fullPath
                        mat.InsertShader(bitmap)
                        mat[c4d.BRDFVRAYMTL_METALNESS_TEXTURE] = bitmap

                    elif mapID == "OPAC":
                        bitmap = c4d.BaseShader(ID.VRAY_BITMAP)
                        bitmap[c4d.BITMAPSHADER_FILENAME] = fullPath
                        mat.InsertShader(bitmap)
                        mat[c4d.BRDFVRAYMTL_OPACITY_COLOR_TEXTURE] = bitmap

                    elif mapID == "SSS":
                        bitmap = c4d.BaseShader(ID.VRAY_BITMAP)
                        bitmap[c4d.BITMAPSHADER_FILENAME] = fullPath
                        mat.InsertShader(bitmap)
                        mat[c4d.BRDFVRAYMTL_TRANSLUCENCY_COLOR_TEXTURE] = bitmap
                        mat[c4d.BRDFVRAYMTL_TRANSLUCENCY] = 6
                                    
                    elif mapID == "SHEEN":
                        bitmap = c4d.BaseShader(ID.VRAY_BITMAP)
                        bitmap[c4d.BITMAPSHADER_FILENAME] = fullPath
                        mat.InsertShader(bitmap)
                        mat[c4d.BRDFVRAYMTL_SHEEN_COLOR_TEXTURE] = bitmap

                    elif mapID == "SHEENGLOSS":
                        bitmap = c4d.BaseShader(ID.VRAY_BITMAP)
                        bitmap[c4d.BITMAPSHADER_FILENAME] = fullPath
                        mat.InsertShader(bitmap)
                        mat[c4d.BRDFVRAYMTL_SHEEN_GLOSSINESS_TEXTURE] = bitmap

                doc = c4d.documents.GetActiveDocument()
                doc.StartUndo()
                doc.InsertMaterial(mat)
                doc.AddUndo(c4d.UNDOTYPE_NEW, mat)
                doc.EndUndo()
                material_to_add.append(mat)                                   
                self.SetString(ID.DIALOG_ERROR, "")


            ################
            ### Redshift ###
            ################

            if self.GetInt32(ID.DIALOG_RENDERER_COMBOBOX) == 6403:

                if not c4d.plugins.FindPlugin(1036219):
                    c4d.gui.MessageDialog("Redshift is not installed")
                    return
                
                color_layer_node = None
                color_layer_added = False
                doc = c4d.documents.GetActiveDocument()
                render_data = doc.GetActiveRenderData()
                render_data[c4d.RDATA_RENDERENGINE] = 1036219
                c4d.EventAdd()

                rs_node_space_id: maxon.Id = maxon.Id("com.redshift3d.redshift4c4d.class.nodespace")
                output_node_id: maxon.Id = maxon.Id(("com.redshift3d.redshift4c4d.nodes.core.standardmaterial"))
                displacement_node_id: maxon.Id = maxon.Id("com.redshift3d.redshift4c4d.nodes.core.displacement")

                displacement_tex_map_input_port_node_id: maxon.String = "com.redshift3d.redshift4c4d.nodes.core.displacement.texmap"
                displacement_out_port_id: maxon.String = "com.redshift3d.redshift4c4d.nodes.core.displacement.out"

                color_input_port_in_output_node_id: maxon.String = "com.redshift3d.redshift4c4d.nodes.core.standardmaterial.base_color"
                roughness_input_port_in_output_node_id: maxon.String = "com.redshift3d.redshift4c4d.nodes.core.standardmaterial.refl_roughness"
                metalness_input_port_in_output_node_id: maxon.String = "com.redshift3d.redshift4c4d.nodes.core.standardmaterial.metalness"
                opacity_input_port_in_output_node_id: maxon.String = "com.redshift3d.redshift4c4d.nodes.core.standardmaterial.opacity_color"
                subsurface_input_port_in_output_node_id: maxon.String = "com.redshift3d.redshift4c4d.nodes.core.standardmaterial.ms_color"
                sheen_input_port_in_output_node_id: maxon.String = "com.redshift3d.redshift4c4d.nodes.core.standardmaterial.sheen_color"
                sheengloss_input_port_in_output_node_id: maxon.String = "com.redshift3d.redshift4c4d.nodes.core.standardmaterial.sheen_roughness"
                bumpmap_input_port_in_output_node_id: maxon.String = "com.redshift3d.redshift4c4d.nodes.core.standardmaterial.bump_input"
                                

                texture_node_id: maxon.Id = maxon.Id("com.redshift3d.redshift4c4d.nodes.core.texturesampler")
                texture_node_port_id: maxon.String = "com.redshift3d.redshift4c4d.nodes.core.texturesampler.tex0"
                texture_nodepath_port_id: maxon.String = "path"
                texture_nodepath_colorspace_id: maxon.String = "colorspace"
                texture_color_out_port_id: maxon.String = "com.redshift3d.redshift4c4d.nodes.core.texturesampler.outcolor"


                bump_node_id: maxon.Id = maxon.Id("com.redshift3d.redshift4c4d.nodes.core.bumpmap")
                bump_in_port_id: maxon.String = "com.redshift3d.redshift4c4d.nodes.core.bumpmap.input"
                bump_out_port_id: maxon.String = "com.redshift3d.redshift4c4d.nodes.core.bumpmap.out"
                bump_type_in_port_id: maxon.String = "com.redshift3d.redshift4c4d.nodes.core.bumpmap.inputtype"

                color_layer_node_id: maxon.Id = maxon.Id("com.redshift3d.redshift4c4d.nodes.core.rscolorlayer")
                color_layer_color_in_port_id: maxon.String = "com.redshift3d.redshift4c4d.nodes.core.rscolorlayer.base_color"
                colorlayer_layer_one_in_port_id: maxon.String = "com.redshift3d.redshift4c4d.nodes.core.rscolorlayer.layer1_color"
                colorlayer_layer_one_blend_mode_in_port_id : maxon.String = "com.redshift3d.redshift4c4d.nodes.core.rscolorlayer.layer1_blend_mode"
                color_layer_color_out_port_id: maxon.String = "com.redshift3d.redshift4c4d.nodes.core.rscolorlayer.outcolor"

                mat: c4d.BaseMaterial = c4d.BaseMaterial(c4d.Mmaterial)
                # parts = file.split(".")[0].split("_")
                mat.SetName(checkbox)
                mat[c4d.MATERIAL_PREVIEWSIZE] = 10
                if not mat:
                    raise MemoryError(f"{mat = }")
                node_material: c4d.node_material = mat.GetNodeMaterialReference()
                graph: maxon.GraphModelRef = node_material.CreateDefaultGraph(rs_node_space_id)
                
                doc.InsertMaterial(mat)
                result: list[maxon.GraphNode] = []
                maxon.GraphModelHelper.FindNodesByAssetId(graph, output_node_id, True, result)
                if len(result) < 1:
                    raise RuntimeError("Could not find standard node in material.")
                output_node: maxon.GraphNode = result[0]

                for index, mapID in enumerate(uploaded_maps):
                    # gets the path of the actual file through its index
                    fullPath = uploaded_paths[index]

                    with graph.BeginTransaction() as transaction:
                                        
                        if mapID == "COL" or mapID == "AO":
                            if mapID == "COL" or "AO" not in uploaded_maps:
                                texture_node = graph.AddChild(maxon.Id(), texture_node_id)
                                                
                                path_port = texture_node.GetInputs().FindChild(texture_node_port_id).FindChild(texture_nodepath_port_id)
                                path_port.SetDefaultValue(maxon.Url(fullPath))

                                texture_out_port: maxon.GraphNode = texture_node.GetOutputs().FindChild(texture_color_out_port_id)
                                color_input_port_in_output_node : maxon.GraphNode = output_node.GetInputs().FindChild(color_input_port_in_output_node_id)
                                texture_out_port.Connect(color_input_port_in_output_node)
                                                
                                transaction.Commit()
                                            
                        elif mapID == "COL":
                            if color_layer_added == False:
                                color_layer_node = graph.AddChild(maxon.Id(), color_layer_node_id)
                                color_layer_out_port_node: maxon.GraphNode = color_layer_node.GetOutputs().FindChild(color_layer_color_out_port_id)
                                color_layer_input_port_in_output_node : maxon.GraphNode = output_node.GetInputs().FindChild(color_input_port_in_output_node_id)
                                color_layer_out_port_node.Connect(color_layer_input_port_in_output_node)
                                color_layer_added = True
                                                
                                texture_node = graph.AddChild(maxon.Id(), texture_node_id)
                                path_port = texture_node.GetInputs().FindChild(texture_node_port_id).FindChild(texture_nodepath_port_id)
                                path_port.SetDefaultValue(maxon.Url(fullPath))
                                texture_out_port: maxon.GraphNode = texture_node.GetOutputs().FindChild(texture_color_out_port_id)
                                color_layer_color_in_port: maxon.GraphNode = color_layer_node.GetInputs().FindChild(color_layer_color_in_port_id)
                                texture_out_port.Connect(color_layer_color_in_port)
                                                
                                transaction.Commit()
                                            
                        elif mapID == "AO":
                            if color_layer_added == False:
                                color_layer_node = graph.AddChild(maxon.Id(), color_layer_node_id)
                                color_layer_out_port_node: maxon.GraphNode = color_layer_node.GetOutputs().FindChild(color_layer_color_out_port_id)
                                color_layer_input_port_in_output_node : maxon.GraphNode = output_node.GetInputs().FindChild(color_input_port_in_output_node_id)
                                color_layer_out_port_node.Connect(color_layer_input_port_in_output_node)
                                color_layer_added = True
                                                
                                texture_node = graph.AddChild(maxon.Id(), texture_node_id)
                                path_port = texture_node.GetInputs().FindChild(texture_node_port_id).FindChild(texture_nodepath_port_id)
                                path_port.SetDefaultValue(maxon.Url(fullPath))
                                texture_out_port: maxon.GraphNode = texture_node.GetOutputs().FindChild(texture_color_out_port_id)
                                colorlayer_layer_one_in_port: maxon.GraphNode = color_layer_node.GetInputs().FindChild(colorlayer_layer_one_in_port_id)
                                colorlayer_layer_one_blend_mode_in_port: maxon.GraphNode = color_layer_node.GetInputs().FindChild(colorlayer_layer_one_blend_mode_in_port_id)
                                colorlayer_layer_one_blend_mode_in_port.SetDefaultValue(4)
                                texture_out_port.Connect(colorlayer_layer_one_in_port)
                                                
                                transaction.Commit()
                            else:
                                continue
                                        
                        elif mapID == "ROUGH":
                            texture_node = graph.AddChild(maxon.Id(), texture_node_id)
                            path_port = texture_node.GetInputs().FindChild(texture_node_port_id).FindChild(texture_nodepath_port_id)
                            path_port.SetDefaultValue(maxon.Url(fullPath))
                            texture_out_port: maxon.GraphNode = texture_node.GetOutputs().FindChild(texture_color_out_port_id)
                            roughness_input_port_in_output_node : maxon.GraphNode = output_node.GetInputs().FindChild(roughness_input_port_in_output_node_id)
                            texture_out_port.Connect(roughness_input_port_in_output_node)
                            
                            transaction.Commit()
                                        
                        elif mapID == "METAL":
                            texture_node = graph.AddChild(maxon.Id(), texture_node_id)
                            path_port = texture_node.GetInputs().FindChild(texture_node_port_id).FindChild(texture_nodepath_port_id)
                            path_port.SetDefaultValue(maxon.Url(fullPath))
                            texture_out_port: maxon.GraphNode = texture_node.GetOutputs().FindChild(texture_color_out_port_id)
                            metalness_input_port_in_output_node : maxon.GraphNode = output_node.GetInputs().FindChild(metalness_input_port_in_output_node_id)
                            texture_out_port.Connect(metalness_input_port_in_output_node)
                                            
                            transaction.Commit()
                                        
                        elif mapID == "OPAC":
                            texture_node = graph.AddChild(maxon.Id(), texture_node_id)
                            path_port = texture_node.GetInputs().FindChild(texture_node_port_id).FindChild(texture_nodepath_port_id)
                            path_port.SetDefaultValue(maxon.Url(fullPath))
                            texture_out_port: maxon.GraphNode = texture_node.GetOutputs().FindChild(texture_color_out_port_id)
                            opacity_input_port_in_output_node : maxon.GraphNode = output_node.GetInputs().FindChild(opacity_input_port_in_output_node_id)
                            texture_out_port.Connect(opacity_input_port_in_output_node)
                                            
                            transaction.Commit()
                                        
                        elif mapID == "SSS":
                            texture_node = graph.AddChild(maxon.Id(), texture_node_id)
                            path_port = texture_node.GetInputs().FindChild(texture_node_port_id).FindChild(texture_nodepath_port_id)
                            path_port.SetDefaultValue(maxon.Url(fullPath))
                            texture_out_port: maxon.GraphNode = texture_node.GetOutputs().FindChild(texture_color_out_port_id)
                            subsurface_input_port_in_output_node : maxon.GraphNode = output_node.GetInputs().FindChild(subsurface_input_port_in_output_node_id)
                            texture_out_port.Connect(subsurface_input_port_in_output_node)
                                            
                            transaction.Commit()
                                        
                        elif mapID == "SHEEN":
                            texture_node = graph.AddChild(maxon.Id(), texture_node_id)
                            path_port = texture_node.GetInputs().FindChild(texture_node_port_id).FindChild(texture_nodepath_port_id)
                            path_port.SetDefaultValue(maxon.Url(fullPath))
                            texture_out_port: maxon.GraphNode = texture_node.GetOutputs().FindChild(texture_color_out_port_id)
                            sheen_input_port_in_output_node : maxon.GraphNode = output_node.GetInputs().FindChild(sheen_input_port_in_output_node_id)
                            texture_out_port.Connect(sheen_input_port_in_output_node)
                                            
                            transaction.Commit()
                                        
                        elif mapID == "SHEENGLOSS":
                            texture_node = graph.AddChild(maxon.Id(), texture_node_id)
                            path_port = texture_node.GetInputs().FindChild(texture_node_port_id).FindChild(texture_nodepath_port_id)
                            path_port.SetDefaultValue(maxon.Url(fullPath))
                            texture_out_port: maxon.GraphNode = texture_node.GetOutputs().FindChild(texture_color_out_port_id)
                            sheengloss_input_port_in_output_node : maxon.GraphNode = output_node.GetInputs().FindChild(sheengloss_input_port_in_output_node_id)
                            texture_out_port.Connect(sheengloss_input_port_in_output_node)
                                            
                            transaction.Commit()

                        elif mapID == "NRM":
                            bump_node = graph.AddChild(maxon.Id(), bump_node_id)
                            bump_out_port_node: maxon.GraphNode = bump_node.GetOutputs().FindChild(bump_out_port_id)
                            bumpmap_input_port_in_output_node : maxon.GraphNode = output_node.GetInputs().FindChild(bumpmap_input_port_in_output_node_id)
                            bump_out_port_node.Connect(bumpmap_input_port_in_output_node)
                                            
                            texture_node = graph.AddChild(maxon.Id(), texture_node_id)
                            path_port = texture_node.GetInputs().FindChild(texture_node_port_id).FindChild(texture_nodepath_port_id)
                            path_port.SetDefaultValue(maxon.Url(fullPath))
                            colorspace_port = texture_node.GetInputs().FindChild(texture_node_port_id).FindChild(texture_nodepath_colorspace_id)
                            colorspace_port.SetDefaultValue("RS_INPUT_COLORSPACE_SRGB_LINEAR")
                                            
                            texture_out_port: maxon.GraphNode = texture_node.GetOutputs().FindChild(texture_color_out_port_id)
                            bumpmap_input_port_in_output_node : maxon.GraphNode = bump_node.GetInputs().FindChild(bump_in_port_id)
                            bumpmapTypeInputPortInoutput_node: maxon.GraphNode = bump_node.GetInputs().FindChild(bump_type_in_port_id)
                            bumpmapTypeInputPortInoutput_node.SetDefaultValue(1)
                            texture_out_port.Connect(bumpmap_input_port_in_output_node)
                                            
                            transaction.Commit()

                    c4d.EventAdd()

                doc.InsertMaterial(mat)
                
            c4d.EventAdd()
            # emptying the lists for another material
            uploaded_indexes.clear()
            uploaded_files.clear()
            uploaded_maps.clear()
            uploaded_paths.clear()

        if id == ID.DIALOG_SELECT_ALL_BUTTON:
            select_all = True
            # goes through all items in tex_list
            for item in tex_list:
                # if the item is not selected
                if item.IsSelected == False:
                    # sets the value to False
                    select_all = False
            # if all checkboxes are selected
            if select_all == True:
                # goes through all items in tex_list
                for item in tex_list:
                    # deselect the item
                    item.Deselect()
            else:
                # otherwise it goes through all checkboxes
                for item in tex_list:
                    # and select all checkboxes
                    item.Select()
            # refresh the treeview
            self._treegui.Refresh()
        
    def SetError(self, message):
        if not message:
            message = ""
        self.SetString(ID.DIALOG_ERROR, message)

    def SetListItems(self, message):
        if not message:
            message= ""
            self.SetString(ID.DIALOG_FOLDER_LIST, message)

    def Reset(self):
        self.materialFolder = None
    
        self.has16bDisp = False
        self.has16bNormal = False
        self.hasDisp = False
        self.hasAO = False
        self.hasIor = False
        
        self.SetBool(ID.DIALOG_MAP_AO_CB, False)
        self.Enable(ID.DIALOG_MAP_AO_CB, False)
        self.SetBool(ID.DIALOG_MAP_DISPL_CB, False)
        self.Enable(ID.DIALOG_MAP_DISPL_CB, False)
        self.SetBool(ID.DIALOG_MAP_16B_DISPL_CB, False)
        self.Enable(ID.DIALOG_MAP_16B_DISPL_CB, False)
        self.SetBool(ID.DIALOG_MAP_16B_NORMAL_CB, False)
        self.Enable(ID.DIALOG_MAP_16B_NORMAL_CB, False)
        self.SetBool(ID.DIALOG_MAP_IOR_CB, False)
        self.Enable(ID.DIALOG_MAP_IOR_CB, False)
        self.Enable(ID.DIALOG_LOAD_BUTTON, False)
        # self.Enable(ID.FILTER_MATERIALS_BUTTON, False)
        
class ReawoteSorter(plugins.CommandData):
    
    thread = None

    def __init__(self) -> None:
        super().__init__()
        global dialog
        if not dialog:
            dialog = ReawoteSorterDialog()

    def Execute(self, doc):
        dialog.Open(c4d.DLG_TYPE_ASYNC, REAWOTE_SORTER_ID, -3, -3, 550, 800)
        return True
        
    def CoreMessage(self, id, msg):
        # Checks if texture baking has finished
        if id==REAWOTE_SORTER_ID:
            print("Command received!")
            print("Path is: " + self.thread.path)
            return True

        return gui.GeDialog.CoreMessage(self, id, msg)