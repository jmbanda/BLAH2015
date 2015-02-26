# BLAH2015  - Annotation group tools 


NCBOannotate.py

This tool will take a text file in XML format with document id (id), Pubmed central id (pmcid), Text (abstractText) and will run the text through the NCBO annotator using the speficied ontologies. The tool will produce a file with all the annotations made, their ontology url code for the term/concept, ontology, perfered term, term start character offset, term end character offset and match type. 

Execution call:
<code>
python NCBOannotate.py RXNORM,CHEBI test_lines.xml
</code>

Output file will be (for this case) test_lines.xml.out

If you are trying to specify more than one ontology, you need to add it with a comma. 


