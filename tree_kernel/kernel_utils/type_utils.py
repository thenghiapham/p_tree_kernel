'''
Created on Apr 16, 2013

@author: thenghiapham
'''
from numbers import Number
from numbers import Integral
import numpy as np

def is_numeric(operand):
    '''Check whether the parameter is of numeric type (python numeric or numpy 
    numeric)
    
    Args:
        operand: the input parameter
    Returns:
        a boolean value: True if operand is numeric, False otherwise
    '''
    return isinstance(operand, (Number, np.number))

def is_integer(operand):
    '''Check whether the parameter is an integer (int, long, )
    
    Args:
        operand: the input parameter
    Returns:
        a boolean value: True if operand is an integer, False otherwise
    '''
    return isinstance(operand, Integral)

def assert_type(instance, type_, message=""):
    '''Assert whether an object belong to a type/class
    
    Args:
        instance: the input object
        type_: the wanted type
    Raises:
        TypeError when instance does not belong to type_
    '''
    if not isinstance(instance,type_):
        raise TypeError("%s\nexpect type: %s receive type:%s" %(message, type_,type(instance)))

