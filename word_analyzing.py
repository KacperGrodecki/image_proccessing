# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 16:53:31 2021

@author: Lenovo

funcions and definitions
"""
 
import os
import pandas as pd
#import cv2
import os
#import PIL
#from PIL import Image,ImageTk
#from pytesseract import image_to_string
import numpy as np
from matplotlib import pyplot as plt
import os
from matplotlib.pyplot import figure
import enchant
import re
import difflib
from difflib import SequenceMatcher
import string
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
import re
from autocorrect import Speller
import pickle

d = enchant.Dict('pl_PL')
string_pl=string.ascii_lowercase+'ąśćęó'

file=r'C:\Users\Lenovo\git\image_proccessing\odm.txt'


def make_dict(file):
    with open(file, encoding='UTF8') as f:
        lines = f.readlines()
    dict_pl = []
    for line in lines:
        word=line.split()
        dict_pl.append(word)
 
    return [item.replace(',','') for sublist in dict_pl for item in sublist]

dict_pl=make_dict(file)

def check_pl(text):
    return text in dict_pl 

def dicts_pl():
    dicts=[None]*len(string_pl)
    i=0
    for ch in string_pl:
        dicts[i]=[x for x in dict_pl if x[0]==ch ]
        i+=1
    return dicts
        

dicts=dicts_pl()

key=[None]*len(string_pl)
i=0
for ch in string_pl:
        key[i]=ch
        i+=1
 


    
def search_similarity(x):
    local_key=x[0]
    number=key.index(local_key)
    for i in range(2,len(x)+1):
       # print(x[i])
        for char in string_pl:
            if i ==0:
                word=char+x[i+1:]
            elif i ==len(x)+1:
                word=x[:i-1]+char
            else:
                word=x[:i]+char+x[i+1:]
          #  print(word)
            
            if i==0 and check_pl(word):
                return word
            if i>0:
                if word in dicts[number]:
                    return word
          
  
#dict_pl.sort()

def word_check(text):
    if isinstance(text, str):
        if len(text.strip())>0:
             num_words = len(text.split())
             words=text.split()
             correct=0
             for word in words:
                correct+=int(d.check(word))
             return correct/num_words
        else:
             return 0
    else:
        return text

def clean_up(s):
    return s.strip(string.punctuation)

def average_word_length(text):
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
        average_word_length(str(text))
        
def std(text):
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
        std(str(text))
        
def longest(text):
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
        std(str(text))



def consist_number(string):
    return type(string)
    if type(string) is str:
        return any(i.isdigit() for i in string)
    
def char_type_counter(text):
    if isinstance(text, str):
        dig,alpha=0,0
        for char in text.strip():
            if char.isdigit():
                dig+=1
            elif char.isalpha():
                alpha+=1
        if dig+alpha==0:
            return 'empty'
        else:
            return alpha/(dig+alpha)
    else:
        return 0
            

def similar_dig(a, b):
    if isinstance(a, str) and isinstance(b, str): 
        
        a=re.sub(r'\d+', '',a)
        b=re.sub(r'\d+', '',b)
        return SequenceMatcher(None, a, b).ratio()
    else:
        return similar_dig(str(a),str(b))
    
def similar_lett(a, b):
    if isinstance(a, str) and isinstance(b, str): 
        a=re.sub(r'\W+', '',a)
        b=re.sub(r'\W+', '',b)
        return SequenceMatcher(None, a, b).ratio()
    else:
        return similar_lett(str(a),str(b))            
    
def spell_checker(text):
    new_text=''
    new_word=''
    for word in text.split():
        #print(word)
        if word[-1]=='.' or word[-1]==',':
            new_text+=word+' '
        elif word[0]=='"':
            new_text+=word[0]+word[1:].lower()
        else:
            new_word=word[0]+word[1:].lower()
            #przerobić duże na małe i z powrotem
            new_text+=spell(new_word)+' '
    return new_text
    
def char_type_counter(text):
    if isinstance(text, str):
        dig,alpha=0,0
        for char in text.strip():
            if char.isdigit():
                dig+=1
            elif char.isalpha():
                alpha+=1
        if dig+alpha==0:
            return 'empty'
        else:
            return alpha/(dig+alpha)
    else:
        return 0
    
#xywh=pd.read_csv('xywh.csv')

"""
firts df cleaning

