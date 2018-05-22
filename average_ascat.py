#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 17:03:49 2017

@author: raja
"""

import os
import pandas as pd
import csv
import numpy as np
from datetime import date

source = '/home/raja/jalna'
store_fname = [] 

for fname in os.listdir(source):
    store_fname.append(fname)
os.chdir(source)
lis =[] 
for yr in range(0,10,1):
    li = [] 
    for i in store_fname:
        with open(i, 'rb') as lt:
            reader = csv.reader(lt)
            rows = [r for r in reader]
        li.append(rows[yr])
    sm = np.array(li, float)
    ssm = np.nanmean(sm, axis=0)            
    lis.append(ssm)
x = np.concatenate(lis)
ix = pd.DatetimeIndex(start = date(2007,1,1), end = date(2016, 12, 31), freq='D')
df = pd.DataFrame({'SM':x}, index = ix)
df.to_csv('/home/raja/jalna_ts.csv')
df['MA'] = df.rolling(window=10, min_periods=1).mean()
ls = []
for j in range(2007,2017,1):
    yr = (df.index.year == j)
    ls.append(df['MA'][yr])
    
with open('/home/raja/jalna_MA.csv', 'wb') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerows(ls)