# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import cv2
from PIL import Image,ImageTk
import numpy as np
import enchant
import re
d = enchant.Dict("pl_PL")
import time
path = 'C:\\Users\\Lenovo\\git\\image_proccessing\\resolution500\\'        
import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image, ImageDraw
from difflib import SequenceMatcher
import pickle

class Window(tk.Frame):

    def __init__(self,master,opening,model):
        tk.Frame.__init__(self, master)   
        self.model=model
        self.df=self.model.model_run()                 
        self.master = master
        self.opening=opening
        self.init_window()
        self.read_images()
        self.init_labels_check()
        #wczytać liczbę obiektów, żeby można było stworzyć liczbę labels i canvas oraz skategoryzować rysunki
        
        
    def init_window(self):
        # master title     
        self.master.title("napisy vs rysunki")
        # menu file
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        file = tk.Menu(menu)
        file.add_command(label="Exit", command=self.client_exit)
        file.add_command(label="Save", command=self.save)
        file.add_command(label="Read", command=self.read_text) 
        menu.add_cascade(label="File", menu=file)
        
        
    def init_labels_check(self):
        
        
        self.var1 = tk.IntVar()
        self.var2 = tk.IntVar()
        self.var3 = tk.IntVar()
        
        self.status_label0 = tk.StringVar()
        self.status_label1 = tk.StringVar()
        self.status_label2 = tk.StringVar()
        
        label1 = tk.Label( self.master, text=self.df.iloc[6,4], relief=tk.RAISED,height=1,width=50 )
        label2 = tk.Label( self.master, text=self.df.iloc[10,4], relief=tk.RAISED,height=1,width=50 )
        label3 = tk.Label( self.master, text=self.df.iloc[12,4], relief=tk.RAISED,height=1,width=50 )
        #
        
        c1 = tk.Checkbutton(self.master, text='Correct?',variable=self.var1, onvalue=1, offvalue=0)
        c2 = tk.Checkbutton(self.master, text='Correct?',variable=self.var2, onvalue=1, offvalue=0)
        c3 = tk.Checkbutton(self.master, text='Correct?',variable=self.var3, onvalue=1, offvalue=0)
        
        print(self.heights[0])
        label1.place(x=self.total_width, y=0,anchor ='nw')
        c1.place(x=self.total_width+300, y=0,anchor ='nw')
        label2.place(x=self.total_width, y=self.heights[0],anchor ='nw')
        c2.place(x=self.total_width+300, y=self.heights[0],anchor ='nw')
        label3.place(x=self.total_width, y=sum(self.heights[0:2]),anchor ='nw')
        c3.place(x=self.total_width+300, y=sum(self.heights[0:2]),anchor ='nw')
        
        
        #label1.pack()
        #c1.pack()
        #label2.pack()
        #c2.pack()
        #label3.pack()
        #c3.pack()
        
          
    def client_exit(self):
        print('exit')
        self.master.destroy()
        
        
    def read_images(self):
        list_wrong=self.df[self.df['results']==1]
        print(list_wrong.index)
        #self.image=self.opening.open_file(r'C:\Users\Lenovo\git\image_proccessing\resolution500\tmp\cropfig1_23.jpeg')
        path='C:\\Users\\Lenovo\\git\\image_proccessing\\resolution500\\tmp\\'
        file1=path+'cropfig1_'+str(list_wrong.index[1])+'.jpeg'
        file2=path+'cropfig1_'+str(list_wrong.index[2])+'.jpeg'
        file3=path+'cropfig1_'+str(list_wrong.index[3])+'.jpeg'
        images = [Image.open(x) for x in [file1, file2, file3]]
        images=[img.resize((int(img.size[0]/4),int(img.size[1]/4))) for img in images]
        #reslace images
                 
        self.widths, self.heights = zip(*(i.size for i in images))
        
        self.total_width = max(self.widths)
        max_height = sum(self.heights)
        
        new_im = Image.new('RGB', (self.total_width, max_height))
        
        y_offset = 0
        for im in images:
          new_im.paste(im, (0,y_offset))
          y_offset += im.size[1]
          
       # self.image = Image.open(r'C:\Users\Lenovo\git\image_proccessing\resolution500\fig1.jpg')
        self.width, self.height = new_im.size
        self.draw  = ImageDraw.Draw(new_im)
        self.photo = ImageTk.PhotoImage(image=new_im)
        
        self.canvas = tk.Canvas(self.master, width=self.width, height=self.height)
        self.canvas.pack()
        self.canvas.place(relx=0, rely=0,anchor ='nw')
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)


    def read_text(self):
        #najpierw trzeba odpalić model żeby df przerobić, potem można pytać czy prawidłowo
        #self.status_label0.set(self.df.iloc[0,5])
        print(self.var1.get())
        print(self.var2.get())
        print(self.var3.get())
    
    
    def save(self):
        pass
        
        
             
      
