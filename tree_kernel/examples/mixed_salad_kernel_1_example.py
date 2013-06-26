'''
Created on Jun 26, 2013

@author: thenghiapham
'''

import os
from tree.syntactic_tree import SyntacticTree
from composes.utils import io_utils
from kernel.naive_compositional_tree_kernel import NaiveCompositionalSemanticTreeKernel
from composes.composition.weighted_additive import WeightedAdditive
from kernel_utils.tree_utils import syntactic_tree_2_semantic_tree

if __name__ == '__main__':
    
    # parsing syntactic tree from xml string
    xml_string1 = '''
    <ccg>
      <rule type="fa" cat="S[dcl]\NP">
        <lf start="1" span="1" word="play-v" lemma="play" pos="VBZ" chunk="I-VP" entity="O" cat="(S[dcl]\NP)/NP" />
        <rule type="lex" cat="NP">
          <lf start="2" span="1" word="guitar-n" lemma="guitar" pos="NN" chunk="I-NP" entity="O" cat="N" />
        </rule>
      </rule>
    </ccg>'''
    xml_string2 = '''
    <ccg>
      <rule type="fa" cat="S[dcl]\NP">
        <lf start="1" span="1" word="play-v" lemma="play" pos="VBZ" chunk="I-VP" entity="O" cat="(S[dcl]\NP)/NP" />
        <rule type="lex" cat="NP">
          <lf start="2" span="1" word="instrument-n" lemma="instrument" pos="NN" chunk="I-NP" entity="O" cat="N" />
        </rule>
      </rule>
    </ccg>'''
    syntactic_tree1 = SyntacticTree.parse_tree_from_xml_string(xml_string1)
    syntactic_tree2 = SyntacticTree.parse_tree_from_xml_string(xml_string2)
    print "syntactic tree 1:", syntactic_tree1
    print "syntactic tree 2:", syntactic_tree2
    
    # loading space, building semantic trees
    current_directory = os.path.dirname(__file__)
    space_file_path = "%s/extracted_space.pkl" %current_directory
    lexical_space = io_utils.load(space_file_path)
    composition_model = WeightedAdditive()
    
    semantic_tree1 = syntactic_tree_2_semantic_tree(syntactic_tree1, lexical_space, composition_model)
    semantic_tree2 = syntactic_tree_2_semantic_tree(syntactic_tree2, lexical_space, composition_model)
    print "semantic tree 1:", semantic_tree1
    print "semantic tree 2:", semantic_tree2
    print "node list 1:", [node._label for node in semantic_tree1.get_nodes()] 
    print "node list 1:", [node._label for node in semantic_tree2.get_nodes()]
    
    # compute kernel
    kernel = NaiveCompositionalSemanticTreeKernel(1.0)
    print "kernel 1 1:\n", kernel.dot_product(semantic_tree1, semantic_tree1)   
    print "kernel 1 2:\n", kernel.dot_product(semantic_tree1, semantic_tree2)   