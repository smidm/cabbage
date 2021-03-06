import sys
sys.path.append('../')
from os.path import join

from cabbage.features.deepmatching import DeepMatching
import cabbage.features.spatio as st
from cabbage.features.ReId import StackNet64x64, get_element

import json


class pairwise_features:
    """ generate pairwise features 
    """
    def __init__(self,delta_max):
        """ ctor
        """
        self.Settings = json.load(open('settings.txt'))
        self.root = self.Settings['data_root']
        self.dm = DeepMatching(self.Settings['deepmatch'], join(self.root, 'deep_matching'),delta_max=delta_max)
        self.stacknet = StackNet64x64(self.root)

        
    def get_pairwise_vector(self,video_name,I1, I2, frame1,frame2,bb1,bb2,conf1,conf2):
        i1 = get_element(I1, bb1, (64,64), force_uint=True)
        i2 = get_element(I2, bb2, (64,64), force_uint=True)        
        
        st_cost = st.calculate(bb1, bb2)
        dm_cost = self.dm.calculate_cost(video_name, frame1, bb1, frame2, bb2)
        reid_cost = self.stacknet.predict(i1, i2)[0][0]
        min_conf = min(conf1,conf2)
        
        return (st_cost , dm_cost , reid_cost , min_conf , \
                st_cost**2,st_cost * dm_cost,st_cost * reid_cost, st_cost * min_conf, \
                dm_cost**2,dm_cost * reid_cost ,dm_cost * min_conf , \
                reid_cost**2,reid_cost * min_conf , \
                min_conf**2)
                