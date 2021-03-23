# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pytesseract 
import sys 
import os
import pandas as pd
import cv2 
import os
from PIL import Image
from pytesseract import image_to_string
import numpy as np
from matplotlib import pyplot as plt
import os
from matplotlib.pyplot import figure
import enchant
import re
d = enchant.Dict("pl_PL")


        
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
from PIL import ImageTk, Image

class Window(tk.Frame):

    def __init__(self,master,opening,imageProcessing):
        tk.Frame.__init__(self, master)                    
        self.master = master
        self.opening=opening
        self.imageProcessing=imageProcessing
        self.init_window()
        self.countter=0
        
    def init_window(self):
        # master title     
        self.master.title("Renishaw")
        self.pack(fill=tk.BOTH, expand=1)
        # menu file
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        file = tk.Menu(menu)
        file.add_command(label = 'Open data', command = self.open_file)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)
        # menu save
        save = tk.Menu(menu)
        menu.add_cascade(label="Saving", menu=save)
        # menu figure
        file = tk.Menu(menu)
        file.add_command(label ="Find contours", command = self.find_contour)
        file.add_command(label ="Read text", command = self.read_text)
        file.add_command(label ="Next contour", command = self.next_contour)
        menu.add_cascade(label="Figure", menu=file)
        
        #progress bar
        self.progressbar = ttk.Progressbar(self.master, maximum = 100,  orient='horizontal', mode='determinate')
        self.progressbar["value"] = 0
        self.progressbar.pack(expand=True, fill=tk.BOTH, side=tk.BOTTOM)
        # status label
        self.status_label = tk.StringVar()
        self.status_label.set("Begining")
        label = tk.Label( self.master, textvariable=self.status_label, relief=tk.RAISED,height=2,width=30 )
        label.pack()
          
    def client_exit(self):
        self.master.destroy()
        
    def open_file(self):
        self.file,self.image=self.opening.open_file(self.status_label)
        tk.Label(root, image=self.image ).pack() 
        
    def find_contour(self):
        self.contours=self.imageProcessing.find_contours(self.file)
        print(len(self.contours))
        self.progressbar["value"]=len(self.contours)
        
    def read_text(self):
        cropped_board,mask_board=self.contours[self.countter]
        self.imageProcessing.analyze_figures(cropped_board,mask_board)
        
    def next_contour(self):
        self.countter+=1
        print(self.countter)
        self.read_text()
            
        
             
      
class Opening:
    
    def __init__(self):
        pass
    
    def open_file(self,status_label):
        status_label.set("Opening file")
        
        #finction1- open file
        file = askopenfilename(initialdir="C:/Users/",
                           filetypes =(("Text File", "*.jpg"),("All Files","*.*")),
                           title = "Choose a file.")  
        img = cv2.imread(file)
        print('file opened')
        status_label.set("File opened")
        
        b,g,r = cv2.split(img)
        img = cv2.merge((r,g,b))
        
        im = Image.fromarray(img)
        im = im.resize((600, 500), Image.ANTIALIAS)
        return file,ImageTk.PhotoImage(image=im) 
    
    
    
