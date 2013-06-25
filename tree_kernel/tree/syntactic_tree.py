'''
Created on Apr 16, 2013

@author: thenghiapham
'''

from syntactic_node import SyntacticNode
from kernel_utils import type_utils

class SyntacticTree(object):
    '''
    An instance of this class represents a syntactic tree (CCG or PSG tree)
    '''

    def __init__(self,root):
        '''
        Constructor
        '''
        type_utils.assert_type(root, SyntacticNode)
        self._root = root
        
    @classmethod
    def parse_tree(cls, xml_string):
        """Read a SyntacticTree from an xml string
        
        Args:
        string: the xml input string from a CCG parser
            
        Returns:
        the SyntacticTree represented by the input xml string
        """
        pass
    
    @classmethod
    def read_tree(cls, string):
        """Read a SyntacticTree from a string
        
        Args:
        string: the input string
            For a PSG tree, the format of the tree is similar to a Penn Treebank
            tree, without newline characters:
            e.g. (S (NP (NNP Mary)) (VP (VBZ loves) (NP (NNP John))))
        
        Returns:
        the SyntacticTree represented by the input string
        """
        
        # first, remove the brackets ()
        string = string.strip()
        if string[0] == "(" and string[-1] == ")":
            string = string[1:-1]
        
        # split the string with blank character
        # if the string has exactly or fewer than one element, it cannot be a 
        # tree
        # if it has two elements, it must be a tree with a terminal node as the
        # root
        # if it has more than two elements, take the first element as the root
        # and other elements as the branches 
        elements = string.split()
        if len(elements) <= 1 or elements[1] == "":
            raise ValueError("%s cannot be a tree or subtree" %string)
        else:
            if len(elements) == 2:
                # TODO: if the label comes from CCG parser, turn [] into ()
                root = cls._read_terminal_node(elements)
            else:
                branch_string = " ".join(elements[1:])
                root = SyntacticNode(elements[0])
                branches = cls._read_branches(branch_string)
                for branch in branches:
                    root.add_child(branch._root)
            
            return SyntacticTree(root)
    
    # TODO: move this method to SyntacticNode?
    @classmethod
    def _read_terminal_node(cls, elements):
        # TODO: add option to read lemma, pos if the input come from ccg
        label = elements[0]
        word = elements[1]
        return SyntacticNode(label, word=word, pos=label)
    
    @classmethod
    def _read_branches(cls, string):
        # read the string from left to right 
        # whenever the number of left brackets and the number of right brackets
        # are the same, read a tree in the (), and read the other trees from the
        # remaining part
        # if at the end, the number of left brackets is still bigger than the
        # number of right brackets, throw an error
        if len(string) == 0:
            raise ValueError("a forest cannot be empty")
            #return []
        elif string[0] != "(":
            raise ValueError("a forest string must starts with (")
        
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
                        return [cls.read_tree(string[0:i+1])]
                    else:
                        first_branch_string = string[0:i+1]
                        first_branch_string = first_branch_string.strip()[1:-1]
                        
                        first_branch = cls.read_tree(first_branch_string)
                        remaining_string = string[i+1:len(string)]
                        remaining_string = remaining_string.strip()
                        return [first_branch] + cls._read_branches(remaining_string)
                # TODO: check whether this is necessary
                elif left_bracket_minus_right_bracket < 0:
                    raise ValueError("%s cannot be a forest" %string)
        if left_bracket_minus_right_bracket > 0:
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
    
    # TODO: implement get_all_subtrees ?


    
        