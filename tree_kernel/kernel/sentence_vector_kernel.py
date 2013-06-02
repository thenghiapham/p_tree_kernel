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


    def __init__(self, similarity=CosSimilarity()):
        '''
        Constructor
        '''
        self._similarity = similarity
    
    def dot_product(self, tree1, tree2):
        assert_type(tree1, SemanticTree)
        assert_type(tree2, SemanticTree)
        return self._similarity(tree1._root._vector, tree2._root._vector)
    