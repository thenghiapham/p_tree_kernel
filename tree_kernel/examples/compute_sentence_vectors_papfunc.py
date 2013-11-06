from __future__ import print_function
import sys
from xml.etree.ElementTree import ParseError
import re
import os
from tree.papfunc import Papfunc_SemanticNode
from tree.semantic_node import SemanticNode
from tree.syntactic_tree import SyntacticTree
from composes.semantic_space.space import Space

#this scripts takes 4 arguments: 
#*directory of input xml files
#*output file
#*vector space prefix (for dm format)
#*matrix spce prefix (for dm format)

if len(sys.argv)!=5: raise TypeError("The script takes exactly 4 arguments, %i given" %len(sys.argv))

print("importing vectors...")
vecfilepref = sys.argv[3]# e.g. "/mnt/cimec-storage-sata/users/denis.paperno/composition_grammar/papfunc_spaces/vectors_ppmi_svd_300_simplistic_training_nouns_only"
matfilepref = sys.argv[4]# e.g. "/mnt/cimec-storage-sata/users/denis.paperno/composition_grammar/papfunc_spaces/matrices_ppmi_svd_300_simplistic_training"
vecspace = Space.build(data = vecfilepref + ".dm",
                       rows = vecfilepref + ".rows",
                       format = "dm")

print("importing matrices...")
matspace = Space.build(data = matfilepref + ".dm",
                       rows = matfilepref + ".rows",
                       format = "dm")

for infile in os.listdir(sys.argv[1]):
 if (re.search (r'\.xml',infile)):
  print("processing %s ..." %infile)
  outname=sys.argv[2]+"."+infile
  outfile= open(outname+".dm",'w')
  matfile=open(outname+".matreps",'w')
  
  sent=0
  succ=0
  vecs=0
  
  currtree=""
  intree=0

#process each xml file in the input directory
  with open(sys.argv[1]+infile) as data:
   for line in data:
    if re.match("^<ccg>",line):
     currtree = currtree + line
     intree=1
     sent +=1
    elif re.match("^</ccg>",line):
     currtree = currtree + line
     intree=0
     try:
      syntactic_tree = SyntacticTree.parse_tree_from_xml_string(currtree)
      succ +=1
      semnode = SemanticNode.create_semantic_node(syntactic_tree.root,None)
      papnode = Papfunc_SemanticNode.create_papfunc_node(semnode,vecspace,matspace)
      try:
        for x in range(len(papnode.get_vector().mat.A[0].tolist())):
         dim=str(papnode.get_vector().mat.A[0].tolist()[x])
         if x>0: print('\t',end='',file=outfile)
         print(dim,end='',file=outfile)
        print(papnode.get_matrep(),file=matfile)
        print("",file=outfile)
        vecs +=1
      except AttributeError: print ("Papnode %s doesn't have a vector representation" %papnode)
     except ParseError:
      "THIS TREE WAS NOT XML-PARSABLE: %s" %currtree
  
    # reset current tree
     currtree=""
  
    elif intree:
     currtree = currtree + line
  print("%i sentences transgressed" %sent)
  print("%i sentences successfully parsed" %succ)
  print("%i vectors produced" %vecs)
  data.close()
  outfile.close()
  matfile.close()
 
print("Done.")
