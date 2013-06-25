'''
Created on Apr 29, 2013

@author: nghia
'''
from tree.syntactic_node import SyntacticNode
from composes.matrix.matrix import Matrix
from kernel_utils.type_utils import assert_type

class SemanticNode(SyntacticNode):
    '''
    classdocs
    '''


    def __init__(self, label, vector, *args, **kwargs):
        '''
        Constructor
        '''
        
        super(SemanticNode, self).__init__(label, args, kwargs)
        
        if vector is not None:
            assert_type(vector, Matrix, "argument vector needs to be of type Matrix")
        self._vector = vector
        
    @classmethod
    def create_semantic_node(cls, syntactic_node, vector):
        label = syntactic_node.label
        if syntactic_node.is_terminal():
            word = syntactic_node.word
            pos = syntactic_node.pos
            # TODO: does this work with "lemma"?
            if hasattr(syntactic_node, "lemma"):
                lemma = syntactic_node.lemma
                return SemanticNode(label,vector, word=word, pos=pos, lemma=lemma)
            else:
                return SemanticNode(label,vector, word=word, pos=pos)
                
        else:
            return SemanticNode(label,vector)
        
    
    def add_child(self, child):
        assert_type(child, SemanticNode)
        SyntacticNode.add_child(self, child)
        
    def get_vector(self):
        if self._vector is not None:
            return self._vector
        else:
            raise AttributeError("Node does not have word form attribute")
    def set_vector(self, vector):
        self._vector = vector
    vector = property(get_vector, set_vector)