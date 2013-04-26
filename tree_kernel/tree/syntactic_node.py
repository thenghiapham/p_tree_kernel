'''
Created on Apr 16, 2013

@author: thenghiapham
'''

from node import Node
from utils import type_utils

class SyntacticNode(Node):
    '''
    classdocs
    '''
    TERMINAL = 0
    NON_TERMINAL = 1
    #PRE_TERMINAL = 2

    def __init__(self, label, node_type=NON_TERMINAL):
        '''
        Constructor
        '''
        self._label = label
        self._children = []
        self._type = node_type
    
    def add_child(self, child):
        if self._type == SyntacticNode.TERMINAL:
            raise ValueError("Terminal node cannot have child node")
        #elif self._type == SyntacticNode.PRE_TERMINAL:
        #    if len(self._children) >= 1:
        #        raise ValueError("Pre_terminal node cannot have more than one child node")
        type_utils.assert_type(child, SyntacticNode)
        Node.add_child(self, child)
        
    def get_child(self, i):
        if i >= 0 and i < len(self._children):
            return self._children[i]
        else:
            raise IndexError("Invalid index")
    
    def is_pre_terminal(self):
        return (self._type != SyntacticNode.TERMINAL and len(self._children) == 1
                and self._children[0]._type == SyntacticNode.TERMINAL) 
    
    def has_same_production(self, node2):
        if not self._label == node2._label:
            return False
        if not len(self._children) == len(node2._children):
            return False
        for i in xrange(len(self._children)):
            if self.get_child(i)._label != node2.get_child(i)._label:
                return False
        return True
    
    def __str__(self):
        if not self._children:
            return self._label
        else:
            child_string = ""
            for child in self._children:
                child_string = child_string + " " + str(child)
            return "(%s%s)" %(self._label, child_string) 
    
    def get_label(self):
        return self._label
        