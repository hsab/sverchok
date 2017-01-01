# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import colorsys
import bpy
from bpy.props import FloatProperty, BoolProperty

from sverchok.node_tree import SverchCustomTreeNode, StringsSocket
from sverchok.data_structure import updateNode, fullList, SvGetSocketAnyType, SvSetSocketAnyType
from sverchok.utils.sv_itertools import sv_zip_longest

nodule_color = (0.899, 0.8052, 0.0, 1.0)


def fprop_generator(**altprops):
    # min can be overwritten by passing in min=some_value into the altprops dict
    default_dict_vals = dict(update=updateNode, precision=3, min=0.0, max=1.0)
    default_dict_vals.update(**altprops)
    return FloatProperty(**default_dict_vals)


class SvColorsOutNode(bpy.types.Node, SverchCustomTreeNode):
    ''' Generator for Color data , color separate'''
    bl_idname = 'SvColorsOutNode'
    bl_label = 'Color Out'
    bl_icon = 'OUTLINER_OB_EMPTY'

    def psuedo_update(self, context):
        for idx, socket in enumerate(self.selected_mode):
            self.outputs[idx].name = socket
            # self.outputs[idx].prop_name = socket.lower() + '_'
        updateNode(self, context)

    # r_ = fprop_generator(name='R', description='Red (0..1)')
    # g_ = fprop_generator(name='G', description='Green (0..1)')
    # b_ = fprop_generator(name='B', description='Blue (0..1)')
    # a_ = fprop_generator(name='A', description='Alpha (0..1) - opacity')

    # y_ = fprop_generator(name='Y', description='Luma (0..1)')
    # i_ = fprop_generator(name='I', min=-1.0, description='orange-blue range (-1..1) - chrominance')
    # q_ = fprop_generator(name='Q', min=-1.0, description='purple-green (-1..1) - chrominance')

    # h_ = fprop_generator(name='H', description='Hue (0..1)')
    # s_ = fprop_generator(name='S', description='Saturation (0..1) - different for hsv and hsl')
    # l_ = fprop_generator(name='L', description='Lightness / Brightness (0..1)')
    # v_ = fprop_generator(name='V', description='Value / Brightness (0..1)')

    mode_options = [
        # having element 0 and 1 helps reduce code.
        ("RGB", "RGB", "", 0),
        ("HSV", "HSV", "", 1),
        ("HSL", "HSL", "", 2),
        ("YIQ", "YIQ", "", 3)
    ]
    
    selected_mode = bpy.props.EnumProperty(
        default="RGB", description="offers color spaces",
        items=mode_options, update=psuedo_update
    )

    def draw_buttons(self, context, layout):
        layout.prop(self, 'selected_mode', expand=True)

    def sv_init(self, context):
        self.width = 100
        inew = self.inputs.new
        inew('StringsSocket', "Colors").nodule_color = nodule_color
        onew = self.outputs.new
        onew('StringsSocket', "R")
        onew('StringsSocket', "G")
        onew('StringsSocket', "B")
        onew('StringsSocket', "A")
        
    
    def process(self):
        """
        colorsys.rgb_to_yiq(r, g, b)
        colorsys.yiq_to_rgb(y, i, q)
        colorsys.rgb_to_hls(r, g, b)
        colorsys.hls_to_rgb(h, l, s)
        colorsys.rgb_to_hsv(r, g, b)
        colorsys.hsv_to_rgb(h, s, v)
        """        
        # if not self.outputs['Colors'].is_linked:
        #     return
        # inputs = self.inputs
        
        # i0 = inputs[0].sv_get()
        # i1 = inputs[1].sv_get()
        # i2 = inputs[2].sv_get()
        # i3 = inputs[3].sv_get()

        # series_vec = []
        # max_obj = max(map(len, (i0, i1, i2, i3)))
        # fullList(i0, max_obj)
        # fullList(i1, max_obj)
        # fullList(i2, max_obj)
        # fullList(i3, max_obj)
        # for i in range(max_obj):
                
        #     max_v = max(map(len, (i0[i], i1[i], i2[i], i3[i])))
        #     fullList(i0[i], max_v)
        #     fullList(i1[i], max_v)
        #     fullList(i2[i], max_v)
        #     fullList(i3[i], max_v)
        #     series_vec.append(list(zip(i0[i], i1[i], i2[i], i3[i])))
        
        # self.outputs['Colors'].sv_set(series_vec)
        pass
    
    
def register():
    bpy.utils.register_class(SvColorsOutNode)


def unregister():
    bpy.utils.unregister_class(SvColorsOutNode)