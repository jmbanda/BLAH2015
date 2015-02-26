# BLAH2015  - Annotation group tools 


<h2>NCBOannotate.py</h2>

This tool will take a text file in XML format with document id (id), Pubmed central id (pmcid), Text (abstractText) and will run the text through the NCBO annotator using the speficied ontologies. The tool will produce a file with all the annotations made, their ontology url code for the term/concept, ontology, perfered term, term start character offset, term end character offset and match type. 

Execution call (using RxNorm and CHEBI ontologies):

<code>
python NCBOannotate.py RXNORM,CHEBI test_lines.xml
</code>

Output file will be (for this case) test_lines.xml.out

If you are trying to specify more than one ontology, you need to add it with a comma. We have included the test_lines.xml file with one randomly selected Euro-pubmed article abstract inside of it. 

<h2>dictionary_annotate.py</h2>

This tool will use a dictionary to annotate any given text. The dictionaries are just a tab delimited file that contain <code>term_identifier \t term_text \n</code>. We have included some dictionaries here extracted from RxNORM, Phenominer, Chebi, FMA and PATO ontologies. 

Execution call (using CHEBI dictionary):

<code>
python annotate_dictionary.py CHEBI-dic.csv test_lines.xml
</code>

This tool will produce a file with all the annotations made in the following format:
<code> document_id \t document_PMCID \t dictionary_term_id \t dictionary_term_text \t character_offset_start \t character_offset_end \n </code> 

