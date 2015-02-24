#####################################################################
#####                                            				        #####
#####            BLAH 2015 - NBCO Annotate Abstracts            #####
#####							                                              #####
#####################################################################

import urllib2
import json
import time
import random
import os
from pprint import pprint

REST_URL = "http://data.bioontology.org"
API_KEY = "197de257-9b62-4da6-baaf-ddcad5783e18" #Replace with your own API key from Bioportal


#Functions to get bioportal results
def get_json(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('Authorization', 'apikey token=' + API_KEY)]
    return json.loads(opener.open(url).read())

#Easy XML tag parsing function - this is for badly formed XML input
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return "NULL"

#If the text is too big, lets split it in parts 
def splitIterator(text, size):
    assert size > 0, "size should be > 0"
    for start in xrange(0, len(text), size):
        yield text[start:start + size]


#Input = lines.xml - Document that contains document id, pmcid (sometimeS) and abstract tags  of the documents to annotate
f= open('lines.xml', 'r')
#Output = annotated_files.txt - Document that contains the id, pmcid, rxcui in this case and preflabel of the RxNorm terms found
ftw= open('annotated_files.txt','w')
c=0
for line in f.xreadlines():
   id_id  = str(find_between(line,'<id>','</id>'))
   pmc_id = str(find_between(line,'<pmcid>','</pmcid>'))
   document_abstract=str(find_between(line,'<abstractText>','</abstractText>'))
   if len(document_abstract) >= 4000:
	splits=int(len(document_abstract)/1500)
	parts=splitIterator(document_abstract, 1500)
	for single_part in parts:
		time.sleep(random.randint(1, 3)) #This timer is needed or the NCBO api will time you out
        	annotations = get_json(REST_URL + "/annotator?ontologies=RXNORM&longest_only=true&text=" + urllib2.quote(single_part))
	        for result in annotations:
			time.sleep(random.randint(2, 7)) #Longer timer to not get blocked by the API
			try:
                		class_details1 = get_json(result["annotatedClass"]["links"]["self"])
		                ids=class_details1["@id"]
                		rxcui=ids[44:]
	                	prefLabel=class_details1["prefLabel"]
	        	        ftw.write(str(id_id) + "\t" + str(pmc_id) + "\t" + str(rxcui) + "\t" + str(prefLabel) + "\n")
			except:
				#print "Empty Result set" - No annotations to be made by the annotator
   else: 
	annotations = get_json(REST_URL + "/annotator?ontologies=RXNORM&longest_only=true&text=" + urllib2.quote(document_abstract))
   	for result in annotations:
		time.sleep(random.randint(1, 4))
		try:
	        	class_details1 = get_json(result["annotatedClass"]["links"]["self"])
        		ids=class_details1["@id"]
			rxcui=ids[44:]
			prefLabel=class_details1["prefLabel"]
			ftw.write(str(id_id) + "\t" + str(pmc_id) + "\t" + str(rxcui) + "\t" + str(prefLabel) + "\n")
		except:
			#print "Empty Result set" - No annotations to be made by the annotator
f.close()
ftw.close()
