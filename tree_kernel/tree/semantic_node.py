'''
Created on Apr 29, 2013

@author: nghia
'''
from tree.syntactic_node import SyntacticNode
from composes.matrix.matrix import Matrix
from utils.type_utils import assert_type

class SemanticNode(SyntacticNode):
    '''
    classdocs
    '''


    def __init__(self, label, vector):
        '''
        Constructor
        '''
        super(SemanticNode, self).__init__(label)
        self._vector = vector
    
    def add_child(self, child):
        assert_type(child, SemanticNode)
        SyntacticNode.add_child(self, child)