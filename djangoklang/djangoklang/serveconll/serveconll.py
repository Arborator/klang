#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
import sys
import os
import glob, re


def allconlls(path="corpussamples"):
	files = glob.glob(os.path.join('djangoklang',
                                'serveconll', path, '**', '*.conll'), recursive=True)
	print('allconlls', files)
	# for filename in files:
	# 	print(filename)
	# return sorted([{'fullname':f, 'basename':os.path.basename(f)} for f in files])
	return sorted([f.replace('djangoklang/serveconll/corpussamples/','').split('/')[0] for f in files])
	# return sorted(files)

def getconll(name):
	# treg = re.compile(r'^\d+\t([\w.,!"\'\-\?\:]+)\t')
	treg = re.compile(r'^\d+\t(.+?)\t.*AlignBegin=(\d+).*AlignEnd=(\d+)')
	t = open(os.path.join('djangoklang/serveconll/corpussamples/', name, name+'.intervals.conll')).read()
	arr = [ ]
	for co in t.split('\n\n'):
		if co:
			sent=[ ]
			for li in co.strip().split('\n'):
				if li and li[0] != '#':
					m = treg.search(li)
					sent += [(m.group(1), int(m.group(2)), int(m.group(3)))]
			arr+=[sent]
			
	# print(arr)
	return arr
	# return [[str(treg.search(li).group(1)) for li in co.split('\n') if li and li[0] != '#'] for co in t.split('\n\n') if co]
