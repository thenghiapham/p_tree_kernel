'''
Created on Apr 26, 2013

@author: thenghiapham
'''
import numpy as np
from tree_kernel import TreeKernel
from utils.type_utils import assert_type, is_numeric
from tree.syntactic_tree import SyntacticTree
from utils.data_structure_utils import list2dict
from tree.syntactic_node import SyntacticNode


class SyntacticTreeKernel(TreeKernel):
    '''
    classdocs
    '''
    kernel_name = "syntactic_kernel"

    def __init__(self, lambda_):
        '''
        Constructor
        '''
        if is_numeric(lambda_):
            self._lambda = lambda_
        else:
            raise ValueError("lambda must be a real number")
    
    def dot_product(self, tree1, tree2):
        assert_type(tree1, SyntacticTree)
        assert_type(tree2, SyntacticTree)
        all_nodes1 = tree1.get_nodes()
        all_nodes1.reverse()
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
        return delta_matrix.sum()
    
    def _delta(self, node1, node2, node2id1, node2id2, delta_matrix):
        if node1._type == SyntacticNode.TERMINAL or node2._type == SyntacticNode.TERMINAL:
            delta_matrix[node2id1[node1],node2id2[node2]] = 0
        else:
            if (node1.is_pre_terminal() and node2.is_pre_terminal() 
                and node1._label == node2._label 
                and node1._children[0]._label == node2._children[0]._label): 
                    delta_matrix[node2id1[node1],node2id2[node2]] = 1
            elif not node1.has_same_production(node2):
                delta_matrix[node2id1[node1],node2id2[node2]] = 0
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
                delta_matrix[node2id1[node1],node2id2[node2]] = product_children_delta
                
def test():
    print "hello"
    syntactic_tree1 = SyntacticTree.read_tree("VP (VBZ kill) (NP (N man))")
    syntactic_tree2 = SyntacticTree.read_tree("VP (VBZ murder) (NP (N man))")
    kernel = SyntacticTreeKernel(1.0)
    print syntactic_tree1
    print syntactic_tree2
    print [node._label for node in syntactic_tree1.get_nodes()] 
    print [node._label for node in syntactic_tree2.get_nodes()]
    print "kernel:\n", kernel.dot_product(syntactic_tree1, syntactic_tree1)   
    print "kernel:\n", kernel.dot_product(syntactic_tree1, syntactic_tree2)              

if __name__ == '__main__':
    test()