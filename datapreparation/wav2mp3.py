import glob, os


files = glob.glob('**/*.wav', recursive=True)
print (files)
for infile in files:
	os.system('lame -b 320 -h "{infile}" "{outfile}";'.format(infile=infile, outfile=infile.replace('.wav','.mp3')))
