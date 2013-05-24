'''
Created on Apr 16, 2013

@author: thenghiapham
'''

from syntactic_node import SyntacticNode
from kernel_utils import type_utils

class SyntacticTree(object):
    '''
    classdocs
    '''


    def __init__(self,root):
        '''
        Constructor
        '''
        type_utils.assert_type(root, SyntacticNode)
        self._root = root
    
    @classmethod
    def read_tree(cls, string, tree_format=0):
        string = string.strip()
        if string[0] == "(" and string[-1] == ")":
            string = string[1:-1]
        elements = string.split()
        if len(elements) <= 1 or elements[1] == "":
            raise ValueError("%s cannot be a tree or subtree" %string)
        else:
            root = SyntacticNode(elements[0])
            branch_string = " ".join(elements[1:])
            branches = cls._read_branches(branch_string)
            for branch in branches:
                root.add_child(branch._root)
            return SyntacticTree(root)
    
    @classmethod
    def _read_branches(cls, string, tree_format=0):
        left_bracket_minus_right_bracket = 0
        left_bracket = 0
        for i in range(len(string)):
            if string[i] == "(":
                left_bracket += 1
                left_bracket_minus_right_bracket += 1
            elif string[i] == ")":
                left_bracket_minus_right_bracket -= 1
                if left_bracket_minus_right_bracket == 0:
                    if i == len(string) - 1 or (string[i+1:len(string)].strip() == ""):
                        return [cls.read_tree(string[0:i+1], tree_format)]
                    else:
                        first_branch_string = string[0:i+1]
                        first_branch_string = first_branch_string.strip()[1:-1]
                        
                        first_branch = cls.read_tree(first_branch_string, tree_format)
                        remaining_string = string[i+1:len(string)]
                        remaining_string = remaining_string.strip()
                        return [first_branch] + cls._read_branches(remaining_string, tree_format)
                elif left_bracket_minus_right_bracket < 0:
                    raise ValueError("%s cannot be a forest" %string)
        if left_bracket_minus_right_bracket > 0:
            raise ValueError("%s cannot be a forest" %string)
        
        if left_bracket == 0:
            return [SyntacticTree(SyntacticNode(string,SyntacticNode.TERMINAL))]
        else:
            raise ValueError("%s cannot be a forest" %string)
    
                 
    def __str__(self):
        return str(self._root)
    
    
    def get_nodes(self):
        all_nodes = [] 
        if not self._root is None:
            all_nodes.append(self._root)
            i = 0
            while i < len(all_nodes):
                for node in all_nodes[i]._children:
                    all_nodes.append(node)
                i += 1 
        return all_nodes
    
    '''
    def get_all_subtrees(self):
        if self._root._children:
            if len(self._root._children) == 1:
                child = self._root._children[0]
                if not child._children:
                    return [self]
            else:
                tree_set = []
                for child in self._root._children:
                    trees = tree_set.a 
    '''
            


    
        