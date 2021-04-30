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
path = '/home/kacper/Dokumenty/GitHub/image_proccessing/'        
import tkinter as tk
from tkinter.filedialog import askopenfilename

class Window(tk.Frame):

    def __init__(self,master,opening,imageProcessing):
        tk.Frame.__init__(self, master)                    
        self.master = master
        self.opening=opening
        self.imageProcessing=imageProcessing
        self.init_window()
        self.countter=0
        self.countter1=0
        self.labels=[]
        self.xywh=[]
        self.xywh1=[]
    def init_window(self):
        # master title     
        self.master.title("Renishaw")
       # self.pack(fill=tk.BOTH, expand=1)
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
        #canvas
        self.status_label0 = tk.StringVar()
        self.status_label0.set("Begining")
        
       
    def client_exit(self):
        self.master.destroy()
        
    def open_file(self):
        self.file,self.image=self.opening.open_file(self.status_label0)
        
        #do rysnku trzeba dodać kontury
        
        self.can=tk.Canvas(self.master, width=1000, height=1500)
        self.can.pack()
        self.can.create_image((0, 0), image=self.image,anchor='nw')
        
    
        self.find_contour()
    def find_contour(self):
        self.contours,self.xywh=self.imageProcessing.find_contours(self.file)
        print('liczba konturów ',len(self.contours))
        
        self.read_text()
        
    def read_text(self):
        cropped_board,mask,mask1=self.contours[self.countter]
        self.analyze_figures(self.xywh,cropped_board,mask,mask1)
        
        self.next_contour()
        
    def next_contour(self):
       
        #self.save_data()
        print(self.countter)
        if self.countter>len(self.contours)-2:
            print('finish')
            df = pd.DataFrame (self.labels)
            df.to_csv(path+'/tmp/labels.csv',sep='\t')
            
            df = pd.DataFrame (self.xywh1)
            df.to_csv(path+'/tmp/xywh.csv',sep='\t')
            
            print('closing')
            return self.client_exit()
        self.countter+=1
        self.read_text()
        
    def analyze_figures(self,xywh,cropped_board,mask,mask1):
        crop=Image.fromarray(cropped_board)
        mask=Image.fromarray(mask)
        let_crop=image_to_string(cropped_board,lang='pol',config='--psm 7 --oem 3')
        let_mask=image_to_string(mask, lang='pol',config='--psm 7 --oem 3')
        let_mask1=image_to_string(mask1,lang='pol',config='--psm 7 --oem 3')
        if re.search('[a-zA-Z]',let_crop) or re.search('[a-zA-Z]',let_mask) or re.search('[a-zA-Z]',let_mask1):
            crop.save(path+'tmp/crop_'+str(self.countter1)+'.jpeg')
            mask.save(path+'tmp/mask_'+str(self.countter1)+'.jpeg')
            
            dig_crop=image_to_string(cropped_board,lang='pol',config = '--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789')#r'--oem 3 --psm 3 outputbase digits'
            #let_board=image_to_string(cropped_board, lang='pol',config = '--psm 13 --oem3')
            
            
            
            self.xywh1.append(xywh[self.countter])
            self.labels.append([dig_crop,let_crop,let_mask,let_mask1])
            self.countter1+=1
            
        else:
            pass
        
             
      
class Opening:
    
    def __init__(self):
        pass
    
    def open_file(self,status_label0):
        status_label0.set("Opening file")
        
        #finction1- open file
        choosen_file = askopenfilename(initialdir=path,
                           filetypes =(("Text File", "*.jpg"),("All F iles","*.*")),
                           title = "Choose a file.")  
        
        file='fig10'
        path_fin = path+file+'.jpg'
        print('defined path ',path_fin)
        print('chosen path ',choosen_file)
        #img = cv2.imread(path_fin)
        img = cv2.imread(choosen_file)
        print('file opened')
        status_label0.set("File opened")
        
        b,g,r = cv2.split(img)
        img = cv2.merge((r,g,b))
        
        im = Image.fromarray(img)
        im = im.resize((500, 700))
        return choosen_file,ImageTk.PhotoImage(image=im)
    
    
    
class ImageProcessing:
    def __init__(self):
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
              sharpened1 = cv2.filter2D(blurred, -1, kernel_sharpening)
              lower=np.array([0,0,0])
              upper=np.array([130,130,130])
    
              return 255- cv2.inRange(sharpened, lower, upper),255 - cv2.inRange(sharpened1, lower, upper)

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
      return cntrs[::-1],topbox
    
    
            
    #loading contours        
    def find_contours(self,file):
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
                  board=30
                  cropped_board = cv2.copyMakeBorder( cropped, board,board, board, board,cv2.BORDER_CONSTANT, value=[190, 190, 190])
                  mask = cv2.copyMakeBorder( mask, board, board, board, board, cv2.BORDER_CONSTANT,value=[255, 255, 255])
                  mask1 = cv2.copyMakeBorder( mask1, board, board, board, board, cv2.BORDER_CONSTANT,value=[255, 255, 255])
                  im=[cropped_board,mask,mask1]
                  images.append(im)  
        return images,xywh
 
    
root = tk.Tk()
opening=Opening()
imageProcessing=ImageProcessing()
    
root.geometry("500x500")
app = Window(root,opening,imageProcessing)
root.mainloop()  
