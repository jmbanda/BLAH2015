#####################################################################
#####################################################################
#####                                                   #############
#####            BLAH 2015 - Dictionary Annotate Text   #############
#####            By. Juan M. Banda                      #############
#####                                                   #############
#####################################################################

import urllib2
import csv
import sys
import os
import re

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return "NULL"

def splitIterator(text, size):
    assert size > 0, "size should be > 0"
    for start in xrange(0, len(text), size):
        yield text[start:start + size]

dictionary = str(sys.argv[1])
text_file = str(sys.argv[2])
f= open(text_file, 'r')
ftw= open(text_file+'-'+ str(dictionary)+'.txt','w')
c=0

for line in f.xreadlines():
   id_id  = str(find_between(line,'<id>','</id>'))
   pmc_id = str(find_between(line,'<pmcid>','</pmcid>'))
   abstract_text = str(find_between(line,'<abstractText>','</abstractText>'))
   #Lets parse the text between the abstractText column
   with open(dictionary, 'rb') as csv_file:
    	csv_reader = csv.reader(csv_file, delimiter='\t')
    	for row in csv_reader:
		for m in re.finditer(re.escape(row[1]), abstract_text):
         		ftw.write(id_id + "\t" + pmc_id + "\t" + row[0] + "\t" + str(row[1]) + "\t" +  str(m.start()) + "\t" + str(m.end()) + "\n")	

ftw.close()
