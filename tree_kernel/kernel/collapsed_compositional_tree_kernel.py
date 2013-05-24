'''
Created on May 20, 2013

@author: thenghiapham
'''
from syntactic_tree_kernel import SyntacticTreeKernel
from composes.similarity.cos import CosSimilarity
from utils.type_utils import assert_type
from tree.semantic_tree import SemanticTree
from tree.syntactic_node import SyntacticNode

class CollapsedCompositionalTreeKernel(SyntacticTreeKernel):
    '''
    Mixed Salad Kernel 2
    '''
    kernel_name = "mixed_salad_kernel2"

    def __init__(self, lambda_):
        '''
        Constructor
        '''
        self._lambda = lambda_
        self._measure = CosSimilarity()
        
    # default one
    def dot_product(self, tree1, tree2):
        assert_type(tree1, SemanticTree)
        assert_type(tree1, SemanticTree)
        return super(CollapsedCompositionalTreeKernel, self).dot_product(tree1, tree2)
    
    # new delta
    def _delta(self, node1, node2, node2id1, node2id2, delta_matrix):
        if node1._type == SyntacticNode.TERMINAL or node2._type == SyntacticNode.TERMINAL:
            delta_matrix[node2id1[node1],node2id2[node2]] = 0
        else:
            if (node1.is_pre_terminal() and node2.is_pre_terminal() 
                and node1._label == node2._label 
                and node1._children[0]._label == node2._children[0]._label): 
                    delta_matrix[node2id1[node1],node2id2[node2]] = 1
            elif not node1.has_same_production(node2):
                if node1._label != node2._label:
                    delta_matrix[node2id1[node1],node2id2[node2]] = 0
                else:
                    delta_matrix[node2id1[node1],node2id2[node2]] = ((self._lambda ** (max(node1.get_depth(),node2.get_depth()) - 1)) * 
                                                                     self._measure.get_sim(node1._vector, node2._vector))
            else:
                product_children_delta = self._lambda 
                for i in xrange(len(node1._children)):
                    child1 = node1.get_child(i)
                    child2 = node2.get_child(i)
                    child_delta = delta_matrix[node2id1[child1],node2id2[child2]]
                    if child_delta == -1:
                        raise ValueError("???")
                    else:
                        product_children_delta *= (1 + child_delta)
                
                sim_children_product = 1
                for i in xrange(len(node1._children)):
                    child1 = node1.get_child(i)
                    child2 = node2.get_child(i)
                    sim_children_product *= self._measure.get_sim(child1._vector, child2._vector)
                    
                final_delta = (product_children_delta + 
                               ((self._lambda ** (max(node1.get_depth(),node2.get_depth()) - 1)) * 
                                (self._measure.get_sim(node1._vector, node2._vector) - 
                                 sim_children_product)))
                 
                delta_matrix[node2id1[node1],node2id2[node2]] = final_delta
        