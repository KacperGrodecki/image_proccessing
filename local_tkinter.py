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
import enchant
import re
d = enchant.Dict("pl_PL")
import time
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
        self.data=[]
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
        
        # status label
        self.var0 = tk.IntVar()
        self.var1 = tk.IntVar()
        self.var2 = tk.IntVar()
        self.var3 = tk.IntVar()
        
        self.status_label0 = tk.StringVar()
        self.status_label1 = tk.StringVar()
        self.status_label2 = tk.StringVar()
        self.status_label3 = tk.StringVar()
        
        self.status_label0.set("Begining")
        
        label0 = tk.Label( self.master, textvariable=self.status_label0, relief=tk.RAISED,height=2,width=50 )
        label1 = tk.Label( self.master, textvariable=self.status_label1, relief=tk.RAISED,height=2,width=50 )
        label2 = tk.Label( self.master, textvariable=self.status_label2, relief=tk.RAISED,height=2,width=50 )
        label3 = tk.Label( self.master, textvariable=self.status_label3, relief=tk.RAISED,height=2,width=50 )
        
        c0 = tk.Checkbutton(self.master, text='Correct?',variable=self.var0, onvalue=1, offvalue=0)
        c1 = tk.Checkbutton(self.master, text='Correct?',variable=self.var1, onvalue=1, offvalue=0)
        c2 = tk.Checkbutton(self.master, text='Correct?',variable=self.var2, onvalue=1, offvalue=0)
        c3 = tk.Checkbutton(self.master, text='Correct?',variable=self.var3, onvalue=1, offvalue=0)
        
        label0.place(relx=1.0, rely=1.0,anchor ='nw')
        c0.place(relx=1.0, rely=1.0,anchor ='nw')
        label1.place(relx=1.0, rely=1.0,anchor ='nw')
        c1.place(relx=1.0, rely=1.0,anchor ='nw')
        label2.place(relx=1.0, rely=1.0,anchor ='nw')
        c2.place(relx=1.0, rely=1.0,anchor ='nw')
        label3.place(relx=1.0, rely=1.0,anchor ='nw')
        c3.place(relx=1.0, rely=1.0,anchor ='nw')
        
        label0.pack()
        c0.pack()
        label1.pack()
        c1.pack()
        label2.pack()
        c2.pack()
        label3.pack()
        c3.pack()
          
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
        #df = pd.DataFrame (xywh,columns=['x','y','w','h'])
        #df.to_csv(path+self.file+'_xywh'+'.csv',sep='\t')
        self.read_text()
        
    def read_text(self):
        cropped_board,mask_board=self.contours[self.countter]
        data=self.imageProcessing.analyze_figures(self.countter,self.file,self.xywh,cropped_board,mask_board,
                                             self.status_label0,self.status_label1,self.status_label2,self.status_label3)
        
        self.next_contour()
        
    def next_contour(self):
        start = time.process_time()
        self.save_data()
        print(self.countter)
        if self.countter>len(self.contours)-2:
            print('finish')
            df = pd.DataFrame (self.data,columns=['0','1','2','3'])
            df.to_csv(path+'/tmp/labels1.csv',sep='\t')
            print('closing')
            return self.client_exit()
            
        self.status_label0.set('')
        self.status_label1.set('')
        self.status_label2.set('')
        self.status_label3.set('')
        self.countter+=1
        stop = time.process_time()
        print(self.countter)
        
        print('labels printing ',stop-start)
        self.read_text()
        
    def save_data(self):
        self.data.append([self.status_label0.get(),
                         self.status_label1.get(),
                         self.status_label2.get(),
                         self.status_label3.get()])
        
             
      
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
  
    def sentences_analyz(self,sentences,status_label0,status_label1,status_label2,status_label3 ):
        start = time.process_time()
        #print('start sentences_analyz \n\n')
        letter,word_new,sentence,sentence_new='','','',''
        w_len,exists=[],[]
        data=[]
        sent=[]
        for sen in sentences:
                    for s in sen[0]:
                        if s.isspace():
                            word_new=word_new.join(letter)
                        
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
                    if sentence_new:
                        data.append([sentence_new,np_w_len,np_exists])
                        sent.append(sentence_new)
                    else:
                        data.append(['',np.nan,np.nan])
                        sent.append('')
                    sentence=''
                    sentence_new=''
                    w_len=[]
                    exists=[]
        status_label0.set(sent[0])
        status_label1.set(sent[1])
        status_label2.set(sent[2])
        status_label3.set(sent[3])
        stop = time.process_time()
        print('word analyzing ',stop-start)
        return data
                    
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
    
    def analyze_figures(self,countter,file,xywh,cropped_board,mask_board,status_label0,status_label1,status_label2,status_label3):
        crop=Image.fromarray(cropped_board)
        start = time.process_time()
        string_let_crop=image_to_string(cropped_board,lang='pol',config='--psm 13 ')
        if re.search('[a-zA-Z]',string_let_crop):
            crop.save(path+'tmp/crop_'+str(countter)+'.jpeg')
            with open(path+'tmp/xywh.npy', 'ab') as f:
                np.savetxt(f, xywh)
            f.close
            
            string_dig_crop=image_to_string(cropped_board,lang='pol',config = '--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')#r'--oem 3 --psm 3 outputbase digits'
            string_dig_mask=image_to_string(cropped_board, lang='pol',config = '--psm 13 --oem 3 outputbase digits')
            string_let_mask=image_to_string(mask_board, lang='pol',config='--psm 13')
            stop = time.process_time()
            data=''
            x0,x1,x2,x3=0,1,2,3
            #sentences=[[string_dig_crop,x0],[string_dig_mask,x1],[string_let_crop,x2],[string_let_mask,x3]]
            
            status_label0.set(string_dig_crop)
            status_label1.set(string_dig_mask)
            status_label2.set(string_let_crop)
            status_label3.set(string_let_mask)
            string=string_dig_crop+'\t'+string_dig_mask+'\t'+string_let_crop+'\t'+string_let_mask
            
            with open(path+'tmp/labels_corrected.txt', 'a') as f:
                f.write(string)
            f.close
            
            #data=self.sentences_analyz(sentences, status_label0,status_label1,status_label2,status_label3)
            print('images analyzing ',stop-start)
            return data
         
        else:
            status_label0.set('') 
            
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
            
                  mask = self.mask_from_cropped(cropped)
                  board=30
                  cropped_board = cv2.copyMakeBorder( cropped, board,board, board, board,cv2.BORDER_CONSTANT, value=[190, 190, 190])
                  mask_board = cv2.copyMakeBorder( mask, board, board, board, board, cv2.BORDER_CONSTANT)
                  im=[cropped_board,mask_board ]
                  images.append(im)  
        return images,xywh
 
    
root = tk.Tk()
opening=Opening()
imageProcessing=ImageProcessing()
    
root.geometry("1000x1000")
app = Window(root,opening,imageProcessing)
root.mainloop()  
