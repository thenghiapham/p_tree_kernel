from __future__ import print_function
import numpy as np
from node import Node
from kernel_utils import type_utils
from tree.syntactic_tree import SyntacticTree
from xml.etree.ElementTree import ParseError
from composes.matrix.dense_matrix import DenseMatrix
from composes.matrix.linalg import Linalg
from kernel_utils.type_utils import assert_type
import re
import sys
from composes.semantic_space.space import Space
from composes.utils import io_utils
from tree.semantic_node import SemanticNode
 
class Papfunc_SemanticNode(SemanticNode):
 '''
 An instance of this class is a semantic tree that has with matrix representations (symbolic and numeric) computed in the papernization composition paradigm.
 '''
 def __init__(self, label, vector, *args, **kwargs):
        super(SemanticNode, self).__init__(label, *args, **kwargs)
        if vector is not None:
            assert_type(vector, Matrix, "argument vector needs to be of type Matrix")
        self._vector = vector
        self._matrep = []
        self._numrep = []

 def get_matrep(self):
        if self._matrep is not None:
            return self._matrep
        else:
            raise AttributeError("Node does not have symbolic matrix representation (matrep) attribute")
 def set_matrep(self, matrep):
        self._matrep = matrep
 matrep = property(get_matrep, set_matrep)

 def get_numrep(self):
        if self._numrep is not None:
            return self._numrep
        else:
            raise AttributeError("Node does not have a numeric matrix representation (numrep) attribute")
 def set_numrep(self, numrep):
        self._numrep = numrep
 numrep = property(get_numrep, set_numrep)

 @classmethod
 def create_papfunc_node(cls, semantic_node, vecspace, matspace,multiply_matrices=False):
  '''
  Create a Papfunc semantic node from a semantic node, a vector space, and a space of (flattened) matrices. An optional Boolean argument, if set to True, makes matrices to be multiplied rather than summed when both subconstituents have arity greater than 0.
  '''
  label = semantic_node.label
  if semantic_node.is_terminal():
            word = semantic_node.word
            pos = semantic_node.pos
            if hasattr(semantic_node, "_lemma"):
                lemma = semantic_node.lemma
                papfunc_node = Papfunc_SemanticNode(label,None, word=word, pos=pos, lemma=lemma)
            else:
                papfunc_node = Papfunc_SemanticNode(label,None, word=word, pos=pos)
                
  else:
        papfunc_node = Papfunc_SemanticNode(label,None)
        if semantic_node._children and not semantic_node.is_terminal():
         print(semantic_node)
         for child in semantic_node._children:
          print(child)
          assert_type(child, SemanticNode, "argument needs to be of type SemanticNode")
          papfunc_child=Papfunc_SemanticNode.create_papfunc_node(child, vecspace, matspace,multiply_matrices=multiply_matrices)
          print(papfunc_child)
          papfunc_node.add_child(papfunc_child)
  papfunc_node.compute_matreps(vecspace,matspace,multiply_matrices=multiply_matrices)
  papfunc_node.set_vector(papfunc_node._numrep[0].transpose())
  return papfunc_node

 def add_child(self, child):
        """Add a child Papfunc_SemanticNode to a Papfunc_SemanticNode.
        This method overrides the add_child method from SemanticNode to
        enforce the constraint that the child parameter must be a Papfunc_SemanticNode

        Args:
        child: the child Papfunc_SemanticNode
        """
	print ("adding child %s..." %child)
        assert_type(child, Papfunc_SemanticNode)
        SemanticNode.add_child(self, child)

 # This module contains a function to perform lexical
 # insertion, to be added as a constructor method to the SemanticNode
 # class, and a simple function to test lexical insertion.
 
