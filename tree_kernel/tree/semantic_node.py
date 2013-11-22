'''
Created on Apr 29, 2013

@author: nghia
'''
from tree.syntactic_node import SyntacticNode
from composes.matrix.matrix import Matrix
from kernel_utils.type_utils import assert_type

class SemanticNode(SyntacticNode):
    '''
    An instance of this class represents a node in a semantic tree (CCG or PSG
    tree)
    
    A semantic node has all the attributes of a syntactic node and one extra
    attribute:
    vector: the vector representation of the node (phrase)
    '''


    def __init__(self, label, vector, *args, **kwargs):
        '''
        Constructor
        
        Args:
            label<string>: the label (cat in CCG tree) of the node
            vector<composes.matrix.matrix.Matrix>: the vector represention of 
                the node
            kwargs: see the constructor of a syntactic node
        '''
        
        super(SemanticNode, self).__init__(label, *args, **kwargs)
        
        if vector is not None:
            assert_type(vector, Matrix, "argument vector needs to be of type Matrix")
        self._vector = vector
        
    @classmethod
    def create_semantic_node(cls, syntactic_node, vector):
        """Create a semantic node from a syntactic node and its vector 
        representation

        Args:
            syntactic_node: a syntatic_node
            vector: a vector representation for the node/phrase
        
        Returns:
            the semantic node, this node has all the information of the syntactic 
            node, except for the child nodes
        """
        
        label = syntactic_node.label
        
        # if the syntactic node is a terminal node, copy the information (also
        # copy lemma attribute if present)
        if syntactic_node.is_terminal():
            word = syntactic_node.word
            pos = syntactic_node.pos
            # TODO: does this work with "lemma"?
            if hasattr(syntactic_node, "_lemma"):
                lemma = syntactic_node.lemma
                semantic_node = SemanticNode(label,vector, word=word, pos=pos, lemma=lemma)
            else:
                semantic_node = SemanticNode(label,vector, word=word, pos=pos)
                
        else:
            semantic_node = SemanticNode(label,vector)
            for child in syntactic_node._children:
                semantic_node.add_child(SemanticNode.create_semantic_node(child,None))
        return semantic_node
        
    
    def add_child(self, child):
        """Add a child SemanticNode to a SemanticNode.
        This method overrides the add_child method from SyntacticNode to
        enforce the constraint that the child parameter must be a SemanticNode

        Args:
        child: the child SemanticNode
        """
        assert_type(child, SemanticNode)
        SyntacticNode.add_child(self, child)
        
        
    # define properties    
    def get_vector(self):
        if self._vector is not None:
            return self._vector
        else:
            raise AttributeError("Node does not have vector attribute")
    def set_vector(self, vector):
        self._vector = vector
    vector = property(get_vector, set_vector)
