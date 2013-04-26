'''
Created on Apr 26, 2013

@author: thenghiapham
'''
from syntactic_tree_kernel import SyntacticTreeKernel
from composes.semantic_space.space import Space
from utils.type_utils import assert_type

class SemanticSyntacticTreeKernel(SyntacticTreeKernel):
    '''
    classdocs
    '''


    def __init__(self, lambda_, lexical_space):
        '''
        Constructor
        '''
        super(SemanticSyntacticTreeKernel, self, lambda_)
        assert_type(lexical_space, Space, "lexical_space must be of type Space")
        self._lexical_space = lexical_space
    
    def _delta(self, node1, node2, node2id1, node2id2, delta_matrix):
        if (node1.is_pre_terminal() and node2.is_pre_terminal() 
            and node1._label == node2._label):
            delta_matrix[node2id1[node1],node2id2[node2]] = self._lexical_space.get_sim(node1.get_child(0)._label,
                                                                                        node2.get_child(0)._label)
        else:
            SyntacticTreeKernel._delta(self, node1, node2, node2id1, node2id2, delta_matrix)
    