class Opening:
    
    def __init__(self):
        pass
    
    def open_file(self,file):
        return Image.open(file)
    
class Model:
    
    def __init__(self):
        pass
    
    def model_run(self):
        labels=pd.read_csv(r'C:\Users\Lenovo\git\image_proccessing\resolution500\tmp\_labelsfig1.csv',sep='\t')
        clf=pickle.load(open('model', 'rb'))
        #print(labels.shape)
        averages=labels.applymap(lambda x: self.average_word_length(x))
        stds=labels.applymap(lambda x: self.std(x))
        long=labels.apply(lambda x: self.longest(x['2']),axis=1)
        words_corr=labels.apply(lambda x: self.similar_lett(x['2'],x['3']) ,axis=1)
        dig_cor_0=labels.apply(lambda x: self.similar_dig(x['0'],x['2']) ,axis=1)
        dig_cor_1=labels.apply(lambda x: self.similar_dig(x['1'],x['2']) ,axis=1)
        
        print(averages.shape,' ',stds.shape,' ',long.shape,' ',words_corr.shape,' ',dig_cor_0.shape,' ',dig_cor_1.shape)
        
        frames=[averages,stds,long,words_corr,dig_cor_0,dig_cor_1]
        
        x=pd.concat(frames,axis=1)
        x=x.fillna(0)    
        x=x.iloc[:,:].values
        results=clf.predict(x)
        labels['results']=results
        
        print(labels.iloc[0,5])
        
        return labels
        
        
    def average_word_length(self,text):
        if isinstance(text, str):
            text=re.sub(r'W+', '',text)
            if len(text.strip())>0:
                total_length = len(text)-text.count(' ')
                num_words = len(text.split())
                return total_length/num_words
            else:
                return 0
        elif text==np.nan:
            return 0
        else:
            self.average_word_length(str(text))
            
    def std(self,text):
        if isinstance(text, str):
            text=re.sub(r'W+', '',text)
            if len(text.strip())>0:
                total_length = len(text)-text.count(' ')
                num_words = len(text.split())
                avg=total_length/num_words
                words=text.split()
                out=0
                for word in words:
                    out+=(len(word)-avg)**2 
                return (out/num_words)**0.5
            else:
                return 0
        elif text==np.nan:
            return 0
        else:
            self.std(str(text))
            
    def longest(self,text):
        if isinstance(text, str):
            if len(text.strip())>0:
                words=text.split()
                out=0
                for word in words:
                    if len(word)>out:
                        out=len(word)
                return out
            else:
                return 0
        elif text==np.nan:
            return 0
        else:
            self.std(str(text))
            
    def similar_dig(self,a, b):
        if isinstance(a, str) and isinstance(b, str): 
            
            a=re.sub(r'\d+', '',a)
            b=re.sub(r'\d+', '',b)
            return SequenceMatcher(None, a, b).ratio()
        else:
            return self.similar_dig(str(a),str(b))
    
    def similar_lett(self,a, b):
        if isinstance(a, str) and isinstance(b, str): 
            a=re.sub(r'\W+', '',a)
            b=re.sub(r'\W+', '',b)
            return SequenceMatcher(None, a, b).ratio()
        else:
            return self.similar_lett(str(a),str(b))   
    
    
    

root = tk.Tk()
opening=Opening()
model=Model()
    
root.geometry("1000x1000")
app = Window(root,opening,model)
root.mainloop()  