# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 17:46:40 2017

@author: Rajasivaranjan
Email: rajasivaranjan92@gmail.com

"""

import gdalnumeric, os
import csv
store_fname = []
for fname in os.listdir("C:/Users/thamir/Downloads/Kolapur"):
    if fname.endswith('.tif'):
        store_fname.append(fname)  
os.chdir("C:/Users/thamir/Downloads/Kolapur")
li = []
for i in store_fname:
    raster_file = gdalnumeric.LoadFile(i)
    pixel_count = (raster_file == 1).sum()  # for pixel value = 1print pixel_count
    li.append(pixel_count)
with open('MH_final.csv', 'w') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerows(zip(store_fname,li))