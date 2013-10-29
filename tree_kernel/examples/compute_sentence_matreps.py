from __future__ import print_function
import sys
from xml.etree.ElementTree import ParseError
import re
from tree.papfunc import Papfunc_SemanticNode
from tree.semantic_node import SemanticNode
from tree.syntactic_tree import SyntacticTree
from composes.semantic_space.space import Space

print("importing vectors...")
vecfilepref = "/mnt/cimec-storage-sata/users/denis.paperno/composition_grammar/papfunc_spaces/vectors_ppmi_nmf_300_simplistic_training"
matfilepref = "/mnt/cimec-storage-sata/users/denis.paperno/composition_grammar/papfunc_spaces/matrices_ppmi_nmf_300_simplistic_training"
vecspace = Space.build(data = vecfilepref + ".dm",
                       rows = vecfilepref + ".rows",
                       format = "dm")

print("importing matrices...")
matspace = Space.build(data = matfilepref + ".dm",
                       rows = matfilepref + ".rows",
                       format = "dm")

infile = sys.argv[1]
outfile= open(sys.argv[2],'w')

sent=0
succ=0
vecs=0

currtree=""
intree=0
with open(infile) as data:
 for line in data:
  if re.match("^<ccg>",line):
   currtree = currtree + line
   intree=1
   sent +=1
  elif re.match("^</ccg>",line):
   currtree = currtree + line
   # print current tree
   #print("sentence %s" %sent)
   #print(currtree.strip('\n'),file=outfile)
   intree=0
   try:
    syntactic_tree = SyntacticTree.parse_tree_from_xml_string(currtree)
    succ +=1
    # print top node 
    semnode = SemanticNode.create_semantic_node(syntactic_tree.root,None)
    papnode = Papfunc_SemanticNode.create_papfunc_node(semnode,vecspace,matspace)
    #print(papnode,end='',file=outfile)
    #for x in (papnode.get_vector()[0]): print(x)#(x,file=outfile)
    print(papnode.get_matrep(),file=outfile)
    #try:
      #for x in numpy.array(papnode.get_vector().flatten()): print(str(x)+"\tJesus")
      #for x in range(len(papnode.get_vector().mat.A[0].tolist())):
      # dim=str(papnode.get_vector().mat.A[0].tolist()[x])
      # if x>0: print('\t',end='',file=outfile)
      # print(dim,end='',file=outfile)
      #print("",file=outfile)
    vecs +=1
    #except AttributeError: print ("Papnode %s doesn't have a vector representation" %papnode)
#   for x in semnode.get_numrep(): print(x,file=outfile)
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
