#!/usr/bin/python
# -*- coding: utf-8 -*-

####
# Copyright (C) 2014 Kim Gerdes
# kim AT gerdes. fr
# http://arborator.ilpga.fr/
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of version 3 of the GNU Affero General Public License (the "License")
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This script is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE
# See the GNU General Public License (www.gnu.org) for more details.
#
# You can retrieve a copy of of version 3 of the GNU Affero General Public License
# from http://www.gnu.org/licenses/agpl-3.0.html 
# For a copy via US Mail, write to the
#     Free Software Foundation, Inc.
#     59 Temple Place - Suite 330,
#     Boston, MA  02111-1307
#     USA
####

import sys, json, codecs, copy, collections, re, hashlib, os, glob, subprocess, fnmatch
import io
#import zipfile
from shutil import copyfile

from datetime import datetime
#import config, xmlsqlite, traceback
#from parseSentences import textToSentences

debug=True

verbose=False
#verbose=True


#print codecs.open("textgrids/Chloe Guyard_23953_assignsubmission_file_guyard2411.TextGrid","r","utf-16").read()






requotes=re.compile(r'\"(.*)\"$',re.U)
rexmin=re.compile(r'\s*xmin = (.*)$',re.U+re.M)
rexmax=re.compile(r'\s*xmax = (.*)$',re.U+re.M)
#reinvers=re.compile('(-je|-tu|-t-il|-il|-elle|-t-elle|-nous|-vous|-t-ils|-ils)',re.U)

incompleteTextLine=re.compile(r'^ *text \= \"\s*\r?\n?',re.U+re.M)
lonelyQuote=re.compile(r'\s*\"\s*$',re.U+re.M)

tierseparator=re.compile(r'\s*class = ',re.U+re.M)
retiername=re.compile(r'\s+name = "(.+)"\s*\n',re.U+re.M)         
repersname=re.compile(r'_\d\d\d\d',re.U+re.M)         
	 


repoint=re.compile(r'(?<![0-9A-ZÀÈÌÒÙÁÉÍÓÚÝÂÊÎÔÛÄËÏÖÜÃÑÕÆÅÐÇØ])([.。]+)')
repointEnd=re.compile(r'([.。]+)$')
reponctWithNum=re.compile(r'(?<![0-9])(\s*[;:,!\(\)§"]+)')
#rehyph=re.compile(ur'(\s*[\/\']+)') # \- pas de segmentation des traits d'union
rehyph=re.compile(r'(\s*[\/]+)') # \- pas de segmentation des traits d'union
revirer=re.compile(r'[`]+')
redoublespace=re.compile(r'\s+',re.U)
reparenth=re.compile(r'\([ \w]*\)',re.U)

def preparetokenize(text):
	text=text.strip()
	text=text.replace("’","'")
	text=revirer.sub(r" ",text)
	text=repointEnd.sub(r" \1 ",text)
	text=repoint.sub(r" \1 ",text)
	text=reponctWithNum.sub(r" \1 ",text)
	#text=rehyph.sub(r"\1 ",text)
	return text

