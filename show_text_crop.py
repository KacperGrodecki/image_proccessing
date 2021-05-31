# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
from PIL import Image,ImageTk
import numpy as np
import enchant
import re
d = enchant.Dict("pl_PL")
path = 'home/kacper/Dokumenty/GitHub/image_proccessing/tmp/'        
import tkinter as tk
from PIL import ImageDraw
from difflib import SequenceMatcher
import pickle


class Window(tk.Frame):

    def __init__(self,master,opening,model):
        tk.Frame.__init__(self, master)   
        self.model=model
        self.result=self.model.model_run()                 
        self.master = master
        self.opening=opening
        self.init_window()
        self.N=self.result.shape[0]
        self.read_0=0
        self.read_1=0
        
        self.label=[None]*self.N
        self.c=[None]*self.N
        self.var=[None]*self.N
        
        
    def init_window(self):
        # master title     
        self.master.title("napisy vs rysunki")
        # menu file
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        file = tk.Menu(menu)
        file.add_command(label="Exit", command=self.client_exit)
        file.add_command(label="Save", command=self.save)
        file.add_command(label="Redeable", command=self.read_text_1) 
        file.add_command(label="Unredeable", command=self.read_text_0) 
        menu.add_cascade(label="File", menu=file)
        
        
    def init_labels_check(self,result_01,distance):
        #N macierz-
        #result-macierz
        i=0
        while i< result_01.shape[0]: 
       # #for i in range(0,self.N):
       #     #problem dla dużych N-wszystkie wyniki result-wszystkie, ale result_01 to lokalne
            print(i,' ',result_01.index[i])#wyświetyla wyniki dla wszystkich i a nie wszystkie są zawarte w 
            self.var[result_01.index[i]] = tk.IntVar()    
            self.c[self.result.index[i]]=tk.Checkbutton(self.master, text=result_01.index[i],variable=self.var[result_01.index[i]], onvalue=1, offvalue=0)#str(result_01.index[i])
            #self.c[self.result.index[i]]
            self.c[self.result.index[i]].place(x=distance, y=sum(self.heights[0:i]),anchor ='nw')
            i+=1
            
          
    def client_exit(self):
        print('exit')
        self.master.destroy()
        
        
    def read_text_0(self):
        result_01=self.read_images(0)
        self.init_labels_check(result_01,0)
        self.read_0=1
        
    
    def read_text_1(self):
        result_01=self.read_images(1)
        self.init_labels_check(result_01,40)
        
    def read_images(self,choose):
        result_01=self.result[self.result['results']==choose]
        N_img=len(result_01)
        path='/home/kacper/Dokumenty/GitHub/image_proccessing/tmp/'
        file=[None]*N_img
        for i in range(0,N_img):
            file[i]=path+'crop_'+str(result_01.index[i])+'.jpeg'  
            
        
        images = [Image.open(x) for x in file]#file1, file2, file3
        images=[img.resize((int(img.size[0]/6),int(img.size[1]/6))) for img in images]
        #reslace images
                 
        self.widths, self.heights = zip(*(i.size for i in images))
        
        self.total_width = max(self.widths)
        max_height = sum(self.heights)
        
        new_im = Image.new('RGB', (self.total_width, max_height))
        
        y_offset = 0
        for im in images:
          new_im.paste(im, (0,y_offset))
          y_offset += im.size[1]
          
       
        self.width, self.height = new_im.size
        self.draw  = ImageDraw.Draw(new_im)
        self.photo = ImageTk.PhotoImage(image=new_im)
        
        self.canvas = tk.Canvas(self.master, width=self.width, height=self.height)
        self.canvas.pack()
        self.canvas.place(x=100, y=0,anchor ='nw')
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        return result_01
    

    def save(self):
        new_results=[]
        for i in range(0,self.N):
            new_results.append(self.var[i].get())
        #np_new=np.array(new_results)
        #np_results=self.result.iloc[:,-1].values
        
        np_xor=np.array(new_results)^self.result.iloc[:,-1].values
        
        print(self.result.iloc[:,-1].values)
        print(np_xor)
        self.result['results_cor']=np_xor
        self.result=self.result[self.result['results_cor']==1]
        self.result=self.result.drop(columns=['results_cor', 'results'])
        self.result.to_csv('result.csv')
        
        
    
        
        
             
      
class Opening:
    
    def __init__(self):
        pass
    
    def open_file(self,file):
        return Image.open(file)
    
class Model:
    
    def __init__(self):
        pass
    
    def model_run(self):
        labels=pd.read_csv('/home/kacper/Dokumenty/GitHub/image_proccessing/tmp/labels.csv',sep='\t',index_col=0)
        clf=pickle.load(open('model', 'rb'))
        #print(labels.shape)
        averages=labels.applymap(lambda x: self.average_word_length(x))
        stds=labels.applymap(lambda x: self.std(x))
        long=labels.apply(lambda x: self.longest(x['1']),axis=1)
        words_corr_12=labels.apply(lambda x: self.similar_lett(x['1'],x['2']) ,axis=1)
        words_corr_23=labels.apply(lambda x: self.similar_lett(x['2'],x['3']) ,axis=1)
        dig_cor=labels.apply(lambda x: self.similar_dig(x['0'],x['1']) ,axis=1)
        frames=[averages,stds,long,words_corr_12,words_corr_23,dig_cor]
        x=pd.concat(frames,axis=1)
        
        #print(averages.shape,' ',stds.shape,' ',long.shape,' ',words_corr.shape,' ',dig_cor_0.shape,' ',dig_cor_1.shape)
        
        x=pd.concat(frames,axis=1)
        x=x.fillna(0)    
        x=x.iloc[:,:].values
        results=clf.predict(x)
        labels['results']=results
        
        
        
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