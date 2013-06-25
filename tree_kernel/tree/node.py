'''
Created on Apr 16, 2013

@author: thenghiapham
'''

from kernel_utils import type_utils

class Node(object):
    '''
    Basic Node class
    The only attribute of this class is _children, which contains a list of child nodes
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._children = []
    
    def add_child(self,child):
        """Add a child Node to a Node.

        Args:
        child: the child Node
        """
        # check whether the child belong to the class Node
        type_utils.assert_type(child, Node)
        
        self._children.append(child)