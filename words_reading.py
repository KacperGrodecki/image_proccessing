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
    first_letter=key.index(a[0])
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
       
String_pl='aąbcćdeęfghijklłmnoópqrsśtuvwxyzż AĄBCĆDEEFGHIJKLŁMNOÓPQQRSŚTUVWXYZŻ'
File='/home/kacper/Dokumenty/GitHub/image_proccessing/odm.txt'
#dict_pl=make_dict(File)
#dicts,key=dicts_pl(dict_pl,String_pl)


def read_labels():
    labels=pd.read_csv('/home/kacper/Dokumenty/GitHub/image_proccessing/result.csv',sep=',',index_col=0 )
    
    labels['type1']=labels['1'].apply(char_type_word)
    labels['type2']=labels['2'].apply(char_type_word)
    labels['type3']=labels['3'].apply(char_type_word)
    
    labels['pl_1']=labels['1'].apply(check_string_pl)
    labels['pl_2']=labels['2'].apply(check_string_pl)
    labels['pl_3']=labels['3'].apply(check_string_pl)
    
    labels['words_corel']=labels.apply(lambda x: similar_lett(x['1'],x['2']) ,axis=1)
    labels['words_corel1']=labels.apply(lambda x: similar_lett(x['2'],x['3']) ,axis=1)
    labels['dig_cor_12']=labels.apply(lambda x: similar_dig(x['1'],x['2']) ,axis=1)
    labels['dig_cor_23']=labels.apply(lambda x: similar_dig(x['2'],x['3']) ,axis=1)
    
    labels.loc[labels['words_corel']>0.9,'final']=labels['2']
    labels.loc[labels['words_corel1']>0.9,'final']=labels['3']
  
    labels['Max']=labels[['pl_1','pl_2','pl_3']].idxmax(axis=1).apply(lambda x: x[-1]).values
    
    labels['final']=np.select([labels.Max=='1',labels.Max=='2',labels.Max=='3'],[labels['1'],labels['2'],labels['3']])
    #type1 lub 2 lub 3
    labels.loc[(labels['dig_cor_12']>0.9) & ((labels['type1']!=None) &(labels['type2']<0.5)),'final']=labels['1']
    labels.loc[(labels['dig_cor_23']>0.9) & ((labels['type2']!=None) &(labels['type2']<0.5)),'final']=labels['2']
    
    return labels

result=read_labels()

result.to_csv('result_out.csv')



