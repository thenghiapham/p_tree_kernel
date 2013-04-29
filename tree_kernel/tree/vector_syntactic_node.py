'''
Created on Apr 26, 2013

@author: nghia
'''
from syntactic_node import SyntacticNode
from utils.type_utils import assert_type

class VectorSyntacticNode(SyntacticNode):
    '''
    classdocs
    '''
    

    def __init__(self, label, phrase):
        '''
        Constructor
        '''
        super(VectorSyntacticNode,self).__init__(label)
        self._phrase = self._phrase
    
    def add_child(self, child):
        assert_type(child, VectorSyntacticNode)
        SyntacticNode.add_child(self, child)