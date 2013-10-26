'''
Created on Apr 29, 2013

@author: nghia
'''
import numpy as np
from tree.semantic_tree import SemanticTree
from tree.semantic_node import SemanticNode
from tree.syntactic_tree import SyntacticTree
from kernel_utils.type_utils import assert_type

from composes.transformation.scaling.row_normalization import RowNormalization
from composes.composition.weighted_additive import WeightedAdditive
from composes.composition.multiplicative import Multiplicative


def syntactic_tree_2_semantic_tree(syntactic_tree, vector_space, 
                                   composition_model, normed=True):
    """Create a SemanticTree from a SyntacticTree
    
    Args:
        syntactic_tree: the input syntatic_tree
        vector_space: a vector space where the lexical vectors can be retrieved
        composition_model: the compositional model, with which the vector
            representations of phrases are computed (the compositional model
            should be either WeightedAdditive, Multiplicative or FullAdditive)
        normed: a boolean value indicating whether the lexical vectors should be
            normalized or not
        
    Returns:
        the semantic tree
    """
    
    assert_type(syntactic_tree, SyntacticTree)
    return SemanticTree(_syntactic_node_2_semantic_node(syntactic_tree._root,
                                                         vector_space,
                                                         composition_model, normed))
    
def _syntactic_node_2_semantic_node(syntactic_node, vector_space,
                                    composition_model, normed=True):
    """Create a SemanticNode from a SyntacticNode recursively
    
    Args:
        syntactic_node: the input syntatic_node
        vector_space: a vector space where the lexical vectors can be retrieved
        composition_model: the compositional model, with which the vector
            representations of phrases are computed (the compositional model
            should be either WeightedAdditive, Multiplicative or FullAdditive)
        normed: a boolean value indicating whether the lexical vectors should be
            normalized or not
        
    Returns:
        the semantic node
    """
    
    new_node = SemanticNode.create_semantic_node(syntactic_node, None)
    
    # if the node is a terminal node:
    #   - retrieve the lexical vector
    # if the node is non-terminal
    #   - recursively apply this function to the child nodes to get the vector
    #     representations of the child nodes
    #   - use the composition model, and the vectors of the children to compute
    #     the vector of the current node
    # 
    if syntactic_node.is_terminal():
        try:
            row_vector = vector_space.get_row(syntactic_node._word)
            if normed:
                new_node._vector = RowNormalization().apply(row_vector)
                print "shouldn't be here"
            else:
                new_node._vector = row_vector
            # print new_node._vector
        except KeyError:
            #print "missing word:", syntactic_node._word
            matrix_type = type(vector_space.cooccurrence_matrix)
            vector_shape = (1,vector_space.cooccurrence_matrix.shape[1])
            if isinstance(composition_model, Multiplicative):
                new_node._vector =  matrix_type(np.ones(vector_shape,
                                                         dtype=np.float))
            else:
                new_node._vector =  matrix_type(np.zeros(vector_shape,
                                                         dtype=np.float))
    else:
        for child in syntactic_node._children:
            new_child = _syntactic_node_2_semantic_node(child, vector_space,
                                                        composition_model, normed)
            new_node.add_child(new_child)
        
        new_vector = new_node.get_child(0).vector
        # print new_node
        for i in range(1,len(new_node._children)):
            new_vector = composition_model._compose(new_vector,
                                                    new_node.get_child(i).vector)
        
        new_node.vector = new_vector
    #print syntactic_node.get_surface_string()
    #print new_node.vector[0,0]
    return new_node

def penn_pos_2_simple_pos(penn_pos):
    simple_pos = penn_pos[0].lower()
    if not simple_pos in "abcdefghijklmnopqrstuvwxyz":
        simple_pos = "x"
    return simple_pos


def lemma_tree_2_lemmapos_tree(syntactic_tree, excluded_poss = {}):
    assert_type(syntactic_tree, SyntacticTree)
    return SyntacticTree(_lemma_tree_2_lemmapos_tree(syntactic_tree._root,
                                                     excluded_poss))

def _lemma_tree_2_lemmapos_tree(syntactic_node, excluded_poss):
    new_node = syntactic_node.copy()
    if syntactic_node.is_terminal():
        simple_pos = penn_pos_2_simple_pos(syntactic_node._pos)
        if simple_pos in excluded_poss:
            new_node.word = syntactic_node.word.lower()
        else:
            new_node.word = syntactic_node.word.lower() + "-" + simple_pos
    else:
        for child in syntactic_node._children:
            new_child = _lemma_tree_2_lemmapos_tree(child, excluded_poss)
            new_node.add_child(new_child)
            
    return new_node
    