'''
Created on Apr 26, 2013

@author: thenghiapham
'''
from syntactic_tree_kernel import SyntacticTreeKernel
from tree.semantic_tree import SemanticTree
from kernel_utils.type_utils import assert_type

from composes.similarity.cos import CosSimilarity

class SemanticTreeKernel(SyntacticTreeKernel):
    '''
    classdocs
    '''
    kernel_name = "semantic_kernel"

    def __init__(self, lambda_):
        '''
        Constructor
        '''
        super(SemanticTreeKernel, self).__init__(lambda_)
    
    # standard kernel
    
        # default one
    def dot_product(self, tree1, tree2):
        assert_type(tree1, SemanticTree)
        assert_type(tree2, SemanticTree)
        return super(SemanticTreeKernel, self).dot_product(tree1, tree2)
    
    def _delta(self, node1, node2, node2id1, node2id2, delta_matrix):
        if (node1.is_pre_terminal() and node2.is_pre_terminal() 
            and node1._label == node2._label):
            if node1._children[0]._label == node2._children[0]._label: 
                delta_matrix[node2id1[node1],node2id2[node2]] = 1
            else:
                delta_matrix[node2id1[node1],node2id2[node2]] = CosSimilarity().get_sim(node1._vector,
                                                                                        node2._vector)
        else:
            SyntacticTreeKernel._delta(self, node1, node2, node2id1, node2id2, delta_matrix)
        
                