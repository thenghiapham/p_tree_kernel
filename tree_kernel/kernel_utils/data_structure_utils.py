'''
Created on Apr 26, 2013

@author: thenghiapham
'''

def list2dict(list_):
    """get the dictionary to access the indices of elements in a list  

    Args:
    list_: the input list
    
    Returns:
    The dictionary: where the keys are the elements of the input list, the 
    values are the indices of the elements in the list.
    E.g.
        if the input list is ["a","b","c"], the output dictionary will be
        {"a":0,"c":2,"b":1}
    """
    return_dict = {}
    
    for idx, word in enumerate(list_):
        if word in return_dict:
            raise ValueError("duplicate string found in list: %s" % (word)) 
        return_dict[word] = idx

    return return_dict