'''
Created on Apr 26, 2013

@author: thenghiapham
'''
from kernel import Kernel

class TreeKernel(Kernel):
    '''
    classdocs
    '''
    kernel_name = "abstract_tree_kernel"

    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def dot_product(self, tree1, tree2):
        raise NotImplementedError