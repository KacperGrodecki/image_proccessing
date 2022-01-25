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
import re
# import matplotlib.pyplot as plt
path = '/home/kacper/Dokumenty/GitHub/image_proccessing/'        
# from tkinter.filedialog import askopenfilename
# from skimage import io, color, morphology
# import pickle
# import functions
# import words_reading
from os import listdir
from os.path import isfile, join
# import gc
# import sys
#import os,psutil
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
File='/home/kacper/Dokumenty/GitHub/image_proccessing/lib/odm.txt'

dict_pl=make_dict(File)
global dicts
global key
dicts, key=dicts_pl(dict_pl,String_pl)


class ImageProcessing:
    def __init__(self):
        print('Constructor called Image Processing')
        pass

    def __del__(self):
        print('Destructor called Image Processing')
        pass

    def fig_prepare(self, file):
        img = cv2.imread(file, 0)
        lower_blue = np.array([0])
        upper_blue = np.array([120])
        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(img, lower_blue, upper_blue)
        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(img, img, mask=mask)

        res[mask == 0] = [255]
        board = int(res.shape[1] * 0.01)
        res[:, :board] = 255
        res[:, -board:] = 255
        return res

    def countrurs(self, gray, ythresh):
        thresh = 255 - gray
        # use morphology erode to blur horizontally
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (151, 3))
        morph = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel)

        # use morphology open to remove thin lines from dotted lines
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 17))
        morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)

        # find contours
        cntrs = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cntrs = cntrs[0] if len(cntrs) == 2 else cntrs[1]

        # find the topmost box

        for c in cntrs:
            box = cv2.boundingRect(c)
            x, y, w, h = box
            if y < ythresh:
                topbox = box
                ythresh = y
        return cntrs[::-1], topbox

    # loading contours
    def find_contours(self, file):
        print('find contours ')
        # file=path+file+'.jpg'
        image = file
        # gray=self.fig_prepare(image)

        # image = cv2.imread(file)
        result = image.copy()
        ythresh = 1000
        cntrs, topbox = self.countrurs(image, ythresh)
        i = 0
        images = []
        xywh = []
        for c in cntrs:
            box = cv2.boundingRect(c)
            if box != topbox:
                i = i + 1
                x, y, w, h = box

                xywh.append([x, y, w, h])

                cv2.rectangle(result, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cropped = image[y:y + h, x:x + w]

                # mask,mask1 = self.mask_from_cropped(cropped)
                board = 50
                cropped_board = cv2.copyMakeBorder(cropped, board, board, board, board, cv2.BORDER_CONSTANT,
                                                   value=[255, 255, 255])
                # mask = cv2.copyMakeBorder( mask, board, board, board, board, cv2.BORDER_CONSTANT,value=[255, 255, 255])
                # mask1 = cv2.copyMakeBorder( mask1, board, board, board, board, cv2.BORDER_CONSTANT,value=[255, 255, 255])

                images.append(cropped_board)
        return images, xywh

class Run():

    def __init__(self):
        print('start')
        self.countter = 0
        self.countter1 = 0
        self.labels = []
        self.xywh = []
        self.xywh1 = []
        #path on the local pc
        self.path = '/home/kacper/Dokumenty/GitHub/data_image_processing/res500_1/'
        self.files = [f for f in listdir(self.path) if isfile(join(self.path, f))]
        self.files.sort()
        self.contours = 0

        #self.open_file()
    def setNumber(self,i):
        self.file_nr = i

    def open_file(self):
        print('opening file')
        self.file = self.path + self.files[self.file_nr]
        print(self.file)
        self.find_contour()

    def find_contour(self):
        print('find_contours')
        print('figure preprocessing')
        fig_prepared = ImageProcessing.fig_prepare(self, self.file)
        print('figure prepered')
        print('find contours')
        self.contours, self.xywh = ImageProcessing.find_contours(self, fig_prepared)
        print('contours number', len(self.contours))

        self.read_text()

    def read_text(self):
        print('read text')
        print('self.countter', self.countter)
        print('self.contours[0] typ', type(self.contours[0]))

        cropped_board = self.contours[self.countter]
        if self.countter == 0:
            self.labels.append([self.file, self.file_nr])
        self.analyze_figures(cropped_board)

        self.next_contour()

    def next_contour(self):
        print('next contour')
        print('self.countter', self.countter)
        print(len(self.labels))

        if self.countter > len(self.contours) - 2:
            print('finish')

            print('labels ', np.array(self.labels).shape)
            self.labels.append([self.file, self.file_nr])

            print('file number ', str(self.file))
            print('df construction ', pd.DataFrame(np.array(self.labels)).shape)
            df_labels = pd.DataFrame(np.array(self.labels))
            print('save', '/home/kacper/Dokumenty/GitHub/data_image_processing/text4/' + str(
                self.files[self.file_nr]) + 'new.csv')
            df_labels.to_csv('/home/kacper/Dokumenty/GitHub/data_image_processing/text4/' + str(
                self.files[self.file_nr]) + 'new.csv', sep=',')

            self.file_nr += 1
            self.countter = 0
            self.countter1 = 0
            return 0

        self.countter += 1
        self.read_text()

    def analyze_figures(self, cropped_board):
        print('analyze figures')
        # crop = Image.fromarray(cropped_board)

        try:
            let_crop = image_to_string(cropped_board, lang='pol', config='--psm 7 --oem 3')
        except:
            let_crop = ''

        try:
            div_crop = image_to_string(cropped_board, lang='pol', config='--psm 6 --oem 3')
        except:
            let_crop = ''

        if re.search('[a-zA-Z]', let_crop) or re.search('[a-zA-Z]', div_crop):

            dig_crop = image_to_string(cropped_board, lang='pol',
                                       config='--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789')  # r'--oem 3 --psm 3 outputbase digits'
            # let_board=image_to_string(cropped_board, lang='pol',config = '--psm 13 --oem3')

            # plt.imshow(crop)
            # plt.show()
            print('\n\n\n')
            print(let_crop, ' ', dig_crop, ' ', div_crop)

            # input('Press Enter to countinue')

            self.labels.append([let_crop, div_crop])

            self.countter1 += 1

        else:
            pass

    # def model(self):
    #     print('model')
    #     label = pd.DataFrame(self.labels, columns=['0', '1', '2', '3'])
    #     print('columns', label.columns)
    #     print('columns', label.head())
    #     # clf=pickle.load(open('model', 'rb'))
    #     # print(labels.shape)

    #     averages = label.applymap(lambda x: functions.average_word_length(x))
    #     stds = label.applymap(lambda x: functions.std(x))
    #     long = label.apply(lambda x: functions.longest(x['1']), axis=1)
    #     words_corr_12 = label.apply(lambda x: functions.similar_lett(x['1'], x['2']), axis=1)
    #     words_corr_23 = label.apply(lambda x: functions.similar_lett(x['2'], x['3']), axis=1)
    #     dig_cor = label.apply(lambda x: functions.similar_dig(x['0'], x['1']), axis=1)
    #     frames = [averages, stds, long, words_corr_12, words_corr_23, dig_cor]
    #     print('x done')

    #     labels = label
    #     labels = words_reading.read_labels(labels, dict_pl, dicts, key)
    #     # if self.file_nr%10==1:
    #     #     #zapis do pliku, reset pamięci i od nowa
    #     #     labels.to_csv('result_out_'+str(self.file_nr)+'.csv')
    #     print('model end')

# def opening(self,choosen_file):
#     print('opening',choosen_file)
#     file=self.path+self.files[choosen_file]
#     return file

#  def __exit__(self,exc_type,exc_value_traceback):
#      pass
# def clear_variables(self):
ImageProcessing=ImageProcessing()
Run=Run()

for i in range(0,400):
    print('-------------------------',i,'--------------------------')
    #ImageProcessing
    Run.setNumber(i)
