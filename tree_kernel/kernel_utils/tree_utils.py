'''
Created on Apr 29, 2013

@author: nghia
'''

from tree.semantic_tree import SemanticTree
from tree.semantic_node import SemanticNode
from tree.syntactic_tree import SyntacticTree
from tree.syntactic_node import SyntacticNode
from kernel_utils.type_utils import assert_type
from composes.transformation.scaling.row_normalization import RowNormalization
import numpy as np
from composes.matrix.dense_matrix import DenseMatrix

def penn_pos_2_simple_pos(penn_pos):
    """
    try:
        simple_pos = pos_map[penn_pos]
        
    except KeyError:
        simple_pos = "?"
    """
    simple_pos = penn_pos[0].lower()
    if not simple_pos in "abcdefghijklmnopqrstuvwxyz":
        simple_pos = "x"
    return simple_pos 

def syntactic_tree_2_semantic_tree(syntactic_tree, vector_space, composition_model, normed=True):
    assert_type(syntactic_tree, SyntacticTree)
    return SemanticTree(_syntactic_node_2_semantic_node(syntactic_tree._root,
                                                         vector_space, composition_model))
def _syntactic_node_2_semantic_node(syntactic_node, vector_space, composition_model, normed=True):
    
    if syntactic_node._type == SyntacticNode.TERMINAL:
        return SemanticNode(syntactic_node._label, None, SyntacticNode.TERMINAL)
    else:
        new_node = SemanticNode(syntactic_node._label, None)
        for child in syntactic_node._children:
            new_child = _syntactic_node_2_semantic_node(child, vector_space, composition_model)
            new_node.add_child(new_child)
            
        if syntactic_node.is_pre_terminal():
            try:
                row_vector = vector_space.get_row(syntactic_node._children[0]._label)
                if normed:
                    new_node._vector = RowNormalization().apply(row_vector)
                else:
                    new_node._vector = row_vector
            except KeyError:
                    new_node._vector = DenseMatrix(np.zeros((1,vector_space.cooccurrence_matrix.shape[1]),
                                                            dtype=np.float))
        else:
            new_vector = new_node.get_child(0)._vector
            # print new_node
            for i in range(1,len(new_node._children)):
                new_vector = composition_model._compose(new_vector,new_node.get_child(i)._vector)
            if normed:
                new_node._vector = RowNormalization().apply(new_vector)
            else:
                new_node._vector = new_vector
        return new_node

def lemma_tree_2_lemmapos_tree(syntactic_tree):
    assert_type(syntactic_tree, SyntacticTree)
    return SyntacticTree(_lemma_tree_2_lemmapos_tree(syntactic_tree._root, None))

def _lemma_tree_2_lemmapos_tree(syntactic_node, parent_node):
    if syntactic_node._type == SyntacticNode.TERMINAL:
        return SyntacticNode(syntactic_node._label.lower() + "-" + penn_pos_2_simple_pos(parent_node._label),
                             SyntacticNode.TERMINAL)
    else:
        new_node = SyntacticNode(syntactic_node._label, syntactic_node._type)
        for child in syntactic_node._children:
            new_child = _lemma_tree_2_lemmapos_tree(child, syntactic_node)
            new_node.add_child(new_child)
            
        return new_node
    