def textToSentences(text, outname, problemout=None, keepEndSent=False, maxlength=50, writeProblemBeforeSentence=True, includeProblemSentence=False):
	"""
	creates one sentence per line file in name outname
	"""
	#writeProblemFile=False, 
	endsent=re.compile('(?<=(?<=\w\w\s?|\s|~))([!?.]+([  ]*»+)*)',re.U) # TODO fix for xx~.
	
	#endsent=re.compile(r"(([\?\!？](?![\?\!])|((?<!\s[A-ZÀÈÌÒÙÁÉÍÓÚÝÂÊÎÔÛÄËÏÖÜÃÑÕÆÅÐÇØ])\.。！……\s)|\s\|)\s*)", re.M+re.U)
	#print 777,text
	#text=preparetokenize(text).strip()
	text=text.strip()
	#print 777,text
	
	#for sent in text.split("."):
	#if keepEndSent: 	sents = endsent.sub(ur"\1\n",u"ça va ? comment ! qsdf. oh!").split("\n")
	#else: 		sents = endsent.sub(ur"\n",u"ça va ? comment ! qsdf. oh!").split("\n")
	if keepEndSent: 	sents = endsent.sub(r"\1\n",text).split("\n")
	else: 			sents = endsent.sub(r"\n",text).split("\n")
	
	#print endsent.sub(ur"\n",u"Si je devais parler d'un événement marquant euh, je parlerais de l'année 2010. En effet je faisais de la GRS à haut niveau, j'ai commencé à l'âge de cinq ans et euh en 2010 je faisais partie euh d'une équipe de cinq. Comment va le P.S.G. ? Et tout le reste ? pas trop mal !").split("\n")
	#qsdf
	
	sents=[s for s in sents if s.strip()]
	#print sents
	if problemout: longfile = codecs.open(problemout,"w","utf-8")
	
	with codecs.open(outname,"w","utf-8") as courtfile:
		
		for sent in sents:
			sent=preparetokenize(sent)
			sent=redoublespace.sub(" ",sent)
			sent=reparenth.sub(" ",sent).strip()
			
			sent=sent.replace("aujourd' hui","aujourd'hui")
			sent=sent.replace("quelqu' un","quelqu'un")
			
			#sent=sent.replace("parce qu","parce_qu")
			#sent=reinvers.sub(ur" \1",sent)
			
			
			if sent:
				if problemout: longfile.write(sent+"\n") # +" .\n"
				if keepEndSent: simp = sent
				else:		simp=reponct.sub(" ",sent)
				simp=redoublespace.sub(" ",simp).strip()
				if not maxlength or len(simp.split())<maxlength:
					courtfile.write(simp+"\n")
				else:
					#pass
					#courtfile.write(u"_______________phrase très longue:\n")
					print("_______________phrase très longue:")
					print(simp)
					#if writeProblemFile:
						#with codecs.open("sentences/"+simplename+".problem.txt","a","utf-8") as probfile:
							#probfile.write(u"_______________phrase très longue:\n"+simp+" \n")
					if includeProblemSentence:
						if writeProblemBeforeSentence:
							courtfile.write("long ! ")
						courtfile.write(simp+"\n")
	return sents					


def intervals2conll(intervals, outname, soundfile):
	"""
	produces an empty conll text that contains only tokens and AlignBegin and AlignEnd
	from intervals (a list of triples xmin, xmax, text)
	"""
	allconll = "" 
	try: basename = os.path.basename(outname)
	except: basename = outname
	scount=1
	for xmin, xmax, text in intervals:
		
		if not text.strip(): continue
		conll = "# sent_id = "+basename+"__"+str(scount)+'\n'
		conll += "# text = "+text+'\n'
		conll += "# sound_url = "+soundfile+'\n'
		#conll += "# minmax = "+xmin+" "+xmax+'\n'
		
		text=preparetokenize(text)
		text=redoublespace.sub(" ",text)
		text=reparenth.sub(" ",text).strip()
		text=text.replace("aujourd' hui","aujourd'hui")
		text=text.replace("quelqu' un","quelqu'un")
		toks=text.split()
		realtoks = [t for t in toks if re.search(r'\w',t)]
		if not realtoks: continue
		msecs = 1000*(float(xmax)-float(xmin))/len(realtoks)
		start = 1000*float(xmin)
		for i,t in enumerate(toks):
			if re.search(r'\w',t): end = start+msecs
			conll += '\t'.join([str(i+1),t,t,'_','_','_','_','_','_','AlignBegin={xmin}|AlignEnd={xmax}'.format(xmin=round(start),xmax=round(end))])+'\n'
			start=end
		scount+=1
		allconll += conll+'\n'
	return allconll

def intervals2conllfile(intervals, outname, soundfile):
	open(outname, 'w').write(intervals2conll(intervals, outname, soundfile))
	

def newtranscription(inconll, transcriptions, samplename, soundfile):
	"""
	uses the time delimitations of inconll to construct a new conll text
	inconll: name of conll file to take as the base
	transcriptions: list of texts
	the number of trees in inconll has to be equal to the number of transcriptions
	samplename: used for constructing the sent_id (sent_id = samplename+"__"+ sentence number)
	soundfile: what is supposed to appear behind sound_url = 
	"""
	conlls = open(inconll).read().strip().split('\n\n')
	if len(conlls) != len(transcriptions): raise Exception
	treg = re.compile(r'^\d+\t(.+?)\t.*AlignBegin=(\d+).*AlignEnd=(\d+)')
	intervals = []
	for co, tr in zip(conlls,transcriptions):
		sent = []
		for li in co.strip().split('\n'):
			if li and li[0] != '#':
				m = treg.search(li)
				w = m.group(1)
				sent += [(w, int(m.group(2)), int(m.group(3)))]
				
		intervals += [(sent[0][1], sent[-1][2], tr)]
	return intervals2conll(intervals, samplename, soundfile)


