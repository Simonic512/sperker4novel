# -*- coding: utf-8 -*-

"""
bag of word model classify words 

author: Simon
date: 24/8/2016
"""

import jieba
import os
import re

def load_word_list(filesdir):

	wordsset = set()
	wordslist = []
	templist = []
	temdict = {}
	# 两个temp为了保留频数前10000的词
	files1 = os.listdir(filesdir)

	files = [i for i in files1 if not i.endswith('_sub') and not i.startswith('.')]

	for f in files:
		# 逐篇分词 词汇加入 set 中 最后变成 list
		seg_list = cut_file(filesdir+'/'+f)
		templist.extend(seg_list)
		for d in templist:
			if d not in temdict.keys():
				temdict[d] = 0
			else:
				temdict[d] += 1

		wordslist = [k for k,v in temdict.items() if v >= 200]

	print('the length of wordset is %d .'% len(wordslist))
	return wordslist

def bulid_bag_of_words(wordlist,file,word):

	# 三个参数，字典list 待建立词所在词袋 待建立词袋的词
	# 返回两个向量 前词词袋与后词词袋
	seg_list = cut_file(file)
	pre_list = []
	next_list = []

	for i in range(seg_list.count(word)):
		windex = seg_list.index(word)
		pre_list.append(seg_list[windex-1])
		next_list.append(seg_list[windex+1])
		seg_list.remove(word)

	def to_vec(wordlist,seg):
		length = len(wordlist)
		vec_seg = length*[0]
		for w in seg:
			if w in wordlist:
				vec_seg[wordlist.index(w)] += 1

		return vec_seg

	pre_vec = to_vec(wordlist, pre_list)
	next_vec = to_vec(wordlist, next_list)

	return pre_vec,next_vec 

def cut_file(file):

	with open('./novel/'+file) as f:
		fstr = f.read()
		fs_sub = re.sub(r'[。，“”？！《》?!\.a-zA-Z0-9/#￥$@*_]+','', fstr)
		seg_list = jieba.cut(fs_sub,cut_all=False)

	return list(seg_list)
