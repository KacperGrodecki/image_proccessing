#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 08:32:01 2021

@author: kacper
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
#%matplotlib inline  # if you are running this code in Jupyter notebook

# reads image 'opencv-logo.png' as grayscale
path='/home/kacper/Dokumenty/GitHub/data_image_processing/res500_1/'
file='fig108.jpg'
img = cv2.imread(path+file,0)

lower_blue = np.array([0])
upper_blue = np.array([130])
mask = cv2.inRange(img, lower_blue, upper_blue)
res = cv2.bitwise_and(img,img, mask=mask)
res[mask == 0] = [255]

path='/home/kacper/Dokumenty/GitHub/data_image_processing/image_processing/'
#cv2.imwrite(path+file, mask)
cv2.imwrite(path+file, res)

plt.figure(figsize=(25,25))      
plt.imshow(res)
res_board = res.copy()
board=int(res_board.shape[1]*0.01)
res_board[:,:board]=255
res_board[:,-board:]=255

plt.figure(figsize=(25,25))      
plt.imshow(res_board)

result = res_board.copy()
ythresh=1000
cntrs,topbox=countrurs(res_board,ythresh)
images=[]
xywh=[]
for c in cntrs:
                  box = cv2.boundingRect(c)
                  if box != topbox:
                      x,y,w,h = box
                      xywh.append([x,y,w,h])
                      
                      cv2.rectangle(result, (x, y), (x+w, y+h), (0,0,255), 2)
                      cropped = img[y:y + h, x:x + w]  
                      
def countrurs(gray,ythresh): 
          thresh=255-gray
          # use morphology erode to blur horizontally
          kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (151, 3))
          morph = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel)
        
          # use morphology open to remove thin lines from dotted lines
          kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 17))
          morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)
        
        
          # find contours
          #tzreba wywietlić kontury z obrazkiem
          cntrs = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
          cntrs = cntrs[0] if len(cntrs) == 2 else cntrs[1]
        
          # find the topmost box
          plt.figure(figsize=(25,25))      
          plt.imshow(morph)
        
          for c in cntrs:
                box = cv2.boundingRect(c)
                x,y,w,h = box
                if y < ythresh:
                    topbox = box
                    ythresh = y
          return cntrs[::-1],topbox
plt.figure(figsize=(25,25))      
plt.imshow(result)

      
plt.imshow(res)
plt.show()

