#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 12:39:31 2017

@author: raja
"""

import os
from datetime import datetime
import pytesmo.colormaps.load_cmap as smcolormaps
import ascat.h_saf as h_saf
from datetime import datetime
import numpy as np
import cartopy
import matplotlib.pyplot as plt
from cartopy.io.shapereader import Reader


h16_path = "/home/raja/Desktop/h16_cur_mon_data"
h16_reader = h_saf.H16img(h16_path, month_path_str='')
lats_li = []
lons_li = []
ssm_li = []
tst = 0
for h16_data, metadata, timestamp, lons, lats, time_var in h16_reader.daily_images(datetime(2017, 9, 20)):
# this tells you the exact timestamp of the read image
#    print(timestamp.isoformat())
    tst = tst+ lons.size
    ssm = h16_data['Surface Soil Moisture (Ms)']
    for i in range (0,ssm.size,1):
        ssm_li.append(ssm[i])
        lats_li.append(lats[i])
        lons_li.append(lons[i])

print tst
print len(ssm_li)
lats = np.array(lats_li)
lons = np.array(lons_li)
data = np.array(ssm_li)
plot_crs = cartopy.crs.Mercator()
data_crs = cartopy.crs.PlateCarree()

fig = plt.figure(figsize=(7, 6), dpi=500)
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], projection=plot_crs)

blue = '#4b92db'
ax.background_patch.set_facecolor(blue)
#
ax.add_feature(cartopy.feature.LAND)
#ax.add_feature(cartopy.feature.OCEAN)
##ax.add_feature(cartopy.feature.COASTLINE)
#ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
#ax.add_feature(cartopy.feature.LAKES, alpha=0.5)
#ax.add_feature(cartopy.feature.RIVERS)
ax.set_extent([-82,-32, -45, 10])
ax.set_title('H16 SSM '+str(timestamp.isoformat()))


sc = ax.scatter(lons, lats, c=data, zorder=2, marker='s', s=2,
transform=data_crs, cmap=smcolormaps.load('SWI_ASCAT'),
vmin=0, vmax=100)
cax = fig.add_axes([0.92, 0.1, 0.025, 0.8])
cbar = fig.colorbar(sc, cax=cax)
cbar.set_label('Degree of Saturation (%)')
ax.coastlines()
fname = '/home/raja/Downloads/BRA_adm_shp/BRA_adm1'
ax.add_geometries(Reader(fname).geometries(), data_crs, 
                  facecolor='none', edgecolor='black', zorder=3)

fig.savefig("/home/raja/h16_ssm.jpg", bbox_inches = 'tight')
