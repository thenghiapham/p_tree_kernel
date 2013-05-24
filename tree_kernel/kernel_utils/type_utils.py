'''
Created on Apr 16, 2013

@author: thenghiapham
'''
from numbers import Number
from numbers import Integral
import numpy as np

def is_numeric(operand):
    return isinstance(operand, (Number, np.number))

def is_integer(operand):
    return isinstance(operand, Integral)

def assert_type(instance, type_, message=""):
    if not isinstance(instance,type_):
        raise TypeError("%s\nexpect type: %s receive type:%s" %(message, type_,type(instance)))