# @classmethod
 def insert_terminal_node_representation(termnode,vecspace,matspace,use_wordform=0):
 # This is the function performing lexical insertion. It expects a
 # terminal syntactic node as input, as well as two DISSECT semantic
 # spaces containing vectors and (flattened) matrices, respectively
 # (that is, if the vectors have n dimensions, the "matrix" space must
 # contain nxn-dimensional vectors).
 
 # The vector space is expected to contain two special vectors, named
 # as follows:
 #
 # - cg.onevec: a vector of 1s
 # - cg.zerovec: a vector of 0s
 #
 # Similarly, the matrix space should contain:
 #
 # -cg.identmat: the (flattened) identity matrix
 # -cg.zeromat: a flattened mmatrix of 0s
 
 # Moreover, for verbs, the flattened matrices are expected to be
 # suffixed by the strings .subjmat and .objmat, respectively.
 
 # When looking if a terminal node lexical item is in the relevant
 # space(s), by default, we work with lemmas, but there is an option to
 # use word forms instead (what we would really need, I suspect, is to
 # decide to use word or lemma on a POS-by-POS basis, e.g., we might
 # want to distinguish singular from plural nouns, but use lemmas for
 # verbs).
 
 # We convert the POS to "shortpos"s that right now include the
 # following types: d (determiner, including predeterminer), j
 # (adjective), n (noun, including pronoun and proper name), r
 # (adverb), p (preposition), o (everything else).
 
 # The function returns a tuple made of two lists. The first list
 # contains a string-representation of the vector and 0 or more
 # matrices representing the terminal, the second contains the
 # corresponding DISSECT objects. Note that for elements that are
 # "empty" for our purposes, both lists contain just a string marking
 # the fact that the item is empty (the string is prefixed by the node
 # lexical item for the string representation, whereas it is just
 # "empty" in the "numerical" representation). The naming conventions
 # for the first list are as follows (where lempos stands for the
 # lexical item -- by default lemma, but wordform if so requested --
 # followed by shortpos):
 
 # - lempos.empty: empty terminal for our purposes
 
 # - lempos.lexvec: the item has a vector representation in the lexicon
 
 # - lempos.onevec: the item has no lexical vector representation and
 #   is represented by a vector of 1s
 
 # - lempos.zerovec: the item has no lexical vector representation and
 #   is represented by a vector of 0s
 
 # - lempos.objmat: the object matrix associated to a verb in the
 #   lexicon
 
 # - lempos.subjmat: the subject matrix associated to a verb in the
 #   lexicon
 
 # - lempos.lexmat: the lexical matrix associated to a (non-verb) item
 
 # - lempos.identmat: the item has no lexical matrix representation (or
 #   not enough of them given its arity) and the identity matrix will
 #   be used instead
 
 # - lempos.zeromat: the item has no lexical matrix representation (or
 #   not enough of them given its arity) and a matrix of 0s will be
 #   used instead
 
 # Note that the function assumes that matrices will be processed in
 # stack order (last in, first out), for example, intransitive verbs
 # are represented by vector, subject matrix, object matrix, in this
 # order.
 
 # TODOS:
 #
 # - decide if lemma or wordform on a POS-by-POS basis
 #
 # - add check for dimensionality of vectors/matrices (target
 #   dimensionality to be passed as argument)
 #
 # - generate 0, 1 and identity matrices/vectors instead of getting
 #   them from semantic space
 
  if not termnode.is_terminal():
   raise ValueError("insert_terminal_node_representation called on non-terminal node")
  
  stringstructure = []
  numericalstructure = []
  pos=termnode.pos
  label=termnode.label
  if not use_wordform:
   lexitem=termnode.lemma
  else:
   lexitem=termnode.word
  if lexitem=="an" or lexitem =="An": lexitem="a"
 
 
  # retrieving the zero, one and identity matrix/vectors (might be a
  # waste of RAM, but makes code below cleaner)
  onevec=vecspace.get_row("cg.onevec")
  zerovec=vecspace.get_row("cg.zerovec")
  identmat=matspace.get_row("cg.identmat")
  zeromat=matspace.get_row("cg.zeromat")
  
 
  # get short pos code
  matched = re.match("^[JNRV]",pos)
  if matched:
   shortpos = matched.group().lower()
  elif termnode.lemma=="that" and pos=="IN": # this is the mysterious way in
                                    # which relative that is tagged
   shortpos="o"
  elif pos=="IN" or (pos=="TO" and label=="PP/NP"): # to used as preposition
   shortpos="p"
  elif pos=="PDT" or pos=="WDT":
   shortpos="d" # pre-determiner and det, wh- (what, which, whatever, whichever)
  elif pos=="DT":
   if label=="NP": # things such as somebody should be
                   # treated as nouns
    shortpos="n"
   else:
    shortpos="d"
 # elif pos=="WP" or pos=="PRP": # treat pronouns like nouns
  elif pos=="PRP": # treat pronouns like nouns
   shortpos="n"
  elif pos=="CD" and label=="N/N" and re.match("one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|((thir|four|fif|six|seven|eigh|nine)teen)|(twen|thir|for|fif|six|seven|eigh|nine)ty",lexitem): #treat numerals like dets
   shortpos="d"
  else:
   shortpos="o"
 
  lempos=lexitem + '-' + shortpos
 
  # processing nouns (both common and proper)
  if shortpos=="n":
   # if the noun is in lexicon, return its vector, if not return the
   # 1-vector
   if lempos in vecspace.row2id:
    stringstructure.append(lempos + '.lexvec')
    numericalstructure.append(vecspace.get_row(lempos))
   else:
    stringstructure.append(lempos + '.onevec')
    numericalstructure.append(onevec)
   return (stringstructure,numericalstructure)
 
  # processing verbs (which might also include auxiliaries!)
  elif shortpos=="v":
   # first look for the vector corresponding to the verb, and insert
   # if no verb in lexicon, insert 0 vector
   if lempos in vecspace.row2id:
    stringstructure.append(lempos + '.lexvec')
    numericalstructure.append(vecspace.get_row(lempos))
   else:
    stringstructure.append(lempos + '.zerovec')
    numericalstructure.append(zerovec)
   
   # if verb is passive (including past participle), pick object
   # matrix, or identity if we don't have the verb in the lexicon
   if re.match("^S\[pss\]",label) or (pos == "VBN" and label=="N/N"):
    if lempos + '.objmat' in matspace.row2id:
     stringstructure.append(lempos + '.objmat')
     numericalstructure.append(matspace.get_row(lempos+'.objmat'))
    else:
     stringstructure.append(lempos + '.identmat')
     numericalstructure.append(identmat)
 
   # if verb is regular intransitive or present participle, look for
   # subject matrix in lexicon, if it is not there, insert identity mat
   elif re.match("^S[^\\\\/]*\\\\NP$",label) or label == "N/N":
    if lempos + '.subjmat' in matspace.row2id:
     stringstructure.append(lempos + '.subjmat')
     numericalstructure.append(matspace.get_row(lempos+'.subjmat'))
    else:
     stringstructure.append(lempos + '.identmat')
     numericalstructure.append(identmat)
   
   # if verb is regular transitive, or tri-argumental with
   # prepositional third argument (that we treat as a normal
   # verb-modifying PP) add, one after the other, subject and object
   # matrix
   elif re.match("^\(S[^\\\\/]*\\\\NP\)/NP$",label) or  re.match("^\(\(S[^\\\\/]*\\\\NP\)/PP\)/NP",label):
    if lempos + '.subjmat' in matspace.row2id:
     stringstructure.append(lempos + '.subjmat')
     numericalstructure.append(matspace.get_row(lempos+'.subjmat'))
    else:
     stringstructure.append(lempos + '.identmat')
     numericalstructure.append(identmat)
    if lempos + '.objmat' in matspace.row2id:
     stringstructure.append(lempos + '.objmat')
     numericalstructure.append(matspace.get_row(lempos+'.objmat'))
    else:
     stringstructure.append(lempos + '.identmat')
     numericalstructure.append(identmat)
 
   # ditransitive constructions: we insert subj and obj as usual, and
   # use zero (!!!) for the nearest argument (outermost matrix)
   elif re.match(".*S.*NP.*NP.*NP$",label):
    if lempos + '.subjmat' in matspace.row2id:
     stringstructure.append(lempos + '.subjmat')
     numericalstructure.append(matspace.get_row(lempos+'.subjmat'))
    else:
     stringstructure.append(lempos + '.identmat')
     numericalstructure.append(identmat)
    if lempos + '.objmat' in matspace.row2id:
     stringstructure.append(lempos + '.objmat')
     numericalstructure.append(matspace.get_row(lempos+'.objmat'))
    else:
     stringstructure.append(lempos + '.identmat')
     numericalstructure.append(identmat)
    # this is the innermost argument matrix
    stringstructure.append(lempos + '.zeromat')
    numericalstructure.append(zeromat)
   
   # "to be" (at least) can take a prepositional phrase as direct
   # object (to be in the park): since the preposition ins this case is
   # indistinguishable from the one that modifies VPs or adjectives, we
   # treat "to be" when it has category (S[dcl]\NP)/PP as a zero vector
   # and an identity matrix: this will result in the combination of "to
   # be" and the PP being the PP vector and the identity matrix
   # (identity matrix from to be plust zero matrix from PP), the
   # identity matrix will then be multiplied by the subject vector,
   # resulting in the sentence being represented by the sum of the
   # subject and PP vectors
   elif re.match("^\(S[^\\\\/]*\\\\NP\)/PP$",label): 
    stringstructure=[lempos + '.zerovec',lempos + '.identmat']
    numericalstructure=[zerovec,identmat]
 
   # finally, auxiliary and the like (including some pro constructions
   # that probably shouldn't be treated this way), if I'm right, are
   # always treated as VP modifiers, and we'll convert them to empty
   # elements
   elif re.match("^\(*S[^\\\\/]*\\\\NP\)/\(S[^\\\\/]*\\\\NP\)$",label):
    stringstructure=[lempos + '.empty']
    numericalstructure=["empty"]
 
   return (stringstructure,numericalstructure)
   # end of verb processing
 
  # processing adjectives and determiners 
  # we treat them in the same way, i.e., one vector (possibly 0) and
  # one matrix
  elif shortpos=="j" or shortpos=="d":
   # a vector from the lexicon or a 0 vector 
   if lempos in vecspace.row2id:
    stringstructure.append(lempos + '.lexvec')
    numericalstructure.append(vecspace.get_row(lempos))
   else:
    stringstructure.append(lempos + '.zerovec')
    numericalstructure.append(zerovec)
   
   # and now matrix, from lexicon or identity
   if lempos in matspace.row2id:
    stringstructure.append(lempos + '.lexmat')
    numericalstructure.append(matspace.get_row(lempos))
   else:
    stringstructure.append(lempos + '.identmat')
    numericalstructure.append(identmat)
 
   return (stringstructure,numericalstructure)
   # done with adjectives and determiners
 
  # handling adverbs
  elif shortpos=="r":
 
   # if the vector has no contentful matrix associated to it, we might
   # as well treat is as an empty element (NB: this means that we will
   # for now treat cases such as "John is here" as identical to
   # "John"!)
   if not (lempos in matspace.row2id):
    return ([lempos + '.empty'],["empty"])
 
   # a vector from the lexicon or a zero vector
   if lempos in vecspace.row2id:
    stringstructure.append(lempos + '.lexvec')
    numericalstructure.append(vecspace.get_row(lempos))
   else:
    stringstructure.append(lempos + '.zerovec')
    numericalstructure.append(zerovec)
 
   # NOT NEEDED FOR FOLLOWING BLOCK FOR NOW, AS WE DO NOT HANDLE THE
   # "is here" CASE!
   ## in predicative constructions
   ## this is all we need (this is here)
   # if re.match("S[^\\\\/]*\\\\NP$"):
   #  return (stringstructure,numericalstructure)
  
   # when adverb is sentence modifier (sadly he did it), we must add its 
   # matrix
   if re.match("^S[^\\\\/]*[\\\\/]S[^\\\\/]*$",label):
    stringstructure.append(lempos + '.lexmat')
    numericalstructure.append(matspace.get_row(lempos))
 
   # if the adverb is modifying an adjective or a VP, we must add as
   # inner matrix a 0 matrix that will be summed to the matrix of the
   # adj or VP, and an outer matrix as above (note that this should be
   # the only other case, so there is no need (I hope) for special
   # regexps!!!)
   # examples:
   #  <lf Astart="2" span="1" word="not" lemma="not" pos="RB" chunk="I-VP" entity="O" cat="(S\NP)\(S\NP)" />
   #  <lf start="2" span="1" word="not" lemma="not" pos="RB" chunk="I-ADJP" entity="O" cat="(S[adj]\NP)/(S[adj]\NP)" />
   #  <lf start="1" span="1" word="very" lemma="very" pos="RB" chunk="I-NP" entity="O" cat="(N/N)/(N/N)" />
   else:
    stringstructure.append(lempos + '.zeromat')
    numericalstructure.append(zeromat)
    stringstructure.append(lempos + '.lexmat')
    numericalstructure.append(matspace.get_row(lempos))
 
   return (stringstructure,numericalstructure)
   # done with adverbs
 
  # processing prepositions
  elif shortpos=="p":
 
   # a vector from the lexicon or a zero vector
   if lempos in vecspace.row2id:
    stringstructure.append(lempos + '.lexvec')
    numericalstructure.append(vecspace.get_row(lempos))
   else:
    stringstructure.append(lempos + '.zerovec')
    numericalstructure.append(zerovec)
 
   # if preposition is modifying a noun/np or sentence, we just need to
   # insert its meaningful lexical matrix, or identity
   if re.match("^\(NP\\\\NP\)/NP$",label) or re.match("^\(S/S\)/NP$",label):
    if lempos in matspace.row2id:
     stringstructure.append(lempos + '.lexmat')
     numericalstructure.append(matspace.get_row(lempos))
    else:
     stringstructure.append(lempos + '.identmat')
     numericalstructure.append(identmat)
 
   # if instead preposition is modifying anything else (VP modifier, PP
   # argument of triargumental verb, adjective modifier, copula
   # argument), we must first insert a 0 matrix (to be combined with
   # the verb/adj matrix by summing), and then the contentful matrix
   # categories:
   # - VP modifier: ((S\NP)\(S\NP))/NP
   # - PP argument of tri-argumental verb: PP/NP
   # - copula argument: PP/NP
   # - adjective modifier: PP/NP
   else:
    stringstructure.append(lempos + '.zeromat')
    numericalstructure.append(zeromat)
    if lempos in matspace.row2id:
     stringstructure.append(lempos + '.lexmat')
     numericalstructure.append(matspace.get_row(lempos))
    else:
     stringstructure.append(lempos + '.identmat')
     numericalstructure.append(identmat)
 
   return (stringstructure,numericalstructure)
   # done with preposition processing
 
  # default: we return an empty item
  return ([lempos + '.empty'],["empty"])
 
 def compute_matreps(self,vecspace,matspace,multiply_matrices=False):
        '''
        This method computes symbolic and numeric matrix representations od a papfunc node, taking as input a vector space, a matrix space. An optional Boolean argument, if set to True, makes matrices to be multiplied rather than summed when both subconstituents have arity greater than 0.
        '''
        # for terminal nodes call insert_terminal_node_representation
 	if self.is_terminal():
 		matrep,temp_numrep=self.insert_terminal_node_representation(vecspace,matspace)
 		self._matrep = matrep
 		if temp_numrep[0] == "empty":
 	    	 numrep = []
 		else:
 		    numrep = [temp_numrep[0].transpose()]
 		    dimensionality=(temp_numrep[0].shape[1])
 		    if len(temp_numrep)>1:
 			    for x in range(1, (len(temp_numrep))):
 				y = DenseMatrix(temp_numrep[x])
 				y.reshape((dimensionality,(y.shape[1]/dimensionality)))
 				numrep.append(y)
                    self._numrep = numrep
