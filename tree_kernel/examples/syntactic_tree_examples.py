'''
Created on Jun 26, 2013

@author: nghia
'''

from tree.syntactic_tree import SyntacticTree

if __name__ == '__main__':
    # input ccg string
    xml_string = '''
    <ccg>
      <rule type="fa" cat="S[dcl]\NP">
        <lf start="1" span="1" word="plays" lemma="play" pos="VBZ" chunk="I-VP" entity="O" cat="(S[dcl]\NP)/NP" />
        <rule type="lex" cat="NP">
          <lf start="2" span="1" word="guitar" lemma="guitar" pos="NN" chunk="I-NP" entity="O" cat="N" />
        </rule>
      </rule>
    </ccg>'''
    
    # parse the tree from the xml string
    syntactic_tree = SyntacticTree.parse_tree_from_xml_string(xml_string)
    
    # print the tree
    print "the syntactic tree:"
    print syntactic_tree, "\n"
    
    # print the height of the tree (for fun)
    print "height of the tree:"
    print syntactic_tree.root.get_height(), "\n"
    
    # get the nodes of the tree
    nodes = syntactic_tree.get_nodes()
    
    # print the label/cat of the nodes
    print "the labels of the nodes:"
    for node in nodes:
        print node.label
    
    # get the string from the tree
    tree_string = str(syntactic_tree)
    
    # read the tree from the string again
    syntactic_tree =  SyntacticTree.read_tree(tree_string)
    
    # check if the tree string is still the same
    assert(tree_string == str(syntactic_tree))
    