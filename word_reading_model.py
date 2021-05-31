#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 14:11:59 2021

@author: kacper
"""

# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from difflib import SequenceMatcher
import string

whitelist = set('aąbcćdeęfghijklłmnoóprsśtuvwxyzźż AĄBCĆDEEFGHIJKLŁMNOÓPQRSŚTUVWXYZŹŻ')
'''
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
 '''         

def clean_up(a):
    return a.strip(string.punctuation)

#[int(a) for a in txt.split() if a.isdigit()]

#similar_dig('98f9g9','98.99.')

def similar_dig(a, b):
    if a.strip()=='':
        return 0
    if isinstance(a, str) and isinstance(b, str): 
        a=[int(d) for d in a if d.isdigit()]
        b=[int(d) for d in b if d.isdigit()]
        return SequenceMatcher(None, a, b).ratio()
    else:
        return similar_dig(str(a),str(b))
    
def similar_lett(a, b):
    if isinstance(a, str) and isinstance(b, str): 
        #a=re.sub(r'\W+', '',a)
        #=re.sub(r'\W+', '',b)
        a=[d for d in a if d.isalpha()]
        b=[d for d in b if d.isalpha()]
        return SequenceMatcher(None, a, b).ratio()
    else:
        return similar_lett(str(a),str(b))         
    
def check_string_pl(a):
    result=0
    a=''.join(filter(whitelist.__contains__, a))
    for word in a.split():
       # print(word,' ',check_pl(word))
        result+=int(check_pl_alfabet(word.lower()))
    if len(a.split())>0:
        return result/len(a.split())
    else:
        return 0

def char_type_word(a):
    dig=0
    alpha=0
    for char in a:
        if char in String_pl:
            alpha+=1
        dig+=int(char.isnumeric())
    if (dig+alpha)>0:
        return alpha/(dig+alpha)
    else:
        return None


def check_pl_alfabet(a):
    try:
        first_letter=key.index(a[0])
    except:
        return False
    if a in dicts[first_letter]:
        return True
    else:
        return False
#def check_pl_first_letter(a):
    
    
def word_correction(a):
    for word in a.split():
        if len(word)>1:
            if check_string_pl(word.lower())<1:
                for i in range(0,len(word)+1):
                    if i==0:
                        for replace in String_pl:
                            word_new=replace+word[1:]
                            if check_pl_alfabet(word_new):
                                print(word_new)
                    else:
                        for replace in String_pl:
                            word_new=word[:i]+replace+word[i+1:]
                            if check_pl_alfabet(word_new):
                                print(word_new)
       
String_pl='aąbcćdeęfghijklłmnoópqrsśtuvwxyzźż AĄBCĆDEEFGHIJKLŁMNOÓPQQRSŚTUVWXYZŹŻ'
File='/home/kacper/Dokumenty/GitHub/image_proccessing/odm.txt'
#dict_pl=make_dict(File)
#dicts,key=dicts_pl(dict_pl,String_pl)



labels10=pd.read_csv('/home/kacper/Dokumenty/GitHub/image_proccessing/result_out10.csv',sep=',',index_col=0 )
labels11=pd.read_csv('/home/kacper/Dokumenty/GitHub/image_proccessing/result_out11.csv',sep=',',index_col=0 )
labels12=pd.read_csv('/home/kacper/Dokumenty/GitHub/image_proccessing/result_out12.csv',sep=',',index_col=0 )
labels13=pd.read_csv('/home/kacper/Dokumenty/GitHub/image_proccessing/result_out13.csv',sep=',',index_col=0 )

result=pd.concat([labels10,labels11,labels12,labels13])


X=result[['type1','type2','type3','pl_1','pl_2','pl_3','words_corel','words_corel','dig_cor_12','dig_cor_23']]
y=result[['correctness']]
X=X.fillna(0)
x=X.iloc[:,:].values

from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(random_state=0)
clf.fit(x,y)
from sklearn.metrics import confusion_matrix
confusion_matrix(y,clf.predict(x))
