'''
Created on Jun 2, 2013

@author: nghia
'''
from kernel import Kernel
from kernel_utils.type_utils import assert_type
from tree.semantic_tree import SemanticTree
from composes.similarity.cos import CosSimilarity

class SentenceVectorKernel(Kernel):
    '''
    classdocs
    '''
    kernel_name = "sentence_vector_kernel"

    def __init__(self, similarity=CosSimilarity()):
        '''
        Constructor
        '''
        self._similarity = similarity
    
    def dot_product(self, tree1, tree2):
        assert_type(tree1, SemanticTree)
        assert_type(tree2, SemanticTree)
        sentence_vector1 = tree1._root._vector
        sentence_vector2 = tree2._root._vector
        if sentence_vector1.norm() == 0.0 or sentence_vector2.norm() == 0.0:
            return 0.0
        else:
            return self._similarity(sentence_vector1, sentence_vector2)
    