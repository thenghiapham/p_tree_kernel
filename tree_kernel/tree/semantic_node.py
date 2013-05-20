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


    def __init__(self, label, vector, node_type=SyntacticNode.NON_TERMINAL):
        '''
        Constructor
        '''
        if vector is not None:
            assert_type(vector, Matrix, "argument vector needs to be of type Matrix")
        self._vector = vector
        super(SemanticNode, self).__init__(label, node_type)
        
    
    def add_child(self, child):
        assert_type(child, SemanticNode)
        SyntacticNode.add_child(self, child)