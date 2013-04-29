'''
Created on Apr 29, 2013

@author: thenghiapham
'''
from syntactic_tree_kernel import SyntacticTreeKernel
from utils.type_utils import assert_type
from tree.semantic_tree import SemanticTree
from composes.similarity.cos import CosSimilarity

class NaiveCompositionalSemanticTreeKernel(SyntacticTreeKernel):
    '''
    classdocs
    '''
    
    NO_COMPATIBILITY = 0
    LABEL_COMPATIBILITY = 1

    def __init__(self, lambda_, compatibility_level):
        '''
        Constructor
        '''
        self._lambda = lambda_
        self._compatibility_level = compatibility_level
        self._measure = CosSimilarity()
    
    def dot_product(self, tree1, tree2):
        assert_type(tree1, SemanticTree)
        assert_type(tree1, SemanticTree)
        return super(NaiveCompositionalSemanticTreeKernel, self).dot_product(tree1, tree2)
    
    def _delta(self, node1, node2, node2id1, node2id2, delta_matrix):
        delta = 0
        if (self._compatibility_level == NaiveCompositionalSemanticTreeKernel.NO_COMPATIBILITY or
            (self._compatibility_level == NaiveCompositionalSemanticTreeKernel.LABEL_COMPATIBILITY and
             node1._label == node2._labe)):
            delta = self._measure.get_sim(node1._vector, node2._vector)
        delta_matrix[node2id1[node1],node2id2[node2]] = delta
        
            
        