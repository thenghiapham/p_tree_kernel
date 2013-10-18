from tree.semantic_node import SemanticNode
from tree.syntactic_tree import SyntacticTree
xml_string = '''
    <ccg>
 <rule type="rp" cat="S[dcl]">
  <rule type="ba" cat="S[dcl]">
   <lf start="0" span="1" word="Somebody" lemma="somebody" pos="DT" chunk="I-NP" entity="O" cat="NP" />
   <rule type="fa" cat="S[dcl]\NP">
    <lf start="1" span="1" word="is" lemma="be" pos="VBZ" chunk="I-VP" entity="O" cat="(S[dcl]\NP)/(S[ng]\NP)" />
    <lf start="2" span="1" word="singing" lemma="sing" pos="VBG" chunk="I-VP" entity="O" cat="S[ng]\NP" />
   </rule>
  </rule>
  <lf start="3" span="1" word="." lemma="." pos="." chunk="O" entity="O" cat="." />
 </rule>
</ccg>'''

syntactic_tree = SyntacticTree.parse_tree_from_xml_string(xml_string)
veclist=[]
matlist=[]
semnode = SemanticNode.create_semantic_node(syntactic_tree.root,None,veclist,matlist)
print semnode.get_matrep()
