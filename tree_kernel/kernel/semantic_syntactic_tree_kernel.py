'''
Created on Apr 26, 2013

@author: thenghiapham
'''
from syntactic_tree_kernel import SyntacticTreeKernel
from tree.syntactic_tree import SyntacticTree
from kernel_utils.type_utils import assert_type

from composes.semantic_space.space import Space
from composes.utils import io_utils
from composes.similarity.cos import CosSimilarity

class SemanticSyntacticTreeKernel(SyntacticTreeKernel):
    '''
    classdocs
    '''
    kernel_name = "semantic_kernel"

    def __init__(self, lambda_, lexical_space):
        '''
        Constructor
        '''
        super(SemanticSyntacticTreeKernel, self).__init__(lambda_)
        assert_type(lexical_space, Space, "lexical_space must be of type Space")
        self._lexical_space = lexical_space
    
    
    # standard kernel
    def _delta(self, node1, node2, node2id1, node2id2, delta_matrix):
        if (node1.is_terminal() and node2.is_terminal() 
            and node1._label == node2._label):
            if node1._word == node2._word: 
                delta_matrix[node2id1[node1],node2id2[node2]] = 1
            else:
                delta_matrix[node2id1[node1],node2id2[node2]] = self._lexical_space.get_sim(node1._word,
                                                                                        node2._word,CosSimilarity())
        else:
            SyntacticTreeKernel._delta(self, node1, node2, node2id1, node2id2, delta_matrix)
        
            
def test():
    print "hello"
    syntactic_tree1 = SyntacticTree.read_tree("VP (VBZ play-v) (NP (N guitar-n))")
    syntactic_tree2 = SyntacticTree.read_tree("VP (VBZ play-v) (NP (N instrument-n))")
    lexical_space = io_utils.load("/home/thenghiapham/work/project/tree_kernel/spaces/lexical_ppmi_svd300.pkl")
    kernel = SemanticSyntacticTreeKernel(1.0, lexical_space)
    print syntactic_tree1
    print syntactic_tree2
    print [node._label for node in syntactic_tree1.get_nodes()] 
    print [node._label for node in syntactic_tree2.get_nodes()]
    print "kernel:\n", kernel.dot_product(syntactic_tree1, syntactic_tree1)   
    print "kernel:\n", kernel.dot_product(syntactic_tree1, syntactic_tree2)   

if __name__ == '__main__':
    test()
    