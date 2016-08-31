# -*- coding: utf-8 -*-
"""
tran classifier.
random forest.

author: Simon
date: 24/8/2016
"""
import bagofwords
#from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier

def input_word_list(wordlist,tranfile):
	# wordlist = ll
	feature_list = []
	label_list = []

	with open(tranfile) as f:
		for line in f.readlines():
			ll = line.strip().split(',')
			feature1,feature2 = bagofwords.bulid_bag_of_words(wordlist,ll[0],ll[1])
			feature1.extend(feature2)
			feature_list.append(feature1)
			label_list.append(ll[-1])

	return feature_list,label_list

def input_word(wordlist,file,word):
	feature_list = []

	feature1,feature2 = bagofwords.bulid_bag_of_words(wordlist,file,word)
	feature1.extend(feature2)
	feature_list.append(feature1)

	return feature_list


def classify(wordlist,tranfile):

	f,l = input_word_list(wordlist,tranfile)
	#classifier = GaussianNB().fit(f,l)
	classifier = RandomForestClassifier().fit(f,l)

	#classifier.predict()

	return classifier


#def classifywords(wordlist,file,word):

