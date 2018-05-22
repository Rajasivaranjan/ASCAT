#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 17:38:59 2017

@author: Rajasivaranjan
"""

import os 
import ascat.h_saf as h_saf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date
import csv
import numpy as np
#fig, ax = plt.subplots(1, 1, figsize=(15, 5))
#from osgeo import ogr
#
#def get_pt(pt,poly):
#    polyshp = ogr.Open(poly)
#    polylyr = polyshp.GetLayer(0)
#    polygon = polylyr.GetNextFeature()
#    polygon_geom = polygon.GetGeometryRef()
#    ptshp = ogr.Open(pt)
#    ptlyr = ptshp.GetLayer(0)
#    li = []
#    for i in ptlyr:
#        point_geom = i.GetGeometryRef()
#        if point_geom.Within(polygon_geom):
#            li.append(i.GetField('gpi'))
#    return li

h108_path = '/home/raja/Desktop/ASCAT/ASCAT_New/h108'
h109_path = '/home/raja/Desktop/ASCAT/ASCAT_New/h109'
h110_path = '/home/raja/Desktop/ASCAT/ASCAT_New/h110'
h111_path = '/home/raja/Desktop/ASCAT/ASCAT_New/h111'
grid_path = '/home/raja/Desktop/ASCAT/grid'
static_layer_path = '/home/raja/Desktop/ASCAT/static_layer'
h108_reader = h_saf.H108Ts(h108_path, grid_path, static_layer_path=static_layer_path)
h109_reader = h_saf.H109Ts(h109_path, grid_path, static_layer_path=static_layer_path)
h110_reader = h_saf.H110Ts(h110_path, grid_path, static_layer_path=static_layer_path)
h111_reader = h_saf.H111Ts(h111_path, grid_path, static_layer_path=static_layer_path)
#gpi_li = [648666,648670,654948,654952,661226,661230,661234,661238,661242,667512,667516]
#gpi_lis = [661238, 17253, 412726, 1128594, 1080298, 1074244]
#gpi = 412726

gpi_li =np.load('/home/raja/Desktop/Sholapur_arr.npy')
for gpi in gpi_li:
    h111_ts = h111_reader.read(gpi_li[0], absolute_sm=True)
    conf_flag_ok = h111_ts.data['conf_flag'] == 0
    df = h111_ts.data[conf_flag_ok]['abs_sm_hwsd']
#print df.shape
#df.to_csv('sm_ES2_top.csv')
#fig, ax = plt.subplots(1, 1, figsize=(15, 5))
#h111_ts.data[conf_flag_ok]['abs_sm_gldas'].plot(ax=ax, label='Absolute SSM using porosity from NOAH GLDAS')
#h111_ts.data[conf_flag_ok]['abs_sm_hwsd'].plot(ax=ax, label='Absolute SSM using porosity from HWSD')
#ax.set_ylabel('Vol. soil moisture ($m^3 m^{-3}$)')
#ax.legend()
#plt.show()
    df1 = pd.DataFrame({'SM':df})
    df_avg = df1.resample('D', how = 'mean')
    ix = pd.DatetimeIndex(start = date(2007,1,1), end = date(2016, 12, 31), freq='D')
    df2 = df_avg.reindex(ix)
    li = []
    for j in range(2007,2017,1):
        yr = (df2.index.year == j)
        li.append(df2['SM'][yr])
        
    with open('gpi_'+str(gpi)+'.csv', 'wb') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(li)
    
#df2['MA'] = df2.rolling(window=10, min_periods=1).mean()
#li = []
#for j in range(2007,2017,1):
#    yr = (df2.index.year == j)
#    li.append(df2['MA'][yr])
#    
#with open('test.csv', 'wb') as f:
#    writer = csv.writer(f, lineterminator='\n')
#    writer.writerows(li)
    
     
#h110_ts = h111_reader.read(gpi)
#conf_flag_ok = h110_ts.data['conf_flag'] == 0
#
#
#
#
#
#ax.plot(h110_ts.data.index, h110_ts.data['sm'], label='H110 SSM')
#ax.set_ylabel('Degree of Saturation (%)')
#ax.legend()
#plt.show()