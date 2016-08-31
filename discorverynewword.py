# -*- coding: utf-8 -*-

"""
1. TF-IDF high-freq word.
2. compare high-freq word and background wordlist,discorvery the new word.
3. the new word has left and right BOW, the feature of classify.

reference: http://www.matrix67.com/blog/archives/5044
		   https://github.com/Moonshile/ChineseWordSegmentation

Author: Simon
Date: 23/8
"""

import jieba.analyse
import re


def freqword(filename):
	with open('./novel/'+filename) as f:
		textstr = f.read()
		tst = re.sub(r'[。，“”？！《》?!\.a-zA-Z0-9/#￥$@*_]+', '', textstr)
		freqlist = jieba.analyse.extract_tags(tst, topK=8, withWeight=False, allowPOS=())

	return freqlist


# def load_dict():
# 	word_list = []
# 	# word_list 是背景字典
# 	with open('Dict.txt') as d:
# 		for word in d.readlines():
# 			w = word.strip().split('|')
# 			if len(w[0]) >1:
# 				word_list.append(w[0])

# 	return word_list

def dis_new_word(filename,wordlist):

	# word_list = load_dict()
	freq_list = freqword(filename)
	new_word_list = [w for w in freq_list if w not in wordlist]

	#  需要把ABC型中AB/BC 去掉
	l2 = [i for i in new_word_list if len(i) == 2]
	l3 = [i for i in new_word_list if len(i) != 2]

	for i in l2:
		for j in l3:
			if i in j and i in new_word_list:
				new_word_list.remove(i)

	return new_word_list


	# 这里判断一下是否人名
