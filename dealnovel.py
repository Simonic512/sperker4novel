# -*- coding:<utf-8> -*-

"""
baseline
import discorverynewword & tranclassify

author: Simon
date : 29/8/2016
rebuild the dealnovel

"""

import re
import os
import jieba
import jieba.posseg as pseg
import jieba.analyse

import discorverynewword
import tran

def load_all_text_dict(freq):

	all_text_dict = []
	# all_text_dict 有两个作用，一是分类所需要的特征向量的网格，二是TF-IDF过滤的背景词典
	with open('dict.txt') as d:
		for word in d.readlines():
			w = word.strip().split(' ')
			if int(w[1]) > freq:
				all_text_dict.append(w[0])
		all_text_dict.append(' ')
		# 字典里加上 \space

	return all_text_dict

def dealdir(dir,wl,classifier):
	# 处理当前目录下除了.DS的所有_sub文件
	countr = 0
	countf = 0

	files_temp = os.listdir(dir)

	files = [i for i in files_temp if i.endswith('_sub') and not i.startswith('.')]

	for f in files:
		r,f = label(f,wl,classifier)
		countr = countr + r
		countf = countf + f
	
	print('the blocks and the right blocks: '(countf+countr),countr)
	print('the rate of successful is: %f'%(countr/(countr+countf)))


def label(file,wordlist,classifier):

	lf = []
	namelist4text = []
	#keyword(file)
	countr = 0
	countf = 0

	list4nn = discorverynewword.dis_new_word(file,wordlist)
	
	for inn in list4nn:
		pred = classifier.predict(tran.input_word(wordlist,file,inn))

		if int(pred[0]) != 0:
			namelist4text.append(inn)
	#namelist4text = list4nn
	for inn in namelist4text:
		jieba.add_word(inn, freq=1000, tag='nn')
	with open('./novel/'+file) as f:
		str4text = f.read()
		# 以两个回车为一个block进行分割
		ls4block = str4text.strip().split('\n\n')

		for block in ls4block:
			lb = dealblock(file,block,wordlist,namelist4text)
			lf.append(lb)
			# 每个 ls 是一个block
			# 打印输出 file 结果
	with open('./result/label_'+file,'w') as f:
		for each in lf:
			f.write('\n')
			if each != -1:
				countr += 1
				for r in each:
					f.write(r+'\n')
			else:
				countf += 1
	

	for inn in namelist4text:
		jieba.del_word(inn)
		print('delete word ' +inn+' successful!')

	print(str(countr+countf)+' blocks complete!')

	return countr,countf

