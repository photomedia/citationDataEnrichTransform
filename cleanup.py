#! /usr/bin/env python
import sys
import string
import getopt
#import re

def main(argv):
	inputfile = ''
	outputfile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print (' -i <inputfile> -o <outputfile>');
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
	print 'Output file is "', outputfile
	filename = inputfile;
	filenamewithheader = outputfile;
	
	#searchquery = 'node'
	#regex = re.compile(searchquery)
	
	with open(inputfile) as f1:
		with open(outputfile, 'w') as f2:
			lines = f1.readlines()
			for i, line in enumerate(lines):
				line=line.replace("\"\"\" ","\" ")
				line=line.replace("9\" ]", "9 ]")
				line=line.replace("9\" magazines", "9 magazines")
				line=line.replace("\"onset", "onset")
				line=line.replace("\" \"","\"");
				line=line.replace("  onset", " onset");
				f2.write(line)
	
	#with open(filename, 'a') as file: file.write(']')  
	#with open(filename, 'rU') as original: data = original.read()
	#with open(filenamewithheader, 'w') as modified: modified.write("graph [\ndirected 0 \n" + data)
	
if __name__ == "__main__":
   main(sys.argv[1:])