# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""
import pytesseract
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
import pandas as pd
import cv2
from PIL import Image,ImageTk
from pytesseract import image_to_string
import numpy as np
import re
import matplotlib.pyplot as plt
path = '/home/kacper/Dokumenty/GitHub/image_proccessing/'        
#from tkinter.filedialog import askopenfilename
#from skimage import io, color, morphology
#import pickle
import functions
import words_reading
from os import listdir
from os.path import isfile, join
import gc
import sys
#import os,psutil
def make_dict(loc_File):
    with open(loc_File, encoding='UTF8') as f:
        lines = f.readlines()
    dict_pl = []
    for line in lines:
        word=line.split()
        dict_pl.append(word)
 
    return [item.replace(',','') for sublist in dict_pl for item in sublist]


def check_pl(a):
    return a in dict_pl 


def dicts_pl(dict_pl,String_pl):
    loc_dicts=[None]*len(String_pl)
    loc_key=[None]*len(String_pl)
    i=0
    for ch in String_pl:
        loc_dicts[i]=[x for x in dict_pl if x[0]==ch ]
        loc_key[i]=ch
        i+=1
    return loc_dicts,loc_key

# String_pl='aąbcćdeęfghijklłmnoópqrsśtuvwxyzż AĄBCĆDEEFGHIJKLŁMNOÓPQQRSŚTUVWXYZŻ'
# File='/home/kacper/Dokumenty/GitHub/image_proccessing/odm.txt'

# dict_pl=make_dict(File)
# global dicts
# global key
# dicts, key=dicts_pl(dict_pl,String_pl)