def test_newtranscription():
	inconll ="/media/kim/schnell/klang/datapreparation/corpussamples/Radya_Laichour/Radya_Laichour.intervals.conll"
	nrsent = len(open(inconll).read().strip().split('\n\n'))
	transcriptions = ['blah blah blah' for i in range(nrsent)]
	print(newtranscription(inconll, transcriptions, 'testsample', 'https://test.mp3'))



# test_newtranscription()
# qsdf

def textgridToSentences(filter="*textgrid*", keepEndSent=True, maxlength=100, writeProblemBeforeSentence=False, skipBefore=None, infolder='textgrids'):
	
	skipnext=False
	skiptier=False
	textgridstodo = []
	if infolder[-1]=='/':infolder=infolder[:-1]
	#for infilename in glob.glob(os.path.join("textgrids", filter)):
	for root, dirnames, filenames in os.walk(infolder):
		#for filename in fnmatch.filter(filenames, filter):
		#print('*')
		for filename in [fn for fn in filenames if 'textgrid' in fn.lower()]:
			print('root',root)
			
			#print(soundfile)
			#open(soundfile,'rb').read()
			#sqdf
			infilename=os.path.join(root, filename)
			print('...',infilename)
			
			#print datetime.fromtimestamp(os.path.getmtime(infilename)) 
			if skipBefore and str( datetime.fromtimestamp(os.path.getmtime(infilename))) < skipBefore: 
				print(infilename,"too old")
				continue
			if '__MACOSX' in infilename:
				continue
			guessedname = repersname.split(infilename[len(infolder)+1:])[0].replace(" ","_") 
			print('guessedname',guessedname)
			
			soundfile=None
			for sroot, sdirnames, sfilenames in os.walk(root):
				#for filename in fnmatch.filter(filenames, filter):
				#print('*')
				for sfilename in [sfn for sfn in sfilenames if '.wav' in sfn.lower() or '.mp3' in sfn.lower()]:
					soundfile=os.path.join(sroot, sfilename) 
			
			
			textgridstodo += [(infilename,guessedname,soundfile)]
	print(len(textgridstodo),"textgrids found")
	#input('continue?')
	#rename = re.compile(".*[/ ](\w*)_\d\d\d\d\d\d_assignsubmission.*", re.U)
	#rename = re.compile(r".*/([ \w\-]+)_\d\d\d\d\d\d_assignsubmission.*", re.U)
	rename = re.compile(r".*/([ \w\-]+)_.*", re.U)
	
	stats = {}
	
	totalsentences = 0
	totaltokens = 0
	
	for f,g,soundfile in textgridstodo:		
		print("\n\n\n\n_______________________________________________________",g,f) #,root, dirnames, filenames
		#simplename = f.split("/")[1].split("_")[0].replace(" ","_") 
		m = rename.match(f)
		if not m:
			print("========== couldn't find name in",f)
			continue
		simplename = m.group(1).replace(" ","_") 
		print("\n\n------------------->",simplename)
		#print f
		
		problem=True
		for enc in ["utf-8","utf-16","iso-8859-1"]:
			try:
				alltext=codecs.open(f,"r",enc).read()
				#print enc
				problem=False
				break
			except Exception as e: 
				pass
				#print str(e)
		
		if problem:
			print("---------------- can't decode",f)
			break
		else:
			nbtiers=alltext.count('class = "IntervalTier"')
			if nbtiers!=1:
				print("the file",simplename,"has",nbtiers,"tiers!")
		with codecs.open(f,"r",enc) as infile:
			#c=infile.read()
			#print c
			#continue
			defaultcounter=1
			texts={}
			intervals={}
			first=infile.readline().strip()
			if first and ord(first[0])==65279: first=first[1:] # fucking boms!
			
			if first.startswith("File type") or '"IntervalTier"' in alltext:
				#print "reading textgrid",simplename
				
				intext=infile.read()
				
				intext = incompleteTextLine.sub('  text = "', intext) # remove new line after incompleteTextLine
				intext = lonelyQuote.sub('"', intext) # move lonelyQuote to previous line
				
				
				for partialintext in tierseparator.split(intext):
					
					m = retiername.search(partialintext)
					if m:
						tiername = m.group(1)
						text = ""
					else: 
						if partialintext.count("intervals [")>5:
							tiername = "default"+str(defaultcounter)
							defaultcounter+=1
							text = ""
						else:
							#print "skipped partialintext"#, partialintext.count("intervals [") # ,partialintext
							continue
					
					#print partialintext
					for line in partialintext.split("\n"):
						line=line.strip()
						if skipnext:
							if line=='"phonèmes"' or line=='"Fonctions"':
								skiptier=line
							skipnext=False
							continue
						
						if line=='"IntervalTier"' or line=='"TextTier"':
							skipnext=True
							skiptier=False
							continue
						else: skipnext= False
						
						if skiptier:
							continue
						if line.startswith("class =") or line.startswith("File type =") or line.startswith("Object class =") or line.startswith("name ="): continue
						
						m = rexmin.search(line)
						if m:
							xmin=m.group(1)
						m = rexmax.search(line)
						if m:
							xmax=m.group(1)
						
						
						m = requotes.search(line)
						if m:
							text+=m.group(1)+" "
							if verbose:print(m.group(1))
							intervals[tiername]=intervals.get(tiername,[])+[(xmin,xmax,m.group(1))]
						else:
							pass
							if verbose:print("no",line)
					texts[tiername]=texts.get(tiername,"")+text
			else:
				print("textfile",f)
				text=""
				text+=first
				for line in infile:
					line=line.strip()
					line=line.replace('"',' ')
					text+=line+" "
				texts={"txt":text}
		#print texts
		goodtexts={}
		maybetexts={}
		for tiername,text in texts.items():
			print('==tier',tiername)
			text=text.replace("...",".")
			text=text.replace("/","~")
			if verbose:
				print("___",text,"___")
			if text.count(".")<5:
				
				print(text)
				print(". count:",text.count("."))
				if ' tu ' in text or ' il ' in text or ' le ' in text:
					print('keeping it')
					maybetexts[tiername]=text
					#print('intervals',intervals[tiername])
				else: 
					print("skipped whole",simplename+"."+tiername)
					continue
			else:
				goodtexts[tiername]=text
			
		for tiername, text in goodtexts.items():
			#textToSentences(text, outname="sentences/"+simplename+"."+tiername+".txt", problemout="longsentences/"+simplename, keepEndSent=keepEndSent, maxlength=maxlength, writeProblemBeforeSentence=writeProblemBeforeSentence, includeProblemSentence=True)	
			#textToSentences(text, outname="sentences/"+simplename+"."+tiername+".txt", problemout=None, keepEndSent=True, maxlength=maxlength, writeProblemBeforeSentence=writeProblemBeforeSentence, includeProblemSentence=True)	
			#textToSentences(text, outname, problemout=None, keepEndSent=False, maxlength=50, writeProblemBeforeSentence=True, includeProblemSentence=False)
			#outfile=codecs.open(outfolder+"/"+infile.split("/")[-1],"w","utf-8")
			print('************',tiername,text)
		try:
			os.mkdir("corpussamples/"+g)
		except OSError:
			pass
		
		if len(goodtexts)==1:
			#sents = textToSentences(text, outname="corpussamples/"+g+"/"+g+".sentences.txt", problemout=None, keepEndSent=True, maxlength=maxlength, writeProblemBeforeSentence=writeProblemBeforeSentence, includeProblemSentence=True)
			print("____ found one good tier for", g)
			#print('goodtexts',goodtexts)
			#totalsentences += len(sents)
			#nrtoks = len((" ".join(sents)).split())
			#totaltokens += nrtoks
			#stats[g]=(nrtoks,len(sents))
		else:
			if len(maybetexts)>=1:
				if  len(maybetexts)==1:
					goodtexts=maybetexts
					print("____ maybe found one good tier for", g)
				else:
					goodtexts={list(maybetexts.keys())[0]:maybetexts[list(maybetexts.keys())[0]]}
				print('goodtexts',goodtexts)
			else:
				tiers = list(goodtexts.keys())
				print(len(goodtexts),"goodtexts for",g,'______________________________!!!')
				coolnames = ['sequence ponctuée']
				for cn in coolnames:
					if cn in tiers:
						goodtexts={cn:goodtexts[cn]}
						break
					
				print(goodtexts.keys())
				
		if len(goodtexts)==1:
			ext = soundfile.split('.')[-1]
			soundoutname = outname="corpussamples/"+g+"/"+g+'.'+ext
			copyfile(soundfile,soundoutname)
			intervals2conllfile(intervals[list(goodtexts.keys())[0]], 
				outname="corpussamples/"+g+"/"+g+".intervals.conll",
				soundfile=g+'.'+ext)
			print('wrote conll file for ',g)
			
			
		else:
			print('nothing done here')
		#input('continue?')
	#print(totalsentences,"sentences.",totaltokens,"tokens.")
	
	# write stats:
	if infolder[-1]=="/":infolder=infolder[:-1]
	outstat = open(infolder.split("/")[-1]+".tsv","w")
	outstat.write("\t".join(["nom",'nrTokens',"nrPhrases",'tok par phrase'])+"\n")
	for g in sorted(stats):
		outstat.write("\t".join([g,str(stats[g][0]),str(stats[g][1]),str(round(float(stats[g][0])/stats[g][1],2))])+"\n")

