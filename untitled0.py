#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 14:36:22 2018

@author: raja
"""


import os 
import ascat.h_saf as h_saf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date
import csv
import numpy as np
fig, ax = plt.subplots(1, 1, figsize=(15, 5))

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
gpi = 412726
h111_ts = h111_reader.read(gpi, absolute_sm=True)
conf_flag_ok = h111_ts.data['conf_flag'] == 0
df = h111_ts.data[conf_flag_ok]['abs_sm_hwsd']
df.to_csv('/home/raja/Desktop/test_grid.csv')
fig, ax = plt.subplots(1, 1, figsize=(15, 5))
h111_ts.data[conf_flag_ok]['abs_sm_gldas'].plot(ax=ax, label='Absolute SSM using porosity from NOAH GLDAS')
h111_ts.data[conf_flag_ok]['abs_sm_hwsd'].plot(ax=ax, label='Absolute SSM using porosity from HWSD')
ax.set_ylabel('Vol. soil moisture ($m^3 m^{-3}$)')
ax.legend()
plt.show()
