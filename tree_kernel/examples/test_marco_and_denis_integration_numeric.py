from tree.semantic_node_numeric import SemanticNode
from tree.syntactic_tree import SyntacticTree
from composes.semantic_space.space import Space
xml_string = '''
    <ccg>
  <rule type="ba" cat="S[dcl]">
   <lf start="0" span="1" word="Somebody" lemma="somebody" pos="DT" chunk="I-NP" entity="O" cat="NP" />
   <rule type="fa" cat="S[dcl]\NP">
    <lf start="1" span="1" word="is" lemma="be" pos="VBZ" chunk="I-VP" entity="O" cat="(S[dcl]\NP)/(S[ng]\NP)" />
    <lf start="2" span="1" word="singing" lemma="sing" pos="VBG" chunk="I-VP" entity="O" cat="S[ng]\NP" />
   </rule>
  </rule>
</ccg>'''
syntactic_tree = SyntacticTree.parse_tree_from_xml_string(xml_string)
vecfilepref = "/mnt/data/marco.baroni/composes/scripts/cctools/vectors"
matfilepref = "/mnt/data/marco.baroni/composes/scripts/cctools/matrices"
vecspace = Space.build(data = vecfilepref + ".dm",
                       rows = vecfilepref + ".rows",
                       format = "dm")
matspace = Space.build(data = matfilepref + ".dm",
                       rows = matfilepref + ".rows",
                       format = "dm")

semnode = SemanticNode.create_semantic_node(syntactic_tree.root,vecspace,matspace)

print semnode.get_matrep()
for x in semnode.get_numrep(): print x