for i in range(0,400):
    print('-------------------------',i,'--------------------------')
        
    class ImageProcessing:
        def __init__(self):
            print('Constructor called Image Processing')
            pass
        
        def __del__(self):
            print('Destructor called Image Processing')
            pass
        
        def fig_prepare(self,image):
            
          kernel_3x3 = np.ones((3, 3), np.float32) / 9
          kernel_sharpening = np.array([[-1,-1,-1], 
                                        [-1, 9,-1],
                                        [-1,-1,-1]])
          blurred=cv2.filter2D(image, -1, kernel_3x3)
          sharpened=cv2.filter2D(blurred, -1, kernel_sharpening)
          blurred=cv2.filter2D(sharpened, -1, kernel_3x3)
          sharpened=cv2.filter2D(blurred, -1, kernel_sharpening)
        
          lower=np.array([0,0,0])
          upper=np.array([100,100,100])
        
          mask = cv2.inRange(sharpened, lower, upper)
          
          return 255-mask
        
        def mask_from_cropped(self,cropped):
                  # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
                  # dilated = cv2.dilate(cropped, kernel)
                  # eroded=cv2.erode(dilated,kernel)
                  # kernel_3x3 = np.ones((5, 5), np.float32) / 25
                  # kernel_sharpening = np.array([[-1,-1,-1], 
                  #                       [-1, 9,-1],
                  #                      [-1,-1,-1]])
                    
                  # blurred = cv2.filter2D(eroded, -1, kernel_3x3)
                  # sharpened = cv2.filter2D(blurred, -1, kernel_sharpening)
                  # blurred = cv2.filter2D(sharpened, -1, kernel_3x3)
                  # sharpened1 = cv2.filter2D(blurred, -1, kernel_sharpening)
                  lower=np.array([0,0,0])
                  upper=np.array([170,170,170])
                  
                  
                  
        
                  return 255- cv2.inRange(cropped, lower, upper),255 - cv2.inRange(cropped, lower, upper)
    
        def countrurs(self,gray,ythresh): 
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
          
          for c in cntrs:
                box = cv2.boundingRect(c)
                x,y,w,h = box
                if y < ythresh:
                    topbox = box
                    ythresh = y
          return cntrs[::-1],topbox\
        
       
        
        
                
        #loading contours        
        def find_contours(self,file):
            print('file ',file)
            #file=path+file+'.jpg'
            image = cv2.imread(file)
            gray=self.fig_prepare(image)
            
            image = cv2.imread(file)
            result = gray.copy()
            ythresh=1000
            cntrs,topbox=self.countrurs(gray,ythresh)
            i=0
            images=[]
            xywh=[]
            for c in cntrs:
                  box = cv2.boundingRect(c)
                  if box != topbox:
                      i=i+1
                      x,y,w,h = box
                
                      xywh.append([x,y,w,h])
                      
                      cv2.rectangle(result, (x, y), (x+w, y+h), (0, 0, 255), 2)
                      cropped = image[y:y + h, x:x + w]  
                
                      mask,mask1 = self.mask_from_cropped(cropped)
                      board=50
                      cropped_board = cv2.copyMakeBorder( cropped, board,board, board, board,cv2.BORDER_CONSTANT, value=[210, 210, 210])
                      mask = cv2.copyMakeBorder( mask, board, board, board, board, cv2.BORDER_CONSTANT,value=[255, 255, 255])
                      mask1 = cv2.copyMakeBorder( mask1, board, board, board, board, cv2.BORDER_CONSTANT,value=[255, 255, 255])
                      im=[cropped_board,mask,mask1]
                      images.append(im)  
            return images,xywh
     
    class run(ImageProcessing):
    
        def __init__(self,number):     
            print('start')            
            ImageProcessing.__init__(self)
            self.countter=0
            self.countter1=0
            self.labels=[]
            self.xywh=[]
            self.xywh1=[]
            self.path='/home/kacper/Dokumenty/GitHub/data_image_processing/res500_1/'  
            self.files=[f for f in listdir(self.path) if isfile(join(self.path, f))]
            self.files.sort()
            self.file_nr=number
            self.contours=0
            
            self.open_file()
            
        def open_file(self):
            if 'fig46' in self.files[self.file_nr]:
                self.file=self.path+self.files[self.file_nr]
                print(self.file)
            
            #file=self.file
            
                self.find_contour()
            else:
                self.file_nr+=1
                self.open_file()
                
        def find_contour(self):
            print('find_contour',ImageProcessing)
            self.contours,self.xywh=ImageProcessing.find_contours(self,self.file)
            print('liczba konturów ',len(self.contours))
            
            self.read_text()
            
        def read_text(self):
            print('read text')
            try:
                cropped_board,mask,mask1=self.contours[self.countter]
                self.analyze_figures(self.xywh,cropped_board,mask,mask1)
            
                self.next_contour()
            except:
                e=sys.exc_info()[0]
                print(e)
        def next_contour(self):
            print('next contour')
            print(self.countter)
            print(len(self.labels))
            if self.countter>len(self.contours)-2:
                print('finish')
            
                print('labels ',np.array(self.labels).shape)
                self.labels.append([self.file,self.file_nr,'',''])
                
                print('numer pliku ',str(self.file))
                print('df construction ',pd.DataFrame(np.array(self.labels)).shape)
                df_labels=pd.DataFrame(np.array(self.labels))
                print('zapis','/home/kacper/Dokumenty/GitHub/data_image_processing/text3/'+str(self.files[self.file_nr])+'new.csv')
                df_labels.to_csv('/home/kacper/Dokumenty/GitHub/data_image_processing/text3/'+str(self.files[self.file_nr])+'new.csv',sep=',')
                
                self.file_nr+=1
                self.countter=0
                self.countter1=0
                return 0
                
            self.countter+=1
            self.read_text()
            
        def analyze_figures(self,xywh,cropped_board,mask,mask1):
            print('analyze figures')
            crop=Image.fromarray(cropped_board)
            mask=Image.fromarray(mask)
            
            plt.imshow(crop)
            plt.show()
            plt.imshow(mask)
            plt.show()
            try:
                let_crop=image_to_string(crop,lang='pol',config='--psm 7 --oem 3')
            except:
                let_crop=''
            try:
                let_mask=image_to_string(mask, lang='pol',config='--psm 7 --oem 3')
            except:
                let_mask=''
            try:
                let_mask1=image_to_string(mask1,lang='pol',config='--psm 7 --oem 3')
            except:
                let_mask1=''
            print(let_crop)
            print(let_mask)
            input("Press Enter to continue...")
            if re.search('[a-zA-Z]',let_crop) or re.search('[a-zA-Z]',let_mask) or re.search('[a-zA-Z]',let_mask1):
                #crop.save(path+'tmp/crop_'+str(self.countter1)+'.jpeg')
                #mask.save(path+'tmp/mask_'+str(self.countter1)+'.jpeg')
                
                dig_crop=image_to_string(cropped_board,lang='pol',config = '--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789')#r'--oem 3 --psm 3 outputbase digits'
                #let_board=image_to_string(cropped_board, lang='pol',config = '--psm 13 --oem3')
                
                
                
                #self.xywh1.append(xywh[self.countter])
                self.labels.append([dig_crop,let_crop,let_mask,let_mask1])
                #print(dig_crop,let_crop,let_mask,let_mask1)
                self.countter1+=1
                
            else:
                pass
            
        def model(self):
            print('model')
            label=pd.DataFrame(self.labels,columns=['0','1','2','3'])
            print('columns',label.columns)
            print('columns',label.head())
            #clf=pickle.load(open('model', 'rb'))
            #print(labels.shape)
            
            averages=label.applymap(lambda x: functions.average_word_length(x))
            stds=label.applymap(lambda x: functions.std(x))
            long=label.apply(lambda x: functions.longest(x['1']),axis=1)
            words_corr_12=label.apply(lambda x: functions.similar_lett(x['1'],x['2']) ,axis=1)
            words_corr_23=label.apply(lambda x: functions.similar_lett(x['2'],x['3']) ,axis=1)
            dig_cor=label.apply(lambda x: functions.similar_dig(x['0'],x['1']) ,axis=1)
            frames=[averages,stds,long,words_corr_12,words_corr_23,dig_cor]
            print('x done')
    
            labels=label
            labels=words_reading.read_labels(labels,dict_pl,dicts,key)
           # if self.file_nr%10==1:
           #     #zapis do pliku, reset pamięci i od nowa
           #     labels.to_csv('result_out_'+str(self.file_nr)+'.csv')
            print('model end')
            
        
       # def opening(self,choosen_file):
       #     print('opening',choosen_file)
       #     file=self.path+self.files[choosen_file]
       #     return file
        
        def client_exit(self):
            self.master.destroy()
        #def clear_variables(self):
    #ImageProcessing=ImageProcessing()


    run(number=i)
    del run
    del ImageProcessing