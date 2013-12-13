import os

count = 0
for dirname, dirnames, filenames in os.walk('C:\\folder'):
	for f in filenames:
		fileName = dirname + "\\" +f
		name, ext = os.path.splitext(fileName)

		if ext == '.pdf':
			print "python pdf2txt.py -o %s.txt -t text %s" % (name,fileName)	
			count+=1
			os.system("python pdf2txt.py -o %s.txt -t text %s" % (fileName,fileName))
			
print count