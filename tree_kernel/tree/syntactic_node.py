'''
Created on Apr 16, 2013

@author: thenghiapham
'''

from node import Node
from kernel_utils import type_utils

class SyntacticNode(Node):
    '''
    An instance of class represents a node in a syntactic tree (CCG or PSG tree)
    '''
    
    # constants to indicate the type of a node
    TERMINAL = 0
    NON_TERMINAL = 1

    def __init__(self, label, *args, **kwargs):
        '''
        Constructor
        '''
        self._label = label
        self._children = []
        # TODO: fix here today
        self._type = node_type
        self._lemma
    
    def add_child(self, child):
        if self._type == SyntacticNode.TERMINAL:
            raise ValueError("Terminal node cannot have child node")
        type_utils.assert_type(child, SyntacticNode)
        Node.add_child(self, child)
        
    def get_child(self, i):
        if i >= 0 and i < len(self._children):
            return self._children[i]
        else:
            raise IndexError("Invalid index")
        
    def get_child_number(self):
        return len(self._children)
    
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
    
    def get_depth(self):
        if self._children: 
            depth = 0
            for child in self._children:
                depth = max(depth, child.get_depth())
            return depth + 1
        else:
            return 0
    def get_label(self):
        return self._label
        