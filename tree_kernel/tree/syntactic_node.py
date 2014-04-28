'''
Created on Apr 16, 2013

@author: thenghiapham
'''

from node import Node
from kernel_utils import type_utils

class SyntacticNode(Node):
    '''
    An instance of this class represents a node in a syntactic tree (CCG or PSG
    tree)
    
    A syntactic node has the following attributes:
    label: the label of the node (cat in CCG, phrase type in PSG)
    children: the child nodes of the node
    type: terminal node or non-terminal node
    
    if the node is a terminal nodes, it has the additional attributes:
    pos: the POS of the terminal node
    word: the word form of the terminal node
    lemma: the lemma of the terminal node (optional, currently only in CCG)
     
    '''
    
    # constants to indicate the type of a node
    TERMINAL = 0
    NON_TERMINAL = 1
    
    LEMMA=0
    LEMMA_POS=1
    WORD=2

    def __init__(self, label, *args, **kwargs):
        '''
        Constructor
        
        Args:
            label<string>: the label (cat in CCG tree) of the node
            kwargs: key word argument, non empty only for terminal/lexical node
                    (if we don't consider la, ba, lex rule in ccg)
                list of argument in kwargs:
                pos= the POS of the terminal node
                word= the word form of the terminal node
                lemma= the lemma of the terminal node
        '''
        self._label = label
        self._children = []
        # TODO: should require all or not
        if kwargs:
            self._type = SyntacticNode.TERMINAL
            if "pos" in kwargs:
                self._pos = kwargs["pos"]
            if "lemma" in kwargs:
                self._lemma = kwargs["lemma"]
            if "word" in kwargs:
                self._word = kwargs["word"]
        else:
            self._type = SyntacticNode.NON_TERMINAL
    
    @staticmethod        
    def _get_short_pos(pos, lemma, label):
        pos = pos[0].lower()
        # NOTE NOTE NOTE: where is "j"
        #if not (pos == "n" or pos == "j" or pos == "v"):
        if not (pos == "n" or pos == "j" or pos == "v" or pos == "r"):
            if pos == "c":
                pos = "d"
            elif pos == "d":
                pos = "d"
            else:
                pos = "o"
        return pos
        
    
    def add_child(self, child):
        """Add a child SyntacticNode to a SyntacticNode.

        Args:
        child: the child SyntacticNode
        """
        if self._type == SyntacticNode.TERMINAL:
            raise ValueError("Terminal node cannot have child node")
        type_utils.assert_type(child, SyntacticNode)
        Node.add_child(self, child)
        
    def copy(self, recursive = False):
        """Create the copy of a syntactic node

        Args:
        recursive<boolean>: copy recursively or not:
            if True, copy the information of its children to the new node
                (not implemented yes)
            if False, the children of the new node is empty
        
        Returns:
        the i-th child
        """
        if self.is_terminal():
            new_node = SyntacticNode(self._label, pos=self._pos, word=self._word)
            if hasattr(self, '_lemma'):
                new_node._lemma = self._lemma
        else:
            new_node = SyntacticNode(self._label)
        
        # TODO: copy recursively?
        return new_node
        
    def get_child(self, i):
        """Get the i-th child from a SyntacticNode.

        Args:
        i: the index of the wanted child
        
        Returns:
        the i-th child
        """
        if i >= 0 and i < len(self._children):
            return self._children[i]
        else:
            raise IndexError("Invalid index")
        
    def get_child_number(self):
        """Get the number of children of a SyntacticNode.
        
        Returns:
        the number of children of the SyntacticNode
        """
        return len(self._children)
    
    def get_height(self):
        """Get the height of the current node in a tree

        Returns:
        An integer value
        """
        if self._children: 
            depth = 0
            for child in self._children:
                depth = max(depth, child.get_height())
            return depth + 1
        else:
            return 0
        
    def has_same_production(self, node2):
        """Check whether the SyntacticNode have the same production rule as that
        of another SyntacticNode
        (example of a production rule: NP -> DET NP, NP -> NP/N N) 

        Args:
        node2: the node to compare with                
        
        Returns:
        A boolean value: True if the current SyntacticNode has the same
        production rule as that of the other SyntacticNode
        """
        
        if not self._label == node2._label:
            return False
        if not len(self._children) == len(node2._children):
            return False
        if self._type != node2._type:
            return False
        if self._type == SyntacticNode.TERMINAL:
            if self._word != node2._word:
                return False 
        else:
            for i in xrange(len(self._children)):
                if self.get_child(i)._label != node2.get_child(i)._label:
                    return False
        return True
    
    def is_terminal(self):
        """Check whether the node is a terminal node
        
        Returns:
        A boolean value: True if the current SyntacticNode is the terminal node,
        False otherwise
        """
        return self._type == SyntacticNode.TERMINAL
    
    def __str__(self):
        """Get the string representation of a node
        
        Returns:
        a string that represents a node (and all of its child nodes)
        Basically, the string represent the subtree at that node
        if a node is non-terminal, the label is used
        if a node is terminal, the label and the word is used
        """
        label = self._label
        if label == "(":
            label = "LRB"
        elif label == ")":
            label = "RRB"
        label = label.replace("(","<")
        label = label.replace(")",">")
        if self._type == SyntacticNode.TERMINAL:
            word = self._word.encode('ascii', 'ignore')
            if word == "(":
                word = "LRB"
            elif word == ")":
                word = "RRB"
            return "(%s %s)" %(label, word)
        else:
            if not self._children:
                return label
            else:
                child_string = ""
                for child in self._children:
                    child_string = child_string + " " + str(child)
                return "(%s%s)" %(label, child_string)
    
    def print_node(self, info_type):
        label = self._label
        if label == "(":
            label = "LRB"
        elif label == ")":
            label = "RRB"
        label = label.replace("(","<")
        label = label.replace(")",">")
        if self._type == SyntacticNode.TERMINAL:
            if info_type == SyntacticNode.LEMMA or info_type == SyntacticNode.LEMMA_POS:
                lemma = self._lemma.encode('ascii', 'ignore')
                if lemma == "(":
                    lemma = "lrb"
                elif lemma == ")":
                    lemma = "rrb"
                if info_type == SyntacticNode.LEMMA:
                    return "(%s (%s %s))" %(label, self._pos, lemma)
                else:
                    return "(%s (%s %s))" %(label, self._pos, "%s-%s" %(lemma, 
                                                                        SyntacticNode._get_short_pos(self._pos, lemma, label)))
            else:
                word = self._word.encode('ascii', 'ignore')
                if word == "(":
                    word = "LRB"
                elif word == ")":
                    word = "RRB"
                return "(%s (%s %s))" %(label, self._pos, word)
        else:
            if not self._children:
                return label
            else:
                child_string = ""
                for child in self._children:
                    child_string = child_string + " " + child.print_node(info_type)
                return "(%s%s)" %(label, child_string)
        
    
    def get_surface_string(self):
        if self.is_terminal():
            return self.word
        else:
            result = self.get_child(0).get_surface_string()
            for i in range(1,self.get_child_number()):
                result = result + " %s" %self.get_child(i).get_surface_string()
            return result
    
    
    # define all attributes    
    def get_label(self):
        return self._label
    label = property(get_label)
    
    # define all attributes    
    def get_type(self):
        return self._type
    type = property(get_type)
    
    def get_children(self):
        return self._children
    children = property(get_children)
    
    def get_lemma(self):
        if hasattr(self, '_lemma'):
            return self._lemma
        else:
            raise AttributeError("Node does not have lemma attribute")
    lemma = property(get_lemma)
        
    def get_word(self):
        if hasattr(self, '_word'):
            return self._word
        else:
            raise AttributeError("Node does not have word form attribute")
    def set_word(self, word):
        self._word = word
    word = property(get_word, set_word)
        
    def get_pos(self):
        if self._pos is not None:
            return self._pos
        else:
            raise AttributeError("Node does not have POS attribute")
    pos = property(get_pos)
        
