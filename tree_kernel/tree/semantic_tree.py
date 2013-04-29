'''
Created on Apr 29, 2013

@author: thenghiapham
'''
from tree.syntactic_tree import SyntacticTree
from tree.semantic_node import SemanticNode
from utils import type_utils

class SemanticTree(SyntacticTree):
    '''
    classdocs
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
    
    @classmethod
    def _read_branches(cls, string, tree_format=0):
        raise NotImplementedError()