def copyOtherFilesIntoCorpussamples(infolder, filter="*"):
	#textgridstodo = []
	#for infilename in glob.glob(os.path.join("textgrids", filter)):
	for root, dirnames, filenames in os.walk(infolder):
		#print filenames
		for filename in fnmatch.filter(filenames, filter):
			if filename.endswith(".rar") or filename.endswith(".gz"):
				print("rar:",root,filename)
				qsdf
			if filename.endswith(".zip"):continue
			infilename=os.path.join(root, filename)
			
			
			#print datetime.fromtimestamp(os.path.getmtime(infilename)) 
			#if skipBefore and str( datetime.fromtimestamp(os.path.getmtime(infilename))) < skipBefore: 
				#print infilename,"too old"
				#continue
			guessedname = repersname.split(infilename[len(infolder):])[0].replace(" ","_") 
			outname=("corpussamples"+guessedname+guessedname+"."+filename).replace(" ","_").replace("..",".").replace("(","").replace(")","")
			print(outname)
			if os.path.isdir("corpussamples"+guessedname):
				copyfile(infilename,outname)
			else:
				print("skipped",guessedname)
			
			#textgridstodo += [(infilename,guessedname)]
	#print len(textgridstodo),"textgrids found"
	


def stat(infolder="corpussamples/", filter="*.sentences.txt"):
	ta = {}
	toli, toto = 0,0
	for root, dirnames, filenames in os.walk(infolder):
		for filename in fnmatch.filter(filenames, filter):
			infilename=os.path.join(root, filename)
			text = codecs.open(infilename,"r",'utf-8').read()
			nbli = len(text.split("\n"))-1
			nbto = len(text.split())
			toli += nbli
			toto += nbto
			ta[filename.split(".")[0]]=(nbli,nbto)
	with codecs.open(infolder+"stat.tsv","w",'utf-8') as outf:
		outf.write("\t".join(["name","nbli","nbto"])+"\n")
		for n in sorted(ta):
			outf.write("\t".join([n]+[str(i) for i in list(ta[n])])+"\n")
		outf.write("\t".join(["_total_",str(toli),str(toto)])+"\n")
	print("wrote",infolder+"stat.tsv")



def rename():
	for fil in glob.glob(os.path.join("parses", '*-dependanaly.txt')):
		os.rename(fil, fil[:-16]+".trees.conll14")






if __name__ == "__main__":
	pass
	# unzip all: find . -name "*.zip" | xargs -P 5 -I fileName sh -c 'unzip -o -d "$(dirname "fileName")/$(basename -s .zip "fileName")" "fileName"'
	#rename()
	
	textgridToSentences("*textgrid*", keepEndSent=True, maxlength=100, writeProblemBeforeSentence=False, infolder="/home/kim/Downloads/20192020-L5FL001-P-devoir phonétique-54837")
	#copyOtherFilesIntoCorpussamples("good")
	#stat()
	#mate(filter="*Fum*")
	
	#for fil in glob.glob(os.path.join(u"sentences", '*')):
		#if "?" in codecs.open(fil,"r","utf-8").read():
			#print fil
