'''
Created on Apr 29, 2013

@author: thenghiapham
'''
from tree.syntactic_tree import SyntacticTree
from tree.semantic_node import SemanticNode
from kernel_utils import type_utils

class SemanticTree(SyntacticTree):
    '''
    An instance of this class represents a semantic tree (CCG or PSG tree)
    '''


    def __init__(self, root):
        '''
        Constructor
        '''
        type_utils.assert_type(root, SemanticNode)
        self._root = root
    
    @classmethod
    def read_tree(cls, string, tree_format=0):
        raise NotImplementedError()
    
    