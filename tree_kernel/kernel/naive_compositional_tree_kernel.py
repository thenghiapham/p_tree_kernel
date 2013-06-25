'''
Created on Apr 29, 2013

@author: thenghiapham
'''
from syntactic_tree_kernel import SyntacticTreeKernel
from kernel_utils.type_utils import assert_type
from tree.semantic_tree import SemanticTree
from composes.similarity.cos import CosSimilarity

class NaiveCompositionalSemanticTreeKernel(SyntacticTreeKernel):
    '''
    Mixed Salad Kernel 1
    '''
    kernel_name = "mixed_salad_kernel1"
    
    NO_COMPATIBILITY = 0
    LABEL_COMPATIBILITY = 1

    def __init__(self, lambda_, compatibility_level = LABEL_COMPATIBILITY):
        '''
        Constructor
        '''
        self._lambda = lambda_
        self._compatibility_level = compatibility_level
        self._measure = CosSimilarity()
    
    def dot_product(self, tree1, tree2):
        assert_type(tree1, SemanticTree)
        assert_type(tree2, SemanticTree)
        return super(NaiveCompositionalSemanticTreeKernel, self).dot_product(tree1, tree2)
    
    def _delta(self, node1, node2, node2id1, node2id2, delta_matrix):
        delta = 0
        if (self._compatibility_level == NaiveCompositionalSemanticTreeKernel.NO_COMPATIBILITY or
            (self._compatibility_level == NaiveCompositionalSemanticTreeKernel.LABEL_COMPATIBILITY and
             node1._label == node2._label)):
            delta = ((self._lambda ** (node1.get_height() + node2.get_height())) 
                     *self._measure.get_sim(node1._vector, node2._vector))
        delta_matrix[node2id1[node1],node2id2[node2]] = delta
    
    
        
            
        