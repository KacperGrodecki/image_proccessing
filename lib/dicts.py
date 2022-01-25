#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 14:23:32 2021

@author: kacper
"""

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

String_pl='aąbcćdeęfghijklłmnoópqrsśtuvwxyzż AĄBCĆDEEFGHIJKLŁMNOÓPQQRSŚTUVWXYZŻ'
File='/home/kacper/Dokumenty/GitHub/image_proccessing/odm.txt'

dict_pl=make_dict(File)
dicts, key=dicts_pl(dict_pl,String_pl)
