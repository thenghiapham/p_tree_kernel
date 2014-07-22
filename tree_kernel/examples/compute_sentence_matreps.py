from __future__ import print_function
import sys
from xml.etree.ElementTree import ParseError
import re
from tree.papfunc import Papfunc_SemanticNode
from tree.semantic_node import SemanticNode
from tree.syntactic_tree import SyntacticTree
from composes.semantic_space.space import Space

# This script computes vector representations for sentences parsed by the C and C parser, stored in xml file. The script takes 4 command line arguments:
#*directory of input xml files of parsed sentences (the script accepts the output of the C and C CCG parser)
#*output file
#*vector space prefix (for dm format)
#*matrix spce prefix (for dm format)

if len(sys.argv)!=5:
    raise TypeError("The script takes exactly 4 arguments, %i given" %len(sys.argv))

print("importing vectors...")
# the third command line argument is the prefix of the vector space in dense matrix format
# e.g. "/mnt/cimec-storage-sata/users/denis.paperno/composition_grammar/papfunc_spaces/vectors_ppmi_svd_300_simplistic_training_nouns_only"

vecfilepref = sys.argv[3]

# the fourth command line argument is the prefix of the matrix space in dense matrix format
# e.g. "/mnt/cimec-storage-sata/users/denis.paperno/composition_grammar/papfunc_spaces/matrices_ppmi_svd_300_simplistic_training"


matfilepref = sys.argv[4]

#build the space of lexical vectors
mvecspace = Space.build(data = vecfilepref + ".dm",
                                   rows = vecfilepref + ".rows",
                                   format = "dm")

print("importing matrices...")
#build the space of lexical matrices
mmatspace = Space.build(data = matfilepref + ".dm",
                                   rows = matfilepref + ".rows",
                                   format = "dm")

infile = sys.argv[1]
outfile= open(sys.argv[2],'w')

#initialize sentence counters
sent=0
succ=0
vecs=0

currtree=""
intree=0 #indicator of whether we are inside a sentence tree or expect a new one

#process the xml file with a list of sentences
with open(infile) as data:
    for line in data:
        if re.match("^<ccg>",line):#beginning of tree routine
            currtree = currtree + line
            intree=1
            sent +=1
        elif re.match("^</ccg>",line): #end of tree routine
            currtree = currtree + line
            intree=0
            try: #output the representations to file
                syntactic_tree = SyntacticTree.parse_tree_from_xml_string(currtree)
                succ +=1
                # print top node 
                semnode = SemanticNode.create_semantic_node(syntactic_tree.root,None)
                papnode = Papfunc_SemanticNode.create_papfunc_node(semnode,mvecspace,mmatspace)
                #output the symbolic representation
                print(papnode.get_matrep(),file=outfile)
                vecs +=1
            except ParseError: #invalid xml tree representation
                "THIS TREE WAS NOT XML-PARSABLE: %s" %currtree

            # reset current tree
            currtree=""

        elif intree:
            currtree = currtree + line
#display sentence statistics for the current input file
print("%i sentences transgressed" %sent)
print("%i sentences successfully parsed" %succ)
print("%i vectors produced" %vecs)

#close the input and output files
data.close()
outfile.close()
