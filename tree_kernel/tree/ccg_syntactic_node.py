'''
Created on Apr 26, 2013

@author: nghia
'''
from syntactic_node import SyntacticNode

class VectorSyntacticNode(SyntacticNode):
    '''
    classdocs
    '''


    def __init__(self, label, phrase):
        '''
        Constructor
        '''
        self._phrase = phrase
        super(VectorSyntacticNode, self).__init__(label)