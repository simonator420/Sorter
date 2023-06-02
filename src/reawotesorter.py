import os
import sys

import c4d
from c4d import plugins, gui, storage, documents

REAWOTE_SORTER_ID=1060870

dialog = None

checkbox_list = []
same_path_dirs = []
material_to_add = []
materialCount = []
child_list = []
child_name_list = []
map_id_list = []
material_id_list = []
material_name_list = []
selected_materials = []
selected_maps = []
selected_files = []
tex_list = []
map_names_list = ["AO_Ambient occlusion", "NRM_Normal map", "DISP_Displacement", "DIFF_Diffuse","COL_Color", "GLOSS_Glossiness", "ROUGH_Roughness", "METAL_Metallic", "SPEC_Specular", "SSS_Subsurface scattering", "SSSABSORB_SSS absorbtion", "OPAC_Opacit", "ANIS_Anisotropy", "SHEEN_Sheen"]    
newID = 0
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
    DIALOG_SCROLL_GROUP = 100012
    DIALOG_SCROLL_GROUP_TWO = 100016
    DIALOG_SECONDARY_GROUP = 10011
    DIALOG_FOLDER_LIST = 100015
    FILTER_MATERIALS_BUTTON = 100017
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
    DIALOG_DROPBOX_MAIN3 = 100026

    DIALOG_GROUP_MINI_BUTTONS = 100031
    DIALOG_SELECT_ALL_BUTTON = 100018
    DIALOG_ADD_TO_QUEUE_BUTTON = 100032

    ID_CHILD = 9000

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
                self.listOfTexture.remove(tex)
    
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
        super(ReawoteSorterDialog, self).__init__()
        pass

    def CreateLayout(self):

        defaultFlags: int = c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT
        scrollflags = c4d.SCROLLGROUP_VERT | c4d.SCROLLGROUP_HORIZ | c4d.SCROLLGROUP_AUTOHORIZ|c4d.SCROLLGROUP_AUTOVERT

        self.SetTitle("Reawote Sorter")

        self.ScrollGroupBegin(ID.DIALOG_SCROLL_GROUP, defaultFlags, c4d.SCROLLGROUP_VERT | c4d.SCROLLGROUP_HORIZ)
        self.GroupBegin(ID.DIALOG_MAIN_GROUP, defaultFlags, 1)

        self.GroupBegin(ID.DIALOG_FOLDER_GROUP, c4d.BFH_SCALEFIT, 2, 1, "Material folder", 0, 10, 10)
        self.GroupBorderSpace(8, 0, 0, 2)
        self.AddStaticText(ID.DIALOG_FOLDER_TEXT, c4d.BFH_SCALEFIT, 0, 0, "Material folder", 0)
        self.AddButton(ID.DIALOG_FOLDER_BUTTON, c4d.BFH_SCALEFIT, 1, 1, "Browse")
        self.GroupEnd()

        pathBox = self.AddEditText(ID.DIALOG_FOLDER_LIST,  c4d.BFH_SCALEFIT, inith=10, initw=50)

        self.GroupBegin(ID.DIALOG_GROUP_DROPBOXES, c4d.BFH_SCALEFIT, 3, 1, "File Select", 0, 10, 10)
        self.AddButton(ID.DIALOG_DROPBOX_BUTTON1,c4d.BFH_LEFT, initw=50,inith=0, name="<")
        self.AddComboBox(ID.DIALOG_DROPBOX_MAIN,c4d.BFH_SCALEFIT, allowfiltering=True)
        self.AddButton(ID.DIALOG_DROPBOX_BUTTON2,c4d.BFH_RIGHT, initw=50,inith=0, name=">")
        self.GroupEnd()

        self.GroupBegin(ID.DIALOG_GROUP2_DOPBOXES, c4d.BFH_SCALEFIT, 3, 1, "Dropbox", 0, 10, 10)
        self.GroupBorderSpace(8, 2, 0, 2)
        self.AddStaticText(ID.DIALOG_TEXT2_DROPBOX, c4d.BFH_SCALEFIT, 0, 0, "Select map", 0)
        self.AddComboBox(ID.DIALOG_DROPBOX_MAIN3, c4d.BFH_CENTER, initw=250, inith=0)
        self.GroupEnd()

        self.GroupBegin(ID.DIALOG_GROUP3_DOPBOXES, c4d.BFH_SCALEFIT, 3, 1, "Map Select", 0, 10, 10)
        self.GroupBorderSpace(8, 2, 0, 2)
        self.AddStaticText(ID.DIALOG_TEXT_DROPBOX, c4d.BFH_SCALEFIT, 0, 0, "Select material", 0)
        self.AddComboBox(ID.DIALOG_DROPBOX_MAIN2, c4d.BFH_CENTER, initw=250, inith=0)
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

        self.AddButton(ID.DIALOG_ADD_TO_LIST_BUTTON, c4d.BFH_SCALEFIT, 1, 1, "Add to list")
        self.AddButton(ID.FILTER_MATERIALS_BUTTON, c4d.BFH_SCALEFIT, 1, 1, "Filter materials")

        cbAO = self.AddCheckbox(ID.DIALOG_MAP_AO_CB, c4d.BFH_SCALEFIT, 1, 1, "Include ambient occlusion (AO) maps")
        cbDispl = self.AddCheckbox(ID.DIALOG_MAP_DISPL_CB, c4d.BFH_SCALEFIT, 1, 1, "Include displacement maps")
        cb16bdispl = self.AddCheckbox(ID.DIALOG_MAP_16B_DISPL_CB, c4d.BFH_SCALEFIT, 1, 1, "Use 16 bit displacement maps (when available)")
        cb16bnormal = self.AddCheckbox(ID.DIALOG_MAP_16B_NORMAL_CB, c4d.BFH_SCALEFIT, 1, 1, "Use 16 bit normal maps (when available)")
        
        self.GroupBegin(ID.DIALOG_GROUP_MINI_BUTTONS, c4d.BFH_SCALEFIT, 2, 1, "Mini Buttons", 0, 10, 10)
        self.AddButton(ID.DIALOG_SELECT_ALL_BUTTON, c4d.BFH_LEFT, 70, 5, "Select All")
        self.AddButton(ID.DIALOG_ADD_TO_QUEUE_BUTTON, c4d.BFH_LEFT, 110, 5, "Add To Queue")
        self.GroupEnd()

        self._treegui = self.AddCustomGui(9300, c4d.CUSTOMGUI_TREEVIEW, "", c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 300, 300, customgui)
        if not self._treegui:
            print ("[ERROR]: Could not create TreeView")
            return False
    
        self.GroupBegin(ID.DIALOG_SCROLL_GROUP, c4d.BFH_SCALEFIT, 2, 1, "Material folder", 0, 10, 10)
        self.GroupEnd()
        self.GroupEnd(ID.DIALOG_MAIN_GROUP)
        self.GroupEnd(ID.DIALOG_SCROLL_GROUP)
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

        self.Enable(ID.DIALOG_ADD_TO_QUEUE_BUTTON, False)
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

        # deletes all items in treeview if not empty
        while len(self._listView.listOfTexture) > 0:
            tex = self._listView.listOfTexture[0]
            self._listView.listOfTexture.remove(tex)
        self._treegui.Refresh()

        return True

    # recognising the string
    def auto_assign(self, actual_name):
        # if there is a variable set
        if actual_name:
            # check all possible map names and types
            if "AO" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4500)
            elif "NRM" in actual_name:
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
            elif "DISP16" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4502)
            elif "DIFF" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4503)
            elif "diff" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4503)
            elif "diffuse" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4503)
            elif "COL" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4504)
            elif "COLOR" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4504)
            elif "GLOSS" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4505)
            elif "Glosiness" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4505)
            elif "ROUGH" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4506)
            elif "METAL" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4507)
            elif "SPEC" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4508)
            elif "Specular" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4508)
            elif "spec" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4508)
            elif "SPECLVL" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4508)
            elif "SSSABSORB_SSS" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4509)
            elif "OPAC" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4510)
            elif "ANIS" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4511)
            elif "SHEEN" in actual_name:
                self.SetInt32(ID.DIALOG_DROPBOX_MAIN3, 4512)
        else:
            print("I'm on the edge")

    def get_name_from_id(self, id: int, index_list: list, name_list: list):
        index = index_list.index(id)
        name = name_list[index]
        return name

    # gets the next item in the dropbox        
    def get_next_item(self, dropbox_id: int, file_list: list, file_name_list: list):
        actual = self.GetLong(dropbox_id)
        if actual+1 in file_list:
            next = actual+1
            self.SetInt32(dropbox_id, next)
            index = file_list.index(next)
            actual_name = file_name_list[index]
            self.auto_assign(actual_name)

    # gets the previous item in the dropbox
    def get_previous_item(self, dropbox_id: int, file_list: list, file_name_list: list):
        actual = self.GetLong(dropbox_id)
        if actual-1 in file_list:
            previous = actual-1
            self.SetInt32(dropbox_id, previous)
            index = file_list.index(previous)
            actual_name = file_name_list[index]
            self.auto_assign(actual_name)


    def Command(self, id, msg,):
        if id == ID.DIALOG_FOLDER_BUTTON:
            path = c4d.storage.LoadDialog(title="Choose material folder", flags=c4d.FILESELECT_DIRECTORY)
            if path == None:
                return True
            try:
                path = path.decode("utf-8")
            except: 
                pass
            
            # textBox fills up with path of chosen folder
            self.SetString(ID.DIALOG_FOLDER_LIST, path)

            print(path)
            # saves all files in path as dir
            dir = os.listdir(path)
            map_names_list = ["AO_Ambient occlusion", "NRM_Normal map", "DISP_Displacement", "DIFF_Diffuse","COL_Color", "GLOSS_Glossiness", "ROUGH_Roughness", "METAL_Metallic", "SPEC_Specular", "SSS_Subsurface scattering", "SSSABSORB_SSS absorbtion", "OPAC_Opacit", "ANIS_Anisotropy", "SHEEN_Sheen"]
            # variable for first item in dir
            first_name = None
            num = 0
            ID_CHILD = 9000
            for file in dir:
                folder_path = os.path.join(path, file)
                while num <= 0:
                    first_name = file
                    num += 1
                ID_CHILD += 1
                self.AddChild(ID.DIALOG_DROPBOX_MAIN, ID_CHILD, file)
                child_list.append(ID_CHILD)
                child_name_list.append(file)
                print(first_name)
                checkbox_list.append(file)
                print(f"{file} checkbox byl vytvořen a přidán do listu")
                print(folder_path)
                print(ID_CHILD)
                print(" ")
                # refresh the TreeView
                self._treegui.Refresh()

                # for targetFolderName in targetFolders:
                #     if targetFolderName in subdirs:
                #         targetFolder = os.path.join(folder_path, targetFolderName)
                #         dirPath = os.listdir(targetFolder)
                #         hasColor = False
                #         for file1 in dirPath:
                #                 try: 
                #                     parts = file1.split(".")[0].split("_")
                #                     manufacturer = parts[0]
                #                     productNumber = parts[1]
                #                     product = parts[2]
                #                     mapID = parts[3]
                #                     resolution = parts[4]
                #                     if mapID == "DIFF" or mapID == "COLOR" or mapID == "COL":
                #                         hasColor = True
                #                     if mapID == "DISP16":
                #                         self.has16bDisp = True
                #                         self.hasDisp = True
                #                     if mapID == "DISP":
                #                         self.hasDisp = True
                #                     if mapID == "AO":
                #                         self.hasAO = True
                #                     if mapID == "IOR":
                #                         self.hasIor = True
                #                     if mapID == "NRM16":
                #                         self.has16bNormal = True
                #                 except:
                #                     pass
                #         if self.hasAO:
                #             self.SetBool(ID.DIALOG_MAP_AO_CB, True)
                #             self.Enable(ID.DIALOG_MAP_AO_CB, True)
                #         if self.hasDisp:
                #             self.SetBool(ID.DIALOG_MAP_DISPL_CB, True)
                #             self.Enable(ID.DIALOG_MAP_DISPL_CB, True)
                #         if self.has16bDisp:
                #             self.SetBool(ID.DIALOG_MAP_16B_DISPL_CB, True)
                #             self.Enable(ID.DIALOG_MAP_16B_DISPL_CB, True)
                #         if self.has16bNormal:
                #             self.SetBool(ID.DIALOG_MAP_16B_NORMAL_CB, True)
                #             self.Enable(ID.DIALOG_MAP_16B_NORMAL_CB, True)
                #         if self.hasIor:
                #             self.SetBool(ID.DIALOG_MAP_IOR_CB, False)
                #             self.Enable(ID.DIALOG_MAP_IOR_CB, True)
                #         if hasColor:
                #             self.materialFolder = path
                #             self.Enable(ID.DIALOG_LOAD_BUTTON, True)
                #             self.SetError("")
                #         else:
                #             self.SetError("One or more folders do not contain the correct Reawote material.")
                #             print(folder, " neobsahuje spravnou slozku")


            # enables pressing the Filter materials button
            self.Enable(ID.FILTER_MATERIALS_BUTTON, True)
            # enables pressing the Select all button
            self.Enable(ID.DIALOG_SELECT_ALL_BUTTON, True)

            self.Enable(ID.DIALOG_DROPBOX_BUTTON1, True)
            self.Enable(ID.DIALOG_DROPBOX_MAIN, True)
            self.Enable(ID.DIALOG_DROPBOX_BUTTON2, True)

            self.Enable(ID.DIALOG_TEXT2_DROPBOX, True)
            self.Enable(ID.DIALOG_DROPBOX_MAIN3, True)

            self.Enable(ID.DIALOG_TEXT_DROPBOX, True)
            self.Enable(ID.DIALOG_DROPBOX_MAIN2, True)
            self.Enable(ID.DIALOG_ADD_TO_QUEUE_BUTTON, True)
            self.Enable(ID.DIALOG_ADD_TO_LIST_BUTTON, True)
            
            count = len(checkbox_list)
            n = 1
            id_mat = 4000
            while count >= n:
                material_name = "Material " + str(n)
                self.AddChild(ID.DIALOG_DROPBOX_MAIN2, id_mat, material_name)
                n+=1
                material_id_list.append(id_mat)
                material_name_list.append(material_name)
                id_mat+=1
            
            id_map = 4500
            map_names_list = ["AO_Ambient occlusion", "NRM_Normal map", "DISP_Displacement", "DIFF_Diffuse","COL_Color", "GLOSS_Glossiness", "ROUGH_Roughness", "METAL_Metallic", "SPEC_Specular", "SSS_Subsurface scattering", "SSSABSORB_SSS absorbtion", "OPAC_Opacit", "ANIS_Anisotropy", "SHEEN_Sheen"]
            for map in map_names_list:
                self.AddChild(ID.DIALOG_DROPBOX_MAIN3, id_map, map)
                map_id_list.append(id_map)                
                id_map+=1
            self.SetInt32(ID.DIALOG_DROPBOX_MAIN, child_list[0])
            parts = first_name.split(".")[0].split("_")
            mapID = parts[3]
            self.auto_assign(first_name)

        if id == ID.DIALOG_ADD_TO_QUEUE_BUTTON:
            path = c4d.storage.LoadDialog(title="Choose folder to be added to TreeView", flags=c4d.FILESELECT_DIRECTORY)
            if path == None:
                return True
            try:
                path = path.decode("utf-8")
            except:
                pass

            self.SetString(ID.DIALOG_FOLDER_LIST, path)
            dir = os.listdir(path)
            ID_CHILD = child_list[-1]
            for file in dir:
                folder_path = os.path.join(path,file)
                ID_CHILD += 1
                self.AddChild(ID.DIALOG_DROPBOX_MAIN, ID_CHILD, file)
                child_list.append(ID_CHILD)
                child_name_list.append(file)
                checkbox_list.append(file)
                print(ID_CHILD)
                            
        # go back button <
        if id == ID.DIALOG_DROPBOX_BUTTON1:
            self.get_previous_item(ID.DIALOG_DROPBOX_MAIN, child_list, child_name_list)
        
        # go forward button >
        if id == ID.DIALOG_DROPBOX_BUTTON2:
            self.get_next_item(ID.DIALOG_DROPBOX_MAIN, child_list, child_name_list)

        #TODO Select all, Hledani obecne materialu mimo reawote, hledani podle zkratek

        #TODO comment all sections of the code

        if id == ID.DIALOG_ADD_TO_LIST_BUTTON:
            selected_file_id = self.GetInt32(ID.DIALOG_DROPBOX_MAIN)
            selected_file_name = self.get_name_from_id(selected_file_id, child_list, child_name_list)
            print("")
            print("Selected file: ", selected_file_name, " and his ID: ", selected_file_id)
            
            map_names_list = ["AO_Ambient occlusion", "NRM_Normal map", "DISP_Displacement", "DIFF_Diffuse","COL_Color", "GLOSS_Glossiness", "ROUGH_Roughness", "METAL_Metallic", "SPEC_Specular", "SSS_Subsurface scattering", "SSSABSORB_SSS absorbtion", "OPAC_Opacit", "ANIS_Anisotropy", "SHEEN_Sheen"]            
            map_shortcuts = ["AO", "NRM", "DISP", "DIFF", "COL", "GLOSS","ROUGH", "METAL", "SPEC", "SSS", "SSSABSORB", "OPAC", "ANIS", "SHEEN"]
            selected_map_id = self.GetInt32(ID.DIALOG_DROPBOX_MAIN3)
            selected_map_name = self.get_name_from_id(selected_map_id, map_id_list, map_shortcuts)
            print("Selected map: ", selected_map_name, " and his ID: ", selected_map_id)
            
            selected_material_id = self.GetInt32(ID.DIALOG_DROPBOX_MAIN2)
            selected_material_name = self.get_name_from_id(selected_material_id, material_id_list, material_name_list)
            print("Selected material:", selected_material_name, " and his ID: ", selected_material_id)

            newID = len(self._listView.listOfTexture) + 1
            print(newID)
            tex = TextureObject(selected_file_name.format(newID),selected_map_name, selected_material_name)
            self._listView.listOfTexture.append(tex)
            self._treegui.Refresh()
            tex_list.append(tex)

            selected_files.append(selected_file_name)
            selected_materials.append(selected_material_name)
            selected_maps.append(selected_map_name)
            
            self.get_next_item(ID.DIALOG_DROPBOX_MAIN, child_list, child_name_list)

        if id == ID.FILTER_MATERIALS_BUTTON:
            # goes through all checkboxes
            materials_upload = []
            map_upload = []
            assigned_material = ""
            for index, checkbox in enumerate(tex_list):
                print("Tohle je checkbox v listu tex_list: ", checkbox)
                # print("Tohle je checkbox: ", checkbox)
                # if checkbox is selected
                if checkbox.IsSelected:
                    print("Dokonce je zaskrtly :O ", checkbox)
                    # saves the index of selected checkbox in his default list
                    assigned_material = selected_materials[index]
            # goes through all selected_materials that are assigned to checkboxes
            print(" ")
            for index, matching_material in enumerate(selected_materials):
                # if the material number is same as the material of the selected checkbox then it also checks itself
                if matching_material == assigned_material:
                    assigned_file = tex_list[index]
                    assigned_file.Select()
                    self._treegui.Refresh()
                    assigned_file_map = selected_maps[index]
                    materials_upload.append(assigned_file_map)
                    print("Tohle je assigned file  ", assigned_file, " a tohle je jeho mapa", assigned_file_map)

            # print("Tohle je mapID pro vybrane materialy", mapID)
            folderToPath = self.GetString(ID.DIALOG_FOLDER_LIST)
            hasColor = False
            # if targetFolder is not None:
            loadAO = self.GetBool(ID.DIALOG_MAP_AO_CB)
            loadDispl = self.GetBool(ID.DIALOG_MAP_DISPL_CB)
            load16bdispl = self.GetBool(ID.DIALOG_MAP_16B_DISPL_CB)
            # loadIor = self.GetBool(ID.DIALOG_MAP_IOR_CB
            mat = c4d.BaseMaterial(ID.CORONA_STR_MATERIAL_PHYSICAL)
            mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_ROUGHNESS_MODE, ID.CORONA_PHYSICAL_MATERIAL_ROUGHNESS_MODE_GLOSSINESS, c4d.DESCFLAGS_SET_NONE)
            mat.SetParameter(ID.CORONA_MATERIAL_PREVIEWSIZE, ID.CORONA_MATERIAL_PREVIEWSIZE_1024, c4d.DESCFLAGS_SET_NONE)
            mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_IOR_VALUE, 1.56, c4d.DESCFLAGS_SET_NONE)
            fusionShader = None
            # dir = os.listdir(targetFolder)
            # for file in dir:
            for mapID in materials_upload:
                print(mapID)
                fullPath = os.path.join(folderToPath, mapID)
                # print("Type of fullpath: ", type(fullPath))
                if mapID == "COL" or mapID == "COLOR":
                    mat.SetName("Materialek")
                    if not loadAO:
                        bitmap = c4d.BaseShader(c4d.Xbitmap)
                        bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                        mat.InsertShader(bitmap)
                        mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_COLOR_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
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
                elif loadDispl and (load16bdispl and mapID == "DISP16") or (not load16bdispl and mapID == "DISP"):
                    bitmap = c4d.BaseShader(c4d.Xbitmap)
                    bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                    mat.InsertShader(bitmap)
                    mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_DISPLACEMENT, True, c4d.DESCFLAGS_SET_NONE)
                    mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                    mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_MIN_LEVEL, 0, c4d.DESCFLAGS_SET_NONE)
                    mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_MAX_LEVEL, 1, c4d.DESCFLAGS_SET_NONE)
                elif loadAO and mapID == "AO":
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
                    bitmap = c4d.BaseShader(c4d.Xbitmap)
                    bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                    mat.InsertShader(bitmap)
                    mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_ROUGHNESS_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                    mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_ROUGHNESS_VALUE, 100.0, c4d.DESCFLAGS_SET_NONE)
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
                doc = c4d.documents.GetActiveDocument()
                doc.StartUndo()
                # nevim proc to je bile, ale funguje to takze save
                doc.InsertMaterial(mat)
                # print("uz to proslo Insertem")
                doc.AddUndo(c4d.UNDOTYPE_NEW, mat)
                doc.EndUndo()
                material_to_add.append(mat)                                   
                self.SetString(ID.DIALOG_ERROR, "")
            c4d.EventAdd()



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
                    

        # if id == ID.FILTER_MATERIALS_BUTTON:
        #     path = self.GetString(ID.DIALOG_FOLDER_LIST)
        #     dir = os.listdir(path)
        #     targetFolder = None
        #     targetFolders = ["1K", "2K", "3K", "4K", "5K", "6K", "7K", "8K", "9K", "10K", "11K", "12K", "13K", "14K", "15K", "16K"]
        #     same_path_dirs = [d for d in dir if os.path.isdir(os.path.join(path, d)) and d.startswith(os.path.basename(path))]
        #     same_path_dirs = sorted(same_path_dirs)
        #     folder_dict = {}
        #     for index, folder in enumerate(same_path_dirs):
        #         folder_dict[folder] = True
        #     for index, checkbox in enumerate(checkbox_list):
        #         if checkbox.IsSelected:
        #             active_checkbox_list.append(index)
        #             # zde se ulozi slozka, ktera ma stejny index jako checkbox
        #             # musi se to vyresit takhle, protoze checkbox sam o sobe nema stejny nazev jako slozka, index ano
        #             folder_name = same_path_dirs[index]
        #             # ulozeni slozky, ktera ma stejny nazev jako text u daneho checkboxu
        #             folder_path = os.path.join(path, folder_name)
        #             print(folder_name)
        #             subdirs = [subdir for subdir in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, subdir))]
        #             # pro vsechny slozky, ktere obsahuji material (napr 4K, 5K, atd...)
        #             for targetFolderName in targetFolders:
        #                 # pokud je slozka 4K, 5K, atd... v te kterou prochazime
        #                 if targetFolderName in subdirs:
        #                     # cesta do slozky s 4K, 5K, atd...
        #                     targetFolder = os.path.join(folder_path, targetFolderName)
        #                     print("Slozka s materialem byla nalezena v ceste " + targetFolder)
        #                     # ulozeni vsech bitmapa ve slozce 4K, 5K, atd...
        #                     dirPath = os.listdir(targetFolder)
        #                     hasColor = False
        #                     if targetFolder is not None:
        #                         loadAO = self.GetBool(ID.DIALOG_MAP_AO_CB)
        #                         loadDispl = self.GetBool(ID.DIALOG_MAP_DISPL_CB)
        #                         load16bdispl = self.GetBool(ID.DIALOG_MAP_16B_DISPL_CB)
        #                         loadIor = self.GetBool(ID.DIALOG_MAP_IOR_CB)

        #                         mat = c4d.BaseMaterial(ID.CORONA_STR_MATERIAL_PHYSICAL)
        #                         mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_ROUGHNESS_MODE, ID.CORONA_PHYSICAL_MATERIAL_ROUGHNESS_MODE_GLOSSINESS, c4d.DESCFLAGS_SET_NONE)
        #                         mat.SetParameter(ID.CORONA_MATERIAL_PREVIEWSIZE, ID.CORONA_MATERIAL_PREVIEWSIZE_1024, c4d.DESCFLAGS_SET_NONE)
        #                         mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_IOR_VALUE, 1.56, c4d.DESCFLAGS_SET_NONE)

        #                         fusionShader = None

        #                         dir = os.listdir(targetFolder)
        #                         for file in dir:
        #                             fullPath = os.path.join(targetFolder, file)
        #                             # print("Type of fullpath: ", type(fullPath))
        #                             parts = file.split(".")[0].split("_")
        #                             mapID = parts[3]
        #                             if mapID == "COL" or mapID == "COLOR":
        #                                 mat.SetName("_".join(parts[0:3]))
        #                                 if not loadAO:
        #                                     bitmap = c4d.BaseShader(c4d.Xbitmap)
        #                                     bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
        #                                     mat.InsertShader(bitmap)
        #                                     mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_COLOR_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
        #                                 else:
        #                                     if not fusionShader:
        #                                         fusionShader = c4d.BaseShader(c4d.Xfusion)
        #                                         fusionShader.SetParameter(c4d.SLA_FUSION_MODE, c4d.SLA_FUSION_MODE_MULTIPLY, c4d.DESCFLAGS_SET_NONE)
        #                                         fusionShader.SetParameter(c4d.SLA_FUSION_BLEND, 1.0, c4d.DESCFLAGS_SET_NONE)
        #                                         mat.InsertShader(fusionShader)
        #                                         mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_COLOR_TEXTURE, fusionShader, c4d.DESCFLAGS_SET_NONE)
        #                                     bitmap = c4d.BaseShader(c4d.Xbitmap)
        #                                     bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
        #                                     fusionShader.InsertShader(bitmap)
        #                                     fusionShader.SetParameter(c4d.SLA_FUSION_BASE_CHANNEL, bitmap, c4d.DESCFLAGS_SET_NONE)
        #                             elif mapID == "NRM":
        #                                 bitmap = c4d.BaseShader(c4d.Xbitmap)
        #                                 bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
        #                                 texture = c4d.BaseShader(ID.PLUGINID_CORONA4D_NORMALSHADER)
        #                                 texture.SetParameter(ID.CORONA_NORMALMAP_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
        #                                 texture.SetParameter(ID.CORONA_NORMALMAP_FLIP_G, True, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.InsertShader(bitmap)
        #                                 mat.InsertShader(texture)
        #                                 mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_BUMPMAPPING_ENABLE, True, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_BUMPMAPPING_VALUE, 1.0, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_BUMPMAPPING_TEXTURE, texture, c4d.DESCFLAGS_SET_NONE)
        #                             elif loadDispl and (load16bdispl and mapID == "DISP16") or (not load16bdispl and mapID == "DISP"):
        #                                 bitmap = c4d.BaseShader(c4d.Xbitmap)
        #                                 bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.InsertShader(bitmap)
        #                                 mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_DISPLACEMENT, True, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_MIN_LEVEL, 0, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_MAX_LEVEL, 1, c4d.DESCFLAGS_SET_NONE)
        #                             elif loadAO and mapID == "AO":
        #                                 if not fusionShader:
        #                                     fusionShader = c4d.BaseShader(c4d.Xfusion)
        #                                     fusionShader.SetParameter(c4d.SLA_FUSION_MODE, c4d.SLA_FUSION_MODE_MULTIPLY, c4d.DESCFLAGS_SET_NONE)
        #                                     fusionShader.SetParameter(c4d.SLA_FUSION_BLEND, 1.0, c4d.DESCFLAGS_SET_NONE)
        #                                     mat.InsertShader(fusionShader)
        #                                     mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_COLOR_TEXTURE, fusionShader, c4d.DESCFLAGS_SET_NONE)
        #                                 bitmap = c4d.BaseShader(c4d.Xbitmap)
        #                                 bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
        #                                 fusionShader.InsertShader(bitmap)
        #                                 fusionShader.SetParameter(c4d.SLA_FUSION_BLEND_CHANNEL, bitmap, c4d.DESCFLAGS_SET_NONE)
        #                             elif mapID == "OPAC":
        #                                 bitmap = c4d.BaseShader(c4d.Xbitmap)
        #                                 bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.InsertShader(bitmap)
        #                                 mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_ALPHA, True, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_ALPHA_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
        #                             elif mapID == "GLOSS":
        #                                 bitmap = c4d.BaseShader(c4d.Xbitmap)
        #                                 bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.InsertShader(bitmap)
        #                                 mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_ROUGHNESS_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_ROUGHNESS_VALUE, 100.0, c4d.DESCFLAGS_SET_NONE)
        #                             elif mapID == "REFL":
        #                                 bitmap = c4d.BaseShader(c4d.Xbitmap)
        #                                 bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.InsertShader(bitmap)
        #                                 mat.SetParameter(ID.CORONA_MATERIAL_REFLECT, True, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.SetParameter(ID.CORONA_REFLECT_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
        #                             elif mapID == "SSS":
        #                                 bitmap = c4d.BaseShader(c4d.Xbitmap)
        #                                 bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.InsertShader(bitmap)
        #                                 mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_SSS, True, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_VOLUME_SSS_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
        #                             elif mapID == "SSSABSORB":
        #                                 bitmap = c4d.BaseShader(c4d.Xbitmap)
        #                                 bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.InsertShader(bitmap)
        #                                 mat.SetParameter(ID.CORONA_MATERIAL_VOLUME, True, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.SetParameter(ID.CORONA_VOLUME_ABSORPTION_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
        #                             elif loadIor and mapID == "IOR":
        #                                 bitmap = c4d.BaseShader(c4d.Xbitmap)
        #                                 bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.InsertShader(bitmap)
        #                                 mat.SetParameter(ID.CORONA_REFLECT_FRESNELLOR_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
        #                             elif mapID == "METAL":
        #                                 bitmap = c4d.BaseShader(c4d.Xbitmap)
        #                                 bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
        #                                 mat.InsertShader(bitmap)
        #                                 mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_METALLIC_MODE_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)

        #                             doc = c4d.documents.GetActiveDocument()
        #                             doc.StartUndo()
        #                             # nevim proc to je bile, ale funguje to takze save
        #                             doc.InsertMaterial(mat)
        #                             # print("uz to proslo Insertem")
        #                             doc.AddUndo(c4d.UNDOTYPE_NEW, mat)
        #                             doc.EndUndo()
        #                             material_to_add.append(mat)                                   
        #                             self.SetString(ID.DIALOG_ERROR, "")

        #     c4d.EventAdd()

        #     return True
        
    def SetError(self, message):
        if not message:
            message = ""
        self.SetString(ID.DIALOG_ERROR, message)

    def SetListItems(self, message):
        if not message:
            message= ""
            self.SetString(ID.DIALOG_FOLDER_LIST, message)

    def LoadMaterial(self):
        if not self.materialFolder:
            self.SetError("Material folder was not selected")
            return False

        loadAO = self.GetBool(ID.DIALOG_MAP_AO_CB)
        loadDispl = self.GetBool(ID.DIALOG_MAP_DISPL_CB)
        load16bdispl = self.GetBool(ID.DIALOG_MAP_16B_DISPL_CB)
        loadIor = self.GetBool(ID.DIALOG_MAP_IOR_CB)

        mat = c4d.BaseMaterial(ID.CORONA_STR_MATERIAL_PHYSICAL)
        mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_ROUGHNESS_MODE, ID.CORONA_PHYSICAL_MATERIAL_ROUGHNESS_MODE_GLOSSINESS, c4d.DESCFLAGS_SET_NONE)
        mat.SetParameter(ID.CORONA_MATERIAL_PREVIEWSIZE, ID.CORONA_MATERIAL_PREVIEWSIZE_1024, c4d.DESCFLAGS_SET_NONE)
        mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_IOR_VALUE, 1.56, c4d.DESCFLAGS_SET_NONE)

        fusionShader = None

        # 4K 8K etc.
        dir = os.listdir(self.materialFolder)
        for file in dir:
            fullPath = os.path.join(self.materialFolder, file)
            try:
                # python2 unicode string handling
                if sys.version_info < (3, 0):
                    fullPath = fullPath.encode("utf-8")
            except:
                pass
            print("Type of fullpath: ", type(fullPath))
            parts = file.split(".")[0].split("_")
            mapID = parts[3]

            if mapID == "COL" or mapID == "COLOR":
                mat.SetName("_".join(parts[0:3]))
                if not loadAO:
                    bitmap = c4d.BaseShader(c4d.Xbitmap)
                    bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                    mat.InsertShader(bitmap)
                    mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_COLOR_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
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
            elif loadDispl and (load16bdispl and mapID == "DISP16") or (not load16bdispl and mapID == "DISP"):
                bitmap = c4d.BaseShader(c4d.Xbitmap)
                bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                mat.InsertShader(bitmap)
                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_DISPLACEMENT, True, c4d.DESCFLAGS_SET_NONE)
                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_MIN_LEVEL, 0, c4d.DESCFLAGS_SET_NONE)
                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_DISPLACEMENT_MAX_LEVEL, 1, c4d.DESCFLAGS_SET_NONE)
            elif loadAO and mapID == "AO":
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
                bitmap = c4d.BaseShader(c4d.Xbitmap)
                bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                mat.InsertShader(bitmap)
                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_ROUGHNESS_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_BASE_ROUGHNESS_VALUE, 100.0, c4d.DESCFLAGS_SET_NONE)
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
            elif loadIor and mapID == "IOR":
                bitmap = c4d.BaseShader(c4d.Xbitmap)
                bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                mat.InsertShader(bitmap)
                mat.SetParameter(ID.CORONA_REFLECT_FRESNELLOR_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)
            elif mapID == "METAL":
                bitmap = c4d.BaseShader(c4d.Xbitmap)
                bitmap.SetParameter(c4d.BITMAPSHADER_FILENAME, fullPath, c4d.DESCFLAGS_SET_NONE)
                mat.InsertShader(bitmap)
                mat.SetParameter(ID.CORONA_PHYSICAL_MATERIAL_METALLIC_MODE_TEXTURE, bitmap, c4d.DESCFLAGS_SET_NONE)

        doc = c4d.documents.GetActiveDocument()
        doc.StartUndo()
        doc.InsertMaterial(mat)
        doc.AddUndo(c4d.UNDOTYPE_NEW, mat)
        doc.EndUndo()
        
        self.SetString(ID.DIALOG_ERROR, "")

        return True

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
        dialog.Open(c4d.DLG_TYPE_ASYNC, REAWOTE_SORTER_ID, -3, -3, 487, 750)
        return True
        
    def CoreMessage(self, id, msg):
        # Checks if texture baking has finished
        if id==REAWOTE_SORTER_ID:
            print("Command received!")
            print("Path is: " + self.thread.path)
            return True

        return gui.GeDialog.CoreMessage(self, id, msg)