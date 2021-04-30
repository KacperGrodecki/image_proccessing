#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 10:50:27 2021

@author: kacper
"""

ywh=pd.read_csv('/home/kacper/Dokumenty/GitHub/image_proccessing/tmp/xywh.csv',sep='\t',index_col=0 )

res_xywh=pd.concat([res, xywh], axis=1,join="inner")
res_xywh['y']=res_xywh['1'].diff()

res_xywh['y']=res_xywh['y']/60
res_xywh.iloc[0,5]=0
res_xywh['x']=40*(res_xywh['0']-np.min(res_xywh['0']))/(np.max(res_xywh['0'])-np.min(res_xywh['0']))
output=''
for index, row in res_xywh.iterrows():
    output+='\n'*int(row['y'])+' '*int(row['x'])+row['final']
    
text_file = open("Output.txt", "w")
text_file.write(output)
text_file.close()
