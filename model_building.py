# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import re
from difflib import SequenceMatcher
import string
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
import pickle
 
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
    labels=pd.read_csv('/home/kacper/Dokumenty/GitHub/image_proccessing/tmp/labels.csv',sep='\t',index_col=0)
    result_fig10=np.array([0,0,0,0,0,#zalacznik 
                           1,0,1,0,1,#pax
                           0,0,1,1,1,1,#dzialanosc
                           1,1,0,1,0,0,1,#płace
                           1,1,1,0,1,1,1,1,#podróże
                           1,1,1,1,1,1,1,1,#augustyna
                           1,1,1,1,1,1,1,1,#wnictw
                           1,1,0,0,1,0,0,1,#budżet
                           1,1,1,1,0,0,0]
            )
    averages=labels.applymap(lambda x: average_word_length(x))
    stds=labels.applymap(lambda x: std(x))
    long=labels.apply(lambda x: longest(x['1']),axis=1)
    words_corr_12=labels.apply(lambda x: similar_lett(x['1'],x['2']) ,axis=1)
    words_corr_23=labels.apply(lambda x: similar_lett(x['2'],x['3']) ,axis=1)
    dig_cor=labels.apply(lambda x: similar_dig(x['0'],x['1']) ,axis=1)
    frames=[averages,stds,long,words_corr_12,words_corr_23,dig_cor]
    x=pd.concat(frames,axis=1)
    
    x=x.fillna(0)    
    x=x.iloc[:,:].values
    
    clf = DecisionTreeClassifier(random_state=0)
    clf.fit(x,result_fig10)
    pickle.dump(clf,open('model', 'wb'))
    print(confusion_matrix(result_fig10, clf.predict(x)))

model_build()

    