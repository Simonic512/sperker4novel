# -*- coding : utf-8 -*-

import re
import os
import jieba
import jieba.analyse
import sklearn
from sklearn.ensemble import RandomForestClassifier

import dealnovel
import discorverynewword
import tran
import bagofwords

#if '__name__' == '__main__':

def main():

	wls = dealnovel.load_all_text_dict(500)
	wll = dealnovel.load_all_text_dict(200)
	print('wordlist complete!')

	classifier = tran.classify(wls, 'labels2')
	print('classifier complete!')


	dealnovel.dealdir('./novel',wls,classifier)