'''
Created on Apr 29, 2013

@author: thenghiapham
'''
from syntactic_tree_kernel import SyntacticTreeKernel
from utils.type_utils import assert_type
from tree.semantic_tree import SemanticTree
from composes.similarity.cos import CosSimilarity
from tree.syntactic_node import SyntacticNode
from utils.data_structure_utils import list2dict
import numpy as np

class NaiveCompositionalSemanticTreeKernel(SyntacticTreeKernel):
    '''
    Mixed Salad Kernel 1
    '''
    kernel_name = "mixed_salad_kernel1"
    
    NO_COMPATIBILITY = 0
    LABEL_COMPATIBILITY = 1

    def __init__(self, lambda_, compatibility_level = NaiveCompositionalSemanticTreeKernel.LABEL_COMPATIBILITY):
        '''
        Constructor
        '''
        self._lambda = lambda_
        self._compatibility_level = compatibility_level
        self._measure = CosSimilarity()
    
    '''
    # testing one
    def dot_product(self, tree1, tree2):
        assert_type(tree1, SemanticTree)
        all_nodes1 = tree1.get_nodes()
        all_nodes1.reverse()
        assert_type(tree2, SemanticTree)
        all_nodes2 = tree2.get_nodes()
        all_nodes2.reverse()
        node2id1 = list2dict(all_nodes1)
        node2id2 = list2dict(all_nodes2)
        delta_matrix = - np.ones((len(all_nodes1),len(all_nodes2)), np.float)
        #print "\n",delta_matrix
        for node1 in all_nodes1:
            for node2 in all_nodes2:
                self._delta(node1, node2, node2id1, node2id2, delta_matrix)
        #print delta_matrix
        return delta_matrix[-1,-1]
    '''
    
    # default one
    def dot_product(self, tree1, tree2):
        assert_type(tree1, SemanticTree)
        assert_type(tree1, SemanticTree)
        return super(NaiveCompositionalSemanticTreeKernel, self).dot_product(tree1, tree2)
    
    def _delta(self, node1, node2, node2id1, node2id2, delta_matrix):
        delta = 0
        if node1._type == SyntacticNode.TERMINAL or node2._type == SyntacticNode.TERMINAL:
            delta = 0
        elif (self._compatibility_level == NaiveCompositionalSemanticTreeKernel.NO_COMPATIBILITY or
            (self._compatibility_level == NaiveCompositionalSemanticTreeKernel.LABEL_COMPATIBILITY and
             node1._label == node2._label)):
            delta = ((self._lambda ** (node1.get_depth() + node2.get_depth())) 
                     *self._measure.get_sim(node1._vector, node2._vector))
        delta_matrix[node2id1[node1],node2id2[node2]] = delta
    
    
        
            
        