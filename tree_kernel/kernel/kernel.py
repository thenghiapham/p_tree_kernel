'''
Created on Apr 26, 2013

@author: thenghiapham
'''

class Kernel(object):
    '''
    classdocs
    '''
    kernel_name = "abstract_kernel"

    def __init__(self):
        '''
        Constructor
        '''
        raise NotImplementedError()
    
    def dot_product(self, s1, s2):
        raise NotImplementedError()