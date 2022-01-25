#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 08:15:05 2021

@author: kacper
"""
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
import pickle
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.model_selection import cross_val_score
import functions
import words_reading
my_pipeline = make_pipeline(SimpleImputer(), RandomForestClassifier(random_state=0))

# =============================================================================
# def make_dict(loc_File):
#     with open(loc_File, encoding='UTF8') as f:
#         lines = f.readlines()
#     dict_pl = []
#     for line in lines:
#         word=line.split()
#         dict_pl.append(word)
#  
#     return [item.replace(',','') for sublist in dict_pl for item in sublist]
# 
# 
# def check_pl(a):
#     return a in dict_pl 
# 
# 
# def dicts_pl(dict_pl,String_pl):
#     loc_dicts=[None]*len(String_pl)
#     loc_key=[None]*len(String_pl)
#     i=0
#     for ch in String_pl:
#         loc_dicts[i]=[x for x in dict_pl if x[0]==ch ]
#         loc_key[i]=ch
#         i+=1
#     return loc_dicts,loc_key
# String_pl='aąbcćdeęfghijklłmnoópqrsśtuvwxyzż AĄBCĆDEEFGHIJKLŁMNOÓPQQRSŚTUVWXYZŻ'
# File='/home/kacper/Dokumenty/GitHub/image_proccessing/odm.txt'
# dict_pl=make_dict(File)
# dicts, key=dicts_pl(dict_pl,String_pl)
# =============================================================================

result=pd.read_csv('/home/kacper/Dokumenty/GitHub/data_image_processing/text/result_out.csv',sep=',',index_col=0 )
result=result.reset_index()
result=result.fillna(0)
label=result[['0','1','2','3']].copy()


#averages=label.applymap(lambda x: functions.average_word_length(x))
#stds=label.applymap(lambda x: functions.std(x))

#words_corr_12=label.apply(lambda x: functions.similar_lett(x['1'],x['2']) ,axis=1)
#words_corr_23=label.apply(lambda x: functions.similar_lett(x['2'],x['3']) ,axis=1)
#dig_cor=label.apply(lambda x: functions.similar_dig(x['0'],x['1']) ,axis=1)

final,labels=words_reading.read_labels(label)

X=labels.iloc[:,4:].fillna(0).values 
y=result.iloc[:,5].values

scores = cross_val_score(RandomForestClassifier(random_state=0,
                                                max_depth=2,
                                                criterion='gini',
                                                min_samples_split=2,
                                                n_estimators=100), X, y,cv=5)
print(scores)

from sklearn.model_selection import GridSearchCV
grid_param = {
    'max_depth':[1,2,5,10],
    'min_samples_split':[2,3,4,5,6,7],
    'n_estimators': [100, 300, 500, 800, 1000],
    'criterion': ['gini', 'entropy'],
}

CV= GridSearchCV(estimator=RandomForestClassifier(random_state=0),
                     param_grid=grid_param,
                     cv=5,
                     n_jobs=-1)
CV.fit(X, y)
best_parameters = CV.best_params_
print(best_parameters)

RF=RandomForestClassifier(random_state=0,
                          max_depth=2,
                          criterion='gini',
                          min_samples_split=2,
                          n_estimators=100)
RF.fit(X,y)

confusion_matrix(y,RF.predict(X))

pickle.dump(RF, open('model_rf', 'wb'))

###############################################
y=RF.predict(x)
result['results']=y
result.to_csv('result_out.csv',sep=',')