#raise an exception for a non-terminal node without children
 	elif len(self._children) == 0:
 		raise ValueError("Non-terminal non-branching node!")
# inherit the value of the single daughter in case of unary branching
 	if len(self._children) == 1:
  	 self._matrep = self.get_child(0)._matrep
  	 self._numrep = self.get_child(0)._numrep
#apply composition for binary branching nodes
	if len(self._children) == 2 and self._matrep == []:
 		matrep1=self.get_child(0)._matrep
 		matrep2=self.get_child(1)._matrep
 		arity1=len(matrep1)-1
 		arity2=len(matrep2)-1
# first, compute symbolic matrix representation
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
 # computing numeric matrix representation of a node from those of its two daughters	
		numrep1=self.get_child(0)._numrep
 		numrep2=self.get_child(1)._numrep
 		if arity1-arity2 == 0:
                         for x in range(0, arity1 +1):
                                 self._numrep.append(numrep1[x].__add__(numrep2[x]))
 		if arity1 < arity2 and not numrep1==[]:
                         for x in range(0, arity2):
                                 if x == 0:
                                         self._numrep.append(numrep2[x].__add__(numrep2[arity2] * numrep1[x]))
                                 elif x < len(numrep1):
                                  if multiply_matrices: self._numrep.append(numrep2[x] * numrep1[x])
                                  else: self._numrep.append(numrep1[x].__add__(numrep2[x]))
                                 else:
                                         self._numrep.append(numrep2[x])
 		if arity1 > arity2 and not numrep2==[]:
                         for x in range(0, arity1):
                                 if x == 0:
                                         self._numrep.append(numrep1[x].__add__(numrep1[arity1]*numrep2[x]))
                                 elif x < len(numrep2):
                                         if multiply_matrices: self._numrep.append(numrep2[x] * numrep1[x])
                                         else: self._numrep.append(numrep1[x].__add__(numrep2[x]))
                                 else:
                                         self._numrep.append(numrep1[x])
 		if (numrep1 == []): self._numrep = numrep2
 		if (numrep2 == []): self._numrep = numrep1
# end of numrep computation  
# Raise an exception for non-binary branching - we don't want to handle those structures
 	if len(self._children)>2:
 		raise ValueError("Matrix representations are not defined for trees with more than binary branching")

