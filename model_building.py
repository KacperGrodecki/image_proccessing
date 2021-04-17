# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import re
from difflib import SequenceMatcher
import string
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
import pickle



def make_dict(loc_File):
    with open(loc_File, encoding='UTF8') as f:
        lines = f.readlines()
    dict_pl = []
    for line in lines:
        word=line.split()
        dict_pl.append(word)
 
    return [item.replace(',','') for sublist in dict_pl for item in sublist]


def check_pl(text):
    return text in dict_pl 

def dicts_pl(dict_pl,String_pl):
    loc_dicts=[None]*len(String_pl)
    loc_key=[None]*len(String_pl)
    i=0
    for ch in String_pl:
        loc_dicts[i]=[x for x in dict_pl if x[0]==ch ]
        loc_key[i]=ch
        i+=1
    return loc_dicts,loc_key
        


    
def search_similarity(x):
    local_key=x[0]
    number=key.index(local_key)
    for i in range(2,len(x)+1):
        for char in String_pl:
            if i ==0:
                word=char+x[i+1:]
            elif i ==len(x)+1:
                word=x[:i-1]+char
            else:
                word=x[:i]+char+x[i+1:]
            
            if i==0 and check_pl(word):
                return word
            elif i>0:
                if word in dicts[number]:
                    return word
          

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
    
def model_build():    
    
    String_pl=string.ascii_lowercase+'ąśćęó'
    File=r'C:\Users\Lenovo\git\image_proccessing\odm.txt'
    dict_pl=make_dict(File)
    key,dicts=dicts_pl(dict_pl,String_pl)
    
    labels=pd.read_csv(r'C:\Users\Lenovo\git\image_proccessing\resolution500\fig2labels.csv',sep='\t')
    print(labels.shape)
    
    result=np.array([0,0,0,1,0,0,1,0,0,0,
            1,1,1,1,0,0,1,1,0,0,
            1,0,1,1,1,0,1,1,0,0,
            1,1,0,1,0,0,1,1,1,1,
            1,1,1,1,1,0,0,1,0,1,
            0,0,0,1,1,1,1,1,0,0,
            0,0,0,0,0,1,1,0,0,1,
            1,1,1,0,0]
            )
    
    averages=labels.applymap(lambda x: average_word_length(x))
    stds=labels.applymap(lambda x: std(x))
    long=labels.apply(lambda x: longest(x['2']),axis=1)
    words_corr=labels.apply(lambda x: similar_lett(x['2'],x['3']) ,axis=1)
    dig_cor_0=labels.apply(lambda x: similar_dig(x['0'],x['2']) ,axis=1)
    dig_cor_1=labels.apply(lambda x: similar_dig(x['1'],x['2']) ,axis=1)
    
    print(averages.shape,' ',stds.shape,' ',long.shape,' ',words_corr.shape,' ',dig_cor_0.shape,' ',dig_cor_1.shape)
    
    frames=[averages,stds,long,words_corr,dig_cor_0,dig_cor_1]
    x=pd.concat(frames,axis=1)
    
    x=x.fillna(0)    
    x=x.iloc[:,:].values
    
    clf = DecisionTreeClassifier(random_state=0)
    clf.fit(x,result)
    confusion_matrix(result, clf.predict(x))
    pickle.dump(clf, open('model', 'wb'))

model_build()