def dealblock(file,block,worddict,namelist4text):
	# 处理每个block
	# 给每个 block 传一个 text_name_list 对于查不到的 在这个list里分配 
	list4block = []
	#global count = 0

	#pattern = re.compile(r'“.*”')
	p = re.compile(r'(.*“)(.*?)(”.*)')

	senlist = block.split('\n')

	senlen = len(senlist)
	
	bnl1 = [' ']*senlen
	bnl2 = [' ']*senlen
	bnl3 = [' ']*senlen

	# bnl1 句子前后拆分出的人名
	# bnl2 隔句人名
	# bnl3 对话中拆分出的人名，给前一句和后一句
	def dealsingle(sencount,ss):
		# 搜索前文
		if sencount > 1:
			if bnl1[sencount] == ' ' and bnl1[sencount-2] != ' ':
				bnl2[sencount] = bnl1[sencount-2] 
			elif bnl1[sencount] == ' ' and bnl2[sencount-2] != ' ':
				bnl2[sencount] = bnl2[sencount-2] 

			#else:
				#bnl3[sencount] = namelist4text[0]
		#else:
			#if bnl3[sencount] == ' ':
				#bnl3[sencount] = namelist4text[0]

		words2 = pseg.cut(ss)
		# 如果对话中有人名，那么把对话中的人名加入到前后文的 bnl3 中
		for k,v in words2:
			if k in namelist4text and sencount >= 1 and sencount < senlen-1:
				bnl3[sencount+1] = k
				bnl3[sencount-1] = k

	def dealright(text,sencount,ss):

		words1 = pseg.cut(text)
	
		for k,v in words1:
			if k in namelist4text :
				bnl1[sencount] = k
				if sencount > 1 and bnl2[sencount-2] == ' ':
					bnl2[sencount-2] = k
				break
			elif v == 'nr':
				bnl2[sencount] = k
				if sencount > 1 and bnl2[sencount-2] == ' ':
					bnl2[sencount-2] = k
				break
				#count += 1
			#elif v == 'nr':
			 	#bnl2[sencount] = k
		if sencount > 1:
			if bnl1[sencount] == ' ' and bnl1[sencount-2] != ' ':
				bnl2[sencount] = bnl1[sencount-2] 
			elif bnl1[sencount] == ' ' and bnl2[sencount-2] != ' ':
				bnl2[sencount] = bnl2[sencount-2] 


			 	#count += 1

		words2 = pseg.cut(ss)
		# 如果对话中有人名，那么把对话中的人名加入到前后文的 bnl3 中
		for k,v in words2:
			if k in namelist4text and sencount >= 1 and sencount < senlen-1:
				bnl3[sencount+1] = k
				bnl3[sencount-1] = k

		# 按照词性找人名
		# 没有人名找 nn 
		# 再没有就认为是上一个人说的

	def dealleft(text,sencount,ss):

		words = pseg.cut(text)

		for k,v in words:
			if k in namelist4text :
				bnl1[sencount] = k
				if sencount > 1 and bnl2[sencount-2] == ' ':
					bnl2[sencount-2] = k
				break
			elif v == 'nr':
				bnl2[sencount] = k
				if sencount > 1 and bnl2[sencount-2] == ' ':
					bnl2[sencount-2] = k
				break
				#count += 1
			#elif v == 'nr':
			 	#bnl2[sencount] = k
			 	#count += 1
		if sencount > 1:
			if bnl1[sencount] == ' ' and bnl1[sencount-2] != ' ':
				bnl2[sencount] = bnl1[sencount-2] 
			elif bnl1[sencount] == ' ' and bnl2[sencount-2] != ' ':
				bnl2[sencount] = bnl2[sencount-2] 


		words2 = pseg.cut(ss)
		# 如果对话中有人名，那么把对话中的人名加入到前后文的 bnl3 中
		for k,v in words2:
			if k in namelist4text and sencount >= 1 and sencount < senlen-1:
				bnl3[sencount+1] = k
				bnl3[sencount-1] = k

	def dealmedium(text,sencount,ss):
		# dealmedium 和 dealright暂时一样 需要细化
	
		words = pseg.cut(text)

		for k,v in words:
			if k in namelist4text :
				bnl1[sencount] = k
				if sencount > 1 and bnl2[sencount-2] == ' ':
					bnl2[sencount-2] = k
				break
				#count += 1
			#elif v == 'nr':
			 	#bnl2[sencount] = k
			elif v == 'nr':
				bnl2[sencount] = k
				if sencount > 1 and bnl2[sencount-2] == ' ':
					bnl2[sencount-2] = k
				break

		if sencount > 1:
			if bnl1[sencount] == ' ' and bnl1[sencount-2] != ' ':
				bnl2[sencount] = bnl1[sencount-2] 
			elif bnl1[sencount] == ' ' and bnl2[sencount-2] != ' ':
				bnl2[sencount] = bnl2[sencount-2] 

			 	#count += 1

		words2 = pseg.cut(ss)
		# 如果对话中有人名，那么把对话中的人名加入到前后文的 bnl3 中
		for k,v in words2:
			if k in namelist4text and sencount >= 1 and sencount < senlen-1:
				bnl3[sencount+1] = k
				bnl3[sencount-1] = k

	sencount = -1

	for sen in senlist:

		m = p.match(sen)

		if m:

			pss = m.group(1).strip('“')
			ss = m.group(2)
			nss = m.group(3).strip('”')

			sencount += 1

			
			if pss == '' and nss == '':
				dealsingle(sencount,ss)
				#print(1)

			elif pss != '' and nss == '':
				dealright(pss.strip(),sencount,ss) 
				#print(2)
					
			elif pss == '' and nss != '':
				dealleft(nss.strip(),sencount,ss)
				#print(3)

			else:
				dealmedium(pss,sencount,ss)
				#print(4)
	# 在这里将 nl1 2 3 合成一个 list4block
	# for i in range(senlen):
	# 	if bnl1[i] != ' ':
	# 		list4block[i] = bnl1[i]
	# 	elif bnl2[i] != ' ':
	# 		list4block[i] = bnl2[i]
	# 	elif bnl3[i] != ' ':
	# 		list4block[i] = bnl3[i]
	# 	else :
	# 		list4block[i] = ''
	for w in bnl2:
		if w != ' ':
			bnl3[bnl2.index(w)] = w

	for w in bnl1:
		if w != ' ':
			bnl3[bnl1.index(w)] = w

	#if count >= 2:
		# 格式化输
	#else:
		#nlist = dealalltext(file,senlist,worddict)
		
		#return nlist
	count1 = 0
	for b in bnl3:
		if b != ' ':
			count1 += 1
	if count1+2 < senlen:
		for i in bnl3:
			if i != ' ':
				if bnl3.index(i) % 2 == 0:
					for j in range(senlen)[::2]:
						if bnl3[j] == ' ':
							bnl3[j] = i
				elif bnl3.index(i) % 2 == 1:
					for j in range(senlen-1)[::2]:
						if bnl3[j+1] == ' ':
							bnl3[j+1] = i

	count2 = 0
	lss = []
	for b in bnl3:
		if b != ' ':
			count2 += 1
			lss.append(b)

	if count2 <= senlen*0.5:

		if len(namelist4text) > 1:
			if count2 == 0:
				for i in range(senlen):
					if i % 2 == 0:
						bnl3[i] = namelist4text[0]
					else:
						bnl3[i] = namelist4text[1]

			elif count2 == 1:
				if lss[0] == namelist4text[0]:
					if bnl3.index(lss[0]) % 2 == 0:
						for i in range(senlen):
							if i % 2 == 0:
								bnl3[i] = lss[0]
							else:
								bnl3[i] = namelist4text[1]
					else:
						for i in range(senlen):
							if i % 2 == 1:
								bnl3[i] = lss[0]
							else:
								bnl3[i] = namelist4text[1]
				else:
					if bnl3.index(lss[0]) % 2 == 0:
						for i in range(senlen):
							if i % 2 == 0:
								bnl3[i] = lss[0]
							else:
								bnl3[i] = namelist4text[0]
					else:
						for i in range(senlen):
							if i % 2 == 1:
								bnl3[i] = lss[0]
							else:
								bnl3[i] = namelist4text[0]
	
	nlist = []

	for i in range(senlen):
		nlist.append(bnl3[i]+'\t\t'+senlist[i])

	return nlist



def dealalltext(file,senlist,bnl,namelist4text):

	comfilename = file.strip('_sub')

	clist = []

	if len(nl) == 1:
		for i in range(len(senlist)):
			clist.append(nl[0]+'\t\t'+senlist[i])

	else:
		if len(senlist)%2 == 0:
			for i in range(len(senlist))[::2]:
				clist.append(nl[0]+'\t\t'+senlist[i])
				clist.append(nl[1]+'\t\t'+senlist[i+1])
		else:
			for i in range(len(senlist)-1)[::2]:
				clist.append(nl[0]+'\t\t'+senlist[i])
				clist.append(nl[1]+'\t\t'+senlist[i+1])


	return clist