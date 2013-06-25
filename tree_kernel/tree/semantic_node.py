'''
Created on Apr 29, 2013

@author: nghia
'''
from tree.syntactic_node import SyntacticNode
from composes.matrix.matrix import Matrix
from kernel_utils.type_utils import assert_type

class SemanticNode(SyntacticNode):
    '''
    classdocs
    '''


    def __init__(self, label, vector, *args, **kwargs):
        '''
        Constructor
        '''
        
        super(SemanticNode, self).__init__(label, args, kwargs)
        
        if vector is not None:
            assert_type(vector, Matrix, "argument vector needs to be of type Matrix")
        self._vector = vector
        
        
    
    def add_child(self, child):
        assert_type(child, SemanticNode)
        SyntacticNode.add_child(self, child)