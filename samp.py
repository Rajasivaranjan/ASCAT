#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 11:17:26 2018

@author: raja
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 14:00:41 2018

@author: raja
"""

import os
from datetime import datetime
import pytesmo.colormaps.load_cmap as smcolormaps
import ascat.h_saf as h_saf
import numpy as np
import cartopy
import matplotlib.pyplot as plt



h14_path = "/home/raja/Desktop/ASCAT/ASCAT_New/h14"
h14_reader = h_saf.H14img(h14_path,month_path_str='')

lats_li = []
lons_li = []
ssm_li = []
tst = 0

h14_data, metadata, timestamp, lons, lats, time_var = h14_reader.read(datetime(2014,5, 15))
print(type(h14_data))

# the data is a dictionary, each dictionary key contains the array of one variable
print("The following variables are in this image", h14_data.keys())
print(h14_data['SM_layer1_0-7cm'].shape)
print(lons.shape)
print(lats.shape)
('The following variables are in this image', ['SM_layer1_0-7cm', 'SM_layer2_7-28cm','SM_layer3_28-100cm', 'SM_layer4_100-289cm'])
(800, 1600)
(800, 1600)
(800, 1600)

plot_crs = cartopy.crs.Robinson()
data_crs = cartopy.crs.PlateCarree()

for layer in h14_data:
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], projection=plot_crs)
    ax.set_title('H14 {:}'.format(layer))
    
ax.add_feature(cartopy.feature.LAND)
ax.add_feature(cartopy.feature.OCEAN)
ax.add_feature(cartopy.feature.COASTLINE)
ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
ax.add_feature(cartopy.feature.LAKES, alpha=0.5)
ax.add_feature(cartopy.feature.RIVERS)
sc = ax.pcolormesh(lons, lats, h14_data[layer], zorder=3,
transform=data_crs, cmap=smcolormaps.load('SWI_ASCAT'))
cax = fig.add_axes([0.92, 0.1, 0.025, 0.8])
cbar = fig.colorbar(sc, cax=cax)
cbar.set_label('Liquid Root Zone Soil Moister')
plt.show()