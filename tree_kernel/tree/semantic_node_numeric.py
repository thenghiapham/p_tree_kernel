'''
Created on Apr 29, 2013

@author: nghia
'''
from tree.syntactic_node import SyntacticNode
import numpy as np
#from composes.matrix.matrix import Matrix
from composes.matrix.dense_matrix import DenseMatrix
from composes.matrix.linalg import Linalg
from kernel_utils.type_utils import assert_type
import re
from tree.temp_marco_numeric import insert_terminal_node_representation

class SemanticNode(SyntacticNode):
    '''
    An instance of this class represents a node in a semantic tree (CCG or PSG
    tree)
    
    A semantic node has all the attributes of a syntactic node and one extra
    attribute:
    vector: the vector representation of the node (phrase)
    '''


    def __init__(self, label, matrep, numrep, *args, **kwargs):
        '''
        Constructor
        
        Args:
            label<string>: the label (cat in CCG tree) of the node	
            vector<composes.matrix.matrix.Matrix>: the vector represention of 
                the node
            kwargs: see the constructor of a syntactic node
        '''
        
        super(SemanticNode, self).__init__(label, *args, **kwargs)
        
	
	self._matrep = matrep
	self._numrep = numrep
        
    @classmethod
    def create_semantic_node(cls, syntactic_node, vecspace, matspace):
        """Create a semantic node from a syntactic node and its vector 
        representation

        Args:
            syntactic_node: a syntatic_node
            vector: a vector representation for the node/phrase
        
        Returns:
            the semantic node, this node has all the information of the syntactic 
            node, except for the child nodes
        """
        
        label = syntactic_node.label
        
        # if the syntactic node is  terminal node, copy the information (also
        # copy lemma attribute if present)
        if SyntacticNode.is_terminal(syntactic_node):
            word = syntactic_node.word
            pos = syntactic_node.pos
            # TODO: does this work with "lemma"?
	#Denis's addition
	    matrep,temp_numrep=insert_terminal_node_representation(syntactic_node,vecspace,matspace,use_wordform=0)
	    if temp_numrep[0] == "empty":
	    	numrep = []
	    else:
		    numrep = [temp_numrep[0].transpose()]
		    dimensionality=(temp_numrep[0].shape[1])
		    if len(temp_numrep)>1:
			    for x in range(1, (len(temp_numrep))):
				y = DenseMatrix(temp_numrep[x])
				y.reshape((3,3))
				numrep.append(y)
            if hasattr(syntactic_node, "_lemma"):
                lemma = syntactic_node.lemma
                semantic_node = SemanticNode(label, matrep,numrep, word=word, pos=pos, lemma=lemma)
            else:
                semantic_node = SemanticNode(label,matrep,numrep, word=word, pos=pos)
                
        else:
            semantic_node = SemanticNode(label,[], [])
	for child in syntactic_node._children:
		semantic_node.add_child(SemanticNode.create_semantic_node(child,vecspace,matspace))
        return semantic_node
        
    
    def add_child(self, child):
        """Add a child SemanticNode to a SemanticNode.
        This method overrides the add_child method from SyntacticNode to
        enforce the constraint that the child parameter must be a SemanticNode

        Args:
        child: the child SemanticNode
        """
        assert_type(child, SemanticNode)
        SyntacticNode.add_child(self, child)
        
        
    # define properties    
    def get_vector(self):
	numrep = self.get_numrep()
	if numrep != []: vector = numrep[0].transpose()
	else: vector = None
        if vector is not None:
            assert_type(vector, Matrix, "argument vector needs to be of type Matrix")
        self._vector = vector
        if self._vector is not None:
            return self._vector
        else:
            raise AttributeError("Node does not have word form attribute")

    def set_vector(self, vector):
        self._vector = vector
    vector = property(get_vector, set_vector)

    def get_matrep(self):
	if len(self._children) == 1:
			self._matrep = self.get_child(0).get_matrep()
	if len(self._children) == 2 and self._matrep == []:
		matrep1=self.get_child(0).get_matrep()
		matrep2=self.get_child(1).get_matrep()
		arity1=len(matrep1)-1
		arity2=len(matrep2)-1
		if arity1-arity2 == 0:
			for x in range(0, arity1 +1):
				self._matrep.append('(' + matrep1[x] + '+' + matrep2[x] + ')')
		if arity1 < arity2 and not re.search('empty$',matrep2[0]):
			for x in range(0, arity2):
				if x == 0:
					self._matrep.append('(' + matrep2[x] + '+' + matrep2[arity2] + '*' + matrep1[x] + ')')
				elif x < len(matrep1):
					self._matrep.append('(' + matrep2[x] + '*' + matrep1[x] + ')')
				else:
					self._matrep.append(matrep2[x])
		if arity1 > arity2 and not re.search('empty$',matrep1[0]):
			for x in range(0, arity1):
				if x == 0:
					self._matrep.append('(' + matrep1[x] + '+' + matrep1[arity1] + '*' + matrep2[x] + ')')
				elif x < len(matrep2):
					self._matrep.append('(' + matrep1[x] + '*' + matrep2[x] + ')')
				else:
					self._matrep.append(matrep1[x])
		if re.search('empty$',matrep1[0]): self._matrep = matrep2
		if re.search('empty$',matrep2[0]): self._matrep = matrep1

	if len(self._children)>2:
		raise ValueError("Matrix representations are not defined for trees with more than binary branching")
	return self._matrep
    matrep = property(get_matrep)

    def get_numrep(self):
        if len(self._children) == 1:
                        self._numrep = self.get_child(0).get_numrep()
        if len(self._children) == 2 and self._numrep == []:
                matrep1=self.get_child(0).get_numrep()
                matrep2=self.get_child(1).get_numrep()
                arity1=len(matrep1)-1
                arity2=len(matrep2)-1
                if arity1-arity2 == 0:
                        for x in range(0, arity1 +1):
                                self._numrep.append(matrep1[x].__add__(matrep2[x]))
                if arity1 < arity2 and not matrep1==[]:
                        for x in range(0, arity2):
                                if x == 0:
                                        self._numrep.append(matrep2[x].__add__(matrep2[arity2] * matrep1[x]))
                                elif x < len(matrep1):
                                        self._numrep.append(matrep2[x] * matrep1[x])
                                else:
                                        self._numrep.append(matrep2[x])
		if arity1 > arity2 and not matrep2==[]:
                        for x in range(0, arity1):
                                if x == 0:
                                        self._numrep.append(matrep1[x].__add__(matrep1[arity1]*matrep2[x]))
                                elif x < len(matrep2):
                                        self._numrep.append(matrep1[x] * matrep2[x])
                                else:
                                        self._numrep.append(matrep1[x])
                if (matrep1 == []): self._numrep = matrep2
                if (matrep2 == []): self._numrep = matrep1
	#if self._numrep != []:
                #if re.search('empty$',self._numrep[0]): self._vector = None
		#else: self._vector = self._numrep[0]
        if len(self._children)>2:
                raise ValueError("Matrix representations are not defined for trees with more than binary branching")
	return self._numrep
    numrep = property(get_numrep)

