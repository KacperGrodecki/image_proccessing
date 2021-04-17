# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 22:26:13 2021

@author: Lenovo
"""
from PIL import Image 
#import pytesseract 
import sys 
from pdf2image import convert_from_path 
import os
#import pandas as pd
#import cv2 

pdf_file=r'C:\Users\Lenovo\git\image_proccessing\BU_0_639_223.pdf'

from pdf2image import pdfinfo_from_path,convert_from_path
info = pdfinfo_from_path(pdf_file, userpw=None, poppler_path=None)

maxPages = info["Pages"]
i=0
#for page in range(1, maxPages+1, 10) : 
for page in range(10, 12, 1) : 
   #pages=convert_from_path(pdf_file, dpi=100, first_page=page, last_page = min(page+10-1,maxPages))
   pages=convert_from_path(pdf_file, dpi=500, first_page=page, last_page = 20)
   for page in pages:
     i=i+1
     #save file
     page.save(r'C:\Users\Lenovo\git\image_proccessing\res500\figa'+str(i)+'.jpg')