class ImageProcessing:
    def __init__(self):
        pass
    
    def fig_prepare(self,image):
      
      kernel_3x3 = np.ones((3, 3), np.float32) / 9
    
      kernel_sharpening = np.array([[-1,-1,-1], 
                                    [-1, 9,-1],
                                    [-1,-1,-1]])
    
      blurred = cv2.filter2D(image, -1, kernel_3x3)
      sharpened = cv2.filter2D(blurred, -1, kernel_sharpening)
    
      blurred = cv2.filter2D(sharpened, -1, kernel_3x3)
      sharpened = cv2.filter2D(blurred, -1, kernel_sharpening)
    
      lower=np.array([0,0,0])
      upper=np.array([100,100,100])
    
      mask = cv2.inRange(sharpened, lower, upper)
      
      return 255-mask
    
    def mask_from_cropped(self,cropped):
              kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
              dilated = cv2.dilate(cropped, kernel)
              eroded=cv2.erode(dilated,kernel)
    
              kernel_3x3 = np.ones((3, 3), np.float32) / 9
    
              kernel_sharpening = np.array([[-1,-1,-1], 
                                    [-1, 9,-1],
                                    [-1,-1,-1]])
    
              blurred = cv2.filter2D(eroded, -1, kernel_3x3)
              sharpened = cv2.filter2D(blurred, -1, kernel_sharpening)
    
              blurred = cv2.filter2D(sharpened, -1, kernel_3x3)
              sharpened = cv2.filter2D(blurred, -1, kernel_sharpening)
    
              
    
              lower=np.array([0,0,0])
              upper=np.array([130,130,130])
    
              return cv2.inRange(sharpened, lower, upper)
    def string_clean(self,word):
      word_new=word
      for char in word:
        if char.isalnum():
          pass
        else:
          word_new = word.replace(char, "")
      return word_new
  
    def sentences_analyz(self,sentences):
        print('start sentences_analyz \n\n')
        letter,word_new,sentence,sentence_new='','','',''
        w_len,exists,correctness=[],[],[0,0,0,0]
    
        for sen in sentences:
                    for s in sen[0]:
                        if s.isspace():
                            word_new=word_new.join(letter)
                            word_new=self.string_clean(word_new)
                        
                        if word_new:
                            w_len.append(len(word_new))
                            if d.check(word_new):
                                exists.append(1)
                            else:
                                exists.append(0)
                            letter=''
                            sentence=sentence+' '+word_new
                            word_new=''
                        else:
                            letter=letter+s
                    sentence_new=sentence_new.join(sentence)
                    np_w_len=np.array(w_len)
                    np_exists=np.array(exists)
                    #print(w_len)
                    if w_len:
                        print('full sentence','\n',sentence_new)
                        print('numeric analysis ','std ',np.std(np_w_len),'mean ',np.mean(np_w_len),'length ',np_w_len.shape)
                        print('dictionary analysis ',np_exists)
                        data=sentence_new,np_w_len,np_exists 
                        #yield data
                    else:
                        print('empty words ',sentence_new)
                    sentence=''
                    sentence_new=''
                    w_len=[]
                    exists=[]
                    print('next method\n')
                    
    def countrurs(self,gray,ythresh): 
      thresh=255-gray
      # use morphology erode to blur horizontally
      kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (151, 3))
      morph = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel)
    
      # use morphology open to remove thin lines from dotted lines
      kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 17))
      morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)
    
    
      # find contours
      cntrs = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
      cntrs = cntrs[0] if len(cntrs) == 2 else cntrs[1]
    
      # find the topmost box
      for c in cntrs:
            box = cv2.boundingRect(c)
            x,y,w,h = box
            if y < ythresh:
                topbox = box
                ythresh = y
      return cntrs[::-1],topbox
    
    def analyze_figures(self,cropped_board,mask_board):
        print('start analyze')
        correctnes_list=[]
        if re.search('[a-zA-Z]',image_to_string(cropped_board,lang='pol',config = r'--oem 3 --psm 3')) or re.search('[a-zA-Z]',image_to_string(mask_board, lang='pol',config= r'--oem 3 --psm 3')):
            print('words inside')
            string_dig_crop=image_to_string(cropped_board,lang='pol',config = r'outputbase digits')#r'--oem 3 --psm 3 outputbase digits'
            string_dig_mask=image_to_string(mask_board, lang='pol',config = r'outputbase digits')
            string_let_crop=image_to_string(cropped_board,lang='pol')
            string_let_mask=image_to_string(mask_board, lang='pol')
            x0,x1,x2,x3=0,1,2,3
            sentences=[[string_dig_crop,x0],[string_dig_mask,x1],[string_let_crop,x2],[string_let_mask,x3]]
            
            self.sentences_analyz(sentences)
            print('figures printing')
            figure(figsize=(20,50))
            plt.imshow(cropped_board)
            plt.show() 
            #figure(figsize=(20,50))
            #plt.imshow(mask_board)
            #plt.show() 
            #print('figures printed')
        else:
            print('not analysing')
            
    #loading contours        
    def find_contours(self,file):
        #file='/home/kacper/resolution500/fig1.jpg'
        image = cv2.imread(file)
        gray=self.fig_prepare(image)
        
        image = cv2.imread(file)
        result = gray.copy()
        ythresh=1000
        cntrs,topbox=self.countrurs(gray,ythresh)
        i=0
        images=[]
        for c in cntrs:
              box = cv2.boundingRect(c)
              if box != topbox:
                  i=i+1
                  x,y,w,h = box
                  cv2.rectangle(result, (x, y), (x+w, y+h), (0, 0, 255), 2)
                  cropped = image[y:y + h, x:x + w]  
            
                  mask = self.mask_from_cropped(cropped)
                  board=30
                  cropped_board = cv2.copyMakeBorder( cropped, board,board, board, board,cv2.BORDER_CONSTANT, value=[190, 190, 190])
                  mask_board = cv2.copyMakeBorder( mask, board, board, board, board, cv2.BORDER_CONSTANT)
                  im=[cropped_board,mask_board ]
                  images.append(im)  
        return images
 
    
root = tk.Tk()
opening=Opening()
imageProcessing=ImageProcessing()
    
root.geometry("700x600")
app = Window(root,opening,imageProcessing)
root.mainloop()  