"""

labels=pd.read_csv(r'C:\Users\Lenovo\git\image_proccessing\resolution500\fig1labels.csv',index_col=0,sep='\t')

labels=pd.read_csv(r'C:\Users\Lenovo\git\image_proccessing\resolution500\fig2labels.csv',index_col=0,sep='\t')

labels=pd.read_csv(r'C:\Users\Lenovo\git\image_proccessing\resolution500\fig3labels.csv',index_col=0,sep='\t')

results=np.array([0,0,0,1,0,0,1,0,0,0,
        1,1,1,1,0,0,1,1,0,0,
        1,0,1,1,1,0,1,1,0,0,
        1,1,0,1,0,0,1,1,1,1,
        1,1,1,1,1,0,0,1,0,1,
        0,0,0,1,1,1,1,1,0,0,
        0,0,0,0,0,1,1,0,0,1,
        1,1,1,0,0]
        )
#poprawki na labels1
results1=labels.iloc[:,4].values
results1[1]=0
results1[53]=1
results1[65]=1

results1[75]=0
results1[76]=0
results1[77]=0
#poprawki na labels3
results3=labels.iloc[:,4].values
results3[1]=0
results3[7]=1
results3[12]=1
results3[23]=1
results3[26]=1
results3[39]=1
results3[42]=1
results3[56]=0



#model-wybór własciwych komurek
averages=labels.applymap(lambda x: average_word_length(x))
stds=labels.applymap(lambda x: std(x))
long=labels.apply(lambda x: longest(x['2']),axis=1)
words_corr=labels.apply(lambda x: similar_lett(x['2'],x['3']) ,axis=1)
dig_cor_0=labels.apply(lambda x: similar_dig(x['0'],x['2']) ,axis=1)
dig_cor_1=labels.apply(lambda x: similar_dig(x['1'],x['2']) ,axis=1)

frames=[averages,stds,long,words_corr,dig_cor_0,dig_cor_1]
x=pd.concat(frames,axis=1)

x=x.fillna(0)    
x=x.iloc[:,:].values

x1=x
x2=x
x3=x

x=np.concatenate((x1,x2,x3))
result=np.concatenate((results1,results2,results3))
#####################
clf = DecisionTreeClassifier(random_state=0)
clf.fit(x,result)
#weryfikacja modelu-prezentacja każdej z linijek i najlepiej obok rysunek-tkinter???jupyter notebook?

#program_w_tkinterze




confusion_matrix(result, clf.predict(x))
pickle.dump(clf, open('model', 'wb'))
#####################
results=clf.predict(x)
labels['results']=results
#model-budowa zdan i liczb
labels_corr=labels[labels['results']==1]
#spradwzenie czy to liczba czy slowo-wyjsciowa kolumna to 2
labels_corr['letters']=labels_corr.apply(lambda x: char_type_counter(x['2']),axis=1)


            



labels_corr['words_cor']=labels_corr.apply(lambda x: similar_lett(x['2'],x['3']) ,axis=1)

labels_corr['num_0']=labels_corr.apply(lambda x: similar_dig(x['0'],x['2']) ,axis=1)
labels_corr['num_1']=labels_corr.apply(lambda x: similar_dig(x['1'],x['2']) ,axis=1)




spell = Speller(lang='pl')#,only_replacements=True)

fin_text=labels_corr[(labels_corr['words_cor']>0.8)&(labels_corr['letters']>0.5)]['3']
fin_text_corected=fin_text.apply(lambda x: spell_checker(x))
fin_t=pd.concat([fin_text,fin_text_corected],axis=1)




fin_dig=labels_corr[(labels_corr['num_0']>0.7) & (labels_corr['letters']<0.5)]['0']        
fin=pd.concat([fin_dig,fin_text])

fin=fin.sort_index()
df_fin=pd.concat([fin],axis=1)
#układanie q dokumencie
xywh=pd.read_csv('xywh1.csv',sep='\t')

fin_pos=pd.merge(df_fin, xywh, left_index=True, right_index=True)


fin_pos=fin_pos.sort_values(by=['y','x'])

fin_pos['y1']=100*(fin_pos['y']-min(fin_pos['y']))/(max(fin_pos['y'])-min(fin_pos['y']))
fin_pos['x1']=20*(fin_pos['x']-min(fin_pos['x']))/(max(fin_pos['x'])-min(fin_pos['x']))

fin_pos['y1']=fin_pos['y1'].diff()
fin_pos.iloc[0,6]=0

fin_pos['x1']=fin_pos['x1'].astype('int32')
fin_pos['y1']=fin_pos['y1'].astype('int32')

text=''
for index, row in fin_pos.iterrows():
    text+=row['y1']*'\n'+row['x1']*' '+str(row[0])
    


text_file = open("Output3.txt", "w")
text_file.write(text)
text_file.close()

text=labels.iloc[6,2]
num_words = len(text.split())
words=text.split()
correct=0
for word in words:
    print(word.lower())
    correct+=d.check(word.lower())
correct/num_words


