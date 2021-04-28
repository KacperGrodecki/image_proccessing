#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 07:52:56 2021

@author: kacper
"""
import os
from os import listdir
from os.path import isfile, join
mypath = '/home/kacper/Dokumenty/GitHub/image_proccessing/tmp/'  
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
[os.remove(mypath+f) for f in listdir(mypath) if isfile(join(mypath, f))]
