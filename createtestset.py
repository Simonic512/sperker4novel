# -*- coding: utf-8 -*-

import os
import discorverynewword

def createtestset(dir,wordlist):

	labellist = []
	files1 = os.listdir(dir)

	files = [i for i in files1 if not i.startswith('.') and not i.startswith('__')]

	for f in files:
		
		words = discorverynewword.dis_new_word(f, wordlist)

		for word in words:
			label = input(f+','+word+',')
			labellist.append([f,word,label])

	with open('labels2','w') as f:
		f.writelines(labellist)