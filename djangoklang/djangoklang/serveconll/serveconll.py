#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
import sys
import os
import glob, re, random, copy


def allconlls(path="corpussamples"):
	files = glob.glob(os.path.join('djangoklang',
                                'serveconll', path, '**', '*.conll'), recursive=True)
	print('allconlls', files)
	# for filename in files:
	# 	print(filename)
	# return sorted([{'fullname':f, 'basename':os.path.basename(f)} for f in files])
	return sorted([f.replace('djangoklang/serveconll/corpussamples/','').split('/')[0] for f in files])
	# return sorted(files)

def getconll(name, isadmin):
	# treg = re.compile(r'^\d+\t([\w.,!"\'\-\?\:]+)\t')
	treg = re.compile(r'^\d+\t(.+?)\t.*AlignBegin=(\d+).*AlignEnd=(\d+)')
	t = open(os.path.join('djangoklang/serveconll/corpussamples/', name, name+'.intervals.conll')).read()
	arr = [ ]
	ws = [] # all tokens
	for co in t.split('\n\n'):
		if co:
			sent=[ ]
			for li in co.strip().split('\n'):
				if li and li[0] != '#':
					m = treg.search(li)
					w = m.group(1)
					sent += [(w, int(m.group(2)), int(m.group(3)))]
					ws += [w]
			arr+=[sent]
			
	# print(arr)
	if isadmin: # just to produce some random data. later this should give the saved transcriptions of all the users for the given sample!
		si = random.randrange(len(arr))
		print("random line:", si, random.choice(ws), random.choice(ws))
		arrcopy1 = copy.deepcopy(arr)
		arrcopy1[si] = [("test"+str(i), mi, ma)
                  for i, (w, mi, ma) in enumerate(arrcopy1[si])]
		arrcopy2 = copy.deepcopy(arr)
		ti = random.randrange(len(arrcopy2[si]))
		print('avant', arrcopy2[si][ti])
		arrcopy2[si][ti] = (random.choice(ws), arrcopy2[si][ti][1], arrcopy2[si][ti][2])
		print('après', arrcopy2[si][ti])
		si = random.randrange(len(arr))
		ti = random.randrange(len(arrcopy2[si]))
		arrcopy2[si][ti] = (random.choice(ws), arrcopy2[si][ti][1], arrcopy2[si][ti][2])
		
		# arrcopy2[si] = [(random.choice(ws), mi, ma) for (w, mi, ma) in arrcopy2[si]]

		return {'original': arr, 'randomuser': arrcopy1, 'anotherrandomuser': arrcopy2}
	else:
		return {'original': arr}
	# return [[str(treg.search(li).group(1)) for li in co.split('\n') if li and li[0] != '#'] for co in t.split('\n\n') if co]
