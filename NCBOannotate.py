#####################################################################
#####################################################################
#####                        				#############
#####            BLAH 2015 - NBCO Annotate Text         #############
#####            By. Juan M. Banda                      #############
#####							#############
#####################################################################

import urllib2
import json
import sys
import time
import random
import os

REST_URL = "http://data.bioontology.org"
API_KEY = "8b5b7825-538d-40e0-9e9e-5ab9274a9aeb" #Replace with your own API key from Bioportal


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


ontologies = str(sys.argv[1])
text_file = str(sys.argv[2])
#Input = lines.xml - Document that contains document id, pmcid (sometimeS) and abstract tags  of the documents to annotate
f= open(str(text_file), 'r')
#Output = annotated_files.txt - Document that contains the id, pmcid, ID, prefLabel, ontology, from, to, type
ftw= open(str(text_file)+".out",'w')
for line in f.xreadlines():
   id_id  = str(find_between(line,'<id>','</id>'))
   pmc_id = str(find_between(line,'<pmcid>','</pmcid>'))
   document_abstract=str(find_between(line,'<abstractText>','</abstractText>'))
   if len(document_abstract) >= 4000: #Avoid pasisng very long strings
	splits=int(len(document_abstract)/1500) #!500 is a good hardcoded limit to split if text is too big
	parts=splitIterator(document_abstract, 1500)
	for single_part in parts:
		time.sleep(random.randint(1, 2)) #This timer is needed or the NCBO api will time you out
        	annotations = get_json(REST_URL + "/annotator?ontologies=" + ontologies + "&longest_only=true&text=" + urllib2.quote(single_part))
	        for result in annotations:
			time.sleep(random.randint(2, 7)) #Longer timer to not get blocked by the API
			try:
                		class_details1 = get_json(result["annotatedClass"]["links"]["self"])
		                ids=class_details1["@id"]
	                	prefLabel=class_details1["prefLabel"]
				ontology=class_details1["links"]["ontology"]

			        for annotation in result["annotations"]:
			            a_from= str(annotation["from"])
			            a_to= str(annotation["to"])
			            a_type= annotation["matchType"]
	        	        ftw.write(str(id_id) + "\t" + str(pmc_id) + "\t" + str(ids) + "\t" + str(prefLabel) + "\t" + str(ontology) + "\t" + str(a_from) +"\t" + str(a_to) + "\t" + str(a_type) + "\n")
			except:
				print "Connection / Formatting issues" #- No annotations to be made by the annotator
   else: 
	annotations = get_json(REST_URL + "/annotator?ontologies=" + ontologies  + "&longest_only=true&text=" + urllib2.quote(document_abstract))
   	for result in annotations:
		time.sleep(random.randint(1, 2))
		try:
	        	class_details1 = get_json(result["annotatedClass"]["links"]["self"])
        		ids=class_details1["@id"]
			prefLabel=class_details1["prefLabel"]
			ontology=class_details1["links"]["ontology"]
                        for annotation in result["annotations"]:
                            a_from= str(annotation["from"])
                            a_to= str(annotation["to"])
                            a_type= annotation["matchType"]
			ftw.write(str(id_id) + "\t" + str(pmc_id) + "\t" + str(ids) + "\t" + str(prefLabel) + "\t" + str(ontology) + "\t" + str(a_from) +"\t" + str(a_to) + "\t" + str(a_type) + "\n")
		except:
			print "Connection / Formatting issues" #- No annotations to be made by the annotator
f.close()
ftw.close()
