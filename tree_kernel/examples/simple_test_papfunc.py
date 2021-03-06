from tree.papfunc import Papfunc_SemanticNode
from tree.semantic_node import SemanticNode
from tree.syntactic_tree import SyntacticTree
from composes.semantic_space.space import Space
from examples import test_vector_file_prefix, test_matrix_file_prefix

# FIRST TEST
xml_string = '''
<ccg>
<lf start="0" span="1" word="dog" lemma="dog" pos="NN" chunk="I-NP" entity="O" cat="N" />
</ccg>
'''
syntactic_tree = SyntacticTree.parse_tree_from_xml_string(xml_string)
vecfilepref = test_vector_file_prefix
matfilepref = test_matrix_file_prefix
vecspace = Space.build(data = vecfilepref + ".dm",
                       rows = vecfilepref + ".rows",
                       format = "dm")
matspace = Space.build(data = matfilepref + ".dm",
                       rows = matfilepref + ".rows",
                       format = "dm")

semnode = SemanticNode.create_semantic_node(syntactic_tree.root,None)
papnode = Papfunc_SemanticNode.create_papfunc_node(semnode,vecspace,matspace)

print "*****"
print "Syntactic tree:", semnode
print "Symbolic representation:", papnode._matrep
print "Numeric representation:"
for x in papnode._numrep: print x

# SECOND TEST
xml_string = '''
<ccg>
 <rule type="fa" cat="NP[nb]">
  <lf start="0" span="1" word="A" lemma="a" pos="DT" chunk="I-NP" entity="O" cat="NP[nb]/N" />
  <rule type="fa" cat="N">
   <lf start="1" span="1" word="dog" lemma="dog" pos="NN" chunk="I-NP" entity="O" cat="N/N" />
   <lf start="2" span="1" word="barks" lemma="bark" pos="NNS" chunk="I-NP" entity="O" cat="N" />
  </rule>
 </rule>
</ccg>
'''

syntactic_tree = SyntacticTree.parse_tree_from_xml_string(xml_string)
semnode = SemanticNode.create_semantic_node(syntactic_tree.root,None)
papnode = Papfunc_SemanticNode.create_papfunc_node(semnode,vecspace,matspace)

print "*****"
print "Syntactic tree:", semnode
print "Symbolic representation:", papnode._matrep
print "Numeric representation:"
print papnode._matrep
for x in papnode._numrep: print x
