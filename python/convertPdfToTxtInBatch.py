import os

####################
## Uses:PdfMiner 
## https://pypi.python.org/pypi/pdfminer/
## Requires Python 2 :-(
####################


count = 0
for dirname, dirnames, filenames in os.walk('folder_name'):

	for f in filenames:
		fileName = dirname + "\\" +f

		name, ext = os.path.splitext(fileName)
		name = name
		fileName = fileName

		if ext == '.pdf':
			print( r'python pdf2txt.py -o "%s.txt" -t text "%s" ' % (name,fileName) )
			count+=1
			os.system( r'python pdf2txt.py -o "%s.txt" -t text "%s" ' % (name,fileName) )
	

print(count)