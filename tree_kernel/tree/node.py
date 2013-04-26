'''
Created on Apr 16, 2013

@author: thenghiapham
'''

from utils import type_utils

class Node(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._children = []
    
    def add_child(self,child):
        type_utils.assert_type(child, Node)
        self._